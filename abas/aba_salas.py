# Aba 2: Alocação de salas (Interval Partitioning)

import streamlit as st

from abas.comum import editor_palestras, tabela_palestras
from algoritmos.partitioning import interval_partitioning, profundidade
from algoritmos.scheduling import formatar_hora
from visual.gantt import gantt


def mostrar():
    st.header("Alocação de salas")
    st.markdown(
        "A organização precisa encaixar **todas** as palestras usando o **menor número de salas**. "
        "O algoritmo ordena por horário de **início** e coloca cada palestra na sala que fica livre "
        "mais cedo; se nenhuma estiver livre, abre uma sala nova."
    )

    with st.expander("Palestras da Semana Acadêmica (edite à vontade)", expanded=False):
        palestras = editor_palestras("editor_salas")

    if not palestras:
        st.info("Adicione pelo menos uma palestra.")
        return

    salas = interval_partitioning(palestras)
    pico, momento = profundidade(palestras)

    c1, c2, c3 = st.columns(3)
    c1.metric("Palestras", len(palestras))
    c2.metric("Salas necessárias", len(salas))
    c3.metric("Pico simultâneo", f"{pico} às {formatar_hora(momento)}")

    st.caption(
        "Nenhuma solução usa menos salas que o pico de palestras ao mesmo tempo, "
        "e o guloso usa exatamente esse número: por isso ele é ótimo."
    )

    itens = [{**p, "sala": f"Sala {n}"} for n, lista in salas.items() for p in lista]
    st.plotly_chart(gantt(itens, linha="sala", cor="sala"), width="stretch")

    st.subheader("Distribuição por sala")
    st.dataframe(
        tabela_palestras(itens, extra=lambda p: {"Sala": p["sala"]}),
        hide_index=True,
        width="stretch",
    )
    st.caption("Complexidade: O(n log n), pela ordenação e pela heap de salas livres.")
