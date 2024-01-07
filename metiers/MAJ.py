# -*- coding: utf-8 -*-
"""
Created on Sat Aug 26 09:53:23 2023

@author: HP TG01
"""
import pandas
from datetime import datetime
from FRML import RMPLC

"mise à jour des coéficient des fonctions modifier"
"tout le mondes cours a la meme courbe de vitesse pour que un pas de 1m en 1s ne le fasse pas avence de 10m"
cf='E:\Program\pyton\MMO\coefficient.csv'
cf_data=pandas.read_csv(cf)
cf_data=cf_data.sort_values('NOM')
vvn='E:/Program/pyton/MMO/vivant.csv'
vvn_data=pandas.read_csv(vvn)
vvn_data=vvn_data.sort_values('NOM')
vvn_hmyn=vvn_data.loc[vvn_data['NOM'].isin(['hmyn'])]
from LOIS import FTG
trvl_tmps=5*60*60
actn_tmps=2
actn_enrg=1
actn2_max=int(trvl_tmps/actn_tmps/2)
poid_objt=1
mdltn_min=1
mdltn_max=mdltn_min+1
poid_min=0
poid_max=140
ftg_min=round(1/(1*60*60),6)  # 1 tout les heurs
dplcmt_min=round(10*60*60*ftg_min) # 1 jour aven que l'homme moyen soit epuiser
ftg_max=10*dplcmt_min
while ftg_max<trvl_tmps*FTG(poid_objt,mdltn_min,mdltn_max,poid_min,poid_max,ftg_min,ftg_max):
    mdltn_max+=1

ligne=cf_data['NOM'].isin(['FTG'])
result=[None,None,mdltn_min,mdltn_max,poid_min,poid_max,ftg_min,ftg_max]
cf_data.loc[ligne]=RMPLC(cf_data.loc[ligne].tolist(),result)

from LOIS import POID_argmt
ligne=cf_data['NOM'].isin(['POID'])
An=1
Ax=POID_argmt(vvn_hmyn)
result=[None,None,An,Ax,An,Ax,poid_min,poid_max]
cf_data.loc[ligne]=RMPLC(cf_data.loc[ligne].tolist(),result)

# from math import ceil
from LOIS import PD_argmt
ligne=cf_data['NOM'].isin(['PD'])
An=1
Ax=PD_argmt(vvn_hmyn)
result=[None,None,An,Ax,An,Ax,dplcmt_min,ftg_max]
cf_data.loc[ligne]=RMPLC(cf_data.loc[ligne].tolist(),result)

ligne=cf_data['NOM'].isin(['Dvtss'])
result=[None,None,-2,2,1,2,55,1]
cf_data.loc[ligne]=RMPLC(cf_data.loc[ligne].tolist(),result)
    
from math import pi
a=['PV','PM','PD']
pi6=round(pi,6)
nuit=round(4*60*60*(1+4/6))
jour=round(6*60*60*(1+4/6))
result=[None,None,-pi6,pi6,0,0,0,ftg_max]
for a_ligne in range(len(a)):
    cf_ligne=cf_data['NOM'].isin(['DODO_'+a[a_ligne]])
    result[3]=nuit
    cf_data=RMPLC(cf_data,cf_ligne,result)
    cf_ligne=cf_data['NOM'].isin(['REPO_'+a[a_ligne]])
    result[3]=jour
    cf_data.loc[cf_ligne]=RMPLC(cf_data.loc[cf_ligne].tolist(),result)
cf_data.to_csv(cf,index=False)

from FRML import NMBRsc
"remise a niveaux des categorie de drope"
ctgr='E:\Program\pyton\MMO\categories.csv'
ctgr_data=pandas.read_csv(ctgr)
ctgr_data=ctgr_data.sort_values('NOM')
ctgr_len=len(ctgr_data)
ctgr_som=sum(ctgr_data['NMBR'])
ctgr_10=NMBRsc(min(ctgr_data['NMBR'])/ctgr_som,'<0')
ctgr_som10=ctgr_som*10**ctgr_10
now1=datetime.now()
for ctgr_ligne in range(ctgr_len):
    ctgr_rprt=round(ctgr_data.loc[ctgr_ligne,'NMBR']/ctgr_som10,0)
    if ctgr_data.loc[ctgr_ligne,'NMBR'].item()!= ctgr_rprt:
        ctgr_data.loc[ctgr_ligne,'MAJ']=now1
        ctgr_data.loc[ctgr_ligne,'NMBR']=ctgr_rprt
ctgr_data.to_csv(ctgr,index=False)

from FRML import sphr_vlm
from FRML import clndr_vlm
"mettre a jour les donnée lier a la culture en fonction de la culture de almnt_base"
"C:cout, D:diametre(m), E:energi, G:poid(Kg), H:hauteur(m), J:(Gj), N:nombre, U:unité, V:volume(litre)"
almnt='E:/Program/pyton/MMO/alimentation.csv'
almnt_data=pandas.read_csv(almnt)
almnt_data=almnt_data.sort_values('NOM')
almnt_base=almnt_data['NOM'].isin(['pomme-terre'])
e_j=round(100*ftg_max*0.8/almnt_data.loc[almnt_base,'J/G'].item()*almnt_data.loc[almnt_base,'G'].item(),6)
ct_e=1/ftg_max/0.8
almnt_len=len(almnt_data)
for ligne in range(almnt_len):
    if pandas.isna(almnt_data.loc[ligne,'H']) :v=round(sphr_vlm(almnt_data.loc[ligne,'D'].item()/2)*1000,6)
    else:v=round(clndr_vlm(almnt_data.loc[ligne,'D'].item()/2,almnt_data.loc[ligne,'H'].item())*1000,6)
    gv=round(almnt_data.loc[ligne,'G'].item()/v,6)
    e=round(e_j*almnt_data.loc[ligne,'J/G'].item()*almnt_data.loc[ligne,'G'].item(),6)
    ct=round(ct_e*e,6)
    n=10**NMBRsc(min(e,ct),'<0')
    en,ctn,gn=round(e*n),round(ct*n),round(n*almnt_data.loc[ligne,'G'])
    result=[None,None,None,ctn,en,gn,n,ct,e,None,gv,v,None,None,None]
    almnt_data.loc[ligne]=RMPLC(almnt_data.loc[ligne].tolist(),result)
almnt_data.to_csv(almnt,index=False)

from FRML import CLEF
"mettre à jour les donnée lier à l'agriculture"
"ce sont les parametre de separation entre les plans et leurs durées de vie"
"A:aire(m²), C:cout, F:'fruit', P:plan, T:temps(ans), U:unité, V:volume(litre)"
agri='E:/Program/pyton/MMO/agriculture.csv'
agri_data=pandas.read_csv(agri)
agri_data=agri_data.sort_values('NOM')
agri_len=len(agri_data)
for ligne in range(agri_len):
    pm=round(1/agri_data.loc[ligne,'L']/agri_data.loc[ligne,'l'],6)
    fmt=round(pm*agri_data.loc[ligne,'F/P/T'],6)
    fm=round(fmt*agri_data.loc[ligne,'T'],6)
    if pandas.isna(agri_data.loc[ligne,'D']) :v=round(clndr_vlm(0.1/2,agri_data.loc[ligne,'H'])*1000,6)
    else:v=round(clndr_vlm(agri_data.loc[ligne,'D']/2,agri_data.loc[ligne,'H'])*1000,6)
    ct=round(fm*CLEF(almnt_data,agri_data,ligne,'F','C'))
    result=[None,None,None,None,ct,v,fm,fmt,pm]
    agri_data.loc[ligne]=RMPLC(agri_data.loc[ligne].tolist(),result)
agri_data.to_csv(agri,index=False)

"mettre à jour les donnée lier à l'elevage"
"A:aire(m²), C:cout, F:'fruit', P:plan, T:temps(ans), U:unité, V:volume(litre)"
elvg='E:/Program/pyton/MMO/elvage.csv'
elvg_data=pandas.read_csv(elvg)
elvg_data=elvg_data.sort_values('NOM')
elvg_len=len(elvg_data)
for elvg_ligne in range(elvg_len):
    almnt_ligne=CLEF(almnt_data,elvg_data,elvg_ligne,'NOM','NOM')
    gm=round(elvg_data.loc[a,'G'].item()*elvg_data.loc[elvg_ligne,'P/M'].item(),6)
    gmt=round(gm/elvg_data.loc[elvg_ligne,'T'].item(),6)
    n=round(1/almnt_data.loc[almnt_ligne,'G'].item(),6)
    ct=round(n*almnt_data.loc[almnt_ligne,'C'].item())
    colone=['C','N','G/M/T','G/M']
    result=[ct,n,gmt,gm]
    elvg_data.loc[elvg_ligne]=RMPLC(elvg_data.loc[elvg_ligne].tolist(),result)
elvg_data.to_csv(elvg,index=False)

"metre a jour les materieau de constructuion"
"C:cout, G:poid(Kg), R:rareté, V:volume(litre)"
mtr='E:\Program\pyton\MMO\materieau.csv'
mtr_data=pandas.read_csv(mtr)
mtr_data=mtr_data.sort_values('NOM')
mtr_len=len(mtr_data)
for a in range(mtr_len):
    if mtr_data.loc[a,'CATG']=='agrcl':
        cg=round(CLEF(agri_data,mtr_data,a,'NOM','C')
                 /CLEF(agri_data,mtr_data,a,'NOM','V')
                 /mtr_data.loc[a,'G/V']
                 /mtr_data.loc[a,'R'],6)
    else:cg=round(mtr_data.loc[a,'G/V']/mtr_data.loc[a,'R'],6)
    if mtr_data.loc[a,'C/G']!=cg:
       mtr_data.loc[a,'MAJ']=datetime.now()
       mtr_data.loc[a,'C/G']=cg
mtr_data.to_csv(mtr,index=False)


"metre a jour la composition des objet"
cmp='E:\Program\pyton\MMO\composition.csv'
cmp_data=pandas.read_csv(cmp)
cmp_data=cmp_data.sort_values('NOM')
mtr_lst=mtr_data['NOM'].tolist()
b=3
for a in range(mtr_len):
    cmp_lst=list(cmp_data.columns.values)
    cmp_lst_len=len(cmp_lst)
    # nom=mtr_data.loc[a,'TYPE']+"_"+mtr_data.loc[a,'NOM']
    nom=mtr_lst[a]
    if nom not in cmp_lst:
        while cmp_lst[b]<nom or cmp_lst_len<b:
            b+=1
        cmp_data.insert(b,nom,'')
    som=cmp_data.loc[a,mtr_lst].sum()
    if som!=1 or som is None:
        cmp_data.loc[a,'MAJ']=datetime.now()
        cmp_data.loc[a,'TOT']=som
        print(cmp_data.loc[a,'NOM'],"n'est pas bien proportionné")

"maitre a jour les objets"
obj='E:\Program\pyton\MMO\objet.csv'
obj_data=pandas.read_csv(obj)
obj_data=obj_data.sort_values('NOM')
obj_len=len(obj_data)
e_gv=1
s_gv=10
for a in range(obj_len):
    cmp_lst=cmp_data['NOM'].tolist()
    cmp_len=len(cmp_data)
    if obj_data.loc[a,'NOM'] not in cmp_lst:
        cmp_data.loc[cmp_len,'MAJ']=datetime.now()
        cmp_data.loc[cmp_len,'NOM']=obj_data.loc[a,'NOM']
        print(obj_data.loc[a,'NOM'],'à été ajouté à la composition')
    v=round(clndr_vlm(obj_data.loc[a,'D']/2, obj_data.loc[a,'H'])*1000,6)
    g=round(sum([cmp_data.loc[a,mtr_lst[b]]*obj_data.loc[a,'G'] for b in range(mtr_len)]),6)
    gv=round(g/v,6)
    s=round(s_gv*gv,6)
    e=round(e_gv*gv)
    c=round(sum([g*cmp_data.loc[a,mtr_lst[b]]*mtr_data.loc[b,'C/G'] for b in range(mtr_len)]))
    if (obj_data.loc[a,'C']!=c
        or obj_data.loc[a,'E']!=e
        or obj_data.loc[a,'S']!=s
        or obj_data.loc[a,'G/V']!=gv
        or obj_data.loc[a,'G']!=g
        or obj_data.loc[a,'V']!=v):
        obj_data.loc[a,'MAJ']=datetime.now()
        obj_data.loc[a,'C']=c
        obj_data.loc[a,'E']=e
        obj_data.loc[a,'S']=s
        obj_data.loc[a,'G/V']=gv
        obj_data.loc[a,'G']=g
        obj_data.loc[a,'V']=v
cmp_data.to_csv(cmp,index=False)
obj_data.to_csv(obj,index=False)