# Aba 3: Tarefas da equipe (Minimize Lateness)

from itertools import permutations
from math import factorial
from pathlib import Path

import pandas as pd
import streamlit as st

from algoritmos.lateness import carregar_tarefas, minimize_lateness
from visual.gantt import gantt

PASTA_DADOS = Path(__file__).resolve().parent.parent / "dados"
LIMITE_FORCA_BRUTA = 9


def mostrar():
    st.header("Tarefas da equipe")
    st.markdown(
        "A equipe precisa preparar o evento, uma tarefa por vez e sem pausas. Cada tarefa tem uma "
        "**duração** e um **prazo**. O algoritmo ordena pelo **prazo mais próximo** "
        "(Earliest Deadline First), o que deixa o **maior atraso** o menor possível."
    )

    tarefas_csv = carregar_tarefas(PASTA_DADOS / "tarefas.csv")
    with st.expander("Tarefas (tempos em minutos desde o início da preparação)", expanded=False):
        editado = st.data_editor(
            pd.DataFrame(tarefas_csv),
            key="editor_tarefas",
            num_rows="dynamic",
            width="stretch",
            column_config={
                "nome": st.column_config.TextColumn("Tarefa", required=True),
                "duracao": st.column_config.NumberColumn("Duração (min)", min_value=1, step=5, required=True),
                "prazo": st.column_config.NumberColumn("Prazo (min)", min_value=0, step=5, required=True),
            },
        )

    tarefas = [
        {"nome": str(l["nome"]), "duracao": int(l["duracao"]), "prazo": int(l["prazo"])}
        for _, l in editado.dropna().iterrows()
    ]
    if not tarefas:
        st.info("Adicione pelo menos uma tarefa.")
        return

    agenda, atraso_maximo = minimize_lateness(tarefas)
    atrasadas = sum(1 for t in agenda if t["atraso"] > 0)

    c1, c2, c3 = st.columns(3)
    c1.metric("Tarefas", len(agenda))
    c2.metric("Atraso máximo", f"{atraso_maximo} min")
    c3.metric("Tarefas atrasadas", atrasadas)

    itens = [{**t, "situacao": "Atrasada" if t["atraso"] else "No prazo"} for t in agenda]
    st.plotly_chart(gantt(itens, linha="nome", cor="situacao"), width="stretch")
    st.caption("O eixo de horário conta a partir do início da preparação (00:00).")

    st.subheader("Ordem de execução")
    st.dataframe(
        pd.DataFrame(
            [
                {
                    "Ordem": i,
                    "Tarefa": t["nome"],
                    "Início": t["inicio"],
                    "Fim": t["fim"],
                    "Prazo": t["prazo"],
                    "Atraso": t["atraso"],
                }
                for i, t in enumerate(agenda, start=1)
            ]
        ),
        hide_index=True,
        width="stretch",
    )
    st.caption("Complexidade: O(n log n), por causa da ordenação por prazo.")

    st.subheader("Conferência com força bruta")
    if len(tarefas) > LIMITE_FORCA_BRUTA:
        st.info(f"A força bruta testa n! ordens; use até {LIMITE_FORCA_BRUTA} tarefas.")
        return
    if st.button("Testar todas as ordens possíveis", key="forca_bruta_tarefas"):
        with st.spinner("Testando..."):
            otimo = min(atraso_da_ordem(ordem) for ordem in permutations(tarefas))
        st.write(f"Ordens possíveis: **{factorial(len(tarefas)):,}**".replace(",", "."))
        if otimo == atraso_maximo:
            st.success(f"O menor atraso máximo possível é {otimo} min: a ordem por prazo é ótima.")
        else:
            st.error(f"A força bruta encontrou {otimo} min, e o guloso {atraso_maximo} min.")


def atraso_da_ordem(ordem):
    """Maior atraso ao executar as tarefas na ordem dada, sem pausas."""
    tempo, pior = 0, 0
    for tarefa in ordem:
        tempo += tarefa["duracao"]
        pior = max(pior, tempo - tarefa["prazo"])
    return pior
