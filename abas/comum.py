# Funções compartilhadas pelas abas de palestras

from pathlib import Path

import pandas as pd
import streamlit as st

from algoritmos.scheduling import carregar_palestras, formatar_hora

PASTA_DADOS = Path(__file__).resolve().parent.parent / "dados"


def para_minutos(hora):
    """Converte "HH:MM" em minutos desde 00:00."""
    h, m = str(hora).strip().split(":")
    return int(h) * 60 + int(m)


def editor_palestras(chave):
    """Mostra a tabela editável de palestras e devolve a lista validada.

    Os horários aparecem como HH:MM para facilitar a edição, e são
    convertidos para minutos antes de ir para os algoritmos.
    """
    palestras = carregar_palestras(PASTA_DADOS / "palestras.csv")
    df = pd.DataFrame(
        {
            "nome": [p["nome"] for p in palestras],
            "inicio": [formatar_hora(p["inicio"]) for p in palestras],
            "fim": [formatar_hora(p["fim"]) for p in palestras],
        }
    )

    editado = st.data_editor(
        df,
        key=chave,
        num_rows="dynamic",
        width="stretch",
        column_config={
            "nome": st.column_config.TextColumn("Palestra", required=True),
            "inicio": st.column_config.TextColumn("Início (HH:MM)", required=True),
            "fim": st.column_config.TextColumn("Fim (HH:MM)", required=True),
        },
    )

    validas, erros = [], []
    for _, linha in editado.dropna(how="all").iterrows():
        try:
            inicio, fim = para_minutos(linha["inicio"]), para_minutos(linha["fim"])
        except (ValueError, AttributeError):
            erros.append(f"{linha['nome']}: horário inválido, use HH:MM")
            continue
        if fim <= inicio:
            erros.append(f"{linha['nome']}: o fim precisa ser depois do início")
            continue
        validas.append({"nome": str(linha["nome"]), "inicio": inicio, "fim": fim})

    for erro in erros:
        st.warning(erro)
    return validas


def tabela_palestras(lista, extra=None):
    """Monta um DataFrame com os horários formatados para exibição."""
    linhas = []
    for p in sorted(lista, key=lambda x: x["inicio"]):
        linha = {"Palestra": p["nome"], "Início": formatar_hora(p["inicio"]), "Fim": formatar_hora(p["fim"])}
        if extra:
            linha.update(extra(p))
        linhas.append(linha)
    return pd.DataFrame(linhas)
