import numpy as np
import math

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

def oval(v):
    r = 0.75
    h = v/(math.pi*r*r)
    return h