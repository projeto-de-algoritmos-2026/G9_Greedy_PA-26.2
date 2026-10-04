import random

from algoritmos.partitioning import interval_partitioning
from algoritmos.scheduling import interval_scheduling
from algoritmos.verificacao import CRITERIOS, forca_bruta_agenda, forca_bruta_salas, guloso_por


def p(nome, inicio, fim):
    return {"nome": nome, "inicio": inicio, "fim": fim}


def aleatorias(n, semente):
    rng = random.Random(semente)
    lista = []
    for i in range(n):
        inicio = rng.randint(0, 50)
        lista.append(p(str(i), inicio, inicio + rng.randint(1, 15)))
    return lista


def test_comeca_primeiro_falha_no_contraexemplo():
    palestras = [p("Longa", 0, 10), p("A", 0, 3), p("B", 3, 6), p("C", 6, 10)]
    assert len(guloso_por(palestras, CRITERIOS["Começa primeiro"])) == 1
    assert len(interval_scheduling(palestras)) == 3


def test_menor_duracao_falha_no_contraexemplo():
    palestras = [p("Curta", 4, 6), p("A", 0, 5), p("B", 5, 10)]
    assert len(guloso_por(palestras, CRITERIOS["Menor duração"])) == 1
    assert len(interval_scheduling(palestras)) == 2


def test_agenda_igual_forca_bruta_em_casos_aleatorios():
    for semente in range(30):
        palestras = aleatorias(9, semente)
        assert len(interval_scheduling(palestras)) == forca_bruta_agenda(palestras)


def test_salas_igual_forca_bruta_em_casos_aleatorios():
    for semente in range(30):
        palestras = aleatorias(9, semente)
        assert len(interval_partitioning(palestras)) == forca_bruta_salas(palestras)
