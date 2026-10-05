# Desenho da árvore de Huffman

# Caracteres que precisam de nome legível ou de escape no formato DOT
NOMES = {" ": "espaço", "\n": "\\\\n", "\t": "tab", '"': '\\"', "\\": "\\\\"}


def _rotulo(caractere):
    return NOMES.get(caractere, caractere)


def desenhar_arvore(arvore):
    """Recebe a raiz da árvore de Huffman e devolve o texto DOT do Graphviz.

    O resultado pode ser usado direto com st.graphviz_chart. Folhas mostram
    o caractere e a frequência; nós internos mostram a soma das frequências.
    """
    linhas = [
        "digraph Huffman {",
        '  node [fontname="Helvetica", fontsize=11];',
        '  edge [fontname="Helvetica", fontsize=10];',
    ]
    if arvore is None:
        linhas.append("}")
        return "\n".join(linhas)

    contador = [0]

    def visitar(no):
        meu_id = f"n{contador[0]}"
        contador[0] += 1
        if no.eh_folha():
            linhas.append(
                f'  {meu_id} [shape=box, style="rounded,filled", fillcolor="#E8F5E9", '
                f'label="{_rotulo(no.caractere)}\\n{no.frequencia}"];'
            )
            return meu_id
        linhas.append(f'  {meu_id} [shape=circle, label="{no.frequencia}"];')
        for filho, bit in ((no.esquerda, "0"), (no.direita, "1")):
            filho_id = visitar(filho)
            linhas.append(f'  {meu_id} -> {filho_id} [label="{bit}"];')
        return meu_id

    visitar(arvore)
    linhas.append("}")
    return "\n".join(linhas)
