# Aba 1: Minha agenda (Interval Scheduling)

import pandas as pd
import streamlit as st

from abas.comum import editor_palestras, tabela_palestras
from algoritmos.scheduling import interval_scheduling
from algoritmos.verificacao import CRITERIOS, forca_bruta_agenda, guloso_por
from visual.gantt import gantt

LIMITE_FORCA_BRUTA = 20


def mostrar():
    st.header("Minha agenda")
    st.markdown(
        "Você quer assistir **o maior número possível de palestras** sem conflito de horário. "
        "O algoritmo ordena as palestras pelo horário de **término** e vai escolhendo a próxima "
        "que começa depois que a última escolhida acabou."
    )

    with st.expander("Palestras da Semana Acadêmica (edite à vontade)", expanded=False):
        palestras = editor_palestras("editor_agenda")

    if not palestras:
        st.info("Adicione pelo menos uma palestra.")
        return

    escolhidas = interval_scheduling(palestras)
    nomes = {p["nome"] for p in escolhidas}

    c1, c2 = st.columns(2)
    c1.metric("Palestras disponíveis", len(palestras))
    c2.metric("Máximo sem conflito", len(escolhidas))

    itens = [{**p, "situacao": "Escolhida" if p["nome"] in nomes else "Fora da agenda"} for p in palestras]
    st.plotly_chart(gantt(itens, linha="nome", cor="situacao"), width="stretch")

    st.subheader("Sua agenda")
    st.dataframe(tabela_palestras(escolhidas), hide_index=True, width="stretch")
    st.caption("Complexidade: O(n log n), por causa da ordenação.")

    mostrar_criterios(palestras)
    mostrar_forca_bruta(palestras, len(escolhidas))


def mostrar_criterios(palestras):
    st.subheader("Por que ordenar pelo término?")
    st.markdown(
        "Outros critérios parecem razoáveis, mas falham em alguns casos. "
        "Escolha um conjunto de palestras e compare:"
    )

    exemplos = {
        "Palestras atuais": palestras,
        "Contraexemplo: começa primeiro": [
            {"nome": "Palestra longa", "inicio": 540, "fim": 720},
            {"nome": "Curta A", "inicio": 540, "fim": 600},
            {"nome": "Curta B", "inicio": 600, "fim": 660},
            {"nome": "Curta C", "inicio": 660, "fim": 720},
        ],
        "Contraexemplo: menor duração": [
            {"nome": "Curta no meio", "inicio": 590, "fim": 620},
            {"nome": "Manhã A", "inicio": 540, "fim": 600},
            {"nome": "Manhã B", "inicio": 610, "fim": 670},
        ],
    }
    escolha = st.radio("Conjunto", list(exemplos), horizontal=True, key="exemplo_criterios")
    lista = exemplos[escolha]

    linhas = []
    for nome, criterio in CRITERIOS.items():
        resultado = guloso_por(lista, criterio)
        linhas.append({
            "Critério": nome,
            "Palestras escolhidas": len(resultado),
            "Quais": ", ".join(p["nome"] for p in sorted(resultado, key=lambda x: x["inicio"])),
        })
    st.dataframe(pd.DataFrame(linhas), hide_index=True, width="stretch")

    if escolha != "Palestras atuais":
        st.plotly_chart(gantt(lista, linha="nome"), width="stretch", key=f"gantt_{escolha}")


def mostrar_forca_bruta(palestras, resultado_guloso):
    st.subheader("Conferência com força bruta")
    if len(palestras) > LIMITE_FORCA_BRUTA:
        st.info(f"A força bruta testa 2^n subconjuntos; use até {LIMITE_FORCA_BRUTA} palestras.")
        return
    if st.button("Testar todos os subconjuntos", key="forca_bruta_agenda"):
        otimo = forca_bruta_agenda(palestras)
        st.write(f"Subconjuntos possíveis: **{2 ** len(palestras):,}**".replace(",", "."))
        if otimo == resultado_guloso:
            st.success(f"A força bruta também encontrou no máximo {otimo} palestras: o guloso deu a resposta ótima.")
        else:
            st.error(f"A força bruta encontrou {otimo} palestras, e o guloso {resultado_guloso}.")
