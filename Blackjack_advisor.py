# -*- coding: utf-8 -*-
"""
Created on Sat Nov  5 19:18:06 2016

@author: Brighton Muffat & Paul Noël Digard
"""

 

import random

################ CODAGE DU SABOT ET DE SON ETAT ############################


def nouveau_sabot():              # Création d'un nouveau sabot
    global sabot
    global etat_sabot
    etat_sabot=[24,24,24,24,24,24,24,24,96,24] #Création d'une liste modélisant l'état du sabot
    sabot=[]
    cartes=[2,3,4,5,6,7,8,9,10,'J','Q','K','A']
    q=0
    while q<24:                                  # Ajout de 6 paquets de cartes au sabot vide (comme dans les casinos français)
        for i in cartes:
            sabot.append(i)
        q+=1
    random.shuffle(sabot)      # On mélange le sabot
     #Création d'une liste modélisant l'état du sabot
    
def modifier_etat_sabot(x):        #dès que l'on tire une carte il faut modifier l'état du sabot
    if x=='J' or x=='Q' or x=='K' :
        etat_sabot[8]-=1             #on modifie l'état du sabot puisque une carte de valeur 10 a été tiré
    elif x=='A' : 
        etat_sabot[9]-=1
    else : 
        etat_sabot[x-2]-=1
        
############## CODAGE DES MAINS INITIALES DES JOUEURS #######################
    
def mains_initiales(): #On se place dans la situation suivante : le dealer, un autre joueur et nous.
    #Premieres cartes distribuées après avoir misé. On se place dans le cas où l'on est à droite du dealer et le joueur 2 à sa gauche
    global dealer
    global moi
    global joueur2
    dealer=[]
    moi=[]
    joueur2=[]
    x=sabot.pop(0)
    joueur2.append(x) #le dealer commence par donner un carte au joueur à sa gauche
    modifier_etat_sabot(x)
    x=sabot.pop(0)
    moi.append(x) #le dealer nous distribue ensuite une carte
    modifier_etat_sabot(x)
    x=sabot.pop(0)
    dealer.append(x) #le dealer se distribue ensuite une carte
    modifier_etat_sabot(x)
    x=sabot.pop(0)
    joueur2.append(x) #le dealer donne une seconde carte au joueur à sa gauche (le joueur 2)
    modifier_etat_sabot(x)
    x=sabot.pop(0)
    moi.append(x) #le dealer nous donne une seconde carte
    modifier_etat_sabot(x)
    return(joueur2,moi,dealer)

################ CODAGE DE LA VALEUR D'UNE MAIN QUELCONQUE #################


def valeur_main(main):
    global as11
    as11=0
    total=0
    nb_as=0   # nombre d'as à valeur 11 
    n=len(main)
    for i in range (n):
        if main[i]=='J' or main[i]=='Q' or main[i]=='K':
            total+=10
        elif main[i]=='A':
            total+=11 
            nb_as+=1
            as11=1
        else :
            total+=main[i]
    while nb_as>0 and total>21:
        total-=10
        nb_as-=1
    if total>21 :
        return(22)
    return(total)
    
################# CODAGE DES ACTIONS DE JEU ###########################
           
def tirer(main):
    input("On tire")
    x=sabot.pop(0)
    modifier_etat_sabot(x)
    main.append(x)
    input("Main après tirage :" + str(main))
    
def doubler(main):
    tirer(main)
    
################ STRATEGIE DU DEALER #########################################
    
def strategie_dealer(main):
    while valeur_main(main)<17:
        tirer(main)
    if valeur_main(main)>21:
            input("Busted")

############### ETABLIR LE GAGNANT ###########################################
    
def comparaison_mains(moi,dealer):
    
    if len(moi)==2 and valeur_main(moi)==21:
        input("Blackjack! Bien joué vous remporter deux fois et demi votre mise!")
        return(mise*1.5)
    elif valeur_main(moi)>21:
        input("Vous avez perdu la main, dommage vous perdez votre mise.")
        return(-mise)
    elif valeur_main(dealer)>21:
        input("Vous avez gagné la main, bien joué vous remporter deux fois votre mise!")
        return(mise)
    elif valeur_main(moi)==valeur_main(dealer):
        input("Egalité, vous regagnez votre mise")
        return(0)
    elif valeur_main(moi)>valeur_main(dealer):
        input("Vous avez gagné la main, bien joué vous remporter deux fois votre mise!")
        return(mise)
    elif valeur_main(moi)<valeur_main(dealer):
        input("Vous avez perdu la main, dommage vous perdez votre mise.")
        return(-mise)

################# CODAGE DU JEU AVEC LA STRATEGIE DU DEALER ################

def tour():
    global mise
    mise=int(input("Combien souhaitez-vous miser? "))
    mains=mains_initiales()
    input("Main du joueur 2 : " + str(mains[0]))
    strategie_dealer(mains[0])
    input("Votre main : " + str(mains[1]))
    strategie_dealer(mains[1])
    input("Main du dealer " + str(mains[2]))
    strategie_dealer(mains[2])
    
    
    
def jeu():
    nouveau_sabot()
    solde=int(input("Quelle est votre bankroll? "))
    while(len(sabot)>63):
        tour()
        x=comparaison_mains(moi,dealer)
        solde+=x
        input("Ton solde est de " + str(solde))
        input("Etat du sabot " + str(etat_sabot))
    jeu()
    
################## PROBABILITE DE TIRAGE ##########################
    
def proba_tirer(k): # probabilité de tirer une carte de valeur k 
    n=len(sabot)
    p=(etat_sabot[k-2]/n)
    return(p)
    
################ MATRICE DU DEALER OU CROUPIER ########################
    
    
def matrice_dealer():
    #lignes 0 à 8 (états initiaux sans as)
    D=[[0]*35 for i in range (35)]#On remplit la matrice de 0
    for i in range(9):          # Des états initiaux sans as...
        for j in range (10,23): #...vers hard
            if j-i>9 and j-i<19:
                D[i][j]=proba_tirer(j-i-8)
        for j in range(24,28):   #...vers soft
            if i<4 and (i+ 24)==j:
                D[i][j]=proba_tirer(11)
        for j in range (28,32): #... vers finaux 
            if j-i<25 : 
                D[i][j]=proba_tirer(j-i-13)
    D[8][33]=proba_tirer(11)    #... vers blackjack
    #ligne 9 (état initial avec as)
    D[9][23]=proba_tirer(11)    #De l'état initial avec as au soft 12
    for j in range(24,32):      #De l'état initial avec as aux états finaux
        D[9][j]=proba_tirer(j-22)
    D[9][33]=proba_tirer(10)     #De l'état initial avec as au blackjack
    #états hard (sans 16),lignes 9 à 21 
    for i in range (10,22): #états hards...
        for j in range (12,23):#...vers hard
            if j-i>1 and j-i<11:
                D[i][j]=proba_tirer(j-i)
        if i>16 :
            D[i][i+1]=proba_tirer(11)
    #...vers soft
    D[10][26]=proba_tirer(11)
    D[11][27]=proba_tirer(11)
    #...vers finaux 
    for i in range (12,22):
        for j in range (28,33):
            if j-i<17:
                D[i][j]=proba_tirer(j-i-5)
    #...vers bust
    for i in range(18,23):
        for j in range(6,11):
            if (i-6)+j>21:
                D[i][34]+=proba_tirer(j)
    #état initial hard 16 vers états finaux
    D[22][28]=proba_tirer(11)
    for j in range(29,33):
        D[22][j]=proba_tirer(j-27)
    #états initiaux soft 
    for i in range(23,28): #...vers hard
        for j in range (18,23):
            if j-i<-4 :
                D[i][j]=proba_tirer(j-i+15)
        D[i][i+1]=proba_tirer(11) #vers soft +1
        for j in range (25,33): #vers soft et finaux 
            if j-i>1:
                D[i][j]=proba_tirer(j-i)
    #états finaux vers états finaux
    for i in range (28,35):
        D[i][i]=1   
    return(D)
    
##################  MATRICE DU JOUEUR  #########################
    
def kron(strat1,strat2):
    if strat1==strat2:
        return(1)
    else:
        return(0)
        
        
def matrice_joueur(strategie):
    J=[[0]*87 for i in range (87)] #On remplit la matrice de 0
    #Des états initiaux hard(sans as valant 11)
    for i in range (0,17):
        #vers états hard avec un as valant 1
        if i>6 and i<16:
            J[i][i+26]=kron(strategie,"Tirer")*proba_tirer(11)
        #vers états hard sans as
        for j in range (27,42): 
            if j-i>26 and j-i<36:
                J[i][j]=kron(strategie,"Tirer")*proba_tirer(j-i-25)
        #vers états hard avec un as valant 11
        if i<6:
            J[i][i+44]=kron(strategie,"Tirer")*proba_tirer(11)
        #vers états finaux rester
        for j in range(50,67):
            J[i][i+50]=kron(strategie,"Rester")
        #vers 21 sans blackjack (colonne 67)
        if i>5 and i<16:
            J[i][67]=kron(strategie,"Tirer")*proba_tirer(17-i)
        #vers 21 avec un as qui vaut 1
        J[16][67]=kron(strategie,"Tirer")*proba_tirer(11)
        #vers états finaux en doublant
        for j in range(68,84):
            if j-i>67 and j-i<78:
                J[i][j]=kron(strategie,"Doubler")*proba_tirer(j-i-66)
        #vers états finaux en doubalnt avec as valant un
        if i>6 :
            J[i][i+67]=kron(strategie,"Doubler")*proba_tirer(11)
        #vers busted en tirant et en doublant
        if i>7:
            for j in range(2,11):
                if j+i+4>21:
                    J[i][84]+=kron(strategie,"Tirer")*proba_tirer(j)
                    J[i][85]+=kron(strategie,"Doubler")*proba_tirer(j)
    #Des initiaux soft (avec as valant 11)
    for i in range (17,26):
        #vers hard : c'est à dire que l'as dans la main initiale prend la valeur 11
        for j in range(33,42):
            if j-i<17:
                J[i][j]=kron(strategie,"Tirer")*proba_tirer(j-i-6)
        if i<25:
            #vers soft sans tirer un as : c'est à dire que l'as dans la mains initiale reste à valeur 11
            for j in range(43,50):
                if j-i>25:
                    J[i][j]=kron(strategie,"Tirer")*proba_tirer(j-i-24)
            #vers soft avec as
            J[i][i+25]=kron(strategie,"Tirer")*proba_tirer(11)
        #vers états finaux sans 21
        J[i][i+41]=kron(strategie,"Rester")
        #vers états finaux avec 21 mais sans blackjack
        if i<25:
            J[i][67]=kron(strategie,"Tirer")*proba_tirer(26-i)
        J[25][67]=kron(strategie,"Tirer")*proba_tirer(11)
        #vers états finaux en doublant 
        for j in range(74,84):
            if j<76:
                J[i][j]=kron(strategie,"Doubler")*proba_tirer(j-i-47)
            if j>=76:
                if j-i<58 :
                    J[i][j]=kron(strategie,"Doubler")*proba_tirer(j-i-47)
                elif j-i==58:
                    J[i][i+58]=kron(strategie,"Doubler")*proba_tirer(11)
                else:
                    J[i][j]=kron(strategie,"Doubler")*proba_tirer(j-i-57)
    #Des états hard non initiaux (donc strategie du double impossible ici)
    for i in range(26,42):
        #Vers états hard 
        for j in range (28,42):
            if j-i>1 and j-i<11:
                J[i][j]=kron(strategie,"Tirer")*proba_tirer(j-i)
        if i>31 and i<41:
            J[i][i+1]=kron(strategie,"Tirer")*proba_tirer(11)
        #Vers états soft 
        if i<31:
            J[i][i+19]=kron(strategie,"Tirer")*proba_tirer(11)
        #Vers états finaux sans doubler
        J[i][i+25]=kron(strategie,"Rester")
        #Vers états finaux avec 21 mais sans blackjack
        if i>30 and i<41:
            J[i][67]=kron(strategie,"Tirer")*proba_tirer(42-i)
        J[41][67]=kron(strategie,"Tirer")*proba_tirer(11)
        #Vers busted en tirant 
        if i>32:
            for j in range(2,11):
                if i-21+j>21:
                    J[i][84]+=kron(strategie,"Tirer")*proba_tirer(j)
    # Des états soft non initiaux (donc strategie du double impossible ici)
    for i in range (42,50):
        #Vers états hard (as se transforme en 1)
        for j in range(33,42):
            if j-i<-7:
                J[i][j]=kron(strategie,"Tirer")*proba_tirer(j-i+18)
        #Vers états soft 
        for j in range (44,50):
            if j-i>1:
                J[i][j]=kron(strategie,"Tirer")*proba_tirer(j-i)
        if i<49:
            J[i][i+1]=kron(strategie,"Tirer")*proba_tirer(11)
        #Vers états finaux 
        J[i][i+17]=kron(strategie,"Rester")
        #Vers états finaux avec 21 mais sans blackjack
        if i<49:
            J[i][67]=kron(strategie,"Tirer")*proba_tirer(50-i)
        J[49][67]=kron(strategie,"Tirer")*proba_tirer(11)
    #Des états finaux aux états finaux
    for i in range(50,87):
        J[i][i]=1
    return(J)
    
################### VERIFICATION DE LA MATRICE JOUEUR (STOCHASTIQUE) ############################
"""
nouveau_sabot()
J=matrice_joueur("Rester")
print(J)
for i in range(len(J)):
    s=0
    for j in range(len(J)):
        s+=J[i][j]
    print(s)
    
"""

################## EXPONENTATION RAPIDE DE MATRICES  ###################

    
def expo_rapide_mat(A,n):
    #La fonction prend en entrée une matrice A et un entier naturel n, et retourne A^n
    X=A
    p=len(A)
    Y=[[0]*p for i in range(p) ] 
    # Construction de la matrice identité
    for i in range (p):
        Y[i][i]=1
    m=n
    while m>0:
        q,r=m//2,m%2 # quotient et reste dans la division euclidienne de m par 2.
        if r==1:
            Y=np.dot(Y,X) # on multiplie y par x, le résultat est affecté à y.
        X=np.dot(X,X) # on met x au carré, le résultat est affecté à x.
        m=q
    return (Y)
    
    

################## SIGMA QUI ASSOCIE AUX ETATS FINAUX LES GAINS ###############

def sigma (Fjoueur,Fcroupier): 
    #états finaux du joueur indépendant de ceux du croupier
    if Fjoueur==84:
        return(-mise)
    elif Fjoueur==85:
        return(-2*mise)
    elif Fjoueur==86:
        return(mise*1.5)
    #états finaux du joueur qui a doublé
    elif Fjoueur>67:
        if Fcroupier==34:
            return(2*mise)
        if Fcroupier==33:
            return(-2*mise)
        if Fjoueur-62==Fcroupier-11:
            return(0)
        elif Fjoueur-62>Fcroupier-11:
            return(2*mise)
        else :
            return(-2*mise)
    #états finaux du joueur qui n'a pas doublé
    elif Fcroupier==34:
        return(mise)
    if Fcroupier==33:
        return(-mise)
    if Fjoueur-46==Fcroupier-11:
        return(0)
    elif Fjoueur-46>Fcroupier-11:
        return(mise)
    else :
        return(-mise)
    


################  PROBABILITE D'ARRIVER DANS UN ETAT FINAL DONNE ##############

#programmation dynamique, on stocke les matrices du joueur dans une liste 
# cela évite de les recalculer pour chaque strategie

def utilisation_matjoueur(): 
    global Cro
    global Jou
    Jou=[]
    Cro=Pc=expo_rapide_mat(matrice_dealer(),17) #élévation de la matrice du croupier à la puissance 17
    J=matrice_joueur("Tirer")
    Jou.append(J)
    for i in range (20):
        J=np.dot(J,matrice_joueur("Tirer"))
        Jou.append(J)
    


def proba_final(Fjoueur,Fcroupier,strategie):
    n=len(strategie)
    #si le joueur dépasse 21 il est inutile de suivre le croupier, le joueur perd sa mise.
    if Fjoueur==85 or Fjoueur==84: 
        if n>1 :
            #les lignes 84 et 85 correspondent aux états BUSTED et 2BUSTED
            J=Jou[n-2]
            J=np.dot(J,matrice_joueur("Rester"))
            P=np.dot(phi_joueur,J) # vecteur initial fois matrice
            return(P[0][Fjoueur])
        else :
            J=matrice_joueur(strategie[0])
            P=np.dot(phi_joueur,J) # vecteur initial fois matrice
            return(P[0][Fjoueur])
    else:
        if n>1 :
            J=Jou[n-2]
            J=np.dot(J,matrice_joueur("Rester"))
            Pj=np.dot(phi_joueur,J) # vecteur initial fois matrice
            Pj=Pj[0][Fjoueur]
            #proba pour que le joueur soit dans cet état final :
            #proba pour que le dealer soit dans cet état final
            Pc=Cro
            Pc=np.dot(phi_croupier,Pc)
            Pc=Pc[0][Fcroupier]
            return(Pj*Pc)
        else :
            J=matrice_joueur(strategie[0])
            Pj=np.dot(phi_joueur,J) # vecteur initial fois matrice
            Pj=Pj[0][Fjoueur]
            Pc=Cro
            Pc=np.dot(phi_croupier,Pc)
            Pc=Pc[0][Fcroupier]
            return(Pj*Pc)
            
            

############################## ESPERANCE ######################################


def esperance(strategie):
    esperance=0
    #états finaux correspondant à ceux du joueur
    for i in range (50,87):
        #états finaux correpondant à ceux du dealer
        for j in range(27,35):
            esperance+=proba_final(i,j,strategie)*sigma(i,j)
    return(esperance)
    
###################### CALCUL DE LA MEILLEURE STRATEGIE #######################

# On implémente le tri_fusion, tri de complexité optimale pour choisir la meilleur esperance

def fusion(L1,L2,g,m,d): # Listes de couple et on trie par rapport à la seconde valeur du couple pour garder la position des strategies
    i1=g
    i2=m
    for i in range(g,d):
        if i2==d or (i1<m and L1[i1][1]<=L1[i2][1]):
            L2[i]=L1[i1]
            i1+=1
        else:
            L2[i]=L1[i2]
            i2+=1
            
            
def tri_fusion_couple(L):
    Ltmp=[[None,None]]*len(L)
    def tri_fusion_rec(g,d):
        if g<d-1:
            m=(g+d)//2
            tri_fusion_rec(g,m)
            tri_fusion_rec(m,d)
            Ltmp[g:d]=L[g:d]
            fusion(Ltmp,L,g,m,d)
    tri_fusion_rec(0,len(L))
   


def meilleur_strategie():
    utilisation_matjoueur()
    # liste de toute les strategies possibles
    liste_strategie=[["Doubler"]] 
    for i in range (21):
        X=(["Tirer"]*i)+["Rester"]
        liste_strategie.append(X)
    n=len(liste_strategie)
    liste_esperance=[None]*n
    for i in range (n):
        x=esperance(liste_strategie[i])
        liste_esperance[i]=x
    # la liste à trier est une liste de couple qui à chaque strategie associe son esperance
    liste_a_trier=[]
    for i in range (n):
        x=liste_strategie[i]
        y=liste_esperance[i]
        liste_a_trier.append([x,y])
    tri_fusion_couple(liste_a_trier)
    return( "La meilleur stratégie est " + str(liste_a_trier[n-1][0]) + " Et son espérance est " + str(liste_a_trier[n-1][1]))

################### CONSTRUCTION VECTEURS INITIAUX ############################

def vecteurs_initiaux(mains):
    global phi_croupier
    global phi_joueur
    vcroupier=valeur_main(mains[2])
    vjoueur=valeur_main(mains[1])
    phi_croupier=[[0]*35]
    phi_joueur=[[0]*87]
    phi_croupier[0][vcroupier-2]=1
    if vjoueur==21:
        phi_joueur[0][86]=1
    #soft
    elif as11==1:
         phi_joueur[0][vjoueur+5]=1
    else:
        phi_joueur[0][vjoueur-4]=1
        
################### CODAGE JEU BLACKJACK ADVISOR ##############################


def tour2():
    global mise
    mise=int(input("Combien souhaitez-vous miser? "))
    mains=mains_initiales()
    #JOUEUR 2 QUI JOUE
    input("Main du joueur 2 : " + str(mains[0]))
    strategie_dealer(mains[0])
    #NOUS JOUONS
    vecteurs_initiaux(mains)
    input("Votre main : " + str(mains[1]))
    action=3
    print(meilleur_strategie())
    while valeur_main(mains[1])<=21 and action != 0 :
        action=int(input("Que souhaitez-vous faire ? Taper 0 pour Rester, 1 pour Tirer et 2 pour Doubler : "))
        if action==2 :
            mise*=2
            doubler(mains[1])
            action=0
        if action==1:
            tirer(mains[1])
    if valeur_main(mains[1])>21:
            input("Busted")
    #AU DEALER DE JOUER
    input("Main du dealer " + str(mains[2]))
    strategie_dealer(mains[2])


def Blackjack_Advisor():
    nouveau_sabot()
    solde=int(input("Quelle est votre bankroll? "))
    while(len(sabot)>63):
        tour2()
        x=comparaison_mains(moi,dealer)
        solde+=x
        input("Ton solde est de " + str(solde))
        input("Etat du sabot " + str(etat_sabot))
    jeu()
    



################### CODAGE DE FENETRE POUR INTERFACE GRAPHIQUE ################


from tkinter import *
from tkinter.simpledialog import *


class Interface_Graphique_Blackjack_Advisor(Frame):
    
    def __init__(self,fenetre):
        Frame.__init__(self,fenetre)
        #création fenetre
        fenetre.title("Blackjack Advisor")
        fenetre.iconbitmap("C:/Users/brighton/Desktop/TIPE Blackjack/Code/icone.ico")

        # fenetre plein écran
        fenetre.wm_state(newstate="zoomed")
        
        # demande de la bankroll
        
        bankroll=self.bankroll=askinteger("Bankroll","Quelle est ta bankroll?")
        
        # Création main croupier
        Frame1=Frame(fenetre, borderwidth=2, relief=GROOVE)
        Frame1.pack(side=TOP, padx=5, pady=5)
        Label(Frame1,height=8, width=200).pack(padx=10,pady=10)
        
        Frame1_2=Frame(Frame1, borderwidth=2, relief=GROOVE)
        Frame1_2.place(in_=Frame1, anchor="c",relx=0.065, rely=0.4)
        Label(Frame1_2,text="Main du croupier :").pack(padx=10, pady=10)
        
        # Création cartes croupier
        photo2=self.photo2=PhotoImage(file="C:/Users/brighton/Desktop/TIPE Blackjack/Code/2pique.gif")
            
        Frame1_3=Frame(Frame1, relief=RAISED)
        Frame1_3.place(in_=Frame1,anchor='c',relx=0.18,rely=0.4)
        Label(Frame1_3,image=photo2).pack()
            
        Frame1_4=self.Frame1_4=Frame(Frame1, relief=FLAT)
        Frame1_4.place(in_=Frame1, anchor='c',relx=0.18,rely=0.86)
        self.Frame1_41=Label(Frame1_4, text="0")
        self.Frame1_41.pack() 
            
        photo3=self.photo3=PhotoImage(file="C:/Users/brighton/Desktop/TIPE Blackjack/Code/3pique.gif")
            
        Frame1_5=Frame(Frame1, relief=RAISED)
        Frame1_5.place(in_=Frame1,anchor='c',relx=0.26,rely=0.4)
        Label(Frame1_5,image=photo3).pack()
            
        Frame1_6=Frame(Frame1, relief=FLAT)
        Frame1_6.place(in_=Frame1, anchor='c',relx=0.26,rely=0.86)
        self.Frame1_61=Label(Frame1_6, text="0")
        self.Frame1_61.pack()
        
        photo4=self.photo4=PhotoImage(file="C:/Users/brighton/Desktop/TIPE Blackjack/Code/4pique.gif")
        
        Frame1_7=Frame(Frame1, relief=RAISED)
        Frame1_7.place(in_=Frame1,anchor='c',relx=0.34,rely=0.4)
        Label(Frame1_7,image=photo4).pack()
        
        Frame1_8=Frame(Frame1, relief=FLAT)
        Frame1_8.place(in_=Frame1, anchor='c',relx=0.34,rely=0.86)
        self.Frame1_81=Label(Frame1_8, text="0")
        self.Frame1_81.pack()
        
        photo5=self.photo5=PhotoImage(file="C:/Users/brighton/Desktop/TIPE Blackjack/Code/5pique.gif")
        
        Frame1_9=Frame(Frame1, relief=RAISED)
        Frame1_9.place(in_=Frame1,anchor='c',relx=0.42,rely=0.4)
        Label(Frame1_9,image=photo5).pack()
        
        Frame1_10=Frame(Frame1, relief=FLAT)
        Frame1_10.place(in_=Frame1, anchor='c',relx=0.42,rely=0.86)
        self.Frame1_101=Label(Frame1_10, text="0")
        self.Frame1_101.pack()
        
        photo6=self.photo6=PhotoImage(file="C:/Users/brighton/Desktop/TIPE Blackjack/Code/6pique.gif")
        
        Frame1_11=Frame(Frame1, relief=RAISED)
        Frame1_11.place(in_=Frame1,anchor='c',relx=0.50,rely=0.4)
        Label(Frame1_11,image=photo6).pack()
        
        Frame1_12=Frame(Frame1, relief=FLAT)
        Frame1_12.place(in_=Frame1, anchor='c',relx=0.50,rely=0.86)
        self.Frame1_121=Label(Frame1_12, text="0")
        self.Frame1_121.pack()
        
        photo7=self.photo7=PhotoImage(file="C:/Users/brighton/Desktop/TIPE Blackjack/Code/7pique.gif")
        
        Frame1_13=Frame(Frame1, relief=RAISED)
        Frame1_13.place(in_=Frame1,anchor='c',relx=0.58,rely=0.4)
        Label(Frame1_13,image=photo7).pack()
        
        Frame1_14=Frame(Frame1, relief=FLAT)
        Frame1_14.place(in_=Frame1, anchor='c',relx=0.58,rely=0.86)
        self.Frame1_141=Label(Frame1_14, text="0")
        self.Frame1_141.pack()
        
        photo8=self.photo8=PhotoImage(file="C:/Users/brighton/Desktop/TIPE Blackjack/Code/8pique.gif")
        
        Frame1_15=Frame(Frame1, relief=RAISED)
        Frame1_15.place(in_=Frame1,anchor='c',relx=0.66,rely=0.4)
        Label(Frame1_15,image=photo8).pack()
        
        Frame1_16=Frame(Frame1, relief=FLAT)
        Frame1_16.place(in_=Frame1, anchor='c',relx=0.66,rely=0.86)
        self.Frame1_161=Label(Frame1_16, text="0")
        self.Frame1_161.pack()
        
        photo9=self.photo9=PhotoImage(file="C:/Users/brighton/Desktop/TIPE Blackjack/Code/9pique.gif")
        
        Frame1_17=Frame(Frame1, relief=RAISED)
        Frame1_17.place(in_=Frame1,anchor='c',relx=0.74,rely=0.4)
        Label(Frame1_17,image=photo9).pack()
        
        Frame1_18=Frame(Frame1, relief=FLAT)
        Frame1_18.place(in_=Frame1, anchor='c',relx=0.74,rely=0.86)
        self.Frame1_181=Label(Frame1_18, text="0")
        self.Frame1_181.pack()
        
        photo10=self.photo10=PhotoImage(file="C:/Users/brighton/Desktop/TIPE Blackjack/Code/10pique.gif")
        
        Frame1_19=Frame(Frame1, relief=RAISED)
        Frame1_19.place(in_=Frame1,anchor='c',relx=0.82,rely=0.4)
        Label(Frame1_19,image=photo10).pack()
        
        Frame1_20=Frame(Frame1, relief=FLAT)
        Frame1_20.place(in_=Frame1, anchor='c',relx=0.82,rely=0.86)
        self.Frame1_201=Label(Frame1_20, text="0")
        self.Frame1_201.pack()
        
        photo11=self.photo11=PhotoImage(file="C:/Users/brighton/Desktop/TIPE Blackjack/Code/Apique.gif")
        
        Frame1_21=Frame(Frame1, relief=RAISED)
        Frame1_21.place(in_=Frame1,anchor='c',relx=0.90,rely=0.4)
        Label(Frame1_21,image=photo11).pack()
        
        Frame1_22=Frame(Frame1, relief=FLAT)
        Frame1_22.place(in_=Frame1, anchor='c',relx=0.90,rely=0.86)
        self.Frame1_221=Label(Frame1_22, text="0")
        self.Frame1_221.pack()
        
        # Création main joueur
        Frame2=Frame(fenetre, borderwidth=2, relief=GROOVE)
        Frame2.pack(padx=5, pady=5)
        Label(Frame2,height=8, width=200).pack(padx=10,pady=10)
        
        Frame2_2=Frame(Frame2, borderwidth=2, relief=GROOVE)
        Frame2_2.place(in_=Frame2, anchor="c",relx=0.065, rely=0.4)
        Label(Frame2_2,text="Ma main :").pack(padx=10, pady=10)
        
        # Création cartes joueur
        
        Frame2_3=Frame(Frame2, relief=RAISED)
        Frame2_3.place(in_=Frame2,anchor='c',relx=0.18,rely=0.4)
        Label(Frame2_3,image=photo2).pack()
        
        Frame2_4=Frame(Frame2, relief=FLAT)
        Frame2_4.place(in_=Frame2, anchor='c',relx=0.18,rely=0.86)
        self.Frame2_41=Label(Frame2_4, text="0")
        self.Frame2_41.pack() 
        
        
        Frame2_5=Frame(Frame2, relief=RAISED)
        Frame2_5.place(in_=Frame2,anchor='c',relx=0.26,rely=0.4)
        Label(Frame2_5,image=photo3).pack()
        
        Frame2_6=Frame(Frame2, relief=FLAT)
        Frame2_6.place(in_=Frame2, anchor='c',relx=0.26,rely=0.86)
        self.Frame2_61=Label(Frame2_6, text="0")
        self.Frame2_61.pack()
        
        
        Frame2_7=Frame(Frame2, relief=RAISED)
        Frame2_7.place(in_=Frame2,anchor='c',relx=0.34,rely=0.4)
        Label(Frame2_7,image=photo4).pack()
        
        Frame2_8=Frame(Frame2, relief=FLAT)
        Frame2_8.place(in_=Frame2, anchor='c',relx=0.34,rely=0.86)
        self.Frame2_81=Label(Frame2_8, text="0")
        self.Frame2_81.pack()
        
        
        Frame2_9=Frame(Frame2, relief=RAISED)
        Frame2_9.place(in_=Frame2,anchor='c',relx=0.42,rely=0.4)
        Label(Frame2_9,image=photo5).pack()
        
        Frame2_10=Frame(Frame2, relief=FLAT)
        Frame2_10.place(in_=Frame2, anchor='c',relx=0.42,rely=0.86)
        self.Frame2_101=Label(Frame2_10, text="0")
        self.Frame2_101.pack()
        
        
        Frame2_11=Frame(Frame2, relief=RAISED)
        Frame2_11.place(in_=Frame2,anchor='c',relx=0.50,rely=0.4)
        Label(Frame2_11,image=photo6).pack()
        
        Frame2_12=Frame(Frame2, relief=FLAT)
        Frame2_12.place(in_=Frame2, anchor='c',relx=0.50,rely=0.86)
        self.Frame2_121=Label(Frame2_12, text="0")
        self.Frame2_121.pack()
        
        
        Frame2_13=Frame(Frame2, relief=RAISED)
        Frame2_13.place(in_=Frame2,anchor='c',relx=0.58,rely=0.4)
        Label(Frame2_13,image=photo7).pack()
        
        Frame2_14=Frame(Frame2, relief=FLAT)
        Frame2_14.place(in_=Frame2, anchor='c',relx=0.58,rely=0.86)
        self.Frame2_141=Label(Frame2_14, text="0")
        self.Frame2_141.pack()
        
        
        Frame2_15=Frame(Frame2, relief=RAISED)
        Frame2_15.place(in_=Frame2,anchor='c',relx=0.66,rely=0.4)
        Label(Frame2_15,image=photo8).pack()
        
        Frame2_16=Frame(Frame2, relief=FLAT)
        Frame2_16.place(in_=Frame2, anchor='c',relx=0.66,rely=0.86)
        self.Frame2_161=Label(Frame2_16, text="0")
        self.Frame2_161.pack()
        
        
        Frame2_17=Frame(Frame2, relief=RAISED)
        Frame2_17.place(in_=Frame2,anchor='c',relx=0.74,rely=0.4)
        Label(Frame2_17,image=photo9).pack()
        
        Frame2_18=Frame(Frame2, relief=FLAT)
        Frame2_18.place(in_=Frame2, anchor='c',relx=0.74,rely=0.86)
        self.Frame2_181=Label(Frame2_18, text="0")
        self.Frame2_181.pack()
        
        
        Frame2_19=Frame(Frame2, relief=RAISED)
        Frame2_19.place(in_=Frame2,anchor='c',relx=0.82,rely=0.4)
        Label(Frame2_19,image=photo10).pack()
        
        Frame2_20=Frame(Frame2, relief=FLAT)
        Frame2_20.place(in_=Frame2, anchor='c',relx=0.82,rely=0.86)
        self.Frame2_201=Label(Frame2_20, text="0")
        self.Frame2_201.pack()
        
        
        Frame2_21=Frame(Frame2, relief=RAISED)
        Frame2_21.place(in_=Frame2,anchor='c',relx=0.90,rely=0.4)
        Label(Frame2_21,image=photo11).pack()
        
        Frame2_22=Frame(Frame2, relief=FLAT)
        Frame2_22.place(in_=Frame2, anchor='c',relx=0.90,rely=0.86)
        self.Frame2_221=Label(Frame2_22, text="0")
        self.Frame2_221.pack()
        
        # Création main de l'autre joueur
        Frame3=Frame(fenetre, borderwidth=2, relief=GROOVE)
        Frame3.pack(padx=5, pady=5)
        Label(Frame3,height=8, width=200).pack(padx=10,pady=10)
        
        Frame3_2=Frame(Frame3, borderwidth=2, relief=GROOVE)
        Frame3_2.place(in_=Frame3, anchor="c",relx=0.065, rely=0.4)
        Label(Frame3_2,text="Main de l'autre joueur :").pack(padx=10, pady=10)
        
        # Création cartes de l'autre joueur
        
        Frame3_3=Frame(Frame3, relief=RAISED)
        Frame3_3.place(in_=Frame3,anchor='c',relx=0.18,rely=0.4)
        Label(Frame3_3,image=photo2).pack()
        
        Frame3_4=Frame(Frame3, relief=FLAT)
        Frame3_4.place(in_=Frame3, anchor='c',relx=0.18,rely=0.86)
        self.Frame3_41=Label(Frame3_4, text="0")
        self.Frame3_41.pack()
        
        
        Frame3_5=Frame(Frame3, relief=RAISED)
        Frame3_5.place(in_=Frame3,anchor='c',relx=0.26,rely=0.4)
        Label(Frame3_5,image=photo3).pack()
        
        Frame3_6=Frame(Frame3, relief=FLAT)
        Frame3_6.place(in_=Frame3, anchor='c',relx=0.26,rely=0.86)
        self.Frame3_61=Label(Frame3_6, text="0")
        self.Frame3_61.pack()        
        
        Frame3_7=Frame(Frame3, relief=RAISED)
        Frame3_7.place(in_=Frame3,anchor='c',relx=0.34,rely=0.4)
        Label(Frame3_7,image=photo4).pack()
        
        Frame3_8=Frame(Frame3, relief=FLAT)
        Frame3_8.place(in_=Frame3, anchor='c',relx=0.34,rely=0.86)
        self.Frame3_81=Label(Frame3_8, text="0")
        self.Frame3_81.pack()
        
        
        Frame3_9=Frame(Frame3, relief=RAISED)
        Frame3_9.place(in_=Frame3,anchor='c',relx=0.42,rely=0.4)
        Label(Frame3_9,image=photo5).pack()
        
        Frame3_10=Frame(Frame3, relief=FLAT)
        Frame3_10.place(in_=Frame3, anchor='c',relx=0.42,rely=0.86)
        self.Frame3_101=Label(Frame3_10, text="0")
        self.Frame3_101.pack()
        
        
        Frame3_11=Frame(Frame3, relief=RAISED)
        Frame3_11.place(in_=Frame3,anchor='c',relx=0.50,rely=0.4)
        Label(Frame3_11,image=photo6).pack()
        
        Frame3_12=Frame(Frame3, relief=FLAT)
        Frame3_12.place(in_=Frame3, anchor='c',relx=0.50,rely=0.86)
        self.Frame3_121=Label(Frame3_12, text="0")
        self.Frame3_121.pack()
        
        
        Frame3_13=Frame(Frame3, relief=RAISED)
        Frame3_13.place(in_=Frame3,anchor='c',relx=0.58,rely=0.4)
        Label(Frame3_13,image=photo7).pack()
        
        Frame3_14=Frame(Frame3, relief=FLAT)
        Frame3_14.place(in_=Frame3, anchor='c',relx=0.58,rely=0.86)
        self.Frame3_141=Label(Frame3_14, text="0")
        self.Frame3_141.pack()
        
        
        Frame3_15=Frame(Frame3, relief=RAISED)
        Frame3_15.place(in_=Frame3,anchor='c',relx=0.66,rely=0.4)
        Label(Frame3_15,image=photo8).pack()
        
        Frame3_16=Frame(Frame3, relief=FLAT)
        Frame3_16.place(in_=Frame3, anchor='c',relx=0.66,rely=0.86)
        self.Frame3_161=Label(Frame3_16, text="0")
        self.Frame3_161.pack()
        
        
        Frame3_17=Frame(Frame3, relief=RAISED)
        Frame3_17.place(in_=Frame3,anchor='c',relx=0.74,rely=0.4)
        Label(Frame3_17,image=photo9).pack()
        
        Frame3_18=Frame(Frame3, relief=FLAT)
        Frame3_18.place(in_=Frame3, anchor='c',relx=0.74,rely=0.86)
        self.Frame3_181=Label(Frame3_18, text="0")
        self.Frame3_181.pack()
        
        
        Frame3_19=Frame(Frame3, relief=RAISED)
        Frame3_19.place(in_=Frame3,anchor='c',relx=0.82,rely=0.4)
        Label(Frame3_19,image=photo10).pack()
        
        Frame3_20=Frame(Frame3, relief=FLAT)
        Frame3_20.place(in_=Frame3, anchor='c',relx=0.82,rely=0.86)
        self.Frame3_201=Label(Frame3_20, text="0")
        self.Frame3_201.pack()
    
    
        Frame3_21=Frame(Frame3, relief=RAISED)
        Frame3_21.place(in_=Frame3,anchor='c',relx=0.90,rely=0.4)
        Label(Frame3_21,image=photo11).pack()
        
        Frame3_22=Frame(Frame3, relief=FLAT)
        Frame3_22.place(in_=Frame3, anchor='c',relx=0.90,rely=0.86)
        self.Frame3_221=Label(Frame3_22, text="0")
        self.Frame3_221.pack()
        
        # Création fenetre sabot 
        
        Frame8=Frame(fenetre, relief=FLAT)
        Frame8.pack(side=RIGHT,padx=5, pady=0)
        Label(Frame8).pack(padx=5,pady=0)
        
        
        Frame4=Frame(Frame8, borderwidth=2, relief=GROOVE)
        Frame4.pack(padx=5, pady=5)
        Label(Frame4,height=3, width=25).pack(padx=10,pady=10)
        
        Frame4_1=Frame(Frame4, borderwidth=2, relief=GROOVE)
        Frame4_1.place(in_=Frame4, anchor="c",relx=0.5, rely=0.3)
        Label(Frame4_1,text="Sabot :").pack(padx=5, pady=5)
        
        Frame4_2=Frame(Frame4, relief=FLAT)
        Frame4_2.place(in_=Frame4, anchor='c',relx=0.5,rely=0.80)
        self.Frame4_21=Label(Frame4_2, text="Pas de Sabot")
        self.Frame4_21.pack()
        
        #Bouton nouvelle main et nouveau sabot
        
        
        Frame6=self.Frame6=Button(Frame8, borderwidth=4,command=self.cliquer_nouveau_sabot)
        Frame6.pack(padx=5, pady=5)
        Label(Frame6,text= "Nouveau Sabot").pack(padx=5,pady=5)
        
        mise=self.mise=0
        
        Frame7=self.Frame7=Button(Frame8, borderwidth=4,command=self.cliquer_nouvellemain)
        Frame7.pack(padx=5, pady=5)
        Label(Frame7,text= "Nouvelle Main").pack(padx=5,pady=5)
        
        # Bouton Que Faire? et affichage mise et bankroll
        
        Frame9=Frame(fenetre, relief=FLAT)
        Frame9.pack(side=LEFT,padx=5, pady=0)
        Label(Frame9).pack(padx=5,pady=0)
        
        Frame10=self.Frame10=Frame(Frame9,borderwidth=4,relief=GROOVE)
        Frame10.pack(padx=5,pady=5)
        self.Frame10_1=Label(Frame10,text="MISE : "+str(mise))
        self.Frame10_1.pack()
        
        Frame11=Frame(Frame9,borderwidth=4,relief=GROOVE)
        Frame11.pack(padx=5,pady=5)
        self.Frame11_1=Label(Frame11,text="BANKROLL : "+str(bankroll))
        self.Frame11_1.pack()
        
        Frame5=Frame(Frame9, borderwidth=2, relief=GROOVE)
        Frame5.pack(side=LEFT,padx=5, pady=0)
        Label(Frame5,height=6, width=30).pack(padx=10,pady=10)
        
        Frame5_1=Button(Frame5, borderwidth=4,command=self.cliquer_meilleure_strategie)
        Frame5_1.place(in_=Frame5, anchor="c",relx=0.5, rely=0.2)
        Label(Frame5_1,text="Que Faire? ").pack(padx=5, pady=5)
        
        Frame5_2=Frame(Frame5, relief=FLAT)
        Frame5_2.place(in_=Frame5, anchor='c',relx=0.5,rely=0.55)
        self.Frame5_21=Label(Frame5_2, text="")
        self.Frame5_21.pack()
        
        Frame5_3=Frame(Frame5, relief=FLAT)
        Frame5_3.place(in_=Frame5, anchor='c',relx=0.5,rely=0.75)
        self.Frame5_31=Label(Frame5_3, text="")
        self.Frame5_31.pack()
        
        
        
        #Bouton Tirer, Rester , Doubler
        
        Frame12=Frame(fenetre,relief=FLAT)
        Frame12.pack(padx=5, pady=5)
        Label(Frame12).pack(padx=5,pady=5)
        
        Frame13=Frame(Frame12, borderwidth=4, relief=RAISED)
        Frame13.pack(side=RIGHT,padx=5, pady=5)
        Label(Frame13,text= "Rester").pack(padx=5,pady=5)
        
        Frame14=Frame(Frame12, borderwidth=4, relief=RAISED)
        Frame14.pack(side=RIGHT,padx=5, pady=5)
        Label(Frame14,text= "Tirer").pack(padx=5,pady=5)
        
        Frame15=Frame(Frame12, borderwidth=4, relief=RAISED)
        Frame15.pack(side=RIGHT,padx=5, pady=5)
        Label(Frame15,text= "Doubler").pack(padx=5,pady=5)
    
        # Affichage message résultat 
        Frame16=Frame(fenetre, borderwidth=4, relief=FLAT)
        Frame16.pack(padx=5, pady=10)
        self.Frame17=Label(Frame16,text= "Cliquez sur Nouveau Sabot")
        self.Frame17.pack(padx=5,pady=10)
        
        
        
    def modifier_etat_sabot2(self,x):        #dès que l'on tire une carte il faut modifier l'état du sabot
        if x=='J' or x=='Q' or x=='K' :
            self.etat_sabot[8]-=1             #on modifie l'état du sabot puisque une carte de valeur 10 a été tiré
        elif x=='A' : 
            self.etat_sabot[9]-=1
        else : 
            self.etat_sabot[x-2]-=1
        self.Frame4_21["text"]=str(self.etat_sabot)
            
                
    def cliquer_nouvellemain(self):
        self.mise=askinteger("Mise","Combien souhaites-tu miser?")
        self.Frame10_1["text"]="MISE: {}".format(self.mise) #Afficher la mise
        #Remise à 0 des compteurs de cartes
        self.Frame1_41["text"]="0"
        self.Frame1_61["text"]="0"
        self.Frame1_81["text"]="0"
        self.Frame1_101["text"]="0"
        self.Frame1_121["text"]="0"
        self.Frame1_141["text"]="0"
        self.Frame1_161["text"]="0"
        self.Frame1_181["text"]="0"
        self.Frame1_201["text"]="0"
        self.Frame1_221["text"]="0"
        self.Frame2_41["text"]="0"
        self.Frame2_61["text"]="0"
        self.Frame2_81["text"]="0"
        self.Frame2_101["text"]="0"
        self.Frame2_121["text"]="0"
        self.Frame2_141["text"]="0"
        self.Frame2_161["text"]="0"
        self.Frame2_181["text"]="0"
        self.Frame2_201["text"]="0"
        self.Frame2_221["text"]="0"
        self.Frame3_41["text"]="0"
        self.Frame3_61["text"]="0"
        self.Frame3_81["text"]="0"
        self.Frame3_101["text"]="0"
        self.Frame3_121["text"]="0"
        self.Frame3_141["text"]="0"
        self.Frame3_161["text"]="0"
        self.Frame3_181["text"]="0"
        self.Frame3_201["text"]="0"
        self.Frame3_221["text"]="0"

        #On se place dans la situation suivante : le dealer, un autre joueur et nous.
        #Premieres cartes distribuées après avoir misé. On se place dans le cas où l'on est à droite du dealer et le joueur 2 à sa gauche
        dealer=self.dealer=[]
        moi=self.moi=[]
        joueur2=self.joueur2=[]
        x=self.sabot.pop(0)
        joueur2.append(x) #le dealer commence par donner un carte au joueur à sa gauche
        self.modifier_etat_sabot2(x)
        x=self.sabot.pop(0)
        moi.append(x) #le dealer nous distribue ensuite une carte
        self.modifier_etat_sabot2(x)
        x=self.sabot.pop(0)
        dealer.append(x) #le dealer se distribue ensuite une carte
        self.modifier_etat_sabot2(x)
        x=self.sabot.pop(0)
        joueur2.append(x) #le dealer donne une seconde carte au joueur à sa gauche (le joueur 2)
        self.modifier_etat_sabot2(x)
        x=self.sabot.pop(0)
        moi.append(x) #le dealer nous donne une seconde carte
        self.modifier_etat_sabot2(x)
        for i in dealer:
            if i==2 :
                self.Frame1_41["text"]=str(int(self.Frame1_41["text"])+1)
            elif i==3 :
                self.Frame1_61["text"]=str(int(self.Frame1_61["text"])+1)
            elif i==4 :
                self.Frame1_81["text"]=str(int(self.Frame1_81["text"])+1)
            elif i==5 :
                self.Frame1_101["text"]=str(int(self.Frame1_101["text"])+1)
            elif i==6 :
                self.Frame1_121["text"]=str(int(self.Frame1_121["text"])+1)
            elif i==7 :
                self.Frame1_141["text"]=str(int(self.Frame1_141["text"])+1)
            elif i==8 :
                self.Frame1_161["text"]=str(int(self.Frame1_161["text"])+1)
            elif i==9 :
                self.Frame1_181["text"]=str(int(self.Frame1_181["text"])+1)
            elif i=='A' :
                self.Frame1_221["text"]=str(int(self.Frame1_221["text"])+1)
            else :
                self.Frame1_201["text"]=str(int(self.Frame1_201["text"])+1)
        for i in moi:
            if i==2 :
                self.Frame2_41["text"]=str(int(self.Frame2_41["text"])+1)
            elif i==3 :
                self.Frame2_61["text"]=str(int(self.Frame2_61["text"])+1)
            elif i==4 :
                self.Frame2_81["text"]=str(int(self.Frame2_81["text"])+1)
            elif i==5 :
                self.Frame2_101["text"]=str(int(self.Frame2_101["text"])+1)
            elif i==6 :
                self.Frame2_121["text"]=str(int(self.Frame2_121["text"])+1)
            elif i==7 :
                self.Frame2_141["text"]=str(int(self.Frame2_141["text"])+1)
            elif i==8 :
                self.Frame2_161["text"]=str(int(self.Frame2_161["text"])+1)
            elif i==9 :
                self.Frame2_181["text"]=str(int(self.Frame2_181["text"])+1)
            elif i=='A' :
                self.Frame2_221["text"]=str(int(self.Frame2_221["text"])+1)
            else :
                self.Frame2_201["text"]=str(int(self.Frame2_201["text"])+1)
        for i in joueur2:
            if i==2 :
                self.Frame3_41["text"]=str(int(self.Frame3_41["text"])+1)
            elif i==3 :
                self.Frame3_61["text"]=str(int(self.Frame3_61["text"])+1)
            elif i==4 :
                self.Frame3_81["text"]=str(int(self.Frame3_81["text"])+1)
            elif i==5 :
                self.Frame3_101["text"]=str(int(self.Frame3_101["text"])+1)
            elif i==6 :
                self.Frame3_121["text"]=str(int(self.Frame3_121["text"])+1)
            elif i==7 :
                self.Frame3_141["text"]=str(int(self.Frame3_141["text"])+1)
            elif i==8 :
                self.Frame3_161["text"]=str(int(self.Frame3_161["text"])+1)
            elif i==9 :
                self.Frame3_181["text"]=str(int(self.Frame3_181["text"])+1)
            elif i=='A' :
                self.Frame3_221["text"]=str(int(self.Frame3_221["text"])+1)
            else :
                self.Frame3_201["text"]=str(int(self.Frame3_201["text"])+1)
        self.Frame17["text"]="L'autre joueur a joué, c'est à votre tour. De l'aide?"
        
    def cliquer_nouveau_sabot(self):              # Création d'un nouveau sabot
        etat_sabot=self.etat_sabot=[24,24,24,24,24,24,24,24,96,24] #Création d'une liste modélisant l'état du sabot
        sabot=self.sabot=[]
        cartes=[2,3,4,5,6,7,8,9,10,'J','Q','K','A']
        q=0
        while q<24:                                  # Ajout de 6 paquets de cartes au sabot vide (comme dans les casinos français)
            for i in cartes:
                sabot.append(i)
            q+=1
        random.shuffle(sabot)# On mélange le sabot
        self.Frame4_21["text"]=str(etat_sabot)
        self.Frame17["text"]="Cliquez sur Nouvelle Main"
    
    def cliquer_meilleure_strategie(self):
        x=self.meilleure_strategie
        mains=[self.joueur2,self.moi,self.dealer]
        self.vecteurs_initiaux(mains)
        self.Frame5_21["text"]=x[0]
        self.Frame5_31["text"]=x[1]
    
    def proba_tirer(self,k): # probabilité de tirer une carte de valeur k 
        n=len(self.sabot)
        p=(self.etat_sabot[k-2]/n)
        return(p)
        
    def matrice_dealer(self):
        #lignes 0 à 8 (états initiaux sans as)
        D=[[0]*35 for i in range (35)]#On remplit la matrice de 0
        for i in range(9):          # Des états initiaux sans as...
            for j in range (10,23): #...vers hard
                if j-i>9 and j-i<19:
                    D[i][j]=self.proba_tirer(j-i-8)
            for j in range(24,28):   #...vers soft
                if i<4 and (i+ 24)==j:
                    D[i][j]=self.proba_tirer(11)
            for j in range (28,32): #... vers finaux 
                if j-i<25 : 
                    D[i][j]=self.proba_tirer(j-i-13)
        D[8][33]=self.proba_tirer(11)    #... vers blackjack
        #ligne 9 (état initial avec as)
        D[9][23]=self.proba_tirer(11)    #De l'état initial avec as au soft 12
        for j in range(24,32):      #De l'état initial avec as aux états finaux
            D[9][j]=self.proba_tirer(j-22)
        D[9][33]=self.proba_tirer(10)     #De l'état initial avec as au blackjack
        #états hard (sans 16),lignes 9 à 21 
        for i in range (10,22): #états hards...
            for j in range (12,23):#...vers hard
                if j-i>1 and j-i<11:
                    D[i][j]=self.proba_tirer(j-i)
            if i>16 :
                D[i][i+1]=self.proba_tirer(11)
        #...vers soft
        D[10][26]=self.proba_tirer(11)
        D[11][27]=self.proba_tirer(11)
        #...vers finaux 
        for i in range (12,22):
            for j in range (28,33):
                if j-i<17:
                    D[i][j]=self.proba_tirer(j-i-5)
        #...vers bust
        for i in range(18,23):
            for j in range(6,11):
                if (i-6)+j>21:
                    D[i][34]+=self.proba_tirer(j)
        #état initial hard 16 vers états finaux
        D[22][28]=self.proba_tirer(11)
        for j in range(29,33):
            D[22][j]=self.proba_tirer(j-27)
        #états initiaux soft 
        for i in range(23,28): #...vers hard
            for j in range (18,23):
                if j-i<-4 :
                    D[i][j]=self.proba_tirer(j-i+15)
            D[i][i+1]=self.proba_tirer(11) #vers soft +1
            for j in range (25,33): #vers soft et finaux 
                if j-i>1:
                    D[i][j]=self.proba_tirer(j-i)
        #états finaux vers états finaux
        for i in range (28,35):
            D[i][i]=1   
        return(D)
    
    def kron(self,strat1,strat2):
        if strat1==strat2:
            return(1)
        else:
            return(0)
    
    def matrice_joueur(self,strategie):
        J=[[0]*87 for i in range (87)] #On remplit la matrice de 0
        #Des états initiaux hard(sans as valant 11)
        for i in range (0,17):
            #vers états hard avec un as valant 1
            if i>6 and i<16:
                J[i][i+26]=self.kron(strategie,"Tirer")*self.proba_tirer(11)
            #vers états hard sans as
            for j in range (27,42): 
                if j-i>26 and j-i<36:
                    J[i][j]=self.kron(strategie,"Tirer")*self.proba_tirer(j-i-25)
            #vers états hard avec un as valant 11
            if i<6:
                J[i][i+44]=self.kron(strategie,"Tirer")*self.proba_tirer(11)
            #vers états finaux rester
            for j in range(50,67):
                J[i][i+50]=self.kron(strategie,"Rester")
                #vers 21 sans blackjack (colonne 67)
            if i>5 and i<16:
                J[i][67]=self.kron(strategie,"Tirer")*self.proba_tirer(17-i)
            #vers 21 avec un as qui vaut 1
            J[16][67]=self.kron(strategie,"Tirer")*self.proba_tirer(11)
            #vers états finaux en doublant
            for j in range(68,84):
                if j-i>67 and j-i<78:
                    J[i][j]=self.kron(strategie,"Doubler")*self.proba_tirer(j-i-66)
            #vers états finaux en doubalnt avec as valant un
            if i>6 :
                J[i][i+67]=self.kron(strategie,"Doubler")*self.proba_tirer(11)
            #vers busted en tirant et en doublant
            if i>7:
                for j in range(2,11):
                    if j+i+4>21:
                        J[i][84]+=self.kron(strategie,"Tirer")*self.proba_tirer(j)
                        J[i][85]+=self.kron(strategie,"Doubler")*self.proba_tirer(j)
        #Des initiaux soft (avec as valant 11)
        for i in range (17,26):
            #vers hard : c'est à dire que l'as dans la main initiale prend la valeur 11
            for j in range(33,42):
                if j-i<17:
                    J[i][j]=self.kron(strategie,"Tirer")*self.proba_tirer(j-i-6)
            if i<25:
                #vers soft sans tirer un as : c'est à dire que l'as dans la mains initiale reste à valeur 11
                for j in range(43,50):
                    if j-i>25:
                        J[i][j]=self.kron(strategie,"Tirer")*self.proba_tirer(j-i-24)
                    #vers soft avec as
                J[i][i+25]=self.kron(strategie,"Tirer")*self.proba_tirer(11)
                #vers états finaux sans 21
            J[i][i+41]=self.kron(strategie,"Rester")
            #vers états finaux avec 21 mais sans blackjack
            if i<25:
                J[i][67]=self.kron(strategie,"Tirer")*self.proba_tirer(26-i)
            J[25][67]=self.kron(strategie,"Tirer")*self.proba_tirer(11)
            #vers états finaux en doublant 
            for j in range(74,84):
                if j<76:
                    J[i][j]=self.kron(strategie,"Doubler")*self.proba_tirer(j-i-47)
                if j>=76:
                    if j-i<58 :
                        J[i][j]=self.kron(strategie,"Doubler")*self.proba_tirer(j-i-47)
                    elif j-i==58:
                        J[i][i+58]=self.kron(strategie,"Doubler")*self.proba_tirer(11)
                    else:
                        J[i][j]=self.kron(strategie,"Doubler")*self.proba_tirer(j-i-57)
        #Des états hard non initiaux (donc strategie du double impossible ici)
        for i in range(26,42):
            #Vers états hard 
            for j in range (28,42):
                if j-i>1 and j-i<11:
                    J[i][j]=self.kron(strategie,"Tirer")*self.proba_tirer(j-i)
            if i>31 and i<41:
                J[i][i+1]=self.kron(strategie,"Tirer")*self.proba_tirer(11)
            #Vers états soft 
            if i<31:
                J[i][i+19]=self.kron(strategie,"Tirer")*self.proba_tirer(11)
            #Vers états finaux sans doubler
            J[i][i+25]=self.kron(strategie,"Rester")
            #Vers états finaux avec 21 mais sans blackjack
            if i>30 and i<41:
                J[i][67]=self.kron(strategie,"Tirer")*self.proba_tirer(42-i)
            J[41][67]=self.kron(strategie,"Tirer")*self.proba_tirer(11)
            #Vers busted en tirant 
            if i>32:
                for j in range(2,11):
                    if i-21+j>21:
                        J[i][84]+=self.kron(strategie,"Tirer")*self.proba_tirer(j)
            # Des états soft non initiaux (donc strategie du double impossible ici)
        for i in range (42,50):
            #Vers états hard (as se transforme en 1)
            for j in range(33,42):
                if j-i<-7:
                    J[i][j]=self.kron(strategie,"Tirer")*self.proba_tirer(j-i+18)
            #Vers états soft 
            for j in range (44,50):
                if j-i>1:
                    J[i][j]=self.kron(strategie,"Tirer")*self.proba_tirer(j-i)
            if i<49:
                J[i][i+1]=self.kron(strategie,"Tirer")*self.proba_tirer(11)
            #Vers états finaux 
            J[i][i+17]=self.kron(strategie,"Rester")
            #Vers états finaux avec 21 mais sans blackjack
            if i<49:
                J[i][67]=self.kron(strategie,"Tirer")*self.proba_tirer(50-i)
            J[49][67]=self.kron(strategie,"Tirer")*self.proba_tirer(11)
        #Des états finaux aux états finaux
        for i in range(50,87):
            J[i][i]=1
        return(J)
    
    def expo_rapide_mat(self,A,n):
        #La fonction prend en entrée une matrice A et un entier naturel n, et retourne A^n
        X=A
        p=len(A)
        Y=[[0]*p for i in range(p) ] 
        # Construction de la matrice identité
        for i in range (p):
            Y[i][i]=1
        m=n
        while m>0:
            q,r=m//2,m%2 # quotient et reste dans la division euclidienne de m par 2.
            if r==1:
                Y=np.dot(Y,X) # on multiplie y par x, le résultat est affecté à y.
            X=np.dot(X,X) # on met x au carré, le résultat est affecté à x.
            m=q
        return (Y)
     
    def sigma (self,Fjoueur,Fcroupier): 
         #états finaux du joueur indépendant de ceux du croupier
        if Fjoueur==84:
            return(-self.mise)
        elif Fjoueur==85:
            return(-2*self.mise)
        elif Fjoueur==86:
            return(self.mise*1.5)
        #états finaux du joueur qui a doublé
        elif Fjoueur>67:
            if Fcroupier==34:
                return(2*self.mise)
            if Fcroupier==33:
                return(-2*self.mise)
            if Fjoueur-62==Fcroupier-11:
                return(0)
            elif Fjoueur-62>Fcroupier-11:
                return(2*self.mise)
            else :
                return(-2*self.mise)
        #états finaux du joueur qui n'a pas doublé
        elif Fcroupier==34:
            return(self.mise)
        if Fcroupier==33:
            return(-self.mise)
        if Fjoueur-46==Fcroupier-11:
            return(0)
        elif Fjoueur-46>Fcroupier-11:
            return(self.mise)
        else :
            return(-self.mise)
        
    #programmation dynamique, on stocke les matrices du joueur dans une liste 
    # cela évite de les recalculer pour chaque strategie

    def utilisation_matjoueur(self): 
        Jou=self.Jou=[]
        Cro=self.Cro=self.expo_rapide_mat(matrice_dealer(),17) #élévation de la matrice du croupier à la puissance 17
        J=self.matrice_joueur("Tirer")
        Jou.append(J)
        for i in range (20):
            J=np.dot(J,self.matrice_joueur("Tirer"))
            Jou.append(J)
    
    def proba_final(self,Fjoueur,Fcroupier,strategie):
        n=len(strategie)
        #si le joueur dépasse 21 il est inutile de suivre le croupier, le joueur perd sa mise.
        if Fjoueur==85 or Fjoueur==84: 
            if n>1 :
                #les lignes 84 et 85 correspondent aux états BUSTED et 2BUSTED
                J=self.Jou[n-2]
                J=np.dot(J,self.matrice_joueur("Rester"))
                P=np.dot(self.phi_joueur,J) # vecteur initial fois matrice
                return(P[0][Fjoueur])
            else :
                J=self.matrice_joueur(strategie[0])
                P=np.dot(self.phi_joueur,J) # vecteur initial fois matrice
                return(P[0][Fjoueur])
        else:
            if n>1 :
                J=self.Jou[n-2]
                J=np.dot(J,self.matrice_joueur("Rester"))
                Pj=np.dot(self.phi_joueur,J) # vecteur initial fois matrice
                Pj=Pj[0][Fjoueur]
                #proba pour que le joueur soit dans cet état final :
                #proba pour que le dealer soit dans cet état final
                Pc=self.Cro
                Pc=np.dot(self.phi_croupier,Pc)
                Pc=Pc[0][Fcroupier]
                return(Pj*Pc)
            else :
                J=self.matrice_joueur(strategie[0])
                Pj=np.dot(self.phi_joueur,J) # vecteur initial fois matrice
                Pj=Pj[0][Fjoueur]
                Pc=self.Cro
                Pc=np.dot(self.phi_croupier,Pc)
                Pc=Pc[0][Fcroupier]
                return(Pj*Pc)
                
    def esperance(self,strategie):
        esperance=0
        #états finaux correspondant à ceux du joueur
        for i in range (50,87):
            #états finaux correpondant à ceux du dealer
            for j in range(27,35):
                esperance+=self.proba_final(i,j,strategie)*self.sigma(i,j)
        return(esperance)
        
    # On implémente le tri_fusion, tri de complexité optimale pour choisir la meilleur esperance

    def fusion(self,L1,L2,g,m,d): # Listes de couple et on trie par rapport à la seconde valeur du couple pour garder la position des strategies
        i1=g
        i2=m
        for i in range(g,d):
            if i2==d or (i1<m and L1[i1][1]<=L1[i2][1]):
                L2[i]=L1[i1]
                i1+=1
            else:
                L2[i]=L1[i2]
                i2+=1
            
            
    def tri_fusion_couple(self,L):
        Ltmp=[[None,None]]*len(L)
        def tri_fusion_rec(self,g,d):
            if g<d-1:
                m=(g+d)//2
                self.tri_fusion_rec(g,m)
                self.tri_fusion_rec(m,d)
                Ltmp[g:d]=L[g:d]
                self.fusion(Ltmp,L,g,m,d)
        self.tri_fusion_rec(0,len(L))
        
    def vecteurs_initiaux(self,mains):
        vcroupier=self.valeur_main(mains[2])
        vjoueur=self.valeur_main(mains[1])
        phi_croupier=self.phi_croupier=[[0]*35]
        phi_joueur=self.phi_joueur=[[0]*87]
        phi_croupier[0][vcroupier-2]=1
        if vjoueur==21:
            phi_joueur[0][86]=1
        #soft
        elif self.as11==1:
            phi_joueur[0][vjoueur+5]=1
        else:
            phi_joueur[0][vjoueur-4]=1
    
    def valeur_main(self,main):
        as11=self.as11=0
        total=0
        nb_as=0   # nombre d'as à valeur 11 
        n=len(main)
        for i in range (n):
            if main[i]=='J' or main[i]=='Q' or main[i]=='K':
                total+=10
            elif main[i]=='A':
                total+=11 
                nb_as+=1
                as11=1
            else :
                total+=main[i]
        while nb_as>0 and total>21:
            total-=10
            nb_as-=1
        if total>21 :
            return(22)
        return(total)
    
    def meilleur_strategie(self):
        self.utilisation_matjoueur
        # liste de toute les strategies possibles
        liste_strategie=[["Doubler"]] 
        for i in range (4):
            X=(["Tirer"]*i)+["Rester"]
            liste_strategie.append(X)
        n=len(liste_strategie)
        liste_esperance=[None]*n
        for i in range (n):
            x=self.esperance(liste_strategie[i])
            liste_esperance[i]=x
        # la liste à trier est une liste de couple qui à chaque strategie associe son esperance
        liste_a_trier=[]
        for i in range (n):
            x=liste_strategie[i]
            y=liste_esperance[i]
            liste_a_trier.append([x,y])
        self.tri_fusion_couple(liste_a_trier)
        return( "La meilleur stratégie est " + str(liste_a_trier[n-1][0]) , " Et son espérance est " + str(liste_a_trier[n-1][1]))

    
fenetre=Tk()
interface=Interface_Graphique_Blackjack_Advisor(fenetre)
interface.mainloop()




###### ETUDE STATISQUE DES DIFFERENTES STRATEGIES SUR PLUSIEURS PARTIES ######## 


#### STRATEGIE DU DEALER STAT #####

import matplotlib.pyplot as plt

def tirer2(main):
    x=sabot.pop(0)
    modifier_etat_sabot(x)
    main.append(x)
    

def comparaison_mains2(moi,dealer):
    if len(moi)==2 and valeur_main(moi)==21:
        return(1.5)
    elif valeur_main(moi)>21:
        return(-1)
    elif valeur_main(dealer)>21:
        return(1)
    elif valeur_main(moi)==valeur_main(dealer):
        return(0)
    elif valeur_main(moi)>valeur_main(dealer):
        return(1)
    elif valeur_main(moi)<valeur_main(dealer):
        return(-1)

def strategie_dealer2(main):
    while valeur_main(main)<17:
        tirer2(main)

def tour3():
    global mise
    mise=1
    mains=mains_initiales()
    strategie_dealer2(mains[0])
    strategie_dealer2(mains[1])
    strategie_dealer2(mains[2])
    
    
    

def stat_strategie_dealer(n):
    nouveau_sabot()
    X=[1]
    Y=[0]
    solde=0
    for i in range (n):
        if len(sabot)<15:
            nouveau_sabot()
        tour3()
        x=comparaison_mains2(moi,dealer)
        solde+=x
        X.append(i)
        Y.append(solde)
    plt.ylabel("Evolution du solde pour 1$ misé par main")
    plt.xlabel("Nombre de mains")
    plt.title("Si adoption de la stratégie du dealer : ")
    plt.plot(X,Y)
    plt.show()
    
stat_strategie_dealer(10000)

##### NOTRE STRATEGIE AVEC OU SANS COMPTAGE DE CARTES #######
        
def meilleur_strategie2():
    utilisation_matjoueur()
    # liste de toute les strategies possibles
    liste_strategie=[["Doubler"]] 
    for i in range (3):
        X=(["Tirer"]*i)+["Rester"]
        liste_strategie.append(X)
    n=len(liste_strategie)
    liste_esperance=[None]*n
    for i in range (n):
        x=esperance(liste_strategie[i])
        liste_esperance[i]=x
    # la liste à trier est une liste de couple qui à chaque strategie associe son esperance
    liste_a_trier=[]
    for i in range (n):
        x=liste_strategie[i]
        y=liste_esperance[i]
        liste_a_trier.append([x,y])
    tri_fusion_couple(liste_a_trier)
    return(liste_a_trier[n-1][0])
    
def doubler2(main):
    tirer2(main)

def tour4():
    global mise
    mise=1
    mains=mains_initiales()
    strategie_dealer2(mains[0])
    #NOUS JOUONS
    vecteurs_initiaux(mains)
    L=meilleur_strategie2()
    for i in L :
        if i=="Doubler" :
            mise*=2
            doubler2(mains[1])
        if i=="Tirer":
            tirer2(mains[1])
    #AU DEALER DE JOUER
    strategie_dealer2(mains[2])
    
def comparaison_mains3(moi,dealer):
    if len(moi)==2 and valeur_main(moi)==21:
        return(mise*1.5)
    elif valeur_main(moi)>21:
        return(-mise)
    elif valeur_main(dealer)>21:
        return(mise)
    elif valeur_main(moi)==valeur_main(dealer):
        return(0)
    elif valeur_main(moi)>valeur_main(dealer):
        return(mise)
    elif valeur_main(moi)<valeur_main(dealer):
        return(-mise)

def compte():
    c=0
    for i in range(0,5):
        c+=etat_sabot[i]
    for i in range (8,10):
        c-=etat_sabot[i]
    return(c)

def stat_notre_strategie(n):
    nouveau_sabot()
    solde=0
    X=[1]
    Y=[0]
    for i in range(n):
        if len(sabot)<15:
            nouveau_sabot()
        tour4()
        x=comparaison_mains3(moi,dealer)
        solde+=x
        X.append(i)
        Y.append(solde)
    plt.ylabel("Evolution du solde pour 1$ misé par main")
    plt.xlabel("Nombre de mains")
    plt.title("Si adoption de notre stratégie : ")
    plt.plot(X,Y)
    plt.show()
    
stat_notre_strategie(10000)


######################## AVEC COMPTAGE DE CARTES ##########################


def tour5():
    global mise
    mise=1
    mains=mains_initiales()
    strategie_dealer2(mains[0])
    if compte()>18:
        mise*=100
    #NOUS JOUONS
    vecteurs_initiaux(mains)
    L=meilleur_strategie2()
    for i in L :
        if i=="Doubler" :
            mise*=2
            doubler2(mains[1])
        if i=="Tirer":
            tirer2(mains[1])
    #AU DEALER DE JOUER
    strategie_dealer2(mains[2])
    
def stat_notre_strategie_plus_comptage(n):
    nouveau_sabot()
    solde=0
    X=[1]
    Y=[0]
    for i in range(n):
        if len(sabot)<15:
            nouveau_sabot()
        tour5()
        x=comparaison_mains3(moi,dealer)
        solde+=x
        X.append(i)
        Y.append(solde)
    plt.ylabel("Evolution du solde")
    plt.xlabel("Nombre de mains")
    plt.title("Si adoption de notre stratégie : ")
    plt.plot(X,Y)
    plt.show()
