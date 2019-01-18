class Scope:
    allow_api=[]
    def __add__(self,other):
        self.allow_api=self.allow_api+other.allow_api
        self.allow_api=list(set(self.allow_api))
        return self

class AdminScope(Scope):
    allow_api=['/v1/user/<uid>']
    def __init__(self):
        self + UserScope()

class UserScope(Scope):
    allow_api = ['/v1/user']


def is_in_scope(scope,endpoint):
    '''
    当前endpoint格式为v1.view_func
    我们修改redprint代码将endpoint的格式变为v1.module_name+view_func 相当于 v1.redprint+view_func
    '''
    scope=globals()[scope]()
    if endpoint in scope.allow_api:
        return True
    else:
        return False