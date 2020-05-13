#!/usr/bin/env python
import math
import numpy as np

def phiChecker(phi1,phi2,phi_test):


  #make all angles in the range -pi to pi
  correct_range = lambda x: math.atan2(math.sin(x),math.cos(x))
  phi1 = correct_range(phi1)
  phi2 = correct_range(phi2)
# print "phi1: "+str(phi1)
# print "phi2: "+str(phi2)
  phi_test = correct_range(phi_test)
  if abs(abs(phi1-phi2)-math.pi) < 5*np.finfo(float).eps: return "Bounds separated by pi"
# print abs(abs(phi1-phi2)-math.pi) 
  if not abs(phi1-phi2) < math.pi:
    if phi1 < phi2: phi1 += 2*math.pi
    else: phi2 += 2*math.pi
# print phi2
  phis = sorted([phi1,phi2,phi_test])
  if phis[1] == phi_test: return True
  phis = sorted([phi1,phi2,phi_test+2*math.pi])
  if phis[1] == phi_test+2*math.pi: return True
  return False


if __name__ == '__main__':
  valid = phiChecker(math.pi,2*math.pi,5)
  print valid

