import math
import matplotlib.pyplot as plt
import numpy as np

def circle_h(v):
    r = 1.5
    h = v/(math.pi*r*r)
    return h


def circle_s1(v):
    return math.pi* 2.25


def circle_s2(v):
    return math.pi * 2.25


def circle_s3(h):
    return 2*math.pi*1.5*h


class Bathtub:
    def __init__(self,v_water,T,function_h,function_s1,function_s2,function_s3,v_person=0,h_person=0):
        self.v_water = v_water
        self.h_person = h_person
        self.v_person = v_person
        self.v_water = v_water
        self.function_h = function_h
        self.function_s1 = function_s1
        self.function_s2 = function_s2
        self.function_s3 = function_s3
        self.Q = self.v_water*1000*4200*T

        self.theta = 18 #室内温度
        self.beta  = pow(22+2*(self.T-self.theta),0.5)
        self.alpha = 0.653*self.beta
        self.sigma = 5.432e-8
        self.deltaP = 0.6*self.p2

    @property
    def p2(self):
        return pow(10,8.10765-1750.286/(self.theta+235.0))/760*1000

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
        return self.function_s1(self.h)

    @property
    def s2(self):
        return self.function_s2(self.h)

    @property
    def s3(self):
        return self.function_s3(self.h)

    def check(self):
        if self.v>0.3:
            self.outflow(self.v-0.3)

    def input(self, v, t):
        self.v_water += v
        self.Q += v*1000*4200*t

    def outflow(self,v):
        self.Q -= self.T*1000*4200*v
        self.v_water -= v
        pass

    def radiate_loss(self,S,k):
        return S*k*self.sigma * pow(self.T + 273.15, 4)

    def heat_loss(self,bubble=0):
        self.Q = self.Q - self.radiate_loss(self.s1,1)*(1-bubble*0.04) - self.radiate_loss(self.s2+self.s3,0.94) \
         - self.alpha*(self.T-self.theta)*self.s1 - (self.beta * self.deltaP)*(1-bubble)


plt.figure(figsize=(10.6,6))
circle = Bathtub(0.2, 38, circle_h, circle_s1, circle_s2, circle_s3)

time=8800
t=[0]*time
x_label=np.linspace(0,time/60,time)
print(circle.p2)
for i in range(time):
    circle.heat_loss()
    t[i] = circle.T
    circle.input(0.00016,50)
    circle.check()

plt.plot(x_label,t,label='Hot water inflows')

'''
circle2 = Bathtub(0.2, 38, circle_h, circle_s1, circle_s2, circle_s3)
for i in range(time):
    circle2.heat_loss(bubble=1)
    t[i] = circle2.T
    circle2.input(0.00016, 50)
    circle2.check()

plt.plot(x_label,t,label='No hot water inflows')
'''
plt.title('Changes in temperature over time')
plt.xlabel('time/min')
plt.ylabel('Temperature/degree')
plt.legend()

plt.show()




