from libs.expr.supported_operations import SUPPORTED_OPERATIONS


class UCP:
    '''
    Unified Code Protocol
    ucp:[type]/[code]/[column]
    '''

    OPERATION_CODE_2_SYMBOL = {op['code']: op['symbol'] for op in SUPPORTED_OPERATIONS}

    def __init__(self, type_, code, column):
        self.ucp_string = f'ucp:{type_}/{code}/{column}'
        self.type_ = type_
        self.code_ = code
        self.column_ = column

    @classmethod
    def from_string(cls, ucp_string):
        type_, code, column = ucp_string.split(':')[1].split('/')
        return cls(type_, code, column)

    @classmethod
    def from_kwargs(cls, type_, code, column):
        return cls(type_, code, column)

    @property
    def ucp(self):
        return self.ucp_string

    @property
    def type(self):
        return self.type_

    @property
    def code(self):
        if self.type != 'operation':
            return self.code_
        else:
            return UCP.OPERATION_CODE_2_SYMBOL[self.code_]

    @property
    def safe_code(self):
        if self.type != 'constant':
            if self.code[0].isdigit():
                return f'_{self.code}'
            if self.code[0] == '.':
                return f'_DOT_{self.code[1:]}'
        return self.code

    @property
    def column(self):
        return self.column_

    def __hash__(self):
        return hash((self.type_, self.code_, self.column_))

    def __eq__(self, other):
        if isinstance(other, UCP):
            return (self.type_, self.code_, self.column_) == (other.type_, other.code_, other.column_)
        return False