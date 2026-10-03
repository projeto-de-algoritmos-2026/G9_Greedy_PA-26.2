from itertools import product

from algoritmos.partitioning import interval_partitioning, profundidade


def p(nome, inicio, fim):
    return {"nome": nome, "inicio": inicio, "fim": fim}


def sem_conflito(lista):
    ordenadas = sorted(lista, key=lambda x: x["inicio"])
    return all(a["fim"] <= b["inicio"] for a, b in zip(ordenadas, ordenadas[1:]))


def forca_bruta(palestras):
    """Menor número de salas testando todas as distribuições possíveis."""
    n = len(palestras)
    for k in range(1, n + 1):
        for distribuicao in product(range(k), repeat=n):
            salas = [[palestras[i] for i in range(n) if distribuicao[i] == s] for s in range(k)]
            if all(sem_conflito(sala) for sala in salas):
                return k
    return 0


def test_lista_vazia():
    assert interval_partitioning([]) == {}


def test_todas_sobrepostas_precisam_de_uma_sala_cada():
    palestras = [p("A", 0, 10), p("B", 1, 11), p("C", 2, 12)]
    assert len(interval_partitioning(palestras)) == 3


def test_palestras_que_encostam_dividem_a_sala():
    palestras = [p("A", 0, 10), p("B", 10, 20), p("C", 20, 30)]
    assert len(interval_partitioning(palestras)) == 1


def test_nenhuma_sala_tem_conflito_e_todas_foram_alocadas():
    palestras = [p("A", 0, 3), p("B", 1, 4), p("C", 2, 6), p("D", 4, 7), p("E", 5, 8), p("F", 6, 9)]
    salas = interval_partitioning(palestras)
    assert all(sem_conflito(lista) for lista in salas.values())
    assert sum(len(lista) for lista in salas.values()) == len(palestras)


def test_numero_de_salas_e_igual_a_profundidade_e_otimo():
    palestras = [p("A", 0, 3), p("B", 1, 4), p("C", 2, 6), p("D", 4, 7), p("E", 5, 8), p("F", 6, 9)]
    salas = interval_partitioning(palestras)
    pico, _ = profundidade(palestras)
    assert len(salas) == pico
    assert len(salas) == forca_bruta(palestras)
