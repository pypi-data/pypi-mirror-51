"""Collection of definitions for Fortran language support."""

import typing as t

import typed_ast.ast3 as typed_ast3

from ..general.misc import dict_mirror
from ..pair import make_slice_from_call


def attribute_chain_components(attribute: typed_ast3.Attribute) -> t.List[typed_ast3.AST]:
    assert isinstance(attribute, typed_ast3.Attribute), type(attribute)
    components = []
    while isinstance(attribute.value, typed_ast3.Attribute):
        components.insert(0, attribute.attr)
        attribute = attribute.value
    components.insert(0, attribute)
    return components


FORTRAN_PYTHON_TYPE_PAIRS = {
    ('logical', None): 'bool',
    ('integer', None): 'int',
    ('real', None): 'float',
    ('double precision', None): 'np.double',
    ('character', t.Any): 'str',
    ('character', 256): 'str[256]',
    ('character', 512): 'str[512]',
    ('character', 1024): 'str[1024]',
    ('integer', 1): 'np.int8',
    ('integer', 2): 'np.int16',
    ('integer', 4): 'np.int32',
    ('integer', 8): 'np.int64',
    ('real', 2): 'np.float16',
    ('real', 4): 'np.float32',
    ('real', 8): 'np.float64'}

PYTHON_FORTRAN_TYPE_PAIRS = {value: key for key, value in FORTRAN_PYTHON_TYPE_PAIRS.items()}

PYTHON_TYPE_ALIASES = {
    'bool': ('np.bool_',),
    'int': ('np.int_', 'np.intc', 'np.intp'),
    'np.float32': ('np.single',),
    'np.float64': ('np.double', 'np.float_',)}

for _name, _aliases in PYTHON_TYPE_ALIASES.items():
    for _alias in _aliases:
        PYTHON_FORTRAN_TYPE_PAIRS[_alias] = PYTHON_FORTRAN_TYPE_PAIRS[_name]

FORTRAN_PYTHON_OPERATORS = {
    # binary
    '+': (typed_ast3.BinOp, typed_ast3.Add),
    '-': (typed_ast3.BinOp, typed_ast3.Sub),
    '*': (typed_ast3.BinOp, typed_ast3.Mult),
    # missing: MatMult
    '/': (typed_ast3.BinOp, typed_ast3.Div),
    '%': (typed_ast3.BinOp, typed_ast3.Mod),
    '**': (typed_ast3.BinOp, typed_ast3.Pow),
    '//': (typed_ast3.BinOp, typed_ast3.Add),  # concatenation operator, only in Fortran
    # LShift
    # RShift
    # BitOr
    # BitXor
    # BitAnd
    # missing: FloorDiv
    '.eq.': (typed_ast3.Compare, typed_ast3.Eq),
    '==': (typed_ast3.Compare, typed_ast3.Eq),
    '.ne.': (typed_ast3.Compare, typed_ast3.NotEq),
    '/=': (typed_ast3.Compare, typed_ast3.NotEq),
    '.lt.': (typed_ast3.Compare, typed_ast3.Lt),
    '<': (typed_ast3.Compare, typed_ast3.Lt),
    '.le.': (typed_ast3.Compare, typed_ast3.LtE),
    '<=': (typed_ast3.Compare, typed_ast3.LtE),
    '.gt.': (typed_ast3.Compare, typed_ast3.Gt),
    '>': (typed_ast3.Compare, typed_ast3.Gt),
    '.ge.': (typed_ast3.Compare, typed_ast3.GtE),
    '>=': (typed_ast3.Compare, typed_ast3.GtE),
    # Is
    # IsNot
    # In
    # NotIn
    '.and.': (typed_ast3.BoolOp, typed_ast3.And),
    '.or.': (typed_ast3.BoolOp, typed_ast3.Or),
    # unary
    # '+': (typed_ast3.UnaryOp, typed_ast3.UAdd),
    # '-': (typed_ast3.UnaryOp, typed_ast3.USub),
    '.not.': (typed_ast3.UnaryOp, typed_ast3.Not),
    # Invert: (typed_ast3.UnaryOp, typed_ast3.Invert)
    }

INTRINSICS_FORTRAN_TO_PYTHON = {
    # Fortran 77
    'abs': 'abs',  # or np.absolute
    'acos': ('numpy', 'arccos'),
    'aimag': None,
    'aint': None,
    'anint': None,
    'asin': ('numpy', 'arcsin'),
    'atan': ('numpy', 'arctan'),
    'atan2': None,
    'char': None,
    'cmplx': None,
    'conjg': ('numpy', 'conj'),
    'cos': ('numpy', 'cos'),
    'cosh': None,
    'dble': 'float',  # incorrect
    'dim': None,
    'dprod': None,
    'exp': ('numpy', 'exp'),
    'ichar': None,
    'index': None,
    'int': 'int',
    'len': None,
    'lge': None,
    'lgt': None,
    'lle': None,
    'llt': None,
    'log': ('numpy', 'log'),
    'log10': ('numpy', 'log10'),
    'max': ('numpy', 'maximum'),
    'min': ('numpy', 'minimum'),
    'mod': None,
    'nint': None,
    'real': 'float',
    'sign': ('numpy', 'sign'),
    'sin': ('numpy', 'sin'),
    'sinh': ('numpy', 'sinh'),
    'sqrt': ('numpy', 'sqrt'),
    'tan': ('numpy', 'tan'),
    'tanh': ('numpy', 'tanh'),
    # non-standard Fortran 77
    'getenv': ('os', 'environ'),
    # Fortran 90
    # Character string functions
    'achar': None,
    'adjustl': None,
    'adjustr': None,
    'iachar': None,
    'len_trim': None,
    'repeat': None,
    'scan': None,
    'trim': ('str', 'rstrip'),
    'verify': None,
    # Logical function
    'logical': None,
    # Numerical inquiry functions
    'digits': None,
    'epsilon': ('numpy', 'finfo', 'eps'),
    'huge': ('numpy', 'finfo', 'max'),
    'maxexponent': None,
    'minexponent': None,
    'precision': None,
    'radix': None,
    'range': None,
    'tiny': ('numpy', 'finfo', 'tiny'),  # np.finfo(np.double).tiny ,
    # Bit inquiry function
    'bit_size': None,
    # Vector- and matrix-multiplication functions
    'dot_product': ('numpy', 'dot'),
    'matmul': ('numpy', 'matmul'),
    # Array functions
    'all': None,
    'any': None,
    'count': ('ndarray', 'count'),
    'maxval': ('numpy', 'amax'),
    'minval': ('numpy', 'amin'),
    'product': None,
    'sum': 'sum',
    # Array location functions
    'maxloc': ('numpy', 'argmax'),
    'minloc':  ('numpy', 'argmin'),
    # Fortran 95
    'cpu_time': None,
    'present': 'is_not_none',  # TODO: TMP
    'set_exponent': None,
    # Fortran 2003
    # Fortran 2008
    }

INTRINSICS_PYTHON_TO_FORTRAN = dict_mirror(INTRINSICS_FORTRAN_TO_PYTHON)


def _transform_print_call(call):
    if not hasattr(call, 'fortran_metadata'):
        call.fortran_metadata = {}
    call.fortran_metadata['is_transformed'] = True
    if len(call.args) == 1:
        arg = call.args[0]
        if isinstance(arg, typed_ast3.Call) and isinstance(arg.func, typed_ast3.Attribute):
            attribute = arg.func
            assert attribute.attr == 'format'
            if isinstance(arg.func.value, typed_ast3.Str):
                call.args = [arg.func.value] + arg.args
            else:
                assert isinstance(arg.func.value, typed_ast3.Name), type(arg.func.value)
                label = int(arg.func.value.id.replace('format_label_', ''))
                call.args = [typed_ast3.Num(n=label)] + arg.args
            return call
    call.args.insert(0, typed_ast3.Ellipsis())
    return call


PYTHON_FORTRAN_INTRINSICS = {
    'np.amax': 'maxval',
    'np.amin': 'minval',
    'np.arcsin': 'asin',
    'np.arctan': 'atan',
    'np.argmin': 'minloc',
    'np.argmax': 'maxloc',
    'np.array': lambda _: _.args[0],
    'np.conj': 'conjg',
    'np.cos': 'cos',
    'np.dot': 'dot_product',
    'np.exp': 'exp',
    'np.finfo.eps': 'epsilon',
    'np.finfo.max': 'huge',
    'np.finfo.tiny': 'tiny',
    'np.log': 'log',
    'np.log10': 'log10',
    'np.matmul': 'matmul',
    'np.maximum': 'max',
    'np.minimum': 'min',
    'np.sign': 'sign',
    'np.sin': 'sin',
    'np.sinh': 'sinh',
    'np.sqrt': 'sqrt',
    'np.zeros': lambda _: typed_ast3.Num(n=0),
    'print': _transform_print_call,
    'os.environ': 'getenv',
    'is_not_none': 'present',
    'MPI.Init': 'MPI_Init',
    'MPI.COMM_WORLD.Comm_size': 'MPI_Comm_size',
    'MPI.COMM_WORLD.Comm_rank': 'MPI_Comm_rank',
    'MPI.COMM_WORLD.Barrier': 'MPI_Barrier',
    'MPI.Bcast': 'MPI_Bcast',
    'MPI.Allreduce': 'MPI_Allreduce',
    'MPI.Finalize': 'MPI_Finalize',
    '{expression}.sum': None,
    '{expression}.size': None,
    'Fortran.file_handles[{name}].read': None,
    'Fortran.file_handles[{name}].close': None,
    '{name}.rstrip': None,
    'slice': make_slice_from_call
    }

INTRINSICS_SPECIAL_CASES = {'getenv', 'trim', 'count'}

PYTHON_TO_FORTRAN_SPECIAL_CASES = {'print', ('numpy', 'array'), ('numpy', 'zeros')}

CALLS_SPECIAL_CASES = {(..., 'rstrip'), ('os', 'environ'), (..., 'count')}

MPI_FORTRAN_TO_PYTHON = {
    'MPI_Init': 'Init',
    'MPI_Comm_size': 'Comm_size',
    'MPI_Comm_rank': 'Comm_rank',
    'MPI_Barrier': 'Barrier',
    'MPI_Bcast': 'Bcast',
    'MPI_Allreduce': 'Allreduce',
    'MPI_Finalize': 'Finalize'
}

MPI_PYTHON_TO_FORTRAN = dict_mirror(MPI_FORTRAN_TO_PYTHON)
