class APIError(IOError):
    def __init__(self, msg, e):
        self.msg = msg
        self.http_exc = e
        self.code = e.code
        IOError.__init__(self)
    
    def __str__(self):
        return "%s (code %i)" % (self.msg, self.code)
        
class UnknownBlocksError(ValueError):
    pass
