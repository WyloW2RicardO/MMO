# -*- coding: utf-8 -*-
"""
Created on Sat Aug 26 11:07:24 2023

@author: HP TG01
"""
#import pandas
"retrouve"
def CLEF(D1,D0,L,C0,C1):return D1.loc[D1['NOM'].isin([D0.loc[L,C0]]),C1].item()

"retourne la puissance de dix pour ecrire en nombre scientifique"
def NMBRsc(real,typ='0'):
    if real==0:print("real est null")
    if typ!='0' and typ!='<0' and typ!='>0': print("err du typ dans NMBsc")
    if abs(real)<1 and (typ=='0' or typ=='<0'):b=+1
    elif typ=='0' or typ=='>0':b=-1
    else: return 0
    
    a=0
    while real*10**a<1 or real*10**a>=10: a+=b
    return a

from datetime import timedelta
"convertie des segond en temps"
def sgnd_heur(n):return str(timedelta(seconds=n))

from math import pi
"surface d'un disque"
def clndr_aire(rayon):return pi*rayon**2
"volume d'un cilindre"
def clndr_vlm(rayon,hauteur):return clndr_aire(rayon)*hauteur
"volume d'une sphere"
def sphr_vlm(rayon):return 4*pi*rayon**3/3

from math import exp
from math import log
from math import tan
from math import atan
"modifier le resulta des fonction"
def FFI(f_txt):
    if f_txt=='f':
        f=lambda a : a
        fi=lambda b : b
    elif f_txt=='1/f':
        f=lambda a : 0 if a<1 else 1/a
        fi=lambda b : 0 if b<1 else 1/b
    elif f_txt=='log':
        f=lambda a : log(a)
        fi=lambda b : exp(b)
    elif f_txt=='exp':
        f=lambda a : exp(a)
        fi=lambda b : log(b)
    elif f_txt=='atan':
        f=lambda a : atan(a)
        fi=lambda b : tan(b)
    else:print("fonction non definit")
    return f,fi

"deplacement de la valeur"
def DP0(f,na,xa,nb,xb):return nb+(xb-nb)*(f-na)/(xa-na)
def DP1(f,a,na,xa,nb,xb):return f(DP0(a,na,xa,nb,xb))
def DP2(f_txt,aa,na,xa,nb,xb,nc,xc,ab=None):
    f,fi=FFI(f_txt)
    if ab is not None:na,xa,nb,xb=nb,xb,na,xa
    return DP0(DP1(f,aa,na,xa,nb,xb),f(nb),f(xb),nc,xc)
def DP0i(fi,na,xa,nb,xb):return na+(xa-na)*(fi-nb)/(xb-nb)
def DP1i(fi,b,na,xa,nb,xb):return DP0i(fi(b),na,xa,nb,xb)
def DP2i(f_txt,c,na,xa,nb,xb,nc,xc):
    f,fi=FFI(f_txt)
    return DP1i(fi,DP0i(c,f(nb),f(xb),nc,xc),na,xa,nb,xb)

"replace dans le csv"
from datetime import datetime
def RMPLC(liste,result):
    liste_len=len(liste)
    if liste_len!=len(result):
        print('diference de taille de colone dans',liste)
    else:
        for c in range(liste_len):
            if (result[c] is not None
                and liste[c]!=result[c]):
                liste[0]=datetime.now()
                liste[c]=result[c]
    return liste