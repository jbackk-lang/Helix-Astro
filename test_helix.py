"""
test_helix.py — prosty program testowy do Thonny.
Sprawdza czy Helix-Astro (helix_spectrum.py) dziala poprawnie.

WYMAGANIA:
- plik helix_spectrum.py musi lezec w TYM SAMYM folderze co ten skrypt
- w Thonny: Narzedzia -> Zarzadzaj pakietami -> doinstaluj "numpy" i "matplotlib",
  jesli nie sa jeszcze zainstalowane

URUCHOMIENIE: otworz ten plik w Thonny i nacisnij F5 (Uruchom).
"""

import numpy as np

try:
    from helix_spectrum import T0, T1, T2, compute_metrics, analyze
except ImportError:
    print("BLAD: nie znaleziono helix_spectrum.py w tym samym folderze co ten skrypt.")
    print("Wrzuc helix_spectrum.py z repo Helix-Astro obok tego pliku i uruchom ponownie.")
    raise SystemExit(1)


def test_plaski_sygnal():
    """Sygnal staly (bez zadnej zmiennosci) -> wszystkie metryki powinny wyjsc ~0.
    To dokladnie ten przypadek, ktory wczesniej lapal sie na dzieleniu przez zero
    (T1 dzielilo przez zakres=0) i dawal NaN zamiast 0 -- test pilnuje, zeby ta
    poprawka dalej dzialala."""
    sygnal = np.ones(50) * 7.0
    t0 = T0(sygnal)
    t1 = T1(sygnal)
    t2 = T2(t1)
    metryki = compute_metrics(t0, t2)
    print("Test 1 (sygnal staly):", metryki)
    assert metryki["entropia"] < 0.01, "entropia powinna byc ~0 dla stalego sygnalu"
    assert metryki["rezonans"] < 0.01, "rezonans powinien byc ~0 dla stalego sygnalu"
    print("  -> OK\n")


def test_szum():
    """Losowy szum -> entropia i rezonans powinny byc WYRAZNIE wyzsze niz dla
    stalego sygnalu, bo szum ma duzo strukturalnej zmiennosci."""
    rng = np.random.default_rng(42)
    szum = rng.normal(10, 3, 200)
    t0 = T0(szum)
    t1 = T1(szum)
    t2 = T2(t1)
    metryki = compute_metrics(t0, t2)
    print("Test 2 (losowy szum):", metryki)
    assert metryki["entropia"] > 1.0, "szum powinien miec wysoka entropie"
    assert metryki["rezonans"] > 0, "szum powinien miec niezerowy rezonans"
    print("  -> OK\n")


def test_schodek():
    """Sygnal-skok (polowa zer, polowa jedynek) -> T2 (pochodna) powinno miec
    wyrazny pik dokladnie w miejscu skoku. To sprawdza, czy 'rezonans przejscia'
    faktycznie wykrywa GDZIE zachodzi zmiana, a nie tylko ze ona jest."""
    sygnal = np.concatenate([np.zeros(50), np.ones(50)])
    t0 = T0(sygnal)
    t1 = T1(sygnal)
    t2 = T2(t1)
    metryki = compute_metrics(t0, t2)
    print("Test 3 (sygnal-skok):", metryki)
    pik_pozycja = int(np.argmax(np.abs(t2)))
    print(f"  Najsilniejsza zmiana (pik T2) w indeksie {pik_pozycja} (oczekiwano w okolicy 50)")
    assert 45 <= pik_pozycja <= 55, "pik rezonansu powinien byc w miejscu skoku sygnalu"
    print("  -> OK\n")


def test_na_prawdziwych_danych():
    """Uruchamia pelny analyze() na przykladowym pliku examples/spectrum.csv,
    jesli jest dostepny obok tego skryptu -- zapisuje wykres do pliku zamiast
    otwierac okienko, zeby dzialalo tez bez wyswietlacza."""
    import os
    sciezka = os.path.join("examples", "spectrum.csv")
    if not os.path.exists(sciezka):
        print(f"Test 4 pominiety -- nie znaleziono {sciezka} w tym folderze")
        return
    metryki = analyze(sciezka, save_path="wynik_test.png")
    print("Test 4 (examples/spectrum.csv):", metryki)
    print("  -> Wykres zapisany jako wynik_test.png w folderze skryptu")


if __name__ == "__main__":
    print("=== Test Helix-Astro ===\n")
    test_plaski_sygnal()
    test_szum()
    test_schodek()
    test_na_prawdziwych_danych()
    print("\nWszystkie testy zaliczone -- Helix-Astro dziala poprawnie.")
