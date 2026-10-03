# Aba 1: Minha agenda (Interval Scheduling)

import streamlit as st

from abas.comum import editor_palestras, tabela_palestras
from algoritmos.scheduling import interval_scheduling
from visual.gantt import gantt


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
