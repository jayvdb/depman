import sys
from syn.base_utils import getitem
from .dependency import Dependencies

#-------------------------------------------------------------------------------

def exit(code):
    sys.exit(code)

#-------------------------------------------------------------------------------

USAGE = '''depman MODE DEPFILE [SCOPE]
'''

def main(*args):
    if not args:
        print(USAGE)
        exit(1)
        return # for tests when exit() is mocked

    mode = args[0]
    path = args[1]
    scope = getitem(args, 2, 'all')

    with open(path, 'rt') as f:
        deps = Dependencies.from_yaml(f)

    if mode == 'satisfy':
        deps.satisfy(scope)
    elif mode == 'check':
        deps.check(scope)
    else:
        print(USAGE)
        exit(1)

#-------------------------------------------------------------------------------

if __name__ == '__main__': # pragma: no cover
    main(*sys.argv[1:])
