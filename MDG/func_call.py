
def bduk(arg1, arg2, arg3='default', *, kwarg1='abc', kwarg2='xyz'):
    print(arg1)
    print(arg2)
    print(arg3)
    print(kwarg2)

def puk(arg_pos, *args):
    print(arg_pos)
    print(args)

bduk(1, 'huj', 'puj', )#kwarg2 = 77)
puk('huj', 1, 7, 33)

