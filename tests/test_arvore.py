from algoritmos.huffman import huffman_codificar
from visual.arvore import desenhar_arvore


def test_arvore_vazia():
    assert desenhar_arvore(None).startswith("digraph")


def test_uma_folha_por_caractere_e_uma_aresta_por_filho():
    texto = "abracadabra"
    codigos, _, arvore = huffman_codificar(texto)
    dot = desenhar_arvore(arvore)
    folhas = dot.count("shape=box")
    arestas = dot.count("->")
    assert folhas == len(codigos)
    assert arestas == 2 * (folhas - 1)  # árvore binária cheia


def test_caracteres_especiais_nao_quebram_o_dot():
    _, _, arvore = huffman_codificar('linha 1\nlinha "2"')
    dot = desenhar_arvore(arvore)
    assert "espaço" in dot and dot.endswith("}")
