import math


def circle_h(v):
    r = 1.5
    h = v/(math.pi*r*r)
    return h


def circle_s1(v):
    pass


def circle_s2(v):
    pass


def circle_s3(v):
    pass


class Bathtub:
    def __init__(self,v_water,T,function_h,function_s1,function_s2,function_s3,v_person=0,h_person=0):
        self.v_water = v_water
        self.T = T
        self.h_person = h_person
        self.v_person = v_person
        self.v_water = v_water
        self.function_h = function_h
        self.S1 = function_s1(self.h)

    @property
    def v(self):
        return self.v_person*0.6+self.v_water

    @property
    def h(self):
        return self.function_h(self.v)

    @property
    def Q(self):
        return self.v_water*4200

    @property
    def T(self):
        return self.Q/self.v_water

    def input(self, v, t):
        self.v_water = self.v_water+v

circle = Bathtub(3, 40, circle_h, circle_s1, circle_s2, circle_s3)
print(circle.h)
circle.input(1,40)
print(circle.h)



