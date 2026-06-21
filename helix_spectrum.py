import numpy as np
import matplotlib.pyplot as plt
import sys

def load_spectrum(path):
    data = np.loadtxt(path, delimiter=",")
    lam = data[:, 0]
    inten = data[:, 1]
    return lam, inten

def T0(inten):
    return inten

def T1(inten):
    # normalizacja + lekkie wygładzenie
    x = inten - np.min(inten)
    x = x / np.max(x)
    kernel = np.array([0.25, 0.5, 0.25])
    return np.convolve(x, kernel, mode="same")

def T2(inten):
    # pochodna jako „rezonans przejścia”
    return np.gradient(inten)

def analyze(path):
    lam, inten = load_spectrum(path)

    t0 = T0(inten)
    t1 = T1(inten)
    t2 = T2(t1)

    plt.figure(figsize=(10, 6))
    plt.plot(lam, t0, label="T0 – surowe")
    plt.plot(lam, t1, label="T1 – filtr")
    plt.plot(lam, t2, label="T2 – rezonans")
    plt.legend()
    plt.title("Helix‑Astro – analiza widma")
    plt.xlabel("λ")
    plt.ylabel("intensywność / rezonans")
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Użycie: python3 helix_spectrum.py spectrum.csv")
        sys.exit(1)

    analyze(sys.argv[1])
