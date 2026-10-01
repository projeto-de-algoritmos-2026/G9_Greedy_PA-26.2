import streamlit as st

st.set_page_config(page_title="Organizador da Semana Acadêmica", layout="wide")
st.title("Organizador da Semana Acadêmica")
st.caption("Projeto de Algoritmos 2026.2, Grupo 9: algoritmos gulosos")

aba_agenda, aba_salas, aba_tarefas, aba_huffman = st.tabs([
    "Minha agenda",
    "Alocação de salas",
    "Tarefas da equipe",
    "Exportar programação",
])

# ===== ABA 1: Interval Scheduling (Pessoa A) =====
with aba_agenda:
    st.header("Minha agenda (Interval Scheduling)")
    st.info("Em construção: máximo de palestras sem conflito de horário.")

# ===== ABA 2: Interval Partitioning (Pessoa A) =====
with aba_salas:
    st.header("Alocação de salas (Interval Partitioning)")
    st.info("Em construção: mínimo de salas para todas as palestras.")

# ===== ABA 3: Minimize Lateness (Pessoa B) =====
with aba_tarefas:
    st.header("Tarefas da equipe (Minimize Lateness)")
    st.info("Em construção: ordem das tarefas que minimiza o atraso máximo.")

# ===== ABA 4: Huffman (Pessoa B) =====
with aba_huffman:
    st.header("Exportar programação (Huffman)")
    st.info("Em construção: compressão do texto da programação.")
