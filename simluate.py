import math
import matplotlib.pyplot as plt

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
        self.h_person = h_person
        self.v_person = v_person
        self.v_water = v_water
        self.function_h = function_h
        self.function_s1 = function_s1
        self.function_s2 = function_s2
        self.function_s2 = function_s3
        self.Q = self.v_water*1000*4200*T

        self.theta = 26 #室内温度
        self.beta  = pow(22+2*(self.T-self.theta),0.5)
        self.alpha = 0.653*self.beta
        self.sigma = 5.432e-8
        self.deltaP = 

    @property
    def v(self):
        return self.v_person*0.6+self.v_water

    @property
    def h(self):
        return self.function_h(self.v)

    @property
    def T(self):
        return self.Q/(self.v_water*1000*4200)

    @property
    def s1(self):
        return self.function_s1(self.v)

    @property
    def s2(self):
        return self.function_s2(self.v)

    @property
    def s3(self):
        return self.function_s3(self.v)

    def input(self, v, t):
        self.v_water += v
        self.Q += v*1000*4200*t

    def outflow(self,v):
        self.Q -= self.T*1000*4200*v
        self.v_water -= v
        pass

    def radiate_loss(self,S,k):
        return S*k*self.sigma * pow(self.T + 273.15, 4)
    def heat_loss(self):
        self.Q = self.Q - self.radiate_loss(self.s1,1) - self.radiate_loss(self.s2+self.s3,0.94) \
         - self.alpha*(t-self.theta)*self.s1 - self.beta * (self.)

circle = Bathtub(3, 40, circle_h, circle_s1, circle_s2, circle_s3)

time=10000
t=[0]*time
for i in range(time):
    circle.heat_loss()
    t[i] = circle.T
    circle.input(0.01,50)

plt.plot(t)
plt.show()




