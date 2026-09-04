from foton import Foton

def generuj_foton_z_pola(pole):
    """Generuje foton TYLKO gdy pole istnieje, ma skręt DODATNI i
    energię >0 (README: "tylko skręt dodatni prowadzi do emisji
    fotonu; skręt ujemny to stan ciemny").

    BUGFIX: wcześniej sprawdzano tylko `energia <= 0`, a `energia()`
    liczy `abs(skret)` — więc pole o skręcie UJEMNYM też miało
    energię > 0 i przechodziło ten warunek, emitując foton mimo że
    reguła mówi "ujemny = stan ciemny". Ten bug uderzał głównie w
    `oscylator.py`, który woła tę funkcję bezpośrednio na `pole_A`/
    `pole_B` (z pominięciem `PolaDualne.aktywne_pole()`, jedynego
    miejsca, gdzie znak był sprawdzany) — w efekcie
    `main_oscylator.py` z `skretA=12.0, skretB=-12.0` drukował "FOTON"
    na KAŻDYM z 10 kroków zamiast naprzemiennie. Jawny warunek
    `pole.skret <= 0` poniżej naprawia to bez zmiany reszty logiki."""
    if pole is None:
        return None
    if pole.skret <= 0:
        return None

    energia = pole.energia()
    if energia <= 0:
        return None

    return Foton(energia)
