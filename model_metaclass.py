'''
    metaclass练习
    http://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000/0014319106919344c4ef8b1e04c48778bb45796e0335839000
'''

class Field(object):
    def __init__(self, name, column_name):
        self.name = name
        self.column_name = column_name
    def __str__(self):
        return '<Field: %s %s>' % (self.name, self.column_name)
    __repr__ = __str__
    
class IntegerField(Field):
    def __init__(self, name):
        super(IntegerField, self).__init__(name, 'int')

class VarcharField(Field):
    def __init__(self, name, length):
        super(VarcharField, self).__init__(name, 'varchar(%d)' % length)

class CharField(Field):
    def __init__(self, name, length):
        super(CharField, self).__init__(name, 'char(%d)' % length)

class ModelMetaclass(type):
    def __new__(cls, name, bases, attrs):
        attrs['__fields__'] = {}
        for k,v in list(attrs.items()):
            if isinstance(v, Field):
                attrs['__fields__'][k] = v
                del attrs[k]
        attrs['__table__'] = name[0:-5].lower()
        return super(ModelMetaclass, cls).__new__(cls, name, bases, attrs)

class Model(object, metaclass=ModelMetaclass):
    def __init__(self, *args, **kwargs):
        fields = ','.join(self.__fields__.keys())
        where = ' and '.join("%s='%s'" % (key,val) for key,val in kwargs.items() if key in self.__fields__)
        sql = 'select %s from %s where %s' % (fields, self.__table__, where)
        self.select = sql
        self.__dict__.update(kwargs)

class UserModel(Model):
    username = VarcharField('name', 15)
    age = IntegerField('age')
