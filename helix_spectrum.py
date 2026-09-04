import numpy as np
import sys

# BUGFIX: matplotlib byl importowany na sztywno na gorze pliku, mimo ze
# README opisuje go jako opcjonalny ("do wykresow"). Bez zainstalowanego
# matplotlib caly skrypt padal na ImportError juz przy starcie -- nawet
# samo liczenie metryk (T0/T1/T2, entropia/zmiennosc/rezonans), ktore nic
# wspolnego z wykresami nie ma, nie dzialalo. Import jest teraz leniwy:
# probowany dopiero w analyze(), i tylko gdy rzeczywiscie potrzebny jest
# wykres (plt.show()) lub zapis do pliku (plt.savefig()).
try:
    import matplotlib.pyplot as plt
    _HAS_MPL = True
except ImportError:
    _HAS_MPL = False

def load_spectrum(path):
    data = np.loadtxt(path, delimiter=",")
    lam = data[:, 0]
    inten = data[:, 1]
    return lam, inten

def T0(inten):
    return inten

def T1(inten):
    # normalizacja + lekkie wygładzenie
    # NAPRAWIONO: dla sygnału stałego (max == min) oryginał dzielił przez 0
    # -> NaN propagujące dalej do T2 i do metryk (rezonans wychodził nan).
    # Sygnał stały ma z definicji zerową zmienność do znormalizowania,
    # więc zwracamy same zera zamiast dzielić przez 0.
    x = inten - np.min(inten)
    rng = np.max(x)
    if rng == 0:
        x_norm = x
    else:
        x_norm = x / rng
    kernel = np.array([0.25, 0.5, 0.25])
    return np.convolve(x_norm, kernel, mode="same")

def T2(inten):
    # pochodna jako „rezonans przejścia”
    return np.gradient(inten)


# ── Metryki (dopisane — README je obiecywał, ale kod ich nigdy nie liczył) ──
#
# Definicje są jawne i policzalne, żeby nie były tylko ozdobnikiem:
#
# entropia   — entropia Shannona (bity) histogramu T0 (32 biny). Mierzy jak
#              "rozłożone"/złożone jest surowe widmo — płaskie widmo o wielu
#              różnych wartościach ma wysoką entropię, widmo prawie stałe ma
#              entropię bliską zeru.
# zmiennosc  — współczynnik zmienności T0: std(T0) / |mean(T0)|. Względna
#              dyspersja sygnału, niezależna od jednostek/skali.
# rezonans   — RMS (root-mean-square) z T2. T2 to już w oryginalnym kodzie
#              nazwany "rezonans przejścia" (pochodna po filtracji), więc
#              rezonans-jako-metryka to jego łączna "energia" — im większe
#              i częstsze skoki w T2, tym wyższa wartość.

def _entropy(inten, bins=32):
    """Entropia Shannona (w bitach) histogramu wartości inten."""
    hist, _ = np.histogram(inten, bins=bins)
    counts = hist[hist > 0]
    if counts.sum() == 0:
        return 0.0
    probs = counts / counts.sum()
    return float(-np.sum(probs * np.log2(probs)))


def _variability(inten):
    """Współczynnik zmienności: std / |mean|."""
    mean = np.mean(inten)
    if mean == 0:
        return 0.0
    return float(np.std(inten) / abs(mean))


def _resonance(t2):
    """RMS sygnału T2 — łączna 'energia' rezonansu przejścia."""
    return float(np.sqrt(np.mean(np.square(t2))))


def compute_metrics(t0, t2):
    """Zwraca metryki opisane w README: entropia, zmiennosc, rezonans."""
    return {
        "entropia":  round(_entropy(t0), 4),
        "zmiennosc": round(_variability(t0), 4),
        "rezonans":  round(_resonance(t2), 4),
    }


def analyze(path, save_path=None):
    lam, inten = load_spectrum(path)

    t0 = T0(inten)
    t1 = T1(inten)
    t2 = T2(t1)

    metrics = compute_metrics(t0, t2)
    print("Metryki:", metrics)

    if not _HAS_MPL:
        print("(matplotlib niezainstalowany -- pomijam wykres, "
              "metryki policzone i zwrocone normalnie)")
        return metrics

    plt.figure(figsize=(10, 6))
    plt.plot(lam, t0, label="T0 – surowe")
    plt.plot(lam, t1, label="T1 – filtr")
    plt.plot(lam, t2, label="T2 – rezonans")
    plt.legend()
    plt.title("Helix‑Astro – analiza widma")
    plt.xlabel("λ")
    plt.ylabel("intensywność / rezonans")
    plt.grid(True)

    metrics_text = (
        f"entropia = {metrics['entropia']}\n"
        f"zmienność = {metrics['zmiennosc']}\n"
        f"rezonans = {metrics['rezonans']}"
    )
    plt.gcf().text(0.72, 0.75, metrics_text, fontsize=10,
                    bbox=dict(boxstyle="round", facecolor="white", alpha=0.85))

    if save_path:
        plt.tight_layout()
        plt.savefig(save_path, dpi=150)
    else:
        plt.show()

    return metrics

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Użycie: python3 helix_spectrum.py spectrum.csv")
        sys.exit(1)

    analyze(sys.argv[1])
