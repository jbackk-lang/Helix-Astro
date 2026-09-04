from pole import Pole
from foton import Foton

def generuj_foton(pole):
    """Generuje foton TYLKO gdy pole ma skręt DODATNI (README: "tylko
    skręt dodatni prowadzi do emisji fotonu; skręt ujemny to stan
    ciemny"). BUGFIX: wcześniej ta funkcja tworzyła Foton dla
    KAŻDEGO pola, niezależnie od znaku skrętu — `energia_pola()` liczy
    `abs(skret)`, więc reguła znaku nigdzie nie była faktycznie
    sprawdzana (nie było to widać w main.py, bo tam skret=10.0 jest
    zawsze dodatni). Zwraca None zamiast Foton, gdy warunek nie jest
    spełniony — wołający musi to obsłużyć (patrz main.py)."""
    if pole.skret <= 0:
        return None
    energia = pole.energia_pola()
    if energia <= 0:
        return None
    return Foton(energia)
