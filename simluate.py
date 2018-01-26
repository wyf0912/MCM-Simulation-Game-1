import math
import matplotlib.pyplot as plt
import numpy as np
import random
from scipy import optimize
from shape import *

class Bathtub:
    def __init__(self,v_water,T,target_T,function_h,function_s1,function_s2,function_s3,v_person=0,h_person=0,action=False,line=False):
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
        self.s_person = 0.0057*self.h_person +0.0121*self.v_person*1000 + 0.0820
        self.action = action
        self.line =line

        self.theta = 18 #室内温度
        self.beta  = pow(22+2*(self.T-self.theta),0.5)
        self.alpha = 0.653*self.beta
        self.sigma = 5.432e-8
        self.deltaP = 0.6*self.p2

        self.pid_p = 0.002
        self.pid_i = 0.0001
        self.pid_d = 0.001
        self.pid_int_i=0
        self.pid_last_error=0

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
         - (self.s1 + self.s2 + self.s3)*(self.T- self.theta)/0.16*0.19 \
        - self.s_person * 1.48 *(self.T - 37.5)*int(self.v_person > 1)

    @property
    def pid(self):
        error=(self.target_T-self.T)
        if abs(error) <0.01:
            error=0
        self.pid_int_i+=error
        output = self.pid_p*error+self.pid_int_i*self.pid_i+(error-self.pid_last_error)*self.pid_d
        self.pid_last_error = error
        if output>0:
            if output>0.0001:
                return 0.0001
            return output
        return 0

    def random_action(self):
        if random.random()>0.98:
            loss_water_v = self.v_person * 0.001
            if self.action:
                self.v_water -= loss_water_v
                self.Q -= self.T * 1000 * 4200 * loss_water_v

    def simluate(self, dv,pid=False,label_str='',time=1800, bubble=0):
        t = [0] * time
        x_label = np.linspace(0, time / 60, time)
        self.total_v=0
        self.int_error=0
        for i in range(time):
            self.heat_loss(bubble)
            t[i] = self.T
            if pid:
                dv=self.pid
            self.total_v += dv
            self.int_error += pow(self.T - self.target_T,2)
            circle2.random_action()
            self.input(dv, 50)
            self.check()
        if self.line:
            plt.plot(x_label,t,'--',label=label_str)
        else:
            plt.plot(x_label, t, label=label_str)
        plt.legend()
        return self.total_v,self.int_error

oval1 = Bathtub(0.15, 38,38, oval_h, oval_s1, oval_s2, oval_s3,v_person=0.075,h_person=1.85)
oval2 = Bathtub(0.15, 38,38, oval_h, oval_s1, oval_s2, oval_s3,v_person=0.070,h_person=1.7)
oval4 = Bathtub(0.15, 38,38, oval_h, oval_s1, oval_s2, oval_s3,v_person=0.080,h_person=1.7)
oval3 = Bathtub(0.15, 38,38, oval_h, oval_s1, oval_s2, oval_s3)

oval1_ = Bathtub(0.15, 38,38, oval_h, oval_s1, oval_s2, oval_s3,v_person=0.075,h_person=1.85,action=1,line='--')
oval2_ = Bathtub(0.15, 38,38, oval_h, oval_s1, oval_s2, oval_s3,v_person=0.070,h_person=1.7,action=1,line='--')
oval4_ = Bathtub(0.15, 38,38, oval_h, oval_s1, oval_s2, oval_s3,v_person=0.080,h_person=1.7,action=1,line='--')
oval3_ = Bathtub(0.15, 38,38, oval_h, oval_s1, oval_s2, oval_s3)


circle1 = Bathtub(0.2, 38,38, circle_h, circle_s1, circle_s2, circle_s3,v_person=0.075,h_person=1.85)
circle2 = Bathtub(0.2, 38,38, circle_h, circle_s1, circle_s2, circle_s3,v_person=0.070,h_person=1.7)
circle4 = Bathtub(0.2, 38,38, circle_h, circle_s1, circle_s2, circle_s3,v_person=0.080,h_person=1.7)
circle3 = Bathtub(0.2, 38,38, circle_h, circle_s1, circle_s2, circle_s3)

circle1_ = Bathtub(0.2, 38,38, circle_h, circle_s1, circle_s2, circle_s3,v_person=0.075,h_person=1.85,action=1,line='--')
circle2_ = Bathtub(0.2, 38,38, circle_h, circle_s1, circle_s2, circle_s3,v_person=0.070,h_person=1.7,action=1,line='--')
circle4_ = Bathtub(0.2, 38,38, circle_h, circle_s1, circle_s2, circle_s3,v_person=0.080,h_person=1.7,action=1,line='--')
circle3_ = Bathtub(0.2, 38,38, circle_h, circle_s1, circle_s2, circle_s3)

plt.figure(figsize=(10.6,6))
plt.title('Changes in temperature over time')
plt.xlabel('time/min')
plt.ylabel('Temperature/degree')

'''
minimum=''
#minimum = optimize.brute(circle.simluate,ranges = ((0.00003, 0.00006),))
#print(minimum)
print(oval3_.simluate(0.0000,pid=True,label_str="PID control hot water inflow(Cirecle)",bubble=0))
#print(oval3.simluate(0.0000213,pid=False,label_str="Oval bathtub with 21.3ml\s hot inflow",bubble=0))
print(oval3_.simluate(0.0000,pid=True,label_str="PID control  hot water inflow(Oval)",bubble=0))
print(oval3.simluate(0.0000,pid=False,label_str="No hot water inflow(Oval)",bubble=0))
print(circle3.simluate(0.0000,pid=False,label_str="No hot water inflow(Cirecle)",bubble=0))
'''
print(oval1.simluate(0.0000213,pid=False,label_str="37.3ml/s hot water inflows with person(75kg 1.85m)",bubble=1))
print(oval2.simluate(0.0000213,pid=False,label_str="37.3ml/s hot water inflows with person(70kg 1.70m)",bubble=1))
print(oval4.simluate(0.0000213,pid=False,label_str="37.3ml/s hot water inflows with person(80kg 1.70m)",bubble=1))
print(oval3.simluate(0.0000213,pid=False,label_str="37.3ml/s hot water inflows without person",bubble=1))

print(oval1_.simluate(0.0000213,pid=True,label_str="37.3ml/s hot water inflows with person and action(75kg 1.85m)",bubble=1))
print(oval2_.simluate(0.0000213,pid=True,label_str="37.3ml/s hot water inflows with person and action(70kg 1.70m)",bubble=1))
print(oval4_.simluate(0.0000213,pid=True,label_str="PID hot water inflows with person and action(80kg 1.70m)",bubble=1))
print(oval3_.simluate(0.0000213,pid=True,label_str="PID hot water inflows without person",bubble=1))


#print(oval3.simluate(0,label_str="No hot water inflows",bubble=1))

plt.show()




