from collections import Counter

from algoritmos.huffman import huffman_codificar, huffman_decodificar


def custo(texto, codigos):
    return sum(len(codigos[c]) for c in texto)


def test_texto_vazio():
    codigos, bits, arvore = huffman_codificar("")
    assert codigos == {} and bits == ""
    assert huffman_decodificar(bits, arvore) == ""


def test_um_unico_caractere():
    codigos, bits, arvore = huffman_codificar("aaaa")
    assert codigos == {"a": "0"}
    assert huffman_decodificar(bits, arvore) == "aaaa"


def test_codifica_e_decodifica_igual():
    texto = "Semana Acadêmica de Computação: programação completa!"
    codigos, bits, arvore = huffman_codificar(texto)
    assert huffman_decodificar(bits, arvore) == texto


def test_nenhum_codigo_e_prefixo_de_outro():
    codigos, _, _ = huffman_codificar("abracadabra alakazam")
    lista = list(codigos.values())
    for a in lista:
        for b in lista:
            assert a == b or not b.startswith(a)


def test_mais_frequente_tem_codigo_menor_ou_igual():
    texto = "aaaaaaaabbbccd"
    codigos, _, _ = huffman_codificar(texto)
    freq = Counter(texto)
    for x in codigos:
        for y in codigos:
            if freq[x] > freq[y]:
                assert len(codigos[x]) <= len(codigos[y])


def test_custo_otimo_exemplo_classico():
    # Frequências do exemplo do CLRS: a=45, b=13, c=12, d=16, e=9, f=5 (custo ótimo 224)
    texto = "a" * 45 + "b" * 13 + "c" * 12 + "d" * 16 + "e" * 9 + "f" * 5
    codigos, bits, _ = huffman_codificar(texto)
    assert custo(texto, codigos) == len(bits) == 224
