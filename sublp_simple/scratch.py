

class Anc1(object):
    pass

class Anc2(object):
    pass

class Anc12(Anc1, Anc2):
    pass

class Anc3(object):
    pass

class Anc123(Anc12, Anc3):
    pass

thing = Anc123()



bases = type(thing).__bases__
print()
print("bases:", type(bases), bases)
print()
import pdb
pdb.set_trace()
print()
