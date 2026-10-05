# Codificação de Huffman

import heapq
from collections import Counter
from dataclasses import dataclass
from itertools import count


@dataclass
class No:
    frequencia: int
    caractere: str | None = None
    esquerda: "No | None" = None
    direita: "No | None" = None

    def eh_folha(self):
        return self.caractere is not None


def construir_arvore(texto):
    """Monta a árvore de Huffman a partir das frequências do texto."""
    frequencias = Counter(texto)
    desempate = count()  # evita comparar nós quando as frequências empatam
    heap = [(freq, next(desempate), No(freq, char)) for char, freq in frequencias.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        f1, _, menor = heapq.heappop(heap)
        f2, _, segundo = heapq.heappop(heap)
        pai = No(f1 + f2, esquerda=menor, direita=segundo)
        heapq.heappush(heap, (pai.frequencia, next(desempate), pai))

    return heap[0][2] if heap else None


def gerar_codigos(arvore):
    """Percorre a árvore e devolve {caractere: código}."""
    if arvore is None:
        return {}
    if arvore.eh_folha():
        return {arvore.caractere: "0"}  # texto com um único caractere distinto

    codigos = {}

    def percorrer(no, caminho):
        if no.eh_folha():
            codigos[no.caractere] = caminho
            return
        percorrer(no.esquerda, caminho + "0")
        percorrer(no.direita, caminho + "1")

    percorrer(arvore, "")
    return codigos


def huffman_codificar(texto):
    """Retorna (codigos, bits, arvore).

    codigos: dict {caractere: "0101"}
    bits: string com o texto codificado
    arvore: raiz da árvore (usada para decodificar e desenhar)
    """
    arvore = construir_arvore(texto)
    codigos = gerar_codigos(arvore)
    bits = "".join(codigos[c] for c in texto)
    return codigos, bits, arvore


def huffman_decodificar(bits, arvore):
    """Retorna o texto original a partir dos bits e da árvore."""
    if arvore is None:
        return ""
    if arvore.eh_folha():
        return arvore.caractere * len(bits)

    texto = []
    no = arvore
    for bit in bits:
        no = no.esquerda if bit == "0" else no.direita
        if no.eh_folha():
            texto.append(no.caractere)
            no = arvore
    return "".join(texto)


if __name__ == "__main__":
    texto = "Semana Academica de Computacao: programacao completa"
    codigos, bits, arvore = huffman_codificar(texto)

    print(f"Texto: {texto}\n")
    for char, codigo in sorted(codigos.items(), key=lambda x: (len(x[1]), x[0])):
        print(f"  {char!r:>5}  {codigo}")

    original = len(texto) * 8
    print(f"\nOriginal: {original} bits (8 por caractere)")
    print(f"Comprimido: {len(bits)} bits ({len(bits) / original:.0%} do original)")
    print(f"Decodificado igual ao original: {huffman_decodificar(bits, arvore) == texto}")
