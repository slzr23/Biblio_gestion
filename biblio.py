from sqlite3 import *
from datetime import *
from time import *
from PIL import *
import PIL.Image
import isbnlib
from isbnlib.registry import bibformatters

connexion = connect('bibliotheque.db')
today = date.today()
td = timedelta(30)
print("Date: "+ str(today))
curseur = connexion.cursor()
curseur.execute("select * from adherent")

def verif_date():
    requete = "DELETE FROM retard WHERE identifiant_retard!=0"
    b=curseur.execute(requete)
    requete1="SELECT n_emprunt,identifiant_livre,identifiant_adherent,dateretour FROM emprunt WHERE dateretour < DATE()"
    a = curseur.execute(requete1)
    retard = a.fetchall()
    print(len(retard))
    for i in range(len(retard)):
        requete2 ="INSERT INTO retard(n_emprunt,identifiant_livre,identifiant_adherent,dateretour) VALUES("+ str(retard[i][0]) +","+str(retard[i][1])+","+str(retard[i][2])+","+str('"')+str(retard[i][3])+str('"')+")"
        print(requete2)
        curseur.execute(requete2)
        connexion.commit()


def table_livre():
    requete="CREATE TABLE if not exists livre(isbn varchar(10) primary key not null,titre varchar(255) not null,auteur varchar(40) not null,editeur varchar(40) not nulL,unique(isbn))"
    resultat = curseur.execute(requete)


def table_adherent():
    requete="CREATE TABLE if not exists adherent (identifiant integer primary key autoincrement,nomAdherent varchar(255),prenomAdherent varchar(255),adresse varchar(255),telephone varchar(10),unique(identifiant),unique(nomAdherent,prenomAdherent))"
    resultat = curseur.execute(requete)


def table_emprunt():
    requete="CREATE TABLE if not exists emprunt(isbn varchar (10),identifiant	INTEGER,dateemprunt date,dateretour date,FOREIGN KEY(identifiant) REFERENCES adherent(identifiant),PRIMARY KEY(isbn,identifiant),FOREIGN KEY(isbn) REFERENCES livre(isbn),unique(isbn,identifiant))"
    resultat = curseur.execute(requete)


def ajouter_adherent(): #OK
    nom_adherant = str('"')+adherent_nom.get()+str('"')
    prenom_adherant = str('"')+adherent_prenom.get()+str('"')
    adresse = str('"')+adherent_adresse.get()+str('"')
    num_adherant = str('"')+adherent_tel.get()+str('"')

    requete ="INSERT INTO adherent(nomAdherent,prenomAdherent,adresse,telephone) VALUES ("+nom_adherant+","+prenom_adherant+","+adresse+","+num_adherant+")"
    print(requete)
    curseur.execute(requete)
    mess_ajout()
    connexion.commit()


def liste_adherent():#OK
    requete="SELECT * FROM adherent"
    curseur.execute(requete)
    ans = curseur.fetchall()
    return ans

def charge_livre(): #OK
    SERVICE = "openl"
    isbn = str(entree_isbn.get())
    book=isbnlib.meta(isbn)
    auteur = str(book.get('Authors'))[2:-2]
    titre = str(book.get('Title'))
    editeur = str(book.get('Publisher'))
    annee = str(book.get('Year'))
    global info
    info = [isbn,auteur,titre,editeur, annee]

    #tableau d'info
    tableau = Treeview(window_principale, columns=('ISBN', 'titre', 'auteur','année','éditeur'))
    tableau.heading('ISBN', text='ISBN du livre')
    tableau.heading('titre', text='Titre du livre')
    tableau.heading('auteur', text='Auteur du livre')
    tableau.heading('éditeur', text='Editeur du livre')
    tableau.heading('année', text='Année de parution')
    tableau['show'] = 'headings' # sans ceci, il y avait une colonne vide à gauche qui a pour rôle d'afficher le paramètre "text" qui peut être spécifié lors du insert
    tableau.grid(row = 3, column=0)
    print(info)
    if len(info):
        for i in range(len(info)):
            tableau.insert('', 'end', iid=info[0], values=(info[0], info[2], info[1], info[4], info[3]))

def charge_livre_suprr(): #OK
    SERVICE = "openl"
    id_suppr_livre = str(id_suppr.get())
    requete = "SELECT isbn FROM livre WHERE identifiant_livre="+id_suppr_livre
    isbn_suppr = curseur.execute(requete)
    isbn_livre = curseur.fetchall()
    print(isbn_livre)
    isbn_suppr_livre = isbn_livre[0][0]
    print(isbn_suppr_livre)
    connexion.commit()
    book=isbnlib.meta(isbn_suppr_livre)
    auteur = str(book.get('Authors'))[2:-2]
    titre = str(book.get('Title'))
    editeur = str(book.get('Publisher'))
    annee = str(book.get('Year'))
    global info
    info = [isbn_suppr_livre,auteur,titre,editeur, annee]

    #tableau d'info
    tableau = Treeview(window_principale, columns=('ISBN', 'titre', 'auteur','année','éditeur'))
    tableau.heading('ISBN', text='ISBN du livre')
    tableau.heading('titre', text='Titre du livre')
    tableau.heading('auteur', text='Auteur du livre')
    tableau.heading('éditeur', text='Editeur du livre')
    tableau.heading('année', text='Année de parution')
    tableau['show'] = 'headings' # sans ceci, il y avait une colonne vide à gauche qui a pour rôle d'afficher le paramètre "text" qui peut être spécifié lors du insert
    tableau.grid(row = 3, column=0)
    print(info)
    if len(info):
        for i in range(len(info)):
            tableau.insert('', 'end', iid=info[0], values=(info[0], info[2], info[1], info[4], info[3]))

def ajouter_livre(): #OK
    requete="INSERT INTO livre(isbn,titre,auteur,editeur) VALUES("+str('"')+info[0]+str('"')+","+str('"')+info[2]+str('"')+","+str('"')+info[1]+str('"')+","+str('"')+info[3]+str('"')+")"
    print(requete)
    curseur.execute(requete)
    connexion.commit()
    mess_ajout()

def charge_adherent_suprr(): #OK
    id_suppr_adherent = str(id_suppr.get())
    requete = "SELECT * FROM adherent WHERE identifiant_adherent="+id_suppr_adherent
    adh_suppr = curseur.execute(requete)
    adherent_suppr = curseur.fetchall()
    print(adherent_suppr)
    connexion.commit()
    id_adh = str(adherent_suppr[0][0])
    nom = str(adherent_suppr[0][1])
    prenom = str(adherent_suppr[0][2])
    adresse = str(adherent_suppr[0][3])
    tel = str(adherent_suppr[0][4])
    print(tel)
    global info
    info = [id_adh,nom,prenom,adresse,tel]

    #tableau d'info
    tableau = Treeview(window_principale, columns=('Identifiant adhérent', 'Nom', 'Prénom','Adresse','N° de téléphone'))
    tableau.heading('Identifiant adhérent', text='Identifiant adhérent')
    tableau.heading('Nom', text='Nom')
    tableau.heading('Prénom', text='Prénom')
    tableau.heading('Adresse', text='Adresse')
    tableau.heading('N° de téléphone', text='N° de téléphone')
    tableau['show'] = 'headings' # sans ceci, il y avait une colonne vide à gauche qui a pour rôle d'afficher le paramètre "text" qui peut être spécifié lors du insert
    tableau.grid(row = 3, column=0)
    print(info)
    if len(info):
        for i in range(len(info)):
            tableau.insert('', 'end', iid=info[0], values=(info[0], info[1], info[2], info[3], info[4]))

def ajouter_emprunt():
    identifiant_adherent=str('"')+str(identifiant_adherant.get())+str('"')
    identifiant_livre=str('"')+str(identif_livre.get())+str('"')
    date_emprunt=str('"')+str(today)+str('"')
    date_de_retour=str('"')+str(today+td)+str('"')
    requete2 = "SELECT titre FROM livre WHERE identifiant_livre="+identifiant_livre
    requete_titre_execute = curseur.execute(requete2)
    titre_livre = '"'+str(requete_titre_execute.fetchone()[0])+'"'

    requete="INSERT INTO emprunt(dateemprunt,dateretour,identifiant_adherent, identifiant_livre,titre_livre) VALUES("+date_emprunt+","+date_de_retour+","+identifiant_livre+","+identifiant_adherent+","+titre_livre+")"
    curseur.execute(requete)
    mess_ajout()

def charge_emprunt_suprr(): #OK
    id_suppr_emprunt = str(id_suppr.get())
    requete = "SELECT * FROM emprunt WHERE n_emprunt="+id_suppr_emprunt
    empr_suppr = curseur.execute(requete)
    emprunt_suppr = curseur.fetchall()
    print(emprunt_suppr)
    connexion.commit()
    n_empr = str(emprunt_suppr[0][0])
    date_e = str(emprunt_suppr[0][1])
    date_r = str(emprunt_suppr[0][2])
    id_livre = str(emprunt_suppr[0][3])
    id_adh = str(emprunt_suppr[0][4])
    titre = str(emprunt_suppr[0][5])
    global info
    info = [n_empr,date_e,date_r,id_livre,id_adh,titre]

    #tableau d'info
    tableau = Treeview(window_principale, columns=("N° d'emprunt", "Date de l'enprunt", "Date de retour prévue","Identifiant du livre emprunté","Identifiant de l'adhérent qui emprunte","Titre du livre emprunté"))
    tableau.heading("N° d'emprunt", text="N° d'emprunt")
    tableau.heading("Date de l'enprunt", text="Date de l'enprunt")
    tableau.heading("Date de retour prévue", text="Date de retour prévue")
    tableau.heading("Identifiant du livre emprunté", text="Identifiant du livre emprunté")
    tableau.heading("Identifiant de l'adhérent qui emprunte", text="Identifiant de l'adhérent qui emprunte")
    tableau.heading("Titre du livre emprunté", text="Titre du livre emprunté")
    tableau['show'] = 'headings' # sans ceci, il y avait une colonne vide à gauche qui a pour rôle d'afficher le paramètre "text" qui peut être spécifié lors du insert
    tableau.grid(row = 3, column=0)
    print(info)
    if len(info):
        for i in range(len(info)):
            tableau.insert('', 'end', iid=info[0], values=(info[0], info[1], info[2], info[3], info[4],info[5]))

def supprimer_adherent(): #OK
    identifiant=str(id_suppr.get())
    requete="delete from adherent where identifiant_adherent =:identifiant"
    curseur.execute(requete,{"identifiant":identifiant})
    mess_suppr()


def supprimer_livre():  #OK
    identifiant_livre=str(id_suppr.get())
    requete="delete from livre where identifiant_livre =:identifiant_livre"
    curseur.execute(requete,{"identifiant_livre":identifiant_livre})
    connexion.commit()
    mess_suppr()


def supprimer_emprunt(): #OK
    n_emprunt=str(id_suppr.get())
    requete="delete from emprunt where n_emprunt =:n_emprunt"
    curseur.execute(requete,{"n_emprunt":n_emprunt})
    connexion.commit()
    mess_suppr()

def supprimer_retard(): #OK
    identifiant_retard=input("identifiant du retard ?")
    requete="delete from retard where identifiant_retard =:identifiant_retard"
    curseur.execute(requete,{"identifiant_retard":identifiant_retard})


def liste_emprunt(): #OK
    requete="SELECT * FROM emprunt"
    curseur.execute(requete)
    ans = curseur.fetchall()
    return ans


def liste_livre(): #OK
    requete="SELECT * FROM livre"
    curseur.execute(requete)
    ans = curseur.fetchall()
    return ans


def liste_retard(): #OK
    requete="SELECT * FROM retard"
    curseur.execute(requete)
    ans = curseur.fetchall()
    return ans


def rechercher_adherent(nom):
    curseur.execute("select identifiant from adherent where nomadherent=:nom", {"nom": nom})
    a=curseur.fetchone()
    return a[0]


######################TKINTER: MENU PRINCIPAL###########################

from tkinter import *
from tkinter.ttk import *

def mess_ajout(duration=2000): #fonction d'affichage du message "Message copié avec succès !" lors de la copie, "duration" est le temps d'affichage du message "Message copié avec succès !" Une fois ce temps écoulé, le message (Label) sera détruit avec ".destroy"
    label_ajout = Label(window_principale, text="Ajout de l'élément réalisé avec succès !", font=("Verdana", 10))
    label_ajout.grid(row=30, column=0)
    label_ajout.after(duration, label_ajout.destroy)

def mess_suppr(duration=2000): #fonction d'affichage du message "Message copié avec succès !" lors de la copie, "duration" est le temps d'affichage du message "Message copié avec succès !" Une fois ce temps écoulé, le message (Label) sera détruit avec ".destroy"
    label_suppr = Label(window_principale, text="Suppression de l'élément réalisée avec succès !", font=("Verdana", 10))
    label_suppr.grid(row=30, column=0)
    label_suppr.after(duration, label_suppr.destroy)


def menu():
    for c in window_principale.winfo_children():
        c.destroy()
    # Ajout de widgets à la fenêtre
    Label1= Label(window_principale, text="Gestion d'une bibliothèque", font=('Verdana', 15))
    Label1.grid(row=1, column=0, columnspan=5)

    #LIVRE
    img1=PhotoImage(file = r"livre.png") #IMAGE
    ico1=img1.subsample(6,6)
    button1=Button(image=ico1, command=afficher_livres)
    button1.grid(row=2,column=0)
    livre=Label(window_principale, text="Livres", font=('Verdana', 10))
    livre.grid(row=3, column=0)

    #ADHERENT
    img2=PhotoImage(file = r"adherent.png") #IMAGE
    ico2=img2.subsample(3,3)
    button2=Button(image=ico2, command=afficher_adherents)
    button2.grid(row=2,column=1)
    livre=Label(window_principale, text="Adhérents", font=('Verdana', 10))
    livre.grid(row=3, column=1)

    #EMPRUNT
    img3=PhotoImage(file = r"emprunt.png") #IMAGE
    ico3=img3.subsample(3,3)
    button3=Button(image=ico3, command=menu_er)
    button3.grid(row=2,column=2)
    livre=Label(window_principale, text="Emprunts & Retards", font=('Verdana', 10))
    livre.grid(row=3, column=2)

    #EXIT
    img4=PhotoImage(file = r"quitter.png") #IMAGE
    ico4=img4.subsample(3,3)
    button4=Button(image=ico4, command=window_principale.destroy)
    button4.grid(row=2,column=3)
    livre=Label(window_principale, text="Quitter", font=('Verdana', 10))
    livre.grid(row=3, column=3)

    # Ajout de la date
    Label1= Label(window_principale, text="Date du jour:"+str(today), font=('Verdana', 10))
    Label1.grid(row=1, column=3,columnspan=5)

    window_principale.mainloop()

###########################################OPTION 1: LIVRE#######################################
from isbnlib import *
import urllib.request
from PIL import ImageTk, Image

def ajoute_livres():
    for c in window_principale.winfo_children():
        c.destroy()
    isbn_label = Label(window_principale, text="ISBN du livre", font=('Verdana', 10))
    isbn_label.grid(row=1, column = 0)
    global entree_isbn
    entree_isbn = Entry(window_principale, font=("Verdana", 10))
    entree_isbn.grid(row=1, column=1)


    #chargement des infos du livre
    charg=Button(text = "Charger le livre", command=charge_livre)
    charg.grid(row=2,column=1)

    #bouton d'ajout du livre à la base
    button2=Button(text = 'ajouter le livre à la bibliothèque', command=ajouter_livre)
    button2.grid(row=10,column=1)

    #BOUTON RETOUR
    button_retour=Button(text='Retour au menu de gestion des livres', command=afficher_livres)
    button_retour.grid(row=1000,column=1)

def suppr_livres():
    for c in window_principale.winfo_children():
        c.destroy()

    id_label = Label(window_principale, text="Identifiant du livre", font=('Verdana', 10))
    id_label.grid(row=1, column = 0)
    global id_suppr
    id_suppr = Entry(window_principale, font=("Verdana", 10))
    id_suppr.grid(row=1, column=1)
    button_retour=Button(text='Supprimer le livre', command=supprimer_livre)
    button_retour.grid(row=1002,column=1)

    #chargement des infos du livre
    charg=Button(text = "Charger le livre", command=charge_livre_suprr)
    charg.grid(row=2,column=1)

    #BOUTON RETOUR
    button_retour=Button(text='Retour au menu de gestion des livres', command=afficher_livres)
    button_retour.grid(row=1003,column=1)


def afficher_livres():
    #SUPPRESION DU CONTENU PRECEDENT
    for c in window_principale.winfo_children():
        c.destroy()
    Label1= Label(window_principale, text="Gestion des livres", font=('Verdana', 15))
    Label1.grid(row=1, column=0)

    #LIVRES AFFICHAGE
    Label1= Label(window_principale, text='liste des livres', font=('Verdana', 10)) #titre
    Label1.grid(row=2, column=0)

    #1 - Creation du tableau
    tableau = Treeview(window_principale, columns=('identifiant_livre', 'titre', 'isbn','auteur','éditeur'))
    tableau.heading('identifiant_livre', text='Identifiant du livre')
    tableau.heading('titre', text='Titre du livre')
    tableau.heading('isbn', text='ISBN du livre')
    tableau.heading('auteur', text='Auteur du livre')
    tableau.heading('éditeur', text='Editeur du livre')
    tableau['show'] = 'headings' # sans ceci, il y avait une colonne vide à gauche qui a pour rôle d'afficher le paramètre "text" qui peut être spécifié lors du insert
    tableau.grid(row = 3, column=0)

    #2 - Remplissage du tableau
    resultat= liste_livre()
    if len(resultat):
            for enreg in resultat:
                # chaque ligne n'a pas de parent, est ajoutée à la fin de la liste, utilise le champ id comme identifiant et on fournit les valeurs pour chacune des colonnes du tableau
                tableau.insert('', 'end', iid=enreg[0], values=(enreg[0], enreg[1], enreg[2], enreg[3], enreg[4]))
    else:
        rien = Label(text = "Il n'y a aucun livre enregistré.")
        tableau.pack_forget()
        rien.grid(row=3, column = 0)

    #3 - BOUTON AJOUT LIVRE
    button5=Button(text = "Ajouter un livre", command=ajoute_livres)
    button5.grid(row=2,column=2)

    #4 - BOUTON SUPPR LIVRE
    button5=Button(text = "Supprimer un livre", command=suppr_livres)
    button5.grid(row=3,column=2)

    #BOUTON RETOUR
    button_retour=Button(text='Retour au menu principal', command=menu)
    button_retour.grid(row=1000,column=0)

########################################OPTION 2: ADHERENT#######################################

def ajoute_adherent():
    for c in window_principale.winfo_children():
        c.destroy()

    Nom= Label(window_principale, text="Nom de l'adhérent", font=('Verdana',10))
    Nom.grid(row=1, column=0)
    global adherent_nom
    adherent_nom = Entry(window_principale, font=("Verdana", 10))
    adherent_nom.grid(row=1, column=1)

    Prenom= Label(window_principale, text="Prénom de l'adhérent", font=('Verdana',10))
    Prenom.grid(row=2, column=0)
    global adherent_prenom
    adherent_prenom = Entry(window_principale, font=("Verdana", 10))
    adherent_prenom.grid(row=2, column=1)

    Tel= Label(window_principale, text="N° de téléphone de l'adhérent", font=('Verdana',10))
    Tel.grid(row=3, column=0)
    global adherent_tel
    adherent_tel = Entry(window_principale, font=("Verdana", 10))
    adherent_tel.grid(row=3, column=1)

    adresse= Label(window_principale, text="Adresse de l'adhérent", font=('Verdana',10))
    adresse.grid(row=4, column=0)
    global adherent_adresse
    adherent_adresse = Entry(window_principale, font=("Verdana", 10))
    adherent_adresse.grid(row=4, column=1)

    #bouton d'ajout de l'adhérent à la base
    button2=Button(text="Ajouter le nouvel adhérent", command=ajouter_adherent)
    button2.grid(row=10,column=0)

    #BOUTON RETOUR
    button_retour=Button(text='Retour au menu de gestion des adhérents', command=afficher_adherents)
    button_retour.grid(row=1000,column=0)

def suppr_adherent():
    for c in window_principale.winfo_children():
        c.destroy()

    id_label = Label(window_principale, text="Identifiant de l'adhérent", font=('Verdana', 10))
    id_label.grid(row=1, column = 0)
    global id_suppr
    id_suppr = Entry(window_principale, font=("Verdana", 10))
    id_suppr.grid(row=1, column=1)
    button_retour=Button(text="Supprimer l'adhérent ", command=supprimer_adherent)
    button_retour.grid(row=1002,column=1)

    #chargement des infos du livre
    charg=Button(text = "Charger l'adhérent", command=charge_adherent_suprr)
    charg.grid(row=2,column=1)

    #BOUTON RETOUR
    button_retour=Button(text='Retour au menu de gestion des adhérents', command=afficher_adherents)
    button_retour.grid(row=1003,column=1)

def afficher_adherents():
    #SUPPRESION DU CONTENU PRECEDENT
    for c in window_principale.winfo_children():
        c.destroy()
    Label1= Label(window_principale, text="Gestion des adherents", font=('Verdana', 15))
    Label1.grid(row=1, column=0)

    #LIVRES AFFICHAGE
    Label1= Label(window_principale, text='liste des adherents', font=('Verdana', 10)) #titre
    Label1.grid(row=2, column=0)

    #1 - Creation du tableau
    tableau = Treeview(window_principale, columns=('identifiant_adherent', 'nomAdherent', 'prenomAdherent','adresse','telephone'))
    tableau.heading('identifiant_adherent', text="Identifiant de l'adhérent")
    tableau.heading('nomAdherent', text='Nom')
    tableau.heading('prenomAdherent', text='Prénom')
    tableau.heading('adresse', text='Adresse')
    tableau.heading('telephone', text='N° de téléphone')
    tableau['show'] = 'headings' # sans ceci, il y avait une colonne vide à gauche qui a pour rôle d'afficher le paramètre "text" qui peut être spécifié lors du insert
    tableau.grid(row = 3, column=0)

    #2 - Remplissage du tableau
    resultat= liste_adherent()
    if len(resultat):
        for enreg in resultat:
            # chaque ligne n'a pas de parent, est ajoutée à la fin de la liste, utilise le champ id comme identifiant et on fournit les valeurs pour chacune des colonnes du tableau
            tableau.insert('', 'end', iid=enreg[0], values=(enreg[0], enreg[1], enreg[2], enreg[3], enreg[4]))
    else:
        rien = Label(text = "Il n'y a aucun adhérent pour le moment.")
        tableau.pack_forget()
        rien.grid(row=3, column = 0)

    #3 - BOUTON AJOUT ADHERENT
    button5=Button(text = "Ajouter un adhérent", command=ajoute_adherent)
    button5.grid(row=2,column=2)

    #4 - BOUTON SUPPR ADHERENT
    button5=Button(text = "Supprimer un adhérent", command=suppr_adherent)
    button5.grid(row=3,column=2)


    #BOUTON RETOUR
    button_retour=Button(text='Retour au menu principal', command=menu)
    button_retour.grid(row=1000,column=0)

################################OPTION 3: EMPRUNTS & RETARD ####################################

def menu_er():
    for c in window_principale.winfo_children():
        c.destroy()
    # Ajout de widgets à la fenêtre
    Label1= Label(window_principale, text="Gestion des emprunts & retards", font=('Verdana', 15))
    Label1.grid(row=1, column=0)

    #EMPRUNT
    button_emprunt=Button(text='Emprunts', command=afficher_emprunts)
    button_emprunt.grid(row=2,column=2)

    #RETARD
    button_retard=Button(text='Retards', command=afficher_retards)
    button_retard.grid(row=2,column=3)

    #BOUTON RETOUR
    button_retour=Button(text='Retour au menu principal', command=menu)
    button_retour.grid(row=1000,column=0)

def ajoute_emprunt():
    for c in window_principale.winfo_children():
        c.destroy()

    id_livre= Label(window_principale, text="Identifiant du livre emprunté", font=('Verdana',10))
    id_livre.grid(row=1, column=0)
    global identif_livre
    identif_livre = Entry(window_principale, font=("Verdana", 10))
    identif_livre.grid(row=1, column=1)

    id_adherant= Label(window_principale, text="Identifiant de l'adhérent qui emprunte", font=('Verdana',10))
    id_adherant.grid(row=2, column=0)
    global identifiant_adherant
    identifiant_adherant = Entry(window_principale, font=("Verdana", 10))
    identifiant_adherant.grid(row=2, column=1)

    #date emprunt
    empr = Label(window_principale, text="Date de l'emprunt ", font=('Verdana',10))
    empr.grid(row=3, column=0)

    empr_date = Label(window_principale, text=str(today), font=('Verdana',10))
    empr_date.grid(row=3, column=1)

    #date retour
    ret = Label(window_principale, text="Date de retour prévue ", font=('Verdana',10))
    ret.grid(row=4, column=0)

    ret_date = Label(window_principale, text=str(today+td), font=('Verdana',10))
    ret_date.grid(row=4, column=1)

    #bouton d'ajout de l'emprunt à la base
    button2=Button(text="Ajouter l'emprunt", command=ajouter_emprunt)
    button2.grid(row=10,column=0)

    #BOUTON RETOUR
    button_retour=Button(text='Retour au menu de gestion des emprunts', command=afficher_emprunts)
    button_retour.grid(row=1000,column=0)

def suppr_emprunt():
    for c in window_principale.winfo_children():
        c.destroy()

    id_label = Label(window_principale, text="Identifiant d'emprunt", font=('Verdana', 10))
    id_label.grid(row=1, column = 0)
    global id_suppr
    id_suppr = Entry(window_principale, font=("Verdana", 10))
    id_suppr.grid(row=1, column=1)
    button_retour=Button(text="Supprimer l'emprunt", command=supprimer_emprunt)
    button_retour.grid(row=1002,column=1)

    #chargement des infos de l'emprunt
    charg=Button(text = "Charger l'emprunt à supprimer", command=charge_emprunt_suprr)
    charg.grid(row=2,column=1)

    #BOUTON RETOUR
    button_retour=Button(text='Retour au menu de gestion des adhérents', command=afficher_emprunts)
    button_retour.grid(row=1003,column=1)


def afficher_emprunts():
    #SUPPRESION DU CONTENU PRECEDENT
    for c in window_principale.winfo_children():
        c.destroy()
    Label1= Label(window_principale, text="Gestion des emprunts & retards", font=('Verdana', 15))
    Label1.grid(row=1, column=0)

    #LIVRES AFFICHAGE
    Label1= Label(window_principale, text='liste des emprunts', font=('Verdana', 10)) #titre
    Label1.grid(row=2, column=0)

    #1 - Creation du tableau emprunt
    tableau = Treeview(window_principale, columns=('n_emprunt', 'dateemprunt', 'dateretour','identifiant_livre','identifiant_adherent','titre_livre'))
    tableau.heading('n_emprunt', text="N° d'emprunt")
    tableau.heading('dateemprunt', text="Date de l'emprunt")
    tableau.heading('dateretour', text="Date de retour prévue")
    tableau.heading('identifiant_livre', text="Identifiant du livre")
    tableau.heading('identifiant_adherent', text="Identifiant de l'adhérent")
    tableau.heading('titre_livre', text="Titre du livre")
    tableau['show'] = 'headings' # sans ceci, il y avait une colonne vide à gauche qui a pour rôle d'afficher le paramètre "text" qui peut être spécifié lors du insert
    tableau.grid(row = 3, column=0)

    #2 - Remplissage du tableau
    resultat= liste_emprunt()
    if len(resultat):
        for enreg in resultat:
            # chaque ligne n'a pas de parent, est ajoutée à la fin de la liste, utilise le champ id comme identifiant et on fournit les valeurs pour chacune des colonnes du tableau
            tableau.insert('', 'end', iid=enreg[0], values=(enreg[0], enreg[1], enreg[2], enreg[3], enreg[4],enreg[5]))
    else:
        rien = Label(text = "Il n'y a aucun emprunt effectué.")
        tableau.pack_forget()
        rien.grid(row=3, column = 0)

    #3 - BOUTON AJOUT EMPRUNT
    button5=Button(text = "Ajouter un emprunt", command=ajoute_emprunt)
    button5.grid(row=2,column=2)

    #4 - BOUTON SUPPR ADHERENT
    button5=Button(text = "Supprimer un adhérent", command=suppr_emprunt)
    button5.grid(row=3,column=2)



    #BOUTON RETOUR
    button_retour=Button(text='Retour', command=menu_er)
    button_retour.grid(row=1000,column=0)

def afficher_retards():
    #SUPPRESION DU CONTENU PRECEDENT
    for c in window_principale.winfo_children():
        c.destroy()
    Label1= Label(window_principale, text="Gestion des retards", font=('Verdana', 15))
    Label1.grid(row=1, column=0)

    #LIVRES AFFICHAGE
    Label1= Label(window_principale, text='liste des retards', font=('Verdana', 10)) #titre
    Label1.grid(row=2, column=0)

    #1 - Creation du tableau retard
    tableau = Treeview(window_principale, columns=('identifiant_retard', 'n_emprunt','identifiant_livre','identifiant_adherent','dateretour'))
    tableau.heading('identifiant_retard', text="Identifiant du retard")
    tableau.heading('n_emprunt', text="N° d'emrpunt")
    tableau.heading('identifiant_livre', text="identifiant du livre non-rendu")
    tableau.heading('identifiant_adherent', text="Identifiant de l'adhérent")
    tableau.heading('dateretour', text="Date de retour prévue")
    tableau['show'] = 'headings' # sans ceci, il y avait une colonne vide à gauche qui a pour rôle d'afficher le paramètre "text" qui peut être spécifié lors du insert
    tableau.grid(row = 3, column=0)

    #2 - Remplissage du tableau
    resultat= liste_retard()
    if len(resultat):
        for enreg in resultat:
            # chaque ligne n'a pas de parent, est ajoutée à la fin de la liste, utilise le champ id comme identifiant et on fournit les valeurs pour chacune des colonnes du tableau
            tableau.insert('', 'end', iid=enreg[0], values=(enreg[0], enreg[1], enreg[2], enreg[3], enreg[4]))
    else:
        rien = Label(text = "Il n'y a aucun retard actuellement.")
        tableau.pack_forget()
        rien.grid(row=3, column = 0)

    #BOUTON RETOUR
    button_retour=Button(text='Retour', command=menu_er)
    button_retour.grid(row=1000,column=0)


##################################DEMARRAGE DU LOGICIEL#################################

#CREATIONDE LA FENETRE
window_principale = Tk()
window_principale.geometry('1300x1000')
window_principale.title('gestionnaire de bibliothèque')

Label1= Label(window_principale, text="Bienvenue sur votre gestionnaire de bibliothèque", font=('Verdana', 15))
Label1.grid(row=1, column=0)
button1=Button(text='Ouvrir ma bibliothèque', command=menu)
button1.grid(row=2,column=0)

#VERIFICATION DES DATES D'EMRPUNTS
verif_date()






mainloop()

def afficher_menu():
    print("Menu: ")
    print("1  Créer la table livre")
    print("2  Créer la table adherent")
    print("3  créer la table emprunt")
    print("4  Ajouter un livre")
    print("5  Ajouter un adhérent")
    print("6  Ajouter un emprunt")
    print("7  Afficher la liste des livres")
    print("8  Afficher la liste des livres empruntés")
    print("9  Afficher la liste des adhérents")
    print("10 Afficher la liste des emprunts en retard")
    print("11 Supprimer un livre")
    print("12 Supprimer un adhérent")
    print("13 Retour d'un livre")
    print("14 Supprimer un retard")
    print("15 Supprimer toute la base de données")
    print("0  Quitter")

def lire_action():
    verif_date()
    afficher_menu()
    reponse = int(input("Votre choix : "))
    choix=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]
    while reponse not in choix:
        afficher_menu()
        reponse = int(input("Votre choix : "))
    return reponse

def appli():
    termine = False
    while not(termine):
        action = lire_action()
        if action == 0:
            termine = True
        else:
            table_actions[action]()
            connexion.commit()

table_actions = [None,
table_livre,
table_adherent,
table_emprunt,
ajouter_livre,
ajouter_adherent,
ajouter_emprunt,
liste_livre,
liste_emprunt,
liste_adherent,
liste_retard,
supprimer_livre,
supprimer_adherent,
supprimer_emprunt,
supprimer_retard]



connexion.close()



