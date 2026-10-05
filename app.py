import streamlit as st

from abas import aba_agenda, aba_huffman, aba_salas, aba_tarefas

st.set_page_config(page_title="Organizador da Semana Acadêmica", layout="wide")
st.title("Organizador da Semana Acadêmica")
st.caption("Projeto de Algoritmos 2026.2, Grupo 9: algoritmos gulosos")

agenda, salas, tarefas, huffman = st.tabs([
    "Minha agenda",
    "Alocação de salas",
    "Tarefas da equipe",
    "Exportar programação",
])

with agenda:
    aba_agenda.mostrar()

with salas:
    aba_salas.mostrar()

with tarefas:
    aba_tarefas.mostrar()

with huffman:
    st.header("Exportar programação (Huffman)")
    st.info("Em construção: compressão do texto da programação.")
    
with tarefas:
    st.header("Tarefas da equipe (Minimize Lateness)")
    st.info("Em construção: ordem das tarefas que minimiza o atraso máximo.")

