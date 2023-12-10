# -*- coding: utf-8 -*-
"""
Created on Sat Aug  5 19:03:29 2023

@author: HP TG01
"""
import matplotlib.pyplot as plt
import numpy as np
import LOIS
# import FRML

fig=plt.figure(figsize=(7, 9), tight_layout=True)
# plt.suptitle("Exemples de régressions de polynômes")
ax1=plt.subplot(211)
#1er exemple ---------------------------------------------------------------------------
x = np.linspace(0, 10, 10+1)
y = [0,1,5,9,10,10,10,10,10,10,10]


ln=1
lx=130
lb=100
xn=0
xx=140
yn=0.0003
yx=300
def mymodel(liste):
    # return [FRML.DP0(1/a,xn,xx,yn,yx) for a in liste]
    # return [FRML.DP2a('1/f',a, ln, lx, xn, xx, yx, yn) for a in liste]
    # return [FRML.DP2('1/f',a, ln, lx, xx, xn, yx, yn,True) for a in liste]
    return [LOIS.FTG(a, ln,lx,xn,xx,yn,yx)*60*60 for a in liste]
# myline = np.linspace(ln,lx, lb)
myline = np.linspace(xn,xx,lb)
# myline = np.linspace(yn,yx,lb)
myimag = mymodel(myline)
# plt.scatter(x, y)
plt.plot(myline, myimag)
#plt.text(2, 1, mymodel)
#plt.text(12, 55, '{:.5f}'.format(r2_score(y, mymodel(x))))

#------------------------------------------------------------------------
fig.savefig("RegressionPolynomes2-3.png", dpi=250)
plt.show() 
c=np.array(mymodel(myline))