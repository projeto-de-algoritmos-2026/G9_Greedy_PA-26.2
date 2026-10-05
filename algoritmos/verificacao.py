# Verificações dos algoritmos de intervalos: critérios alternativos e força bruta

from itertools import combinations

CRITERIOS = {
    "Termina primeiro (guloso correto)": lambda p: p["fim"],
    "Começa primeiro": lambda p: p["inicio"],
    "Menor duração": lambda p: p["fim"] - p["inicio"],
}


def guloso_por(palestras, criterio):
    """Mesmo guloso do Interval Scheduling, mas ordenando pelo critério dado."""
    escolhidas = []
    for p in sorted(palestras, key=criterio):
        if all(p["fim"] <= e["inicio"] or p["inicio"] >= e["fim"] for e in escolhidas):
            escolhidas.append(p)
    return escolhidas


def compativeis(palestras):
    ordenadas = sorted(palestras, key=lambda p: p["inicio"])
    return all(a["fim"] <= b["inicio"] for a, b in zip(ordenadas, ordenadas[1:]))


def forca_bruta_agenda(palestras):
    """Maior número de palestras sem conflito testando todos os subconjuntos. O(2^n)."""
    for tamanho in range(len(palestras), 0, -1):
        for combo in combinations(palestras, tamanho):
            if compativeis(combo):
                return tamanho
    return 0


def forca_bruta_salas(palestras):
    """Menor número de salas testando todas as distribuições possíveis (backtracking)."""
    ordenadas = sorted(palestras, key=lambda p: p["inicio"])
    n = len(ordenadas)

    def cabe(k):
        fim_das_salas = []

        def colocar(i):
            if i == n:
                return True
            p = ordenadas[i]
            for s in range(len(fim_das_salas)):
                if fim_das_salas[s] <= p["inicio"]:
                    anterior = fim_das_salas[s]
                    fim_das_salas[s] = p["fim"]
                    if colocar(i + 1):
                        return True
                    fim_das_salas[s] = anterior
            if len(fim_das_salas) < k:  # abrir uma sala nova (só uma, para evitar repetição)
                fim_das_salas.append(p["fim"])
                if colocar(i + 1):
                    return True
                fim_das_salas.pop()
            return False

        return colocar(0)

    for k in range(1, n + 1):
        if cabe(k):
            return k
    return 0
