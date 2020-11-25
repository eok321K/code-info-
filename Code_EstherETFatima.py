#Programmes nécessaires à l'interraction avec
##l'utilisateur

#Importation des modules nécessaires
import csv
import pandas as pd
import matplotlib.pyplot as plt
import math
import numpy

#Ouverture du fichier csv
fichierCSV=pd.read_csv("eivp.csv",sep=';')
frame=pd.DataFrame(fichierCSV)
columns=frame.columns #renvoie l'intitulé des colonnes avec : print(columns)

#transformation des colonnes en listes :
temperature=fichierCSV['temp'].to_list()
id=fichierCSV['id'].to_list()
noise=fichierCSV['noise'].to_list()
humidity=fichierCSV['humidity'].to_list()
lum=fichierCSV['lum'].to_list()
co2=fichierCSV['co2'].to_list()
sent=fichierCSV['sent_at'].to_list()

##Valeurs statistiques et indice humidex

#Calcul de l'indice humidex
def humi(temp, hum):
    return temp+5/9*6.112*(10**(7.5*temp/(237.7+temp)))*hum/100

#Création d'une liste comportant les indices humidex de au cours du temps
humidex=[]
n=len(temperature)
for i in range (n):
    humidex+=[humi(temperature[i], humidity[i])]

#Calcul des valeurs statistiques
def min(liste) :
    min = liste[0]
    for elem in liste :
        if elem < min :
            min = elem
    return min

def max(liste) :
    max = liste[0]
    for elem in liste :
        if elem > max :
            max = elem
        return max

def moy_ar(liste)  :
    n = len(liste)
    S = 0
    for elem in liste :
        S += elem
    return S/n

def moy_ge(liste) : #inff
    n = len(liste)
    P = 1
    for elem in liste :
        P = P*elem
    return P**(1/n)

def var(liste)   :  #Calcul de la variance
    moy = moy_ar(liste)
    n = len(liste)
    S = 0
    for elem in liste :
        S += (elem - moy)**2

    return S/n

def eca_ty(liste) : #Calcul d'ecart type
   return var(liste)**(1/2)


#Calcul de la médiane

def mediane(liste):
    liste.sort()
    n=len(liste)
    if n%2==0:
        return (liste[(n)//2]+liste[(n+2)//2])/2
    else:
        return liste[(n-1)//2]

##Interraction avec l'utilisateur
a=input("Que souhaitez-vous faire? (tapez 1, 2 ou 3) \n 1: Afficher la courbe d'un paramètre pour un capteur et calculer les valeurs statistiques \n 2: Comparer les similarités entre 2 capteurs pour un paramètre donné \n 3: Afficher les horaires d'occupation des bureaux\n")
affichage=int(a)
unite=""

if affichage==1:
    nb1=input("Quelle courbe voulez-vous afficher?\n 1: la température\n 2: le bruit \n 3: l humidité \n 4: la luminosité \n 5: le taux de co2\n 6:humidex\n ")
    param=int(nb1)
    parametre=[]
    if param==1:
        parametre=temperature
        unite="degres"
    elif param==2:
        parametre=noise
        unite="decibels"
    elif param==3:
        parametre=humidity
        unite= "rapport d'humidité"
    elif param==4:
        parametre=lum
        unite="lux"
    elif param==5:
        parametre=co2
        unite="ppm"
    elif param==6:
        parametre=humidex
        unite="unité humidex"

    nb2=input("Quel capteur voulez vous afficher?\n 1 :capteur 1 \n 2 :capteur 2 \n 3 :capteur 3\n 4 :capteur 4\n 5 :capteur 5\n 6 :capteur 6\n ")
    capteur=int(nb2)

    n=len(id)
    liste_affichee=[]
    sent_att=[]
    for i in range (n):
        if id[i]==capteur:
            liste_affichee+=[parametre[i]]
            sent_att+=[sent[i]]


#Affichage de la courbe demandee (Ajouter à l'affichage les valeurs statistiques)


    y=liste_affichee
    x=sent_att
    plt.title("Courbe représentant le paramètre demandé \n en fonction du temps pour le capteur demandé")
    plt.xlabel("Date")
    plt.ylabel("unité du paramètre demandé")
    plt.plot(x,y,color='g')

    print(" La moyenne est", moy_ar(liste_affichee),unite,"\n Le maximum est", max(liste_affichee),unite, "\n Le minimum est", min (liste_affichee), unite,"\n La variance est", var(liste_affichee),unite, "\n L'écart type est", eca_ty(liste_affichee),unite,"\n La médiane est",mediane(liste_affichee),unite)

    plt.show()

elif affichage==2:#Montrer la liste de la différence des moyennes
# On propose 2 manières différentes pour comparer les courbes
    possibilite=input("Avec quelle méthode voulez-vous travailler? (taper 1 ou 2)\n 1: Calculer la différence moyenne entre les 2 courbes de deux capteurs différents.\n 2: Calculer le coefficient de corrélation entre les capteurs.\n")
    possible=int(possibilite)
    #Calculer la différences moyenne entre les 2 courbes choisies et afficher ces courbes
    if possible==1:
        data=pd.read_csv("eivp.csv",sep=';', index_col = 'sent_at', parse_dates = True)

        p1=input("Quel est le paramètre à traiter\n 1: la température\n 2: le bruit \n 3: l humidité \n 4: la luminosité \n 5: le taux de co2\n 6:humidex\n ") #Entrer le 1er Paramètre
        param1=int(p1)
        parametre=[]
        unite2=""

        if param1==1:
            x = 'temp'
            unite2="degrés"
        elif param1==2:
            x = 'noise'
            unite2="decibels"
        elif param1==3:
            x = 'humidity'
            unite2="rapport humidité"
        elif param1==4:
            x = 'lum'
            unite2="lux"
        elif param1==5:
            x = 'co2'
            unite2="ppm"
        elif param1==6:
            x = 'humidex'
            unite2="unité humidex"

        nb1=input("Quels capteurs voulez vous utiliser pour le test de similarité?\n 1 :capteur 1 \n 2 :capteur 2 \n 3 :capteur 3\n 4 :capteur 4\n 5 :capteur 5\n 6 :capteur 6\n ")
        nb2=input("et le deuxième?\n")

        capt1=int(nb1)
        capt2=int(nb2)

        id1 = data[data['id'] == capt1 ]
        id2 = data[data['id'] == capt2 ]
        id1_parm= id1[x]
        id2_parm= id2[x]


#colonnes des moyennes par heure pour les deux capteurs
        moyID1 = id1_parm.resample('H').mean()
        moyID2 = id2_parm.resample('H').mean()

#Code pour corriger les erreures "nan"
        moyID11=pd.to_numeric(moyID1, errors='coerce').fillna(0, downcast='infer')
        moyID22=pd.to_numeric(moyID2, errors='coerce').fillna(0, downcast='infer')

        L1=moyID11.to_list() #transformation en liste
        L2=moyID22.to_list()

        S = []
        for i in range(len(L1)) :
            S+=[abs(L1[i]-L2[i])]
        #print(S)   #liste contenant la différence des listes moyennes
        h=moy_ar(S) #moyenne de la liste S
        print("la moyenne des différences entre les 2 courbes est de", h,unite2)
        moyID1.plot()  #Afficher les courbes des moyennes du param des deux capteurs pour freq=UNE HEURE
        moyID2.plot()
        plt.show()

    elif possible==2:#On calcule le coefficient de corrélation entre les capteurs (à compléter)

        data=pd.read_csv("eivp.csv",sep=';', index_col = 'sent_at', parse_dates = True)

        p1=input("Quel est le paramètre à traiter\n 1: la température\n 2: le bruit \n 3: l humidité \n 4: la luminosité \n 5: le taux de co2\n 6:humidex\n ") #Entrer le 1er Paramètre
        param1=int(p1)
        parametre=[]

        if param1==1:
            x = 'temp'
        elif param1==2:
            x = 'noise'
        elif param1==3:
            x = 'hum'
        elif param1==4:
            x = 'lum'
        elif param1==5:
            x = 'co2'
        elif param1==6:
            x = 'humidex'

        id1 =data[data['id'] == 1 ]
        id2 =data[data['id'] == 2 ]
        id3 =data[data['id'] == 3 ]
        id4 =data[data['id'] == 4 ]
        id5 =data[data['id'] == 5 ]
        id6 =data[data['id'] == 6 ]

        id1_parm= id1[x]
        id2_parm= id2[x]
        id3_parm= id3[x]
        id4_parm= id4[x]
        id5_parm= id5[x]
        id6_parm= id6[x]


        paramID1 = id1_parm.resample('H').mean()  #colonnes des moyennes par heure pour les deux
        paramID2 = (id2_parm.resample('H').mean()).tolist()
        paramID3 = (id3_parm.resample('H').mean()).tolist()
        paramID4 = (id4_parm.resample('H').mean()).tolist()
        paramID5 = (id5_parm.resample('H').mean()).tolist()
        paramID6 = (id6_parm.resample('H').mean()).tolist()

    #print(type(paramID2))

        Data = pd.DataFrame({"Id1": paramID1, "Id2": paramID2, "Id3": paramID3, "Id4": paramID4, "Id5": paramID5, "Id6": paramID6})
        corr=Data.corr()
        print(corr) #la matrice de corrélation
        capteurs = ["Id1","Id2","Id3","Id4","Id5","Id6"]
#Tracé d'un diagramme de corrélation entre les capteurs
        fig = plt.figure()
        ax  = fig.add_subplot(111)
        cax=ax.matshow(corr , vmin = -1 , vmax = 1)
        fig.colorbar(cax)
        ticks = numpy.arange(0,6,1)
        ax.set_xticks(ticks)
        ax.set_yticks(ticks)
        ax.set_xticklabels(capteurs)
        ax.set_yticklabels(capteurs)
    plt.show()


elif affichage==3:
    nb3=input("Avec quel capteur voulez-vous travailler?\n 1 :capteur 1 \n 2 :capteur 2 \n 3 :capteur 3\n 4 :capteur 4\n 5 :capteur 5\n 6 :capteur 6\n ")
    capteur=int(nb3)
    liste_capteur=[]
    i=0
#On sélectionne les valeurs de la liste noise correspondant au capteur demandé
    for elem in id:
        if elem==capteur:
            liste_capteur+=[noise[i]]
            i+=1
    min_noise=min(noise)
    n=len(liste_capteur)
    temps_occupation=[]
    bar=[]
#Si le bruit dans la salle est supérieur à la valeur minimum, alors la salle est occupée
    for i in range(n):
        temps_occupation+=[sent[i]]
        if liste_capteur[i]>min_noise:
            bar+=[1]
        else:
            bar+=[0]
    fig, ax=plt.subplots()
    labels=temps_occupation
    occup=bar
    ax.bar(labels, bar, width=0.25,label='occupation')
    ax.set_title("horaires d'occupation des bureaux")
    ax.set_ylabel('0 si pas occupé, 1 si occupé')
    ax.set_xlabel('date')
    ax.legend()
    plt.show()