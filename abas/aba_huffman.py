# Aba 4: Exportar programação (Huffman)

from collections import Counter
from pathlib import Path

import pandas as pd
import streamlit as st

from algoritmos.huffman import huffman_codificar, huffman_decodificar
from algoritmos.scheduling import carregar_palestras, formatar_hora

PASTA_DADOS = Path(__file__).resolve().parent.parent / "dados"
NOMES_ESPECIAIS = {" ": "(espaço)", "\n": "(quebra de linha)", "\t": "(tab)"}


def texto_programacao():
    """Gera o texto da programação a partir do CSV de palestras."""
    palestras = sorted(carregar_palestras(PASTA_DADOS / "palestras.csv"), key=lambda p: p["inicio"])
    linhas = ["Programação da Semana Acadêmica de Computação", ""]
    linhas += [f"{formatar_hora(p['inicio'])} às {formatar_hora(p['fim'])}: {p['nome']}" for p in palestras]
    return "\n".join(linhas)


def mostrar():
    st.header("Exportar programação")
    st.markdown(
        "Antes de enviar a programação, ela é **comprimida com Huffman**. O algoritmo junta sempre "
        "os dois caracteres (ou grupos) **menos frequentes**, montando uma árvore em que os caracteres "
        "mais comuns ganham os códigos mais curtos."
    )

    texto = st.text_area("Texto da programação", value=texto_programacao(), height=260)
    if not texto:
        st.info("Digite algum texto para comprimir.")
        return

    codigos, bits, arvore = huffman_codificar(texto)
    original = len(texto) * 8
    decodificado = huffman_decodificar(bits, arvore)

    c1, c2, c3 = st.columns(3)
    c1.metric("Original", f"{original} bits", help="Considerando 8 bits por caractere")
    c2.metric("Comprimido", f"{len(bits)} bits")
    c3.metric("Tamanho final", f"{len(bits) / original:.0%} do original")

    if decodificado == texto:
        st.success("Decodificação conferida: o texto recuperado é idêntico ao original.")
    else:
        st.error("A decodificação não bateu com o texto original.")

    st.subheader("Tabela de códigos")
    frequencias = Counter(texto)
    tabela = pd.DataFrame(
        [
            {
                "Caractere": NOMES_ESPECIAIS.get(c, c),
                "Frequência": frequencias[c],
                "Código": codigo,
                "Bits": len(codigo),
            }
            for c, codigo in codigos.items()
        ]
    ).sort_values(["Frequência", "Caractere"], ascending=[False, True])
    st.dataframe(tabela, hide_index=True, width="stretch")

    with st.expander("Ver texto codificado em bits"):
        st.code(bits[:2000] + ("..." if len(bits) > 2000 else ""), language=None)

    st.download_button("Baixar bits (.txt)", bits, file_name="programacao_huffman.txt")
    st.caption("Complexidade: O(n log n), com n = número de caracteres distintos.")
