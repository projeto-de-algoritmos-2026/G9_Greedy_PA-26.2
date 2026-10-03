# Interval Partitioning

import heapq
from pathlib import Path

from algoritmos.scheduling import carregar_palestras, formatar_hora


def interval_partitioning(palestras):
    """Recebe uma lista de dicts {"nome", "inicio", "fim"} (minutos).

    Retorna um dict {numero_da_sala: [palestras]}, com salas numeradas a
    partir de 1. Palestras que encostam podem usar a mesma sala.
    """
    ordenadas = sorted(palestras, key=lambda p: p["inicio"])

    salas = {}
    livres = []  # heap de (horario_em_que_fica_livre, numero_da_sala)
    for palestra in ordenadas:
        if livres and livres[0][0] <= palestra["inicio"]:
            _, sala = heapq.heappop(livres)
        else:
            sala = len(salas) + 1
            salas[sala] = []
        salas[sala].append(palestra)
        heapq.heappush(livres, (palestra["fim"], sala))

    return salas


def profundidade(palestras):
    """Maior número de palestras acontecendo ao mesmo tempo.

    Retorna (profundidade, momento_do_pico). Nenhuma solução usa menos
    salas que a profundidade, e o guloso usa exatamente esse número.
    """
    eventos = []
    for p in palestras:
        eventos.append((p["inicio"], 1))
        eventos.append((p["fim"], -1))
    # Num mesmo horário, a saída (-1) vem antes da entrada (+1)
    eventos.sort()

    atual, maximo, momento = 0, 0, None
    for horario, delta in eventos:
        atual += delta
        if atual > maximo:
            maximo, momento = atual, horario
    return maximo, momento


if __name__ == "__main__":
    caminho = Path(__file__).resolve().parent.parent / "dados" / "palestras.csv"
    palestras = carregar_palestras(caminho)
    salas = interval_partitioning(palestras)
    pico, momento = profundidade(palestras)

    print(f"Palestras: {len(palestras)}")
    print(f"Salas necessárias: {len(salas)}")
    print(f"Pico: {pico} palestras ao mesmo tempo às {formatar_hora(momento)}\n")
    for sala, lista in salas.items():
        print(f"Sala {sala}:")
        for p in lista:
            print(f"  {formatar_hora(p['inicio'])} às {formatar_hora(p['fim'])}  {p['nome']}")
