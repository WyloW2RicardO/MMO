# -*- coding: utf-8 -*-
"""
Created on Sat Aug  5 14:02:09 2023

@author: HP TG01
"""
## LOI
bnfc = 1
## temps
"""
calandrier et heur republicain :
    1 ans jeux de 12 mois jeux de 3 semaine jeux de 10 jour jeux de 10 heur jeux de 100 min de 100 segonde real
    et 5 jour de fette et 6 en pour les année sextil
lever et crépuscul seront fixé 1h pour l'instant
"""
tmps_max = {'mois':12,'smn':3,'jour':10,'heur':10,'mnt':100,'sgnd':100}
tmps = {'ans':1,'mois':1,'smn':1,'jour':1,'heur':1,'mnt':1,'sgnd':1}

## joueur
from pandas import read_csv
from FRML import DP2
"pour les bare il y a malus si <20% & bunus si >80% qui son inverser pour poid et contenace"

"point maximal de vie"
def PV(aglt,cf_data): # (aglt,endrnc):
    a=cf_data['NOM'].isin(['PV'])
    return int( # aglt*
               DP2('f',aglt # endrnc
                         ,cf_data.loc[a,'An'].item(),cf_data.loc[a,'Ax'].item()
                         ,cf_data.loc[a,'Xn'].item(),cf_data.loc[a,'Xx'].item()
                         ,cf_data.loc[a,'Yn'].item(),cf_data.loc[a,'Yx'].item()))
"point maximal de magie"
def PM(magic,cf_data): # (intlgnc,magic):
    a=cf_data['NOM'].isin(['PM'])
    return int( # magic*
               DP2('f',magic # intlgnc
                         ,cf_data.loc[a,'An'].item(),cf_data.loc[a,'Ax'].item()
                         ,cf_data.loc[a,'Xn'].item(),cf_data.loc[a,'Xx'].item()
                         ,cf_data.loc[a,'Yn'].item(),cf_data.loc[a,'Yx'].item()))
"point maximal de déplacement"
def PD_argmt(stat):return stat['RPDT'].item()
def PD(stat,an,ax,xn,xx,yn,yx):return int(DP2('f',PD_argmt(stat),an,ax,xn,xx,yn,yx))
"poid maximal qui peut etre porté"
def POID_argmt(stat):return stat['FRC'].item()
def POID(stat,an,ax,xn,xx,yn,yx):return int(DP2('f',POID_argmt(stat),an,ax,xn,xx,yn,yx))
"contenace maximal qui peut etre porté"
def CNTNC(intlgnc,cf_data):
    a=cf_data['NOM'].isin(['CNTNC'])
    return int(intlgnc
               *DP2('f',intlgnc
                         ,cf_data.loc[a,'An'].item(),cf_data.loc[a,'Ax'].item()
                         ,cf_data.loc[a,'Xn'].item(),cf_data.loc[a,'Xx'].item()
                         ,cf_data.loc[a,'Yn'].item(),cf_data.loc[a,'Yx'].item()))
"fatigue du au poid porté par segonde"
def FTG(poid_objt,an,ax,xn,poid_max,yn,enrg_max):
    return DP2('1/f',poid_objt,an,ax,poid_max,xn,enrg_max,yn,True)
"la vitessse de deplacement maximal"
def Vtss_max(poid,poid_max,cf_data):
    "le personage trote au maximaume de sa vitesse par defaut"
    if poid/poid_max>0.8:print(poid/poid_max,"% du poid maximal")
    a=cf_data['NOM'].isin(['Dvtss'])
    return DP2('1/f',poid
                    ,cf_data.loc[a,'An'].item(),cf_data.loc[a,'Ax'].item()
                    ,cf_data.loc[a,'Xn'].item(),poid_max
                    ,cf_data.loc[a,'Yn'].item(),cf_data.loc[a,'Yx'].item())

"retourne la vitesse en DP2 du type de deplacement choisie"
def Vtss(typ,vtss_max,cf_data):
    a=cf_data['NOM'].isin(['Dvtss'])
    if typ=='trote':
        if vtss_max/cf_data.loc[a,'Yn'].item()>0.66: # si il peut ateindre ce type
            return ('trote',0.66*cf_data.loc[a,'Yn'].item())
        if vtss_max/cf_data.loc[a,'Yn'].item()>0.33:
            return ('trote',vtss_max)
        return ('marche',vtss_max)
    elif typ=='marche':
        if vtss_max/cf_data.loc[a,'Yn'].item()>0.33:
            return ('marche',0.33*cf_data.loc[a,'Yn'].item())
        return ('marche',vtss_max)
    return ('cours',vtss_max)
"retourne la fatigue par segonde du au type de vitesse choisie"
def Vtss_ftg(typ,cf_data):
    if typ=='course':return 1/36
    elif typ=='trote':return 1/360
    elif typ=='marche':return 1/3600
    print(typ,"le type de vitesse n'est pas definis")

"recuperaration du a l'endormisement en DP2 des segonde passer"
def DODO(nom,sgnd,typ,cf_data):
    a=cf_data['NOM'].isin(['DODO_'+nom])
    if (type(nom)!=str or not True in a): print(nom,"erreur dans le nom du dodo")
    return DP2('atan',sgnd
                    ,cf_data.loc[a,'An'].item(),cf_data.loc[a,'Ax'].item()
                    ,cf_data.loc[a,'Xn'].item(),cf_data.loc[a,'Xx'].item()
                    ,cf_data.loc[a,'Yn'].item(),typ)
"recuperation du au repo en DP2 des segonde passer"
def REPO(nom,sgnd,typ,cf_data):
    a=cf_data['NOM'].isin(['REPO_'+nom])
    if (type(nom)!=str or not True in a):print(nom,"erreur dans le nom du repo")
    return DP2('atan',sgnd
                    ,cf_data.loc[a,'An'].item(),cf_data.loc[a,'Ax'].item()
                    ,cf_data.loc[a,'Xn'].item(),cf_data.loc[a,'Xx'].item()
                    ,cf_data.loc[a,'Yn'].item(),typ)

from random import uniform
from datetime import datetime
"determine la categorie des objet dorpé"
ctgr='E:\Program\pyton\MMO\categories.csv'
ctgr_data=read_csv(ctgr) # cherche le doc
def DROP(chnc,karma):
    ctgr_stat=[(1+karma*(1*(a<6)-1*(a>=6)))*(ctgr_data.loc[a,'nbr']+chnc/6*(a<6)) for a in range(ctgr_data['nbr'])]
    altr=uniform(0,sum(ctgr_stat['nbr']))
    for a in range(len(ctgr_data['nbr'])):
        if altr<sum(ctgr_data['nbr'][:a]):
            if a>0:
                for b in range(a):
                    ctgr_data.loc[b,'nbr']+=1 #modifi les stat inferieur
                    ctgr_data.loc[b,'maj']=datetime.now()
            ctgr_data.to_csv(ctgr,index=False) #on enregistre
            return ctgr_data.loc[a,'NOM'] 
"modification des stats en fonction de la categorie"
def STAT_objet_modif(ctgr_nom,stat_objet):
    return int(ctgr_data.loc[ctgr_data['NOM'].isin([ctgr_nom]),'mltpl']*stat_objet)

def DEGA(frc,chnc):return frc*ctgr_data.loc[ctgr_data['NOM'].isin[DROP(chnc)],'mltpl']

### AGRI
"def NET():return"

"""
PNJ :
    il vit 100ans et son adulte entre de 20 à 80ans
        
base :
    n'a besoin de manger qu'une pomme de terre et de faire sa nuit complette
    365+365/10=402u /5=80.4m² par persone en auto-sufisence
    365*10=3650$ minimum par ans et par persone
    4020*0.1=402$ de benefice net par ans
    4020-402=3618$ de charge
"""
## metier
agralmnt = {'ftg':1,'succ':1,'endrnc':1}
