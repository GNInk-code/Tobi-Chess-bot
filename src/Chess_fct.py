import copy
import Funcs_for_GUI
alphabet="abcdefgh"
def transfo_coup_positionliste(coup):
    lettre=["a","b","c","d","e","f","g","h"]
    # a1 -> (0,0)
    if isinstance(coup,str):
        position=(int(coup[1])-1,lettre.index(coup[0]))
        return position
    # le contraire
    elif isinstance(coup,list) or isinstance(coup,tuple):
        position=lettre[coup[1]]+str(coup[0]+1)
        return position
    # c la merde
    else:
        raise Exception("Y'a un paramètre autre qu'une liste ou un coup d'échec dans la fct transfo_coup")

#full ia celui là, je l'assume (à part le nom)
def nouveau_plateau(plateau):
#    plateau=[]
#    for i in plateau_initial:
#        ligne=[]
#        for j in i:
#            if j==".":
#                ligne.append(".")
#            else:
#                ligne.append(pièce(j.Blanc,j.type,j.position,j.has_moved))
#        plateau.append(ligne)
#    return plateau
    #return copy.deepcopy(plateau_initial)
    nouveau = []
    for ligne in plateau:
        nouvelle_ligne = []
        for case in ligne:
            if case == ".":
                nouvelle_ligne.append(".")
            else:
                p = pièce(case.Blanc, case.type, case.position, case.has_moved)
                p.a_bougé_de_2_cases = case.a_bougé_de_2_cases
                nouvelle_ligne.append(p)
        nouveau.append(nouvelle_ligne)
    return nouveau
    
def est_en_echec(plateau,Couleur_Blanc:bool):
    p=plateau
    position_roi=None
    plateau_initial=p
    
    casevisée=[]
    for i in p:
        for j in i:
            if j!="." and j.type=="K" and j.Blanc==Couleur_Blanc:
                position_roi=transfo_coup_positionliste(j.position)
    for i in range(8):
        for j in range(8):
            if not p[int(i)][int(j)]=="." and p[i][j].Blanc!=Couleur_Blanc:        
                pp=[i,j]
                if p[i][j].type=="P":
                    if p[i][j].Blanc:
                        casevisée.append((pp[0]+1,pp[1]+1)) if 0<=pp[0]+1<=7 and 0<=pp[1]+1<=7 and (not (pp[0]+1,pp[1]+1) in casevisée) else None
                        casevisée.append((pp[0]+1,pp[1]-1)) if 0<=pp[0]+1<=7 and 0<=pp[1]-1<=7 and (not (pp[0]+1,pp[1]-1) in casevisée) else None
                    elif p[i][j].Blanc==False:
                        casevisée.append((pp[0]-1,pp[1]+1)) if 0<=pp[0]-1<=7 and 0<=pp[1]+1<=7 and (not (pp[0]-1,pp[1]+1) in casevisée) else None
                        casevisée.append((pp[0]-1,pp[1]-1)) if 0<=pp[0]-1<=7 and 0<=pp[1]-1<=7 and (not (pp[0]-1,pp[1]-1) in casevisée) else None
                elif p[i][j].type=="N":
                    déplacement=[(2,1),(1,2),(-1,2),(-2,1),(-2,-1),(-1,-2),(1,-2),(2,-1)]
                    for z in déplacement:
                        if 0<=pp[0]+z[0]<=7 and 0<=pp[1]+z[1]<=7 and (not (pp[0]+z[0],pp[1]+z[1]) in casevisée):
                            casevisée.append((pp[0]+z[0],pp[1]+z[1]))
                elif p[i][j].type=="B":
                    déplacement=[(1,1),(1,-1),(-1,-1),(-1,1)]
                    coordonné_temp=[pp[0],pp[1]]
                    for z in déplacement:
                        coordonné_temp=[pp[0],pp[1]]
                        while coordonné_temp[0]+z[0] in range(8) and coordonné_temp[1]+z[1] in range(8):
                            if plateau_initial[coordonné_temp[0]+z[0]][coordonné_temp[1]+z[1]]==".":
                                if (coordonné_temp[0]+z[0],coordonné_temp[1]+z[1]) not in casevisée:
                                    casevisée.append((coordonné_temp[0]+z[0],coordonné_temp[1]+z[1]))
                                coordonné_temp[0]+=z[0]
                                coordonné_temp[1]+=z[1]
                            else:
                                if (coordonné_temp[0]+z[0],coordonné_temp[1]+z[1]) not in casevisée:
                                    casevisée.append((coordonné_temp[0]+z[0],coordonné_temp[1]+z[1]))
                                break
                elif p[i][j].type=="R":
                    déplacement=[(1,0),(0,-1),(-1,0),(0,1)]
                    coordonné_temp=[pp[0],pp[1]]
                    for z in déplacement:
                        coordonné_temp=[pp[0],pp[1]]
                        while coordonné_temp[0]+z[0] in range(8) and coordonné_temp[1]+z[1] in range(8):
                            if plateau_initial[coordonné_temp[0]+z[0]][coordonné_temp[1]+z[1]]==".":
                                if (coordonné_temp[0]+z[0],coordonné_temp[1]+z[1]) not in casevisée:
                                    casevisée.append((coordonné_temp[0]+z[0],coordonné_temp[1]+z[1]))
                                coordonné_temp[0]+=z[0]
                                coordonné_temp[1]+=z[1]
                            else:
                                if (coordonné_temp[0]+z[0],coordonné_temp[1]+z[1]) not in casevisée:
                                    casevisée.append((coordonné_temp[0]+z[0],coordonné_temp[1]+z[1]))
                                break
                elif p[i][j].type=="Q":
                    déplacement=[(1,0),(0,-1),(-1,0),(0,1),(1,1),(1,-1),(-1,-1),(-1,1)]
                    coordonné_temp=[pp[0],pp[1]]
                    for z in déplacement:
                        coordonné_temp=[pp[0],pp[1]]
                        while coordonné_temp[0]+z[0] in range(8) and coordonné_temp[1]+z[1] in range(8):
                            if plateau_initial[coordonné_temp[0]+z[0]][coordonné_temp[1]+z[1]]==".":
                                if (coordonné_temp[0]+z[0],coordonné_temp[1]+z[1]) not in casevisée:
                                    casevisée.append((coordonné_temp[0]+z[0],coordonné_temp[1]+z[1]))
                                coordonné_temp[0]+=z[0]
                                coordonné_temp[1]+=z[1]
                            else:
                                if (coordonné_temp[0]+z[0],coordonné_temp[1]+z[1]) not in casevisée:
                                    casevisée.append((coordonné_temp[0]+z[0],coordonné_temp[1]+z[1]))
                                break
                elif p[i][j].type=="K":
                    déplacement=[(1,0),(0,-1),(-1,0),(0,1),(1,1),(1,-1),(-1,-1),(-1,1)]
                    for z in déplacement:
                        if 0<=pp[0]+z[0]<=7 and 0<=pp[1]+z[1]<=7 and (not (pp[0]+z[0],pp[1]+z[1]) in casevisée):
                            casevisée.append((pp[0]+z[0],pp[1]+z[1]))
    if position_roi in casevisée:
        return True
    else:
        return False

def jouer_le_coup(coup,Couleur_Blanc:bool,plateau_initial):
    p=nouveau_plateau(plateau_initial)
    if "#" in coup:
        coup=coup.replace("#","")
    elif "+" in coup:
        coup=coup.replace("+","")
    elif "*" in coup:
        coup=coup.replace("*","")
    
    #a bougé de 2 cases pour en passant
    if coup[0] in ["R","B","Q","N","K","O"]: #si ce n'est pas un pion
        if Couleur_Blanc:    
            for i in range(8):
                if not p[3][i]=="." and p[3][i].type=="P" and p[3][i].Blanc and p[3][i].a_bougé_de_2_cases:
                    p[3][i].a_bougé_de_2_cases=False
        elif Couleur_Blanc==False:
            for i in range(8):
                if not p[4][i]=="." and p[4][i].type=="P" and p[4][i].Blanc==False and p[4][i].a_bougé_de_2_cases:
                    p[4][i].a_bougé_de_2_cases=False
    else: #si c'est un pion
        if Couleur_Blanc:
            for i in range(8):
                if not str(i+1)==coup[1] and not p[3][i]=="." and p[3][i].type=="P" and p[3][i].Blanc and p[3][i].a_bougé_de_2_cases:
                    p[3][i].a_bougé_de_2_cases=False
        elif Couleur_Blanc==False:
            for i in range(8):
                if not str(i+1)==coup[1] and not p[4][i]=="." and p[4][i].type=="P" and p[4][i].Blanc==False and p[4][i].a_bougé_de_2_cases:
                    p[4][i].a_bougé_de_2_cases=False
    
    if coup=="O-O" or coup=="O-O-O":
        if coup=="O-O":#roque petit
            if Couleur_Blanc:
                #déplacement du roi
                p[0][6]=p[0][4]
                p[0][4]="."
                p[0][6].position="g1"
                p[0][6].has_moved=True
                #déplacement de la tour
                p[0][5]=p[0][7]
                p[0][7]="."
                p[0][5].position="f1"
                p[0][5].has_moved=True
                return p
            elif Couleur_Blanc==False:
                #déplacement du roi
                p[7][6]=p[7][4]
                p[7][4]="."
                p[7][6].position="g8"
                p[7][6].has_moved=True
                #déplacement de la tour
                p[7][5]=p[7][7]
                p[7][7]="."
                p[7][5].position="f8"
                p[7][5].has_moved=True
                return p
        elif coup=="O-O-O":#roque grand
            if Couleur_Blanc:
                #déplacement du roi
                p[0][2]=p[0][4]
                p[0][4]="."
                p[0][2].position="c1"
                p[0][2].has_moved=True
                #déplacement de la tour
                p[0][3]=p[0][0]
                p[0][0]="."
                p[0][3].position="d1"
                p[0][3].has_moved=True
                return p
            elif Couleur_Blanc==False:
                #déplacement du roi
                p[7][2]=p[7][4]
                p[7][4]="."
                p[7][2].position="c8"
                p[7][2].has_moved=True
                #déplacement de la tour
                p[7][3]=p[7][0]
                p[7][0]="."
                p[7][3].position="d8"
                p[7][3].has_moved=True
                return p


    if not coup[0] in ["R","B","Q","N","K"]:#pion uniquement
        if len(coup)==2:
            coup_num=transfo_coup_positionliste(coup)
            #il n'y pas besoin de vérifier car il est sur que le coup est possible
            #une case ou deux cases
            if Couleur_Blanc:
                if p[coup_num[0]-1][coup_num[1]]!=".":
                    # Le pion est juste en dessous (mouvement d'une case)
                    p[coup_num[0]][coup_num[1]]=p[coup_num[0]-1][coup_num[1]]
                    p[coup_num[0]-1][coup_num[1]]="."
                    p[coup_num[0]][coup_num[1]].position=coup
                    p[coup_num[0]][coup_num[1]].has_moved=True
                    p[coup_num[0]][coup_num[1]].a_bougé_de_2_cases=False
                    return p
                else:
                    # Le pion est deux cases en dessous (mouvement de deux cases)
                    p[coup_num[0]][coup_num[1]]=p[coup_num[0]-2][coup_num[1]]
                    p[coup_num[0]-2][coup_num[1]]="."
                    p[coup_num[0]][coup_num[1]].position=coup
                    p[coup_num[0]][coup_num[1]].has_moved=True
                    p[coup_num[0]][coup_num[1]].a_bougé_de_2_cases=True
                    return p
            else:
                if p[coup_num[0]+1][coup_num[1]]!=".":
                    # Le pion est juste au dessus (mouvement d'une case)
                    p[coup_num[0]][coup_num[1]]=p[coup_num[0]+1][coup_num[1]]
                    p[coup_num[0]+1][coup_num[1]]="."
                    p[coup_num[0]][coup_num[1]].position=coup
                    p[coup_num[0]][coup_num[1]].has_moved=True
                    p[coup_num[0]][coup_num[1]].a_bougé_de_2_cases=False
                    return p
                else:
                    # Le pion est deux cases au dessus (mouvement de deux cases)
                    p[coup_num[0]][coup_num[1]]=p[coup_num[0]+2][coup_num[1]]
                    p[coup_num[0]+2][coup_num[1]]="."
                    p[coup_num[0]][coup_num[1]].position=coup
                    p[coup_num[0]][coup_num[1]].has_moved=True
                    p[coup_num[0]][coup_num[1]].a_bougé_de_2_cases=True
                    return p
        elif len(coup)==4 and coup[1]=="x":#manger basique axb5
            coup_num=transfo_coup_positionliste(coup[2:])
            colonne_de_base=alphabet.index(coup[0])
            if Couleur_Blanc:
                p[coup_num[0]][coup_num[1]]=p[coup_num[0]-1][colonne_de_base]
                p[coup_num[0]-1][colonne_de_base]="."
                p[coup_num[0]][coup_num[1]].position=coup[2:]
                p[coup_num[0]][coup_num[1]].has_moved=True
                p[coup_num[0]][coup_num[1]].a_bougé_de_2_cases=False
                return p
            elif Couleur_Blanc==False:
                p[coup_num[0]][coup_num[1]]=p[coup_num[0]+1][colonne_de_base]
                p[coup_num[0]+1][colonne_de_base]="."
                p[coup_num[0]][coup_num[1]].position=coup[2:]
                p[coup_num[0]][coup_num[1]].has_moved=True
                p[coup_num[0]][coup_num[1]].a_bougé_de_2_cases=False
                return p
        elif "e.p." in coup:#manger en passant axb6e.p.
            coup_num=transfo_coup_positionliste(coup[2:4])
            colonne_de_base=alphabet.index(coup[0])
            if Couleur_Blanc:
                p[coup_num[0]][coup_num[1]]=p[coup_num[0]-1][alphabet.index(coup[0])]
                p[coup_num[0]-1][alphabet.index(coup[0])]="."
                p[coup_num[0]-1][coup_num[1]]="."
                p[coup_num[0]][coup_num[1]].position=coup[2:4]
                p[coup_num[0]][coup_num[1]].has_moved=True
                p[coup_num[0]][coup_num[1]].a_bougé_de_2_cases=False
                return p
            elif Couleur_Blanc==False:
                p[coup_num[0]][coup_num[1]]=p[coup_num[0]+1][alphabet.index(coup[0])]
                p[coup_num[0]+1][alphabet.index(coup[0])]="."
                p[coup_num[0]+1][coup_num[1]]="."
                p[coup_num[0]][coup_num[1]].position=coup[2:4]
                p[coup_num[0]][coup_num[1]].has_moved=True
                p[coup_num[0]][coup_num[1]].a_bougé_de_2_cases=False
                return p
        elif len(coup)==4 and coup[2]=="=":#promotion sans manger a1=Q
            coup_num=transfo_coup_positionliste(coup[0:2])
            if Couleur_Blanc:
                if coup[3] in ["Q","R","B","N"]:
                    p[coup_num[0]][coup_num[1]]=pièce(True,coup[3],coup[0:2],True)
                    p[coup_num[0]-1][coup_num[1]]="."
                    return p
            else:
                if coup[3] in ["Q","R","B","N"]:
                    p[coup_num[0]][coup_num[1]]=pièce(False,coup[3],coup[0:2],True)
                    p[coup_num[0]+1][coup_num[1]]="."
                    return p
        elif len(coup)==6 and coup[4]=="=":#promotion en mangeant axb8=Q et pas a7xb8=Q
            coup_num=transfo_coup_positionliste(coup[2:4])
            colonne_de_base=alphabet.index(coup[0])
            if Couleur_Blanc:
                if coup[5] in ["Q","R","B","N"]:
                    p[coup_num[0]][coup_num[1]]=pièce(True,coup[5],coup[2:4],True)
                    p[coup_num[0]-1][colonne_de_base]="."
                    return p
            else:
                if coup[5] in ["Q","R","B","N"]:
                    p[coup_num[0]][coup_num[1]]=pièce(False,coup[5],coup[2:4],True)
                    p[coup_num[0]+1][colonne_de_base]="."
                    return p        

    elif coup[0]=="R":
        if not "x" in coup: #déplacement basique forme Ra1e5
            coup_num=transfo_coup_positionliste(coup[3:])
            coup_num_initial=transfo_coup_positionliste(coup[1:3])
            p[coup_num[0]][coup_num[1]]=p[coup_num_initial[0]][coup_num_initial[1]]
            p[coup_num_initial[0]][coup_num_initial[1]]="."
            p[coup_num[0]][coup_num[1]].position=coup[3:]
            p[coup_num[0]][coup_num[1]].has_moved=True
            return p
        else: #manger forme Ra1xe5
            coup_num=transfo_coup_positionliste(coup[4:])
            coup_num_initial=transfo_coup_positionliste(coup[1:3])
            p[coup_num[0]][coup_num[1]]=p[coup_num_initial[0]][coup_num_initial[1]]
            p[coup_num_initial[0]][coup_num_initial[1]]="."
            p[coup_num[0]][coup_num[1]].position=coup[4:]
            p[coup_num[0]][coup_num[1]].has_moved=True
            return p

    elif coup[0]=="B":
        if not "x" in coup: #déplacement basique forme Ba1e5
            coup_num=transfo_coup_positionliste(coup[3:])
            coup_num_initial=transfo_coup_positionliste(coup[1:3])
            p[coup_num[0]][coup_num[1]]=p[coup_num_initial[0]][coup_num_initial[1]]
            p[coup_num_initial[0]][coup_num_initial[1]]="."
            p[coup_num[0]][coup_num[1]].position=coup[3:]
            p[coup_num[0]][coup_num[1]].has_moved=True
            return p
        else: #manger forme Ba1xe5
            coup_num=transfo_coup_positionliste(coup[4:])
            coup_num_initial=transfo_coup_positionliste(coup[1:3])
            p[coup_num[0]][coup_num[1]]=p[coup_num_initial[0]][coup_num_initial[1]]
            p[coup_num_initial[0]][coup_num_initial[1]]="."
            p[coup_num[0]][coup_num[1]].position=coup[4:]
            p[coup_num[0]][coup_num[1]].has_moved=True
            return p

    elif coup[0]=="Q":
        if not "x" in coup: #déplacement basique forme Qa1e5
            coup_num=transfo_coup_positionliste(coup[3:])
            coup_num_initial=transfo_coup_positionliste(coup[1:3])
            p[coup_num[0]][coup_num[1]]=p[coup_num_initial[0]][coup_num_initial[1]]
            p[coup_num_initial[0]][coup_num_initial[1]]="."
            p[coup_num[0]][coup_num[1]].position=coup[3:]
            p[coup_num[0]][coup_num[1]].has_moved=True
            return p
        else: #manger forme Qa1xe5
            coup_num=transfo_coup_positionliste(coup[4:])
            coup_num_initial=transfo_coup_positionliste(coup[1:3])
            p[coup_num[0]][coup_num[1]]=p[coup_num_initial[0]][coup_num_initial[1]]
            p[coup_num_initial[0]][coup_num_initial[1]]="."
            p[coup_num[0]][coup_num[1]].position=coup[4:]
            p[coup_num[0]][coup_num[1]].has_moved=True
            return p

    elif coup[0]=="N":
        if not "x" in coup: #déplacement basique forme Na1e5
            coup_num=transfo_coup_positionliste(coup[3:])
            coup_num_initial=transfo_coup_positionliste(coup[1:3])
            p[coup_num[0]][coup_num[1]]=p[coup_num_initial[0]][coup_num_initial[1]]
            p[coup_num_initial[0]][coup_num_initial[1]]="."
            p[coup_num[0]][coup_num[1]].position=coup[-2:]
            p[coup_num[0]][coup_num[1]].has_moved=True
            return p
        else: #manger forme Na1xe5
            coup_num=transfo_coup_positionliste(coup[4:]) 
            coup_num_initial=transfo_coup_positionliste(coup[1:3])
            p[coup_num[0]][coup_num[1]]=p[coup_num_initial[0]][coup_num_initial[1]]
            p[coup_num_initial[0]][coup_num_initial[1]]="."
            p[coup_num[0]][coup_num[1]].position=coup[4:]
            p[coup_num[0]][coup_num[1]].has_moved=True
            return p

    elif coup[0]=="K":
        if not "x" in coup: #déplacement basique forme Ka1e5
            coup_num=transfo_coup_positionliste(coup[3:])
            coup_num_initial=transfo_coup_positionliste(coup[1:3])
            p[coup_num[0]][coup_num[1]]=p[coup_num_initial[0]][coup_num_initial[1]]
            p[coup_num_initial[0]][coup_num_initial[1]]="."
            p[coup_num[0]][coup_num[1]].position=coup[3:]
            p[coup_num[0]][coup_num[1]].has_moved=True
            return p
        else: #manger forme Ka1xe5
            coup_num=transfo_coup_positionliste(coup[4:]) 
            coup_num_initial=transfo_coup_positionliste(coup[1:3])
            p[coup_num[0]][coup_num[1]]=p[coup_num_initial[0]][coup_num_initial[1]]
            p[coup_num_initial[0]][coup_num_initial[1]]="."
            p[coup_num[0]][coup_num[1]].position=coup[4:]
            p[coup_num[0]][coup_num[1]].has_moved=True
            return p

def est_echec_et_mat(plateau,Couleur_Blanc:bool):
    if est_en_echec(plateau,Couleur_Blanc):
        #vérifier si y'a des coups possibles
        for i in plateau:
            for j in i:
                if j!="." and j.Blanc==Couleur_Blanc:
                    liste_coup_possible=j.possible_moves(plateau,True)
                    for k in liste_coup_possible:
                        nouveau_plateau_test=jouer_le_coup(k,Couleur_Blanc,nouveau_plateau(plateau))
                        if not est_en_echec(nouveau_plateau_test,Couleur_Blanc):
                            return False
                        del nouveau_plateau_test
        return True
    else:
        return False


class pièce:
    def __init__(self,Blanc,type,position,has_moved):
        self.Blanc = Blanc
        self.type = type
        self.position = position
        self.has_moved=has_moved
        self.a_bougé_de_2_cases=False 
    #output = a1, b2, Cc3, etc
    def possible_moves(self,plateau_initial,coup_interne):
        liste_coup_possible=[]
        p=transfo_coup_positionliste(self.position)
        Chess_board=plateau_initial
        ECHEC_ACTIF=False #sera modifié par la suite pour gérer les échecs
        if self.type=="P": #pion uniquement
            #avancer de une case
            if plateau_initial[p[0]+1][p[1]]=="." and self.Blanc and not "7" in self.position:
                    liste_coup_possible.append(self.position[0]+str(int(self.position[1])+1))
            if plateau_initial[p[0]-1][p[1]]=="." and self.Blanc==False and not "2" in self.position:
                    liste_coup_possible.append(self.position[0]+str(int(self.position[1])-1))
            #avancer de deux cases
            if p[0]==1 and plateau_initial[p[0]+1][p[1]]=="." and plateau_initial[p[0]+2][p[1]]=="." and self.Blanc:
                liste_coup_possible.append(self.position[0]+str(int(self.position[1])+2))
            if p[0]==6 and plateau_initial[p[0]-1][p[1]]=="." and plateau_initial[p[0]-2][p[1]]=="." and self.Blanc==False:
                    liste_coup_possible.append(self.position[0]+str(int(self.position[1])-2))
                #manger colonne inférieur
            if self.Blanc and p[0]+1 < 7 and p[1]-1 >= 0 and not "a" in self.position and not isinstance(plateau_initial[p[0]+1][p[1]-1],str):
                if plateau_initial[p[0]+1][p[1]-1].Blanc != self.Blanc:
                    liste_coup_possible.append(chr(ord(self.position[0]))+"x"+transfo_coup_positionliste([p[0]+1,p[1]-1]))
            if self.Blanc==False and p[0]-1 > 0 and p[1]-1 >= 0 and not "h" in self.position and not isinstance(plateau_initial[p[0]-1][p[1]-1],str):
                if plateau_initial[p[0]-1][p[1]-1].Blanc != self.Blanc:
                    liste_coup_possible.append(chr(ord(self.position[0]))+"x"+transfo_coup_positionliste([p[0]-1,p[1]-1]))
            
            #manger colonne supérieur
            if self.Blanc and p[0]+1 < 7 and p[1]+1 <= 7 and not "h" in self.position and not isinstance(plateau_initial[p[0]+1][p[1]+1],str):
                if plateau_initial[p[0]+1][p[1]+1].Blanc != self.Blanc:
                    liste_coup_possible.append(chr(ord(self.position[0]))+"x"+transfo_coup_positionliste([p[0]+1,p[1]+1]))
            if self.Blanc==False and p[0]-1 > 0 and p[1]+1 <= 7 and not "a" in self.position and not isinstance(plateau_initial[p[0]-1][p[1]+1],str):
                if plateau_initial[p[0]-1][p[1]+1].Blanc != self.Blanc:
                    liste_coup_possible.append(chr(ord(self.position[0]))+"x"+transfo_coup_positionliste([p[0]-1,p[1]+1]))
            #promotion
            if self.Blanc and "7" in self.position:
                if plateau_initial[p[0]+1][p[1]]==".":
                    liste_coup_possible.append(transfo_coup_positionliste([p[0]+1,p[1]])+"=Q")
                    liste_coup_possible.append(transfo_coup_positionliste([p[0]+1,p[1]])+"=R")
                    liste_coup_possible.append(transfo_coup_positionliste([p[0]+1,p[1]])+"=B")
                    liste_coup_possible.append(transfo_coup_positionliste([p[0]+1,p[1]])+"=N")
            if self.Blanc==False and "2" in self.position:
                if plateau_initial[p[0]-1][p[1]]==".":
                    liste_coup_possible.append(transfo_coup_positionliste([p[0]-1,p[1]])+"=Q")
                    liste_coup_possible.append(transfo_coup_positionliste([p[0]-1,p[1]])+"=R")
                    liste_coup_possible.append(transfo_coup_positionliste([p[0]-1,p[1]])+"=B")
                    liste_coup_possible.append(transfo_coup_positionliste([p[0]-1,p[1]])+"=N")    
            #promotion en mangeant
            if self.Blanc and "7" in self.position:
                if not "a" in self.position and not isinstance(plateau_initial[p[0]+1][p[1]-1],str):
                    if plateau_initial[p[0]+1][p[1]-1].Blanc != self.Blanc:  
                        liste_coup_possible.append(chr(ord(self.position[0]))+"x"+transfo_coup_positionliste([p[0]+1,p[1]-1])+"=Q")
                        liste_coup_possible.append(chr(ord(self.position[0]))+"x"+transfo_coup_positionliste([p[0]+1,p[1]-1])+"=R")
                        liste_coup_possible.append(chr(ord(self.position[0]))+"x"+transfo_coup_positionliste([p[0]+1,p[1]-1])+"=B")
                        liste_coup_possible.append(chr(ord(self.position[0]))+"x"+transfo_coup_positionliste([p[0]+1,p[1]-1])+"=N")
                if not "h" in self.position and not isinstance(plateau_initial[p[0]+1][p[1]+1],str):
                    if plateau_initial[p[0]+1][p[1]+1].Blanc != self.Blanc:  
                        liste_coup_possible.append(chr(ord(self.position[0]))+"x"+transfo_coup_positionliste([p[0]+1,p[1]+1])+"=Q")
                        liste_coup_possible.append(chr(ord(self.position[0]))+"x"+transfo_coup_positionliste([p[0]+1,p[1]+1])+"=R")
                        liste_coup_possible.append(chr(ord(self.position[0]))+"x"+transfo_coup_positionliste([p[0]+1,p[1]+1])+"=B")
                        liste_coup_possible.append(chr(ord(self .position[0]))+"x"+transfo_coup_positionliste([p[0]+1,p[1]+1])+"=N")
            if self.Blanc==False and "2" in self.position:
                if not "a" in self.position and not isinstance(plateau_initial[p[0]-1][p[1]-1],str):
                    if plateau_initial[p[0]-1][p[1]-1].Blanc != self.Blanc:  
                        liste_coup_possible.append(chr(ord(self.position[0]))+"x"+transfo_coup_positionliste([p[0]-1,p[1]-1])+"=Q")
                        liste_coup_possible.append(chr(ord(self.position[0]))+"x"+transfo_coup_positionliste([p[0]-1,p[1]-1])+"=R")
                        liste_coup_possible.append(chr(ord(self.position[0]))+"x"+transfo_coup_positionliste([p[0]-1,p[1]-1])+"=B")
                        liste_coup_possible.append(chr(ord(self.position[0]))+"x"+transfo_coup_positionliste([p[0]-1,p[1]-1])+"=N")
                if not "h" in self.position and not isinstance(plateau_initial[p[0]-1][p[1]+1],str):
                    if plateau_initial[p[0]-1][p[1]+1].Blanc != self.Blanc:  
                        liste_coup_possible.append(self.position[0]+"x"+transfo_coup_positionliste([p[0]-1,p[1]+1])+"=Q")
                        liste_coup_possible.append(self.position[0]+"x"+transfo_coup_positionliste([p[0]-1,p[1]+1])+"=R")
                        liste_coup_possible.append(self.position[0]+"x"+transfo_coup_positionliste([p[0]-1,p[1]+1])+"=B")
                        liste_coup_possible.append(self.position[0]+"x"+transfo_coup_positionliste([p[0]-1,p[1]+1])+"=N")
            #en passant
            if self.Blanc:
                if p[0]==4 and p[1]-1 >=0 and not "a" in self.position:
                    if not isinstance(plateau_initial[p[0]][p[1]-1],str):
                        if plateau_initial[p[0]][p[1]-1].type=="P" and plateau_initial[p[0]][p[1]-1].Blanc==False and plateau_initial[p[0]][p[1]-1].a_bougé_de_2_cases:
                            liste_coup_possible.append(chr(ord(self.position[0]))+"x"+transfo_coup_positionliste([p[0]+1,p[1]-1])+"e.p.")
                if p[0]==4 and p[1]+1 <=7 and not "h" in self.position:
                    if not isinstance(plateau_initial[p[0]][p[1]+1],str):
                        if plateau_initial[p[0]][p[1]+1].type=="P" and plateau_initial[p[0]][p[1]+1].Blanc==False and plateau_initial[p[0]][p[1]+1].a_bougé_de_2_cases:
                            liste_coup_possible.append(chr(ord(self.position[0]))+"x"+transfo_coup_positionliste([p[0]+1,p[1]+1])+"e.p.")
            if self.Blanc==False:
                if p[0]==3 and p[1]-1 >=0 and not "a" in self.position:
                    if not isinstance(plateau_initial[p[0]][p[1]-1],str):
                        if plateau_initial[p[0]][p[1]-1].type=="P" and plateau_initial[p[0]][p[1]-1].Blanc==True and plateau_initial[p[0]][p[1]-1].a_bougé_de_2_cases:
                            liste_coup_possible.append(chr(ord(self.position[0]))+"x"+transfo_coup_positionliste([p[0]-1,p[1]-1])+"e.p.")
                if p[0]==3 and p[1]+1 <=7 and not "h" in self.position:
                    if not isinstance(plateau_initial[p[0]][p[1]+1],str):
                        if plateau_initial[p[0]][p[1]+1].type=="P" and plateau_initial[p[0]][p[1]+1].Blanc==True and plateau_initial[p[0]][p[1]+1].a_bougé_de_2_cases:
                            liste_coup_possible.append(chr(ord(self.position[0]))+"x"+transfo_coup_positionliste([p[0]-1,p[1]+1])+"e.p.")
        
        if self.type=="N": #a1e5 ou a1xe5
            déplacement=[(2,1),(2,-1),(-2,1),(-2,-1),(1,2),(1,-2),(-1,2),(-1,-2)]
            for i in déplacement:
                nouvelle_coordonné=(p[0]+i[0],p[1]+i[1])
                if not (nouvelle_coordonné[0]<0 or nouvelle_coordonné[0]>7 or nouvelle_coordonné[1]<0 or nouvelle_coordonné[1]>7):
                    if plateau_initial[nouvelle_coordonné[0]][nouvelle_coordonné[1]]==".":
                        liste_coup_possible.append("N"+self.position+transfo_coup_positionliste(nouvelle_coordonné))
                    elif plateau_initial[nouvelle_coordonné[0]][nouvelle_coordonné[1]].Blanc != self.Blanc:
                        liste_coup_possible.append("N"+self.position+"x"+transfo_coup_positionliste(nouvelle_coordonné))

        if self.type=="B": #a1e5 ou a1xe5
            direction=[(1,1),(1,-1),(-1,-1),(-1,1)]
            for i in direction:
                coordonné_temp=[p[0]+i[0],p[1]+i[1]]
                while 8>coordonné_temp[0]>-1 and 8>coordonné_temp[1]>-1:
                    if plateau_initial[coordonné_temp[0]][coordonné_temp[1]]==".":
                        liste_coup_possible.append("B"+self.position+transfo_coup_positionliste(coordonné_temp))
                        coordonné_temp[0]+=i[0]
                        coordonné_temp[1]+=i[1]
                    elif plateau_initial[coordonné_temp[0]][coordonné_temp[1]].Blanc != self.Blanc:
                        liste_coup_possible.append("B"+self.position+"x"+transfo_coup_positionliste(coordonné_temp))
                        break
                    else:
                        break

        if self.type=="R": #a1e5 ou a1xe5
            direction=[(1,0),(0,-1),(-1,0),(0,1)]
            for i in direction:
                coordonné_temp=[p[0]+i[0],p[1]+i[1]]
                while 8>coordonné_temp[0]>-1 and 8>coordonné_temp[1]>-1:
                    if plateau_initial[coordonné_temp[0]][coordonné_temp[1]]==".":
                        liste_coup_possible.append("R"+self.position+transfo_coup_positionliste(coordonné_temp))
                        coordonné_temp[0]+=i[0]
                        coordonné_temp[1]+=i[1]
                    elif plateau_initial[coordonné_temp[0]][coordonné_temp[1]].Blanc != self.Blanc:
                        liste_coup_possible.append("R"+self.position+"x"+transfo_coup_positionliste(coordonné_temp))
                        break
                    else: 
                        break
        
        if self.type=="Q": #a1e5 ou a1xe5
            direction=[(1,0),(0,-1),(-1,0),(0,1),(1,1),(1,-1),(-1,-1),(-1,1)]
            for i in direction:
                coordonné_temp=[p[0]+i[0],p[1]+i[1]]
                while 8>coordonné_temp[0]>-1 and 8>coordonné_temp[1]>-1:
                    if plateau_initial[coordonné_temp[0]][coordonné_temp[1]]==".":
                        liste_coup_possible.append("Q"+self.position+transfo_coup_positionliste(coordonné_temp))
                        coordonné_temp[0]+=i[0]
                        coordonné_temp[1]+=i[1]
                    elif plateau_initial[coordonné_temp[0]][coordonné_temp[1]].Blanc != self.Blanc:
                        liste_coup_possible.append("Q"+self.position+"x"+transfo_coup_positionliste(coordonné_temp))
                        break
                    else: 
                        break
        
        if self.type=="K": #a1e5 ou a1xe5 + roque
            ddddéplacement=[(1,0),(0,-1),(-1,0),(0,1),(1,1),(1,-1),(-1,-1),(-1,1)]
            case_protégé=[]
            #case d'échec
            for i in plateau_initial:
                for z in i:
                    if (not z==".") and z.Blanc!=self.Blanc:
                        pp=transfo_coup_positionliste(z.position)
                        if z.type=="P":
                            if z.Blanc:
                                case_protégé.append((pp[0]+1,pp[1]+1)) if 0<=pp[0]+1<=7 and 0<=pp[1]+1<=7 and (not (pp[0]+1,pp[1]+1) in case_protégé) else None
                                case_protégé.append((pp[0]+1,pp[1]-1)) if 0<=pp[0]+1<=7 and 0<=pp[1]-1<=7 and (not (pp[0]+1,pp[1]-1) in case_protégé) else None
                            elif z.Blanc==False:
                                case_protégé.append((pp[0]-1,pp[1]+1)) if 0<=pp[0]-1<=7 and 0<=pp[1]+1<=7 and (not (pp[0]-1,pp[1]+1) in case_protégé) else None
                                case_protégé.append((pp[0]-1,pp[1]-1)) if 0<=pp[0]-1<=7 and 0<=pp[1]-1<=7 and (not (pp[0]-1,pp[1]-1) in case_protégé) else None
                        elif z.type=="N":
                            déplacement=[(2,1),(1,2),(-1,2),(-2,1),(-2,-1),(-1,-2),(1,-2),(2,-1)]
                            for i in déplacement:
                                if 0<=pp[0]+i[0]<=7 and 0<=pp[1]+i[1]<=7 and (not (pp[0]+i[0],pp[1]+i[1]) in case_protégé):
                                    case_protégé.append((pp[0]+i[0],pp[1]+i[1]))
                        elif z.type=="B":
                            déplacement=[(1,1),(1,-1),(-1,-1),(-1,1)]
                            coordonné_temp=[pp[0],pp[1]]
                            for i in déplacement:
                                coordonné_temp=[pp[0],pp[1]]
                                while coordonné_temp[0]+i[0] in range(8) and coordonné_temp[1]+i[1] in range(8):
                                    if plateau_initial[coordonné_temp[0]+i[0]][coordonné_temp[1]+i[1]]=="." and (not (coordonné_temp[0]+i[0],coordonné_temp[1]+i[1]) in case_protégé):
                                        case_protégé.append((coordonné_temp[0]+i[0],coordonné_temp[1]+i[1]))
                                        coordonné_temp[0]+=i[0]
                                        coordonné_temp[1]+=i[1]
                                    elif not plateau_initial[coordonné_temp[0]+i[0]][coordonné_temp[1]+i[1]]=="." and plateau_initial[coordonné_temp[0]+i[0]][coordonné_temp[1]+i[1]].Blanc != self.Blanc and (not (coordonné_temp[0]+i[0],coordonné_temp[1]+i[1]) in case_protégé):
                                        case_protégé.append((coordonné_temp[0]+i[0],coordonné_temp[1]+i[1]))
                                        break
                                    else:
                                        break
                        elif z.type=="R":
                            déplacement=[(1,0),(0,-1),(-1,0),(0,1)]
                            coordonné_temp=[pp[0],pp[1]]
                            for j in déplacement:
                                coordonné_temp=[pp[0],pp[1]]
                                while coordonné_temp[0]+j[0] in range(8) and coordonné_temp[1]+j[1] in range(8):
                                    if plateau_initial[coordonné_temp[0]+j[0]][coordonné_temp[1]+j[1]]=="." and (not (coordonné_temp[0]+j[0],coordonné_temp[1]+j[1]) in case_protégé):
                                        case_protégé.append((coordonné_temp[0]+j[0],coordonné_temp[1]+j[1]))
                                        coordonné_temp[0]+=j[0]
                                        coordonné_temp[1]+=j[1]
                                    elif not plateau_initial[coordonné_temp[0]+j[0]][coordonné_temp[1]+j[1]]=="." and plateau_initial[coordonné_temp[0]+j[0]][coordonné_temp[1]+j[1]].Blanc != self.Blanc and (not (coordonné_temp[0]+j[0],coordonné_temp[1]+j[1]) in case_protégé):
                                        case_protégé.append((coordonné_temp[0]+j[0],coordonné_temp[1]+j[1]))
                                        break
                                    else:
                                        break
                        elif z.type=="Q":
                            déplacement=[(1,0),(0,-1),(-1,0),(0,1),(1,1),(1,-1),(-1,-1),(-1,1)]
                            coordonné_temp=[pp[0],pp[1]]
                            for i in déplacement:
                                coordonné_temp=[pp[0],pp[1]]
                                while coordonné_temp[0]+i[0] in range(8) and coordonné_temp[1]+i[1] in range(8):
                                    if plateau_initial[coordonné_temp[0]+i[0]][coordonné_temp[1]+i[1]]=="." and (not (coordonné_temp[0]+i[0],coordonné_temp[1]+i[1]) in case_protégé):
                                        case_protégé.append((coordonné_temp[0]+i[0],coordonné_temp[1]+i[1]))
                                        coordonné_temp[0]+=i[0]
                                        coordonné_temp[1]+=i[1]
                                    elif not plateau_initial[coordonné_temp[0]+i[0]][coordonné_temp[1]+i[1]]=="." and plateau_initial[coordonné_temp[0]+i[0]][coordonné_temp[1]+i[1]].Blanc != self.Blanc and (not (coordonné_temp[0]+i[0],coordonné_temp[1]+i[1]) in case_protégé):
                                        case_protégé.append((coordonné_temp[0]+i[0],coordonné_temp[1]+i[1]))
                                        break
                                    else:
                                        break
                        elif z.type=="K":
                            déplacement=[(1,0),(0,-1),(-1,0),(0,1),(1,1),(1,-1),(-1,-1),(-1,1)]
                            for i in déplacement:
                                if 0<=pp[0]+i[0]<=7 and 0<=pp[1]+i[1]<=7 and (not (pp[0]+i[0],pp[1]+i[1]) in case_protégé):
                                    case_protégé.append((pp[0]+i[0],pp[1]+i[1]))            
            #déplacement
            for i in ddddéplacement:
                coordonné_temp=(p[0]+i[0],p[1]+i[1])
                if not coordonné_temp in case_protégé and 0<=coordonné_temp[0]<=7 and 0<=coordonné_temp[1]<=7:
                    if Chess_board[coordonné_temp[0]][coordonné_temp[1]]==".":    
                        liste_coup_possible.append("K"+transfo_coup_positionliste((p))+transfo_coup_positionliste((coordonné_temp)))
                    elif Chess_board[coordonné_temp[0]][coordonné_temp[1]].Blanc != self.Blanc:
                        liste_coup_possible.append("K"+transfo_coup_positionliste((p))+"x"+transfo_coup_positionliste((coordonné_temp)))
            #roque
            # Le roque n'est possible que si le roi n'est pas actuellement en échec
            if not est_en_echec(plateau_initial, self.Blanc):
                if self.Blanc:
                    if not self.has_moved and Chess_board[0][7]!="." and Chess_board[0][7].has_moved==False and Chess_board[0][5]=="." and Chess_board[0][6]=="." and not (0,5) in case_protégé and not (0,6) in case_protégé and not (0,4) in case_protégé:
                        liste_coup_possible.append("O-O")
                    if not self.has_moved and Chess_board[0][0]!="." and Chess_board[0][0].has_moved==False and Chess_board[0][1]=="." and Chess_board[0][2]=="." and Chess_board[0][3]=="." and not (0,1) in case_protégé and not (0,2) in case_protégé and not (0,3) in case_protégé and not (0,4) in case_protégé:
                        liste_coup_possible.append("O-O-O")
                elif self.Blanc==False:
                    if not self.has_moved and Chess_board[7][7]!="." and Chess_board[7][7].has_moved==False and Chess_board[7][5]=="." and Chess_board[7][6]=="." and not (7,5) in case_protégé and not (7,6) in case_protégé and not (7,4) in case_protégé:
                        liste_coup_possible.append("O-O")
                    if not self.has_moved and Chess_board[7][0]!="." and Chess_board[7][0].has_moved==False and Chess_board[7][1]=="." and Chess_board[7][2]=="." and Chess_board[7][3]=="." and not (7,1) in case_protégé and not (7,2) in case_protégé and not (7,3) in case_protégé and not (7,4) in case_protégé:
                        liste_coup_possible.append("O-O-O")
                  
        #si en échec, vérif si le coup enlève échec
        for i in range(len(liste_coup_possible)-1,-1,-1):
            plateau_temp=nouveau_plateau(plateau_initial)
            plateau_temp=jouer_le_coup(liste_coup_possible[i],self.Blanc,plateau_temp)
            if est_en_echec(plateau_temp,self.Blanc):
                liste_coup_possible.pop(i)
        

        #regarde si le coup met en échec l'adversaire
        if not coup_interne:
            for i in liste_coup_possible:
                plateau_temp=nouveau_plateau(plateau_initial)
                plateau_temp=jouer_le_coup(i,self.Blanc,plateau_temp)
                if est_en_echec(plateau_temp,not self.Blanc):
                    if est_echec_et_mat(plateau_temp,not self.Blanc):
                        liste_coup_possible[liste_coup_possible.index(i)]=i+"#"
                    else:
                        liste_coup_possible[liste_coup_possible.index(i)]=i+"+"
                elif listage_coup_possible(plateau_temp,not self.Blanc,True)==[]:
                    liste_coup_possible[liste_coup_possible.index(i)]=i+"*" 
                del plateau_temp
        return liste_coup_possible

def listage_coup_possible(plateau_initial,Couleur_Blanc,coup_interne):
    liste_coup_possible_total=[]
    for i in plateau_initial:
        for j in i:
            if not j=="." and j.Blanc==Couleur_Blanc:
                liste_coup_possible_total+=j.possible_moves(plateau_initial,coup_interne)

    # All this to see if there is a move that contains a draw
    index = 0
    for move in liste_coup_possible_total: # for every move it will see what it does on the board and see if it will be the third time the same board appeared
        _temp_board = nouveau_plateau(plateau_initial)
        jouer_le_coup(move, Couleur_Blanc, _temp_board)

        if previous_boards.count(Funcs_for_GUI.bitify(_temp_board)) >= 2: # If the same board has already appeared twice in the history of boards
            liste_coup_possible_total[index] = move + '*' # Adding the * draw sign

        del _temp_board
        index += 1

    return liste_coup_possible_total

# Pièces blanches
RB1 = pièce(True, "R", "a1", False)
NB1 = pièce(True, "N", "b1", False)
BB1 = pièce(True, "B", "c1", False) 
DB = pièce(True, "Q", "d1", False)  
KB = pièce(True, "K", "e1", False)   
BB2 = pièce(True, "B", "f1", False)  
NB2 = pièce(True, "N", "g1", False)  
RB2 = pièce(True, "R", "h1", False)  

# Pions blancs
PB1 = pièce(True, "P", "a2", False)
PB2 = pièce(True, "P", "b2", False)
PB3 = pièce(True, "P", "c2", False)
PB4 = pièce(True, "P", "d2", False)
PB5 = pièce(True, "P", "e2", False)
PB6 = pièce(True, "P", "f2", False)
PB7 = pièce(True, "P", "g2", False)
PB8 = pièce(True, "P", "h2", False)

# Pions noirs
PN1 = pièce(False, "P", "a7", False)
PN2 = pièce(False, "P", "b7", False)
PN3 = pièce(False, "P", "c7", False)
PN4 = pièce(False, "P", "d7", False)
PN5 = pièce(False, "P", "e7", False)
PN6 = pièce(False, "P", "f7", False)
PN7 = pièce(False, "P", "g7", False)
PN8 = pièce(False, "P", "h7", False)

# Pièces noires (False = Noir)
RN1 = pièce(False, "R", "a8", False) 
NN1 = pièce(False, "N", "b8", False) 
BN1 = pièce(False, "B", "c8", False)  
DN = pièce(False, "Q", "d8", False)  
KN = pièce(False, "K", "e8", False)   
BN2 = pièce(False, "B", "f8", False)  
NN2 = pièce(False, "N", "g8", False)  
RN2 = pièce(False, "R", "h8", False)  

n = [
    [RB1, NB1, BB1, DB, KB, BB2, NB2, RB2],  
    [PB1, PB2, PB3, PB4, PB5, PB6, PB7, PB8], 
    [".", ".", ".", ".", ".", ".", ".", "."],   
    [".", ".", ".", ".", ".", ".", ".", "."],  
    [".", ".", ".", ".", ".", ".", ".", "."],    
    [".", ".", ".", ".", ".", ".", ".", "."],    
    [PN1, PN2, PN3, PN4, PN5, PN6, PN7, PN8],  
    [RN1, NN1, BN1, DN, KN, BN2, NN2, RN2]]

b=nouveau_plateau(n)


def plaetau_départ():
    return b

def creer_plateau_mat_en_2():
    #full ia
    """
    Crée une position où les blancs peuvent mater en 2 coups.
    Position:
    - Roi blanc en g1, Dame en d1, Tour en h1
    - Roi noir en g8, Pions en f7, g7, h7
    La solution est 1. Qh5 g6 2. Qxg6#
    """
    # Créer un plateau vide
    plateau = [[ "." for _ in range(8)] for _ in range(8)]

    # Définir les pièces nécessaires
    # Pièces blanches
    KB = pièce(True, "K", "g1", True)
    DQ = pièce(True, "Q", "d1", True)
    RH = pièce(True, "R", "h1", True)

    # Pièces noires
    KN = pièce(False, "K", "g8", True)
    PN_f = pièce(False, "P", "f7", True)
    PN_g = pièce(False, "P", "g7", True)
    PN_h = pièce(False, "P", "h7", True)

    # Placer les pièces sur le plateau (ligne, colonne)
    # Blancs
    plateau[0][6] = KB  # g1
    plateau[0][3] = DQ  # d1
    plateau[0][7] = RH  # h1

    # Noirs
    plateau[7][6] = KN  # g8
    plateau[6][5] = PN_f # f7
    plateau[6][6] = PN_g # g7
    plateau[6][7] = PN_h # h7
    
    return plateau

previous_boards = []


def Test_sur_plateau():
        liste_coup_possible=listage_coup_possible(n,True,False)
        for i in liste_coup_possible:
            print(i)

if __name__ == "__main__":   
    print("Tests sur le plateau initial :")
    Test_sur_plateau()
    print(creer_plateau_mat_en_2())