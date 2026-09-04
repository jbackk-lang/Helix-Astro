## 🔗 Wszystkie modele i repozytoria
Pełna lista projektów znajduje się na stronie:
https://jbackk-lang.github.io
---

# Helix‑Astro  
Analiza widm kosmosu oparta na modelu przejść T₀ / T₁ / T₂.

Helix‑Astro to narzędzie naukowe wykorzystujące ideę „helisy przejść”  
z projektu Helix‑Lock, ale zastosowane do danych astronomicznych:  
widm, sygnałów, krzywych intensywności i innych form danych ciągłych.

---

## 🔭 Cel projektu
- Analiza widm kosmicznych w sposób strukturalny, a nie tylko numeryczny.
- Wykrywanie „rezonansu przejść” — odpowiednika T₁ i T₂ z Helix‑Lock.
- Porównywanie widm z różnych epok, źródeł i instrumentów.
- Tworzenie wspólnego języka dla danych: pliki ↔ widma ↔ sygnały.

---

## 🐛 Poprawki
- **matplotlib naprawdę opcjonalny.** Wcześniej import `matplotlib.pyplot`
  był na sztywno na górze `helix_spectrum.py`, więc bez zainstalowanego
  matplotlib cały skrypt padał na starcie — nawet samo liczenie metryk
  (entropia/zmienność/rezonans), które nic wspólnego z wykresami nie ma.
  Import jest teraz leniwy: `analyze()` liczy i zwraca metryki zawsze,
  wykres/zapis do pliku próbuje zrobić tylko, jeśli matplotlib jest
  dostępny.
- **`index.html` to osobny, dekoracyjny symulator**, nie część silnika
  analizy widm. Panel „telemetrii" (Równowaga Heliosfery, Rezonans
  Skalarny, Epoka Koniunkcji) liczony jest z gołych `sin()`/`cos()` czasu
  animacji — nie z pozycji planet, nie z żadnych danych, i nie ma
  związku z metryką `rezonans` z `helix_spectrum.py`. Oznaczone wprost
  w kodzie i w samej stronie.

## 📦 Zależności
- Python 3.x  
- numpy  
- matplotlib (opcjonalnie, do wykresów — patrz Poprawki wyżej)

---

## 📁 Struktura repozytorium

```
helix_spectrum.py     # silnik analizy widm
examples/             # przykładowe widma
README.md             # dokumentacja
```

---

## 🌀 Model przejść T₀ / T₁ / T₂

### T₀ — widmo surowe  
Dane wejściowe bez zmian.

### T₁ — pierwsze przejście  
Normalizacja + filtracja szumu + wygładzenie.

### T₂ — drugie przejście  
Transformacja strukturalna (pochodna / korelacja / rezonans).

Celem nie jest „upiększenie widma”,  
ale **wyciągnięcie śladu przejść**, tak jak w Helix‑Lock.

---

## 🧪 Przykład użycia

```bash
python3 helix_spectrum.py examples/spectrum.csv
```

Wynik:
- wykres T₀ / T₁ / T₂  
- metryki: entropia, zmienność, rezonans  
- porównanie widm

---

## 🔗 Powiązane projekty

Projekt korzysta z idei helisy z repozytorium:

**TIMDR-Cosmology-Filters**  
[https://github.com/jbackk-lang/TIMDR-Cosmology-Filters](https://github.com/jbackk-lang/TIMDR-Cosmology-Filters)

---

## 📜 Licencja
MIT
