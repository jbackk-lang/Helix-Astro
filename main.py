from pole import Pole
from generator import generuj_foton
from timdr import TIMDR

def main():
    pole = Pole(skret=10.0)
    foton = generuj_foton(pole)

    print("=== GENERATOR FOTONÓW ===")
    if foton is None:
        print("Brak emisji — skręt pola nie jest dodatni.")
        return
    print("Energia:", foton.energia)
    print("Częstotliwość:", foton.czestotliwosc)

    timdr = TIMDR()
    wynik = timdr.filtr((0, foton.energia))
    print("TIMDR:", wynik)

if __name__ == "__main__":
    main()
