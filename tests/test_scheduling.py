from itertools import combinations

from algoritmos.scheduling import interval_scheduling


def p(nome, inicio, fim):
    return {"nome": nome, "inicio": inicio, "fim": fim}


def compativeis(palestras):
    ordenadas = sorted(palestras, key=lambda x: x["inicio"])
    return all(a["fim"] <= b["inicio"] for a, b in zip(ordenadas, ordenadas[1:]))


def forca_bruta(palestras):
    for tamanho in range(len(palestras), 0, -1):
        for combo in combinations(palestras, tamanho):
            if compativeis(combo):
                return tamanho
    return 0


def test_lista_vazia():
    assert interval_scheduling([]) == []


def test_contraexemplo_inicio_mais_cedo():
    # Pegar a que começa primeiro (A) daria só 1 palestra
    palestras = [p("A", 540, 720), p("B", 540, 600), p("C", 600, 660), p("D", 660, 720)]
    nomes = [x["nome"] for x in interval_scheduling(palestras)]
    assert nomes == ["B", "C", "D"]


def test_intervalos_que_encostam_sao_compativeis():
    palestras = [p("A", 0, 10), p("B", 10, 20)]
    assert len(interval_scheduling(palestras)) == 2


def test_resultado_sem_conflito_e_otimo():
    palestras = [
        p("1", 0, 6), p("2", 1, 4), p("3", 3, 5), p("4", 3, 8),
        p("5", 4, 7), p("6", 5, 9), p("7", 6, 10), p("8", 8, 11),
    ]
    escolhidas = interval_scheduling(palestras)
    assert compativeis(escolhidas)
    assert len(escolhidas) == forca_bruta(palestras)
