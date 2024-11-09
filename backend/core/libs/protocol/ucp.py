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

    @staticmethod
    def from_string(ucp_string):
        type_, code, column = ucp_string.split(':')[1].split('/')
        return UCP(type_, code, column)

    @staticmethod
    def from_kwargs(**kwargs):
        return UCP(kwargs['type_'], kwargs['code'], kwargs['column'])

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