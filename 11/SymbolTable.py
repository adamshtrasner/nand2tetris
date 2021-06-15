class SymbolTable:

    STATIC = "static"
    THIS = "field"
    ARG = "argument"
    LCL = "var"

    def __init__(self):

        # each pair in each scope dictionary is defined like this:
        # {name : (type, kind, index)}
        # for example: if the variable 'x' is defined within a class like this:
        # field int x; ---> class_scope = {'x': ('int', 'field', 0)}

        self.class_scope = dict()
        self.class_indexes = {self.STATIC: 0, self.THIS: 0}
        self.subroutine_scope = None
        self.subroutine_indexes = None

    def start_subroutine(self):
        # resets the subroutine scope table
        self.subroutine_scope = dict()
        self.subroutine_indexes = {self.ARG: 0, self.LCL: 0}

    def define(self, _name, _type, _kind):
        if _kind in [self.STATIC, self.THIS]:
            index = self.class_indexes[_kind]
            self.class_indexes[_kind] += 1
            self.class_scope.update({_name: (_type, _kind, index)})
        else:
            index = self.subroutine_indexes[_kind]
            self.subroutine_indexes[_kind] += 1
            self.subroutine_scope.update({_name: (_type, _kind, index)})

    def var_count(self, _kind):
        # returns the number of variables of the given kind
        if _kind in [self.STATIC, self.THIS]:
            return self.class_indexes[_kind]
        else:
            return self.subroutine_indexes[_kind]

    def kind_of(self, _name):
        # returns the kind of the given variable if defined,
        # if not defined - returns None
        if self.subroutine_scope:
            if _name in self.subroutine_scope:
                return self.subroutine_scope[_name][1]
        if _name in self.class_scope:
            return self.class_scope[_name][1]
        return None

    def type_of(self, _name):
        # returns the type of the given variable if defined,
        # if not defined - returns None
        if self.subroutine_scope:
            if _name in self.subroutine_scope:
                return self.subroutine_scope[_name][0]
        if _name in self.class_scope:
            return self.class_scope[_name][0]
        return None

    def index_of(self, _name):
        # returns the index of the given variable if defined,
        # if not defined - returns None
        if self.subroutine_scope:
            if _name in self.subroutine_scope:
                return self.subroutine_scope[_name][2]
        if _name in self.class_scope:
            return self.class_scope[_name][2]
        return None
