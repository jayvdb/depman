from syn.base import init_hook, Attr
from .dependency import Dependency, command, output
from .operation import Combinable
from .relation import Eq, Le

#-------------------------------------------------------------------------------
# Pip Operations

#-----------------------------------------------------------
# pip install


class Install(Combinable):
    def execute(self):
        args = ' '.join(map(str, self))
        command('pip install --upgrade {}'.format(args))


#-------------------------------------------------------------------------------
# Pip


class Pip(Dependency):
    '''Representation of a pip dependency'''
    key = 'pip'
    freeze = dict()
    order = 30

    _attrs = dict(order = Attr(int, order))

    @init_hook
    def _populate_freeze(self):
        cls = type(self)
        if not cls.freeze:
            pkgs = output('pip freeze')
            cls.freeze = dict([tuple(line.split('==')) 
                               for line in pkgs.split('\n') if line])

    def check(self):
        if self.name in self.freeze:
            if self.version(self.freeze[self.name]):
                return True
        return False

    def satisfy(self):
        inst = [Install(self.name, order=self.order)]
        instver = [Install('{}=={}'.format(self.name, self.version.rhs),
                           order=self.order)]

        if self.always_upgrade:
            return inst
            
        if not self.check():
            if isinstance(self.version, (Eq, Le)):
                return instver
            return inst
        return []


#-------------------------------------------------------------------------------
# __all__

__all__ = ('Pip',)

#-------------------------------------------------------------------------------
