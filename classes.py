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

def si_o_no(frase, si_frase, no_frase):
    risposta = input(frase)
    if risposta.lower()[0] == 's':
        risposta = True
        print(si_frase)
    elif risposta.lower()[0] == 'n':
        risposta = False
        print(no_frase)
    else:
        raise ValueError("Accetto solo si o no come risposte.")

    return risposta