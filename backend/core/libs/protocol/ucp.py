class UCP:
    '''
    Unified Code Protocol
    ucp:[type]/[code]/[column]
    '''
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
    def from_kwargs(cls, **kwargs):
        return cls(kwargs['type_'], kwargs['code'], kwargs['column'])

    @property
    def ucp(self):
        return self.ucp_string

    @property
    def type(self):
        return self.type_

    @property
    def code(self):
        return self.code_

    @property
    def column(self):
        return self.column_

    def __hash__(self):
        return hash((self.type_, self.code_, self.column_))

    def __eq__(self, other):
        if isinstance(other, UCP):
            return (self.type_, self.code_, self.column_) == (other.type_, other.code_, other.column_)
        return False