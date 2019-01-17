from functools import partial

def f1(p1,p2):
    print(p1)
    print(p2)


a=partial(f1,1)

a("xxx")