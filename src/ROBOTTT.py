from Chess_fct import jouer_le_coup, listage_coup_possible, pièce, nouveau_plateau, est_en_echec, plaetau_départ, creer_plateau_mat_en_2, previous_boards
import Funcs_for_GUI
from time import time, sleep
import copy
from multiprocessing import Process, Manager, freeze_support
import os

# Full ia
def copie_plateau_rapide(plateau):
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

CENTRE = ["e4", "d4", "e5", "d5"]
EXTENDED_CENTRE = ["c3","c4","c5","c6", "d3", "d6", "e3", "e6", "f3","f4","f5","f6"]
BISHOP_DIAGS = ["b7","b2","g7","g2"]
CASTLED_WHITE = ["g1","c1"]
CASTLED_BLACK = ["g8","c8"]
PAWN_PROMOTION_MAP_W = [-2, -1.5, 0.5, 1, 2, 4, 10]
PAWN_PROMOTION_MAP_B = PAWN_PROMOTION_MAP_W[::-1]
nbPieces = 32

threads = [] # Used by multiprocessing

def evaluation_statique(plateau):
    #temporaire
    score=0
    global nbPieces
    nbPieces = sum(1 for ligne in plateau for case in ligne if case != ".")
    for ligne in plateau:
        for case in ligne:
            if case!=".":
                if case.Blanc:
                    if case.type=="P": 
                        if case.position in CENTRE:
                            score+=1.2
                        elif case.position in EXTENDED_CENTRE:
                            score+=1.1

                        if nbPieces < 20:
                            score += PAWN_PROMOTION_MAP_W[int(case.position[1]) - 1]*((32-nbPieces)/16)
                        else:
                            if case.position[1] in ["1", "2"]:
                                score += 1.1

                    elif case.type=="R":
                        if case.position[0] in ["a", "b", "g", "h"] and case.position[1] == "1" and len(previous_boards) < 10: #To get the rooks to move at the beginning
                            score -= 1
                        if case.position in EXTENDED_CENTRE:
                            score += 0.1
                        score+=5
                    elif case.type=="Q":
                        if case.position in EXTENDED_CENTRE:
                            score+=9.1
                        else:
                            score+=9
                    elif case.type=="B":
                        if case.position in BISHOP_DIAGS:
                            score+=3.2
                        else:
                            score+=3
                    elif case.type=="N":
                        if case.position in EXTENDED_CENTRE:
                            score+=3.2
                        else:
                            score+=3
                    elif case.type=="K":
                        if case.position in CASTLED_WHITE:
                            score+=101
                        else:    
                            score+=100

                        if case.position[1] in ["3", "4", "5", "6"]: # Pour qu'il ne s'aventure pas trop loin
                            score -= ((nbPieces)/16)
                else:
                    if case.type=="P":
                        if case.position in CENTRE: 
                            score-=1.2
                        elif case.position in EXTENDED_CENTRE:
                            score-=1.1
                        
                        if nbPieces < 20:
                            score -= PAWN_PROMOTION_MAP_B[int(case.position[1]) - 1]*((32-nbPieces)/16)
                        else:
                            if case.position[1] in ["7", "8"]:
                                score -= 1.1

                    elif case.type=="R":
                        if case.position[0] in ["a", "b", "g", "h"] and case.position[1] == "8" and len(previous_boards) < 10: #To get the rooks to move at the beginning
                            score += 1
                        if case.position in EXTENDED_CENTRE:
                            score -= 0.1
                        score-=5
                    elif case.type=="Q":
                        if case.position in CENTRE:
                            score-=9.1
                        else:
                            score-=9
                    elif case.type=="B":
                        if case.position in BISHOP_DIAGS:
                            score-=3.1
                        else:
                            score-=3
                    elif case.type=="N":
                        if case.position in EXTENDED_CENTRE:
                            score-=3.2
                        else:
                            score-=3
                    elif case.type=="K":
                        if case.position in CASTLED_BLACK:
                            score-=101
                        else:
                            score-=100

                        if case.position[1] in ["3", "4", "5", "6"]: # Pour qu'il ne s'aventure pas trop loin
                            score += ((nbPieces)/16)

    return score

# Full ia (tri d'abord les captures puis le reste)
def trier_coups(coups):
    captures = [c for c in coups if "x" in c or "#" in c or "=" in c or c[-1]=="+"]
    autres = [c for c in coups if c not in captures]
    return captures + autres


def minimax_alphabeta(plateau, profondeur, alpha, beta, Blanc):  
    if profondeur==0:
        return evaluation_statique(plateau)
    if Blanc:
        Score_max=-1000
        couppossible=listage_coup_possible(plateau,True,True)
        if not couppossible:
            return -10000
        couppossible = trier_coups(couppossible)

        for coup in couppossible:
            if "#" in coup:
                return 10000
            if "*" in coup:
                return 0
            #plateau_temp=nouveau_plateau(plateau)
            plateau_temp=copie_plateau_rapide(plateau)
            plateau_temp=jouer_le_coup(coup, Blanc, plateau_temp)
            score_obtenu=minimax_alphabeta(plateau_temp, profondeur-1, alpha, beta, False)
            Score_max=max(Score_max, score_obtenu)
            alpha=max(alpha, Score_max)
            if beta<=alpha:
                break
        return Score_max
    elif not Blanc:
        Score_min=1000
        couppossible=listage_coup_possible(plateau,False,True)
        if not couppossible:
            return 10000
        couppossible = trier_coups(couppossible)
        for coup in couppossible:
            if "#" in coup:
                return -10000
            if "*" in coup:
                return 0
            #plateau_temp=nouveau_plateau(plateau)
            plateau_temp=copie_plateau_rapide(plateau)
            plateau_temp=jouer_le_coup(coup, False, plateau_temp)
            score_obtenu=minimax_alphabeta(plateau_temp, profondeur-1, alpha, beta, True)
            Score_min=min(Score_min, score_obtenu)
            beta=min(beta, Score_min)
            if beta<=alpha:
                break
        return Score_min
    return 0


# Fonction globale pour multiprocessing (doit être en dehors de gestion_minimax pour Windows)
def _sub_call_minimax(coup, data, plateau, profondeur, Blanc):
    plateau_temp = copie_plateau_rapide(plateau)
    plateau_temp = jouer_le_coup(coup, Blanc, plateau_temp)
    score_obtenu = minimax_alphabeta(plateau_temp, profondeur-1, -1000, 1000, not Blanc)

    if Blanc and score_obtenu > data[0]:
        data[0] = score_obtenu
        data[1] = coup
    elif not Blanc and -score_obtenu > data[0]:
        data[0] = -score_obtenu
        data[1] = coup


def gestion_minimax(plateau, profondeur, Blanc, max_time_s):
    """
    This function will separate each move into different threads, so that several minimax algorithms can run simultaneously.

    The usual Process function from multiprocessing doesn't allow shared memory, however this is what we need for the `meilleur_score` and `meilleur_coup` variables. This is why I found that multiprocessing has a function called Manager() that lets you share a variable or list with the processes
    """
    global threads
    
    start_time = time() # Time at beginning

    meilleur_score_et_coup = Manager().list([-10000, None])
    """
    Above, creating shared memory between processes
    meilleur_score_et_coup[0] -> score
            ""            [1] -> coup
    """


    couppossible=listage_coup_possible(plateau,Blanc,False)
    couppossible = trier_coups(couppossible)

    for coup in couppossible:
        if coup[-1] == '#':
            return coup
      
    for move in couppossible:
        p = Process(target=_sub_call_minimax, args=(move, meilleur_score_et_coup, plateau, profondeur, Blanc))
        threads.append(p)
        p.start()

    # --------- May be commented for optimal performance ------------
    try: # Little try, except to avoid processes that last too long
        while time()-start_time < max_time_s:
            sleep(0.05) #So it doesn't check indefinitely
            _finished_work = True
            for thread in threads:
                if thread.is_alive(): # If all threads are dead, it will break out of the loop
                    _finished_work = False
            else:
                if _finished_work == True:
                    break

            if time()-start_time > max_time_s:
                raise Exception(f"Timeout: {time()-start_time} > {max_time_s} s")
    except Exception as err:
        print(err)
        for thread in threads:
            thread.kill()
    # -------------------------***-------------------------------

    for thread in threads:
        thread.join()
    
    threads = [] # Re-initialize threads list

    try: # There are sometimes errors with Manager() when closing app
        return meilleur_score_et_coup[1] if meilleur_score_et_coup[1] != None else couppossible[0] #meilleur_coup
    except:
        return None

def possible_ouverture_moves(Blanc, historique, seed=0):
    if Blanc:
        if len(historique)==0:
            coups=["e4", "d4", "Ng1f3", "g3"]
            return coups[seed%len(coups)]
        elif len(historique)==2:
        # Après e4 (full ia)
            if historique==["e4", "e5"]:
                coups=["Ng1f3", "Nb1c3", "Bf1c4", "d4"]
                return coups[seed%len(coups)]
            elif historique==["e4", "c5"]:
                coups=["Ng1f3", "Nb1c3", "d4", "c3"]
                return coups[seed%len(coups)]
            elif historique==["e4", "e6"]:
                coups=["d4", "Ng1f3", "Nb1c3", "Bf1d3"]
                return coups[seed%len(coups)]
            elif historique==["e4", "g6"]:
                coups=["d4", "Ng1f3", "Bf1c4", "Nb1c3"]
                return coups[seed%len(coups)]
            
            # Après d4
            elif historique==["d4", "d5"]:
                coups=["c4", "Nb1c3", "Ng1f3", "Bc1f4"]
                return coups[seed%len(coups)]
            elif historique==["d4", "Ng8f6"]:
                coups=["c4", "Nb1c3", "Ng1f3", "Bc1g5"]
                return coups[seed%len(coups)]
            elif historique==["d4", "e6"]:
                coups=["c4", "Ng1f3", "Nb1c3", "e4"]
                return coups[seed%len(coups)]
            elif historique==["d4", "g6"]:
                coups=["c4", "Nb1c3", "Ng1f3", "e4"]
                return coups[seed%len(coups)]
            
            # Après Ng1f3
            elif historique==["Ng1f3", "d5"]:
                coups=["d4", "c4", "g3", "e3"]
                return coups[seed%len(coups)]
            elif historique==["Ng1f3", "Ng8f6"]:
                coups=["c4", "g3", "d4", "b3"]
                return coups[seed%len(coups)]
            elif historique==["Ng1f3", "g6"]:
                coups=["d4", "g3", "c4", "e4"]
                return coups[seed%len(coups)]
            elif historique==["Ng1f3", "e6"]:
                coups=["d4", "c4", "g3", "e3"]
                return coups[seed%len(coups)]
            
            # Après g6
            elif historique==["g6", "d5"]:
                coups=["Bf1g2", "d4", "Ng1f3", "c4"]
                return coups[seed%len(coups)]
            elif historique==["g6", "e5"]:
                coups=["Bf1g2", "d4", "Ng1f3", "c4"]
                return coups[seed%len(coups)]
            elif historique==["g6", "Ng8f6"]:
                coups=["Bf1g2", "Ng1f3", "d4", "c4"]
                return coups[seed%len(coups)]
            elif historique==["g6", "e6"]:
                coups=["Bf1g2", "d4", "Ng1f3", "c4"]
                return coups[seed%len(coups)]
    else:
        if len(historique)==1:
            if historique[0]=="e4":
                coups=["e5", "c5", "e6"]
                return coups[seed%len(coups)]
            elif historique[0]=="d4":
                coups=["d5", "Ng8f6", "e6"]
                return coups[seed%len(coups)]
            elif historique[0]=="Nf3":
                coups=["d5", "Ng8f6", "g6"]
                return coups[seed%len(coups)]
            elif historique[0]=="c4":
                coups=["e5", "c5", "e6"]
                return coups[seed%len(coups)]
        elif len(historique)==3:
            # Après e4 e5
            if historique==["e4", "e5", "Ng1f3"]:
                coups=["Nb8c6", "Ng8f6", "d6"]
                return coups[seed%len(coups)]
            elif historique==["e4", "e5", "Nb1c3"]:
                coups=["Ng8f6", "Nb8c6", "Bf8c5"]
                return coups[seed%len(coups)]
            elif historique==["e4", "e5", "Bf1c4"]:
                coups=["Ng8f6", "Nb8c6", "Bf8c5"]
                return coups[seed%len(coups)]
            elif historique==["e4", "e5", "d4"]:
                coups=["exd4", "Ng8f6", "d6"]
                return coups[seed%len(coups)]
            
            # Après e4 c5 (Sicilienne)
            elif historique==["e4", "c5", "Ng1f3"]:
                coups=["d6", "Nb8c6", "e6", "g6"]
                return coups[seed%len(coups)]
            elif historique==["e4", "c5", "Nb1c3"]:
                coups=["Nb8c6", "e6", "g6"]
                return coups[seed%len(coups)]
            elif historique==["e4", "c5", "d4"]:
                coups=["cxd4", "Ng8f6", "e6"]
                return coups[seed%len(coups)]
            elif historique==["e4", "c5", "c3"]:
                coups=["Ng8f6", "d5", "e6"]
                return coups[seed%len(coups)]
            
            # Après e4 e6 (Française)
            elif historique==["e4", "e6", "d4"]:
                coups=["d5", "Ng8f6", "c5"]
                return coups[seed%len(coups)]
            elif historique==["e4", "e6", "Ng1f3"]:
                coups=["d5", "c5", "Ng8f6"]
                return coups[seed%len(coups)]
            elif historique==["e4", "e6", "Nb1c3"]:
                coups=["d5", "Bf8b4", "Ng8f6"]
                return coups[seed%len(coups)]
            elif historique==["e4", "e6", "Bf1d3"]:
                coups=["d5", "c5", "Ng8f6"]
                return coups[seed%len(coups)]
            
            # Après e4 g6 (Pirc/Moderne)
            elif historique==["e4", "g6", "d4"]:
                coups=["Bf8g7", "Ng8f6", "d6"]
                return coups[seed%len(coups)]
            elif historique==["e4", "g6", "Ng1f3"]:
                coups=["Bf8g7", "d6", "Ng8f6"]
                return coups[seed%len(coups)]
            elif historique==["e4", "g6", "Bf1c4"]:
                coups=["Bf8g7", "Ng8f6", "d6"]
                return coups[seed%len(coups)]
            elif historique==["e4", "g6", "Nb1c3"]:
                coups=["Bf8g7", "d6", "Ng8f6"]
                return coups[seed%len(coups)]
            
            # Après d4 d5 (Gambit Dame)
            elif historique==["d4", "d5", "c4"]:
                coups=["e6", "Ng8f6", "c6", "dxc4"]
                return coups[seed%len(coups)]
            elif historique==["d4", "d5", "Nb1c3"]:
                coups=["Ng8f6", "e6", "c5"]
                return coups[seed%len(coups)]
            elif historique==["d4", "d5", "Ng1f3"]:
                coups=["Ng8f6", "e6", "Bc8f5"]
                return coups[seed%len(coups)]
            elif historique==["d4", "d5", "Bc1f4"]:
                coups=["Ng8f6", "e6", "c5"]
                return coups[seed%len(coups)]
            
            # Après d4 Nf6 (Indiennes)
            elif historique==["d4", "Ng8f6", "c4"]:
                coups=["e6", "g6", "c5", "d5"]
                return coups[seed%len(coups)]
            elif historique==["d4", "Ng8f6", "Nb1c3"]:
                coups=["d5", "g6", "e6"]
                return coups[seed%len(coups)]
            elif historique==["d4", "Ng8f6", "Ng1f3"]:
                coups=["e6", "g6", "d5"]
                return coups[seed%len(coups)]
            elif historique==["d4", "Ng8f6", "Bc1g5"]:
                coups=["e6", "d5", "Nb8d7"]
                return coups[seed%len(coups)]
            
            # Après d4 e6
            elif historique==["d4", "e6", "c4"]:
                coups=["Ng8f6", "d5", "Bf8b4+"]
                return coups[seed%len(coups)]
            elif historique==["d4", "e6", "Ng1f3"]:
                coups=["Ng8f6", "d5", "c5"]
                return coups[seed%len(coups)]
            elif historique==["d4", "e6", "Nb1c3"]:
                coups=["d5", "Ng8f6", "Bf8b4"]
                return coups[seed%len(coups)]
            elif historique==["d4", "e6", "e4"]:
                coups=["d5", "c5", "Ng8f6"]
                return coups[seed%len(coups)]
            
            # Après d4 g6 (Grünfeld/King's Indian)
            elif historique==["d4", "g6", "c4"]:
                coups=["Bf8g7", "Ng8f6", "d5"]
                return coups[seed%len(coups)]
            elif historique==["d4", "g6", "Nb1c3"]:
                coups=["Bf8g7", "Ng8f6", "d5"]
                return coups[seed%len(coups)]
            elif historique==["d4", "g6", "Ng1f3"]:
                coups=["Bf8g7", "Ng8f6", "d6"]
                return coups[seed%len(coups)]
            elif historique==["d4", "g6", "e4"]:
                coups=["Bf8g7", "d6", "Ng8f6"]
                return coups[seed%len(coups)]
            
            # Après Nf3 d5 (Réti)
            elif historique==["Ng1f3", "d5", "d4"]:
                coups=["Ng8f6", "e6", "Bc8f5"]
                return coups[seed%len(coups)]
            elif historique==["Ng1f3", "d5", "c4"]:
                coups=["e6", "Ng8f6", "d6"]
                return coups[seed%len(coups)]
            elif historique==["Ng1f3", "d5", "g3"]:
                coups=["Ng8f6", "c6", "g6"]
                return coups[seed%len(coups)]
            elif historique==["Ng1f3", "d5", "e3"]:
                coups=["Ng8f6", "e6", "c5"]
                return coups[seed%len(coups)]
            
            # Après Nf3 Nf6 (Symétrique)
            elif historique==["Ng1f3", "Ng8f6", "c4"]:
                coups=["g6", "e6", "c5"]
                return coups[seed%len(coups)]
            elif historique==["Ng1f3", "Ng8f6", "g3"]:
                coups=["g6", "d5", "e6"]
                return coups[seed%len(coups)]
            elif historique==["Ng1f3", "Ng8f6", "d4"]:
                coups=["e6", "g6", "d5"]
                return coups[seed%len(coups)]
            elif historique==["Ng1f3", "Ng8f6", "b3"]:
                coups=["g6", "e6", "d5"]
                return coups[seed%len(coups)]
    return False
    
    

def ROBOT(plateau, Blanc, profondeur_max, temps_max_s=300):
    meilleur_coup=gestion_minimax(plateau, profondeur_max, Blanc, temps_max_s)
    return meilleur_coup, profondeur_max

def trysurplateau():
    print(ROBOT(plaetau_départ(), True, 5))
  
def trysurmaten2():
    print(ROBOT(creer_plateau_mat_en_2(), False, 4))

if __name__ == "__main__":
    trysurmaten2()
    a=time()
    print(ROBOT(plaetau_départ(), True, 1))
    print("temps(1) : ",time()-a)
    a=time()
    print(ROBOT(plaetau_départ(), True, 2))
    print("temps(2) : ",time()-a)
    a=time()
    print(ROBOT(plaetau_départ(), True, 3))
    print("temps(3) : ",time()-a)
    a=time()
    print(ROBOT(plaetau_départ(), True, 4))
    print("temps(4) : ",time()-a)
    a=time()
    print(ROBOT(plaetau_départ(), True, 5))
    print("temps(5) : ",time()-a)
    a=time()
    print(ROBOT(plaetau_départ(), True, 6))
    print("temps(6) : ",time()-a)
    a=time()
    print(ROBOT(plaetau_départ(), True, 7))
    print("temps(7) : ",time()-a)
    a=time()
    print(ROBOT(plaetau_départ(), True, 8))
    print("temps(8) : ",time()-a)


"""
Saved times for different depths at beginning position:
('Nb1c3', 1)
temps(1) :  0.04100608825683594
('Ng1f3', 2)
temps(2) :  0.03616070747375488
('Nb1c3', 3)
temps(3) :  0.042142629623413086
('e4', 4)
temps(4) :  0.09517407417297363
('e4', 5)
temps(5) :  0.18044734001159668
('e4', 6)
temps(6) :  1.7766568660736084
('d4', 7)
temps(7) :  4.655293703079224
('e4', 8)
temps(8) :  44.65061664581299
"""
    

      







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

