import random

class Carta():
    def __init__(self, seme, valore) -> None:
        self.figure_valori = {
            'Asso' : 1,
            'Fante' : 8,
            'Cavallo' : 9,
            'Re' : 10}
        self.valori_figure = {valore: figura for figura, valore in self.figure_valori.items()}

        self.seme = seme.capitalize()
        self.valore = self._converti_figura_in_valore(valore)
        self.key = f'{self.seme[0]}{self.valore}'

        self._check_seme()
        self._check_valore()

    def _check_seme(self):
        possible_semi = ['Bastoni', 'Denari', 'Spade', 'Coppe']
        if self.seme not in possible_semi:
            raise ValueError(f"Trovato {self.seme} come seme\n"
                              f"Il seme della carta deve essere per forza tra {possible_semi}")
                              
    def _check_valore(self):
        possible_valori = range(1,11)
        if self.valore not in possible_valori:
            raise ValueError(f"Trovato {self.valore} come valore\n"
                              f"Il valore della carta deve essere per forza tra {[i for i in possible_valori]}")

    def _converti_in_figura(self, valore):
        if valore > 7 or valore == 1:
            return self.valori_figure[valore]
        else:
            return str(valore)

    def _converti_figura_in_valore(self, valore):
        if isinstance(valore, str):
            return self.figure_valori[valore]
        else:
            return valore

    def __repr__(self) -> str:
        return f"{self._converti_in_figura(self.valore)} di {self.seme}"


class Mazzo():
    def __init__(self) -> None:
        semi = ['Bastoni', 'Denari', 'Spade', 'Coppe']
        valori = range(1,11)
                
        self.carte = {f'{seme[0]}{valore}' : Carta(seme, valore) for seme in semi for valore in valori}
        self.shuffle()

    def shuffle(self):
        keys =  list(self.carte.keys())
        random.shuffle(keys)
        self.carte = {key:self.carte[key] for key in keys}

    def togli_carta(self, carta):
        try:
            self.carte.pop(self.convert_carta_to_key(carta))
        except KeyError:
            print(f"{carta} gia' scartata")
    
    def pesca_carta(self):
        return self.carte.pop(list(self.carte.keys())[0])

    def convert_carta_to_key(self, carta):
        return f'{carta.seme[0]}{carta.valore}'

    def __repr__(self) -> str:
        return f"Mazzo con {len(self.carte)} carte"


class Giocatore():
    def __init__(self, nome) -> None:
        self.nome = nome
        self.carte_in_mano = []

    def pesca_carta(self, mazzo):
        self.carte_in_mano.append(mazzo.pesca_carta())

    def usa_carta(self, posizione_carta):
        return self.carte_in_mano.pop(posizione_carta)

    def __repr__(self) -> str:
        return f"{self.nome} ha {len(self.carte_in_mano)} carte in mano"


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
        while input("Volete iniziare? (s/n)").lower()[0] != 's':
            pass
        self.init_distribuisci_carte()
        self.pesca_briscola()
        self.chi_inizia()

    def init_giocatori(self):
        self.giocatori = {}
        self.numero_giocatori = int(input("In quanti volete giocare?"))
        self.contro_AI = False

        assert isinstance(self.numero_giocatori, int), "Non ho mai sentito mezze persone giocare a briscola. Metti un numero intero pls."

        if self.numero_giocatori == 1:
            contro_AI = input("Sei da solo: vuoi giocare contro l'AI? (s/n)")
            if contro_AI.lower()[0] == 's':
                print("Ottimo, allora in bocca al lupo!")
                self.contro_AI = True
            elif contro_AI.lower()[0] == 'n':
                print("Allora nada. Ricomincia il gioco se ti va.")
            else:
                raise ValueError("Accetto solo si o no come risposte.")
            
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
            nome = input(f"Giocatore {i}")
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
        pass

    def chi_inizia(self):
        giocatori = list(self.giocatori.keys())
        random.shuffle(giocatori)
        self.giocatore_iniziale = giocatori[0]
        print(f"Inizia {self.giocatore_iniziale}!")

    def __repr__(self) -> str:
        return f"Gioco di Briscola con {self.numero_giocatori} giocatori"