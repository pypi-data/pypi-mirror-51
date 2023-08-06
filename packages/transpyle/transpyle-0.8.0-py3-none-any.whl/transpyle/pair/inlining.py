"""Preliminary implementation of inlining."""

import copy
import functools
import logging
import pathlib
import tempfile
import types
import typing as t

import horast
import horast.nodes as horast_nodes
import static_typing as st
import typed_ast.ast3 as typed_ast3
import typed_astunparse

from ..general import Language, CodeReader, Parser, CodeWriter
from ..general.misc import flatten_syntax
from .assertions import names_equivalent
from .ast_query import ReturnFinder
from .manipulate import convert_return_to_assign

_LOG = logging.getLogger(__name__)

VALID_CONTEXTS = {
    typed_ast3.For: ('body', list),
    typed_ast3.FunctionDef: ('body', list),
    typed_ast3.Expr: ('value', typed_ast3.AST)}

VALID_CONTEXTS_TUPLE = tuple(VALID_CONTEXTS.keys())


class Replacer(st.ast_manipulation.RecursiveAstTransformer[typed_ast3]):

    def __init__(self, replacer):
        super().__init__()
        self._replacer = replacer

    def visit_node(self, node):
        return self._replacer(node)

    def __repr__(self):
        return 'Replacer({})'.format(self._replacer)


class DeclarationReplacer(st.ast_manipulation.RecursiveAstTransformer[typed_ast3]):

    def __init__(self):
        super().__init__()
        self.replaced = []

    def replace_declaration(self, declaration):
        if isinstance(declaration, (typed_ast3.Import, typed_ast3.ImportFrom)):
            # TODO: it's a hack
            _ = horast_nodes.Comment(' skipping a "use" statement when inlining', eol=False)
            self.replaced.append((declaration, _))
            return _
        if not isinstance(declaration, (typed_ast3.Assign, typed_ast3.AnnAssign)):
            return declaration
        intent = getattr(declaration, 'fortran_metadata', {}).get('intent', None)
        if intent in {'in', 'out', 'inout'}:
            _ = horast_nodes.Comment(
                ' skipping intent({}) declaration when inlining'.format(intent), eol=False)
            self.replaced.append((declaration, _))
            return _
        if getattr(declaration, 'fortran_metadata', {}).get('is_declaration', False):
            # TODO: it's a hack
            _ = horast_nodes.Comment(' skipping a declaration when inlining', eol=False)
            self.replaced.append((declaration, _))
            return _
        return declaration

    def visit_node(self, node):
        return self.replace_declaration(node)

    def __repr__(self):
        return 'DeclarationReplacer()'


def replace_name(arg, value, name):
    if isinstance(name, typed_ast3.Name) and name.id == arg:
        return value
    return name


def create_name_replacers(values, replacements):
    args_mapping = {arg: value for arg, value in zip(values, replacements)
                    if not names_equivalent(arg, value)}
    return [Replacer(functools.partial(replace_name, arg, value))
            for arg, value in args_mapping.items()]


class CallInliner(st.ast_manipulation.RecursiveAstTransformer[typed_ast3]):

    def __init__(self, inlined_function: st.nodes.StaticallyTypedFunctionDef[typed_ast3],
                 verbose: bool = True):
        super().__init__(fields_first=False)
        assert isinstance(inlined_function, typed_ast3.FunctionDef), type(inlined_function)
        assert inlined_function.body

        decorators = inlined_function.decorator_list
        if decorators:
            raise NotImplementedError('inlining with decorators not supported')

        arguments = inlined_function.args
        if arguments.vararg is not None or arguments.kwarg is not None:
            raise NotImplementedError('inlining of functions with *args or **kwargs not supported')
        if arguments.kwonlyargs or arguments.kw_defaults:
            raise NotImplementedError('only simple function definitions are currently supported')

        if arguments.defaults:
            _LOG.warning('default values for inlined function parameters will be ignored!')

        self._body = None
        self._omitted_declarations = []
        self._inlined_function = inlined_function
        self._inlined_args = [arg.arg for arg in inlined_function.args.args]
        self._verbose = verbose

        self._valid_inlining_contexts = {typed_ast3.Return}

        last_statement = self._inlined_function.body[-1]
        return_finder = ReturnFinder()
        return_finder.visit(self._inlined_function)
        _LOG.warning('last statement is: %s', last_statement)
        if len(self._inlined_function.body) == 1 and isinstance(last_statement, typed_ast3.Return):
            self._valid_inlining_contexts |= {t.Any}
        if not return_finder.found_any_with_value:
            self._valid_inlining_contexts |= {typed_ast3.Expr}
        if not return_finder.found_any:
            self._valid_inlining_contexts |= {typed_ast3.Assign, typed_ast3.AnnAssign,
                                              typed_ast3.Expr}
        elif len(return_finder.found) == 1 and return_finder.found[0] is last_statement:
            self._valid_inlining_contexts |= {typed_ast3.Assign, typed_ast3.AnnAssign}

        _LOG.warning('function %s can only be inlined when in %s',
                     self._inlined_function.name, self._valid_inlining_contexts)

    def _inline_call_in_return(self, return_stmt):
        call = return_stmt.value
        assert self._is_valid_target_for_inlining(call)

        replacers = []
        replacers += create_name_replacers(self._inlined_args, call.args)

        inlined = self._inline_call(call, replacers)
        last_statement = inlined[-2] if self._verbose \
            else (inlined[-1] if isinstance(inlined, list) else inlined)
        if not isinstance(last_statement, typed_ast3.Return):
            if not isinstance(inlined, list):
                inlined = [inlined]
            inlined += [typed_ast3.Return(value=None)]
        return inlined

    def _inline_call_in_assign(self, assign):
        call = assign.value
        assert self._is_valid_target_for_inlining(call)
        assert isinstance(assign, typed_ast3.AnnAssign) or len(assign.targets) == 1

        target = getattr(assign, 'target', getattr(assign, 'targets', [None])[0])
        return_replacer = Replacer(functools.partial(convert_return_to_assign, target))

        replacers = []
        replacers += create_name_replacers(self._inlined_args, call.args)
        replacers += [return_replacer]

        return self._inline_call(call, replacers)

    def _inline_call_in_expr(self, expr):
        call = expr.value
        assert self._is_valid_target_for_inlining(call)

        replacers = []
        decl_replacer = DeclarationReplacer()
        replacers.append(decl_replacer)
        replacers += create_name_replacers(self._inlined_args, call.args)

        inlined = self._inline_call(call, replacers)

        if decl_replacer.replaced:
            _LOG.warning('omitted %i declarations', len(decl_replacer.replaced))
            if self._omitted_declarations:
                _LOG.warning('will not restore them because there already are some declarations')
            else:
                if self._verbose:
                    call_code = typed_astunparse.unparse(call).strip()
                    self._omitted_declarations.append((horast_nodes.Comment(
                        ' start of declarations from inlined {}'.format(call_code), eol=False),
                                                       None))
                self._omitted_declarations += decl_replacer.replaced
                if self._verbose:
                    self._omitted_declarations.append((horast_nodes.Comment(
                        ' end of declarations from inlined {}'.format(call_code), eol=False), None))

        return inlined

    def _inline_call(self, call, replacers):
        # template_code = '''for dummy_variable in (0,):\n    pass'''
        # inlined_call = typed_ast3.parse(template_code).body[0]
        call_code = typed_astunparse.unparse(call).strip()
        inlined_statements = []
        if self._verbose:
            inlined_statements.append(
                horast_nodes.Comment(' inlined {}'.format(call_code), eol=False))
        for stmt in self._inlined_function.body:
            stmt = st.augment(copy.deepcopy(stmt), eval_=False)
            for replacer in replacers:
                stmt = replacer.visit(stmt)
            if stmt is not None:
                inlined_statements.append(stmt)
        if self._verbose:
            inlined_statements.append(
                horast_nodes.Comment(' end of inlined {}'.format(call_code), eol=False))
        _LOG.warning('inlined a call %s using replacers %s', call_code, replacers)
        # inlined_call.body = scope
        # return st.augment(inlined_call), eval_=False)
        assert inlined_statements
        if len(inlined_statements) == 1:
            return inlined_statements[0]
        return inlined_statements

    def visit(self, node):
        first_call = False
        if self._body is None:
            first_call = True
            self._body = node.body
            _LOG.warning('%s is the target', node)
        node = super().visit(node)
        flatten_syntax[typed_ast3](node)
        if first_call:
            if self._omitted_declarations:
                line_after_declarations = 0  # TODO: find line after declarations in target function
                inserted = []
                for orig, repl in reversed(self._omitted_declarations):
                    if any(_ is orig for _ in inserted):
                        continue
                    intent = getattr(orig, 'fortran_metadata', {}).get('intent', None)
                    if intent in {'in', 'out', 'inout'}:
                        continue
                    _LOG.warning('inserting omitted decl %s', orig)
                    node.body.insert(line_after_declarations, orig)
                    inserted.append(orig)
        return node

    def generic_visit(self, node):
        """Copied implementation from parent class - get rid of it at some point."""
        if not self._fields_first:
            _LOG.debug('visiting node %s', node)
            node = self.visit_node(node)
            if not hasattr(node, '_fields'):
                return node
        _LOG.debug('visiting all fields of node %s', node)
        for name, value in typed_ast3.iter_fields(node):
            setattr(node, name, self.generic_visit_field(node, name, value))
        if self._fields_first:
            _LOG.debug('visiting node %s', node)
            node = self.visit_node(node)
        return node

    def _is_target_for_inlining(self, call) -> bool:
        return isinstance(call, typed_ast3.Call) and isinstance(call.func, typed_ast3.Name) \
            and call.func.id == self._inlined_function.name

    def _is_valid_target_for_inlining(self, call) -> bool:
        if call.keywords:
            raise NotImplementedError('currently only simple calls can be inlined')
        if len(self._inlined_args) != len(call.args):
            # raise ValueError(  # TODO: TMP
            _LOG.warning(
                'Inlined function has {} parameters: {}, but target call has {} arguments: {}.'
                .format(len(self._inlined_args), self._inlined_args, len(call.args), call.args))
        return True

    def visit_node(self, node):
        # _LOG.warning('visiting %s', node)
        if isinstance(node, typed_ast3.Return) and self._is_target_for_inlining(node.value):
            return self._inline_call_in_return(node)
        if isinstance(node, (typed_ast3.Assign, typed_ast3.AnnAssign)) \
                and self._is_target_for_inlining(node.value):
            if typed_ast3.Assign not in self._valid_inlining_contexts:
                raise NotImplementedError('{} cannot be inlined inside {}'
                                          ' -- return supported only at the end of the function'
                                          .format(self._inlined_function.name, type(node)))
            return self._inline_call_in_assign(node)
        if isinstance(node, typed_ast3.Expr) and self._is_target_for_inlining(node.value):
            if typed_ast3.Expr not in self._valid_inlining_contexts:
                raise NotImplementedError('{} cannot be inlined inside {}'
                                          ' -- returns not supported'
                                          .format(self._inlined_function.name, type(node)))
            return self._inline_call_in_expr(node)
        if self._is_target_for_inlining(node):
            if t.Any not in self._valid_inlining_contexts:
                raise NotImplementedError('{} cannot be inlined in arbitrary context'
                                          ' -- only one-liners are supported'
                                          .format(self._inlined_function.name))
            replacers = create_name_replacers(self._inlined_args, node.args)
            replacers.append(Replacer(lambda return_: return_.value
                                      if isinstance(return_, typed_ast3.Return) else return_))
            return self._inline_call(node, replacers)
        return node

    def visit_field(self, node, name: str, value: t.Any):
        # _LOG.warning('visiting %s=%s in %s', name, value, node)
        return value


def inline_syntax(target: typed_ast3.FunctionDef, inlined_function: typed_ast3.FunctionDef,
                  globals_=None, *args, **kwargs) -> typed_ast3.FunctionDef:
    if not isinstance(target, st.nodes.StaticallyTypedFunctionDef[typed_ast3]):
        target = st.augment(target, eval_=False, globals_=globals_)
    if not isinstance(inlined_function, st.nodes.StaticallyTypedFunctionDef[typed_ast3]):
        inlined_function = st.augment(inlined_function, eval_=False, globals_=globals_)
    call_inliner = CallInliner(inlined_function, *args, **kwargs)
    target = call_inliner.visit(target)
    assert isinstance(target, typed_ast3.FunctionDef)
    return target


def inline(target_function, inlined_function, globals_=None) -> object:
    """Inline all calls to given inlined function within the target.

    Can be used as decorator.
    """
    assert isinstance(target_function, types.FunctionType)
    assert isinstance(inlined_function, types.FunctionType)
    language = Language.find('Python 3')
    parser = Parser.find(language)()
    target_code = CodeReader.read_function(target_function)
    inlined_code = CodeReader.read_function(inlined_function)
    target_syntax = parser.parse(target_code).body[0]
    inlined_syntax = parser.parse(inlined_code).body[0]
    target_inlined_syntax = inline_syntax(target_syntax, inlined_syntax, globals_=globals_,
                                          verbose=False)
    target_inlined_code = horast.unparse(target_inlined_syntax).lstrip()

    with tempfile.NamedTemporaryFile(suffix='.py', delete=False) as output_file:
        # TODO: this leaves garbage behind in /tmp/ but is neeeded by subsequent transpiler passes
        code_writer = CodeWriter('.py')
        target_inlined_path = pathlib.Path(output_file.name)
        code_writer.write_file(target_inlined_code, target_inlined_path)

    code_obj = compile(target_inlined_code, filename=str(target_inlined_path), mode='exec')
    if globals_ is None:
        globals_ = {'__builtins__': globals()['__builtins__']}
    locals_ = {}
    eval_result = eval(code_obj, globals_, locals_)
    assert eval_result is None, eval_result
    assert target_function.__name__ in locals_
    target_inlined_function = locals_[target_function.__name__]
    assert isinstance(target_inlined_function, types.FunctionType)
    return target_inlined_function
