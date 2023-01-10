import random
from classes import Giocatore, Mazzo, Carta, si_o_no

class GiocatoreBriscola(Giocatore):
    def __init__(self, nome) -> None:
        super().__init__(nome)
        self.punti = 0
        self.dict_punti = {1: 11, 3: 10, 10: 4, 9: 3, 8: 2}
        self.carte_vinte = []

    def aggiungi_carte_vinte(self, carte_vinte: list or dict):
        assert len(set(carte_vinte)) == len(carte_vinte), "Una carta tra quelle vinte si ripete"
        
        self.carte_vinte += [carta for carta in carte_vinte]

    def conta_punti(self):
        punti_totali = 0
        for carta in self.carte_vinte:
            try:
                punti_totali += self.dict_punti[int(carta.key[1:])]
            except:
                pass
        return punti_totali

class Briscola():
    def __init__(self) -> None:
        self.mazzo = Mazzo()
        self.dict_punti = {1: 11, 3: 10, 10: 4, 9: 3, 8: 2}

        self.init_giocatori()
        while input("Volete iniziare? (s/n) ").lower()[0] != 's':
            pass
        self.init_distribuisci_carte()
        self.pesca_briscola()
        self.chi_inizia()

        # while len(self.mazzo.carte) > 35:
        self.turno()

    def init_giocatori(self):
        self.giocatori = {}
        self.numero_giocatori = int(input("In quanti volete giocare?"))
        self.contro_AI = False

        assert isinstance(self.numero_giocatori, int), "Non ho mai sentito mezze persone giocare a briscola. Metti un numero intero pls."

        if self.numero_giocatori == 1:
            self.contro_AI = si_o_no(
                "Sei da solo: vuoi giocare contro l'AI? (s/n) ", 
                "Ottimo, allora in bocca al lupo!", 
                "Allora nada. Ricomincia il gioco se ti va.")
            
            print("Initializing AI...")
            self.giocatori["Giocatore"] = GiocatoreBriscola(nome="Giocatore")
            self.giocatori["AI"] = GiocatoreBriscola(nome='AI')

            return None

        elif self.numero_giocatori == 3:
            coppe_2 = self.mazzo.togli_carta(Carta("Coppe", 2))
            print(f"Dato che siete in 3 tolgo il 2 di Coppe, che e' la piu' inutile")

        elif self.numero_giocatori in [2,4]:
            print(f"Ottimo, siete {self.numero_giocatori} giocatori")
            
        elif self.numero_giocatori == 5:
            print("Mi dispiace ma non si puo' giocare per il momento a Briscola chiamata")
        
        elif self.numero_giocatori > 5:
            print("Il numero massimo di giocatori e' 4")      

        else:
            raise ValueError("Non so come interpretare questo valore. Inserisci un numero intero tra 1 e 4.")    

        print("Ora inserite i vostri nomi")
        for i, giocatore in enumerate(range(self.numero_giocatori), start=1):
            nome = input(f"Giocatore {i}: ")
            self.giocatori[nome] = GiocatoreBriscola(nome=nome)

        print(f"Benvenuti: {[nome for nome in self.giocatori.keys()]}")

    def init_distribuisci_carte(self):
        for i in range(3):
            for giocatore in self.giocatori.keys():
                self.giocatori[giocatore].pesca_carta(self.mazzo)

    def pesca_briscola(self):
        self.carta_fondo = self.mazzo.pesca_carta()
        self.seme_briscola = self.carta_fondo.seme
        print(f"La carta sul fondo e' un {self.carta_fondo}")
        print(f"Il seme di briscola quindi e' {self.seme_briscola}")

    def check_ultimo_turno(self):
        if len(self.mazzo.carte) == self.numero_giocatori:
            print("Attenzione giocatori, questo e' l'ultimo giro!")

    def turno(self):
        ordine_giocatori = self.set_ordine_giocatori()
        [print(self.giocatori[giocatore].nome, self.giocatori[giocatore].carte_in_mano) 
               for giocatore in ordine_giocatori]
        carte_giocate = {}
        for i, giocatore in enumerate(ordine_giocatori):
            opzioni = list(range(len(self.giocatori[giocatore].carte_in_mano)))
            carta_id = int(input(f"{self.giocatori[giocatore]}: scegli una delle tue carte (opzioni: {opzioni})"))
            carte_giocate[i] = self.giocatori[giocatore].usa_carta(carta_id)
            print(carte_giocate[i])

    def chi_inizia(self):
        giocatori = list(self.giocatori.keys())
        random.shuffle(giocatori)
        self.giocatore_iniziale = giocatori[0]
        print(f"Inizia {self.giocatore_iniziale}!")

    def set_ordine_giocatori(self):
        list_giocatori = list(self.giocatori.keys())
        for id_inizio, nome in enumerate(list_giocatori):
            if nome == self.giocatore_iniziale:
                break
        ordine_giocatori = list_giocatori[id_inizio:] + list_giocatori[:id_inizio]
        return ordine_giocatori

    def __repr__(self) -> str:
        return f"Gioco di Briscola con {self.numero_giocatori} giocatori"


if __name__ == '__main__':
    briscola = Briscola()
    [print(giocatore.nome, giocatore.carte_in_mano) for giocatore in briscola.giocatori.values()]