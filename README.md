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

## 📦 Zależności
- Python 3.x  
- numpy  
- matplotlib (opcjonalnie, do wykresów)

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

**Helix‑Lock**  
https://github.com/jbackk-lang/Helix-Lock

---

## 📜 Licencja
MIT
