# KALKULATOR OPTYCZNY (Z WIZUALIZACJĄ)
# Program powinien umożliwiać analizę prostych układów optycznych w oparciu o prawo załamania światła oraz konstrukcję obrazów w soczewkach cienkich. Program pozwala na ustawienie rodzaju soczewki, jej ogniskowej oraz położenia przedmiotu, a następnie wizualizuje bieg promieni oraz powstający obraz.
# Funkcje programu:
# - Wczytywanie parametrów soczewki (zbieżna/rozbieżna, ogniskowa)
# - Wczytywanie parametrów przedmiotu (wysokość, odległość od soczewki)
# - Obliczanie położenia obrazu oraz powiększenia liniowego
# - Rysowanie schematu optycznego:
# -- oś optyczna,
# -- soczewka,
# -- promienie główne (równoległy, przechodzący przez ognisko, przez środek soczewki)
# - Wyświetlanie położenia i wielkości obrazu
# - (Opcjonalnie) Obsługa układu dwóch soczewek

# FIZYKA I OBLICZENIA

import numpy as np

class Soczewka:
    def __init__(self):
        self.f = 0.0 #ogniskowa soczewki
        self.typ_soczewki = "" #soczewka zbiezna lub rozbiezna
        self.h_przedmiotu = 0.0 #wysokosc przedmiotu
        self.x_przedmiotu = 0.0 #polozenie przedmiotu
        self.dane = False #dane poprawne lub nie

    def ustawienie_soczewki(self,typ,ogniskowa):
        """ Wczytuje parametry soczewki, ustala znak ogniskowej """

        try:
            wartosc_f = float(ogniskowa)

            if wartosc_f == 0:
                print("Ogniskowa nie moze być równa 0.")
                self.dane = False
                return False
            
            wartosc_f = abs(wartosc_f)

            if typ.lower() == "rozbiezna":
                self.f = -wartosc_f
                self.typ_soczewki = "rozbiezna"
            else:
                self.f = wartosc_f
                self.typ_soczewki = "zbiezna"

            self.dane = True
            return True
        
        except ValueError:
            print("Podana ogniskowa nie jest liczbą.")
            self.dane = False
            return False
        
    def ustawienie_przedmiot(self,wysokosc,odleglosc):
        """ Wczytuje parametry przedmiotu. Zamienia odległość przedmiotu od soczewki na ujemną współrzędną x """

        try:
            h = float(wysokosc)
            d = float(odleglosc)

            if d < 0:
                print("Odległość powinna być dodatnia. Zamieniam podaną odległość na liczbę dodatnią.")
                d = abs(d)
            
            self.h_przedmiotu = h
            self.x_przedmiotu = -d

            return True
        
        except ValueError:
            print("Parametry przedmiotu muszą być liczbami.")
            return False
    
    def obliczenia(self):
        """ Oblicza połozenie obrazu, wysokość oraz powiększenie. Zwraca słownik z wynikami lub None, jeśli obraz nie powstaje """

        if not self.dane:
            print("Brak poprawnych danych do wykonania obliczeń.")
            return None
        
        # korzystam z równania soczewki dla x ujemnego: 1/f = 1/y - 1/x, wiec y = x*f/(x+f)

        if abs(self.x_przedmiotu + self.f) < 1e-8: # liczba bliska 0
            print("Przedmiot w ognisku. Obraz powstaje w nieskończoności.")
            return None
        
        x_obrazu = (self.x_przedmiotu * self.f) / (self.x_przedmiotu + self.f)
        powiekszenie = x_obrazu / self.x_przedmiotu
        h_obrazu = self.h_przedmiotu * powiekszenie

        wyniki = {
            "x_obrazu": round(x_obrazu,2),
            "h_obrazu": round(h_obrazu,2),
            "powiekszenie": round(powiekszenie,2),
            "typ_obrazu": "Rzeczywisty" if x_obrazu > 0 else "Pozorny"
        }
        return wyniki
    
    def generuj_promienie(self):
        """ Zwraca listę trzech ściezek promieni, gdzie kazda ściezka to lista punktow (x,y), potrzebnych do narysowania wykresu """

        wyniki = self.obliczenia()

        if wyniki is None:
            return [] # brak obrazu oznacza brak promieni
        
        x_p = self.x_przedmiotu
        h_p = self.h_przedmiotu
        x_o = wyniki["x_obrazu"]
        h_o = wyniki["h_obrazu"]

        promien_rownolegly = [
            (x_p,h_p), # początek promienia (przedmiot)
            (0,h_p), # soczewka
            (x_o,h_o) # koniec promienia (obraz)
        ]

        promien_srodkowy = [
            (x_p,h_p), # początek promienia (przedmiot)
            (0,0), # środek soczewki
            (x_o,h_o) # koniec promienia (obraz)
        ]

        promien_ogniskowy = [
            (x_p,h_p), # początek promienia (przedmiot)
            (0,h_o), # soczewka
            (x_o,h_o) # koniec promienia (obraz)
        ]

        if self.typ_soczewki == "zbiezna":
            promien_ogniskowy = [
                (x_p,h_p), # początek promienia (przedmiot)
                (-self.f,0), # przejście przez przednie ognisko
                (0,h_o), # soczewka
                (x_o,h_o) # koniec promienia (obraz)
            ]

        return [promien_rownolegly,promien_srodkowy,promien_ogniskowy]



if __name__ == "__main__":
    kalkulator_optyczny = Soczewka()

    # Test dla soczewki zbieznej, dla przedmiotu o wysokości 6, o odległości 10 od soczewki
    kalkulator_optyczny.ustawienie_soczewki("zbiezna", 15)
    kalkulator_optyczny.ustawienie_przedmiot(6,10)

    wynik = kalkulator_optyczny.obliczenia()
    print(f"Wyniki: {wynik}")

    promienie = kalkulator_optyczny.generuj_promienie()

    # Wypisanie punktów promieni
    if promienie:
        print(f"Promień równoległy: {promienie[0]}")
        print(f"Promień środkowy: {promienie[1]}")
    else:
        print("Nie wygenerowano promieni.")

