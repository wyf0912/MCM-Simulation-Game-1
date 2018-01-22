import math
import matplotlib.pyplot as plt
import numpy as np
import random
import scipy

def circle_h(v):
    r = 0.75
    h = v/(math.pi*r*r)
    return h


def circle_s1(v):
    return math.pi* 2.25/4


def circle_s2(v):
    return math.pi * 0.25


def circle_s3(h):
    return 2*math.pi*0.75*h


class Bathtub:
    def __init__(self,v_water,T,target_T,function_h,function_s1,function_s2,function_s3,v_person=0,h_person=0):
        self.v_water = v_water
        self.h_person = h_person
        self.v_person = v_person
        self.v_water = v_water
        self.target_T = target_T
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

        self.pid_p = 0.02
        self.pid_i = 0
        self.pid_d = 0
        self.pid_int_i=0

        self.total_v = 0
        self.int_error = 0

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
         - self.alpha*(self.T-self.theta)*self.s1 - (self.beta * self.deltaP)*(1-bubble) \
         - (self.s1 + self.s2 + self.s3)*(self.T- self.theta)/0.16*0.19

    def pid(self):
        output = self.pid_p*(self.target_T-self.T)
        if output>0:
            if output>0.0001:
                return 0.0001
            return output
        return 0

    def random_action(self):
        if random.random()>0.98:
            loss_water_v=0.0005
            self.v_water -= loss_water_v
            self.Q -= self.T * 1000 * 4200 * loss_water_v

    def simluate(self, dv,label,time=1800, bubble=0):
        t = [0] * time
        x_label = np.linspace(0, time / 60, time)
        self.total_v=0
        self.int_error=0
        for i in range(time):
            self.heat_loss(bubble)
            t[i] = self.T
            self.total_v += dv
            self.int_error += pow(self.T - self.target_T,2)
            # circle2.random_action()
            self.input(dv, 50)
            self.check()
        plt.plot(x_label,t,label=label)
        return self.total_v,self.int_error




circle = Bathtub(0.2, 38,38, circle_h, circle_s1, circle_s2, circle_s3)
circle2 = Bathtub(0.2, 38,38, circle_h, circle_s1, circle_s2, circle_s3)

plt.figure(figsize=(10.6,6))
plt.title('Changes in temperature over time')
plt.xlabel('time/min')
plt.ylabel('Temperature/degree')
plt.legend()

print(circle.simluate(0.00004,label="With hubble-bubble",bubble=1))

plt.show()




