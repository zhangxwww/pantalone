class UCP:
    '''
    Unified Code Protocol
    ucp:[type]/[code]/[column]
    '''
    def __init__(self, type_, code, column):
        self.ucp_string = f'ucp:{type_}/{code}/{column}'

    @property
    def ucp(self):
        return self.ucp_string