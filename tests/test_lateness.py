from itertools import permutations

from algoritmos.lateness import minimize_lateness


def t(nome, duracao, prazo):
    return {"nome": nome, "duracao": duracao, "prazo": prazo}


def atraso_da_ordem(ordem):
    tempo, pior = 0, 0
    for tarefa in ordem:
        tempo += tarefa["duracao"]
        pior = max(pior, tempo - tarefa["prazo"])
    return pior


def forca_bruta(tarefas):
    return min(atraso_da_ordem(ordem) for ordem in permutations(tarefas))


def test_lista_vazia():
    assert minimize_lateness([]) == ([], 0)


def test_ordena_por_prazo_e_sem_pausas():
    tarefas = [t("A", 3, 9), t("B", 2, 4), t("C", 1, 6)]
    agenda, _ = minimize_lateness(tarefas)
    assert [x["nome"] for x in agenda] == ["B", "C", "A"]
    assert all(a["fim"] == b["inicio"] for a, b in zip(agenda, agenda[1:]))


def test_tudo_no_prazo():
    _, atraso = minimize_lateness([t("A", 1, 5), t("B", 2, 5)])
    assert atraso == 0


def test_atraso_maximo_e_otimo():
    tarefas = [t("1", 3, 6), t("2", 2, 8), t("3", 1, 9), t("4", 4, 9), t("5", 3, 14), t("6", 2, 15)]
    agenda, atraso = minimize_lateness(tarefas)
    assert atraso == 1
    assert atraso == forca_bruta(tarefas)
    assert atraso == max(x["atraso"] for x in agenda)
