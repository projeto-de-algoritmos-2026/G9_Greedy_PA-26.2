# Gráfico de Gantt usado nas abas de intervalos e de tarefas

from datetime import datetime, timedelta

import pandas as pd
import plotly.express as px

BASE = datetime(2026, 10, 5)  # dia fictício da Semana Acadêmica

CORES = {
    "Escolhida": "#2E7D32",
    "Fora da agenda": "#B0BEC5",
    "No prazo": "#2E7D32",
    "Atrasada": "#C62828",
}


def _para_data(minutos):
    return BASE + timedelta(minutes=int(minutos))


def gantt(itens, linha="nome", cor=None, titulo=None):
    """Recebe uma lista de dicts com "nome", "inicio" e "fim" (minutos).

    linha: chave usada para as linhas do gráfico (ex.: "sala" ou "nome").
    cor: chave opcional usada para colorir as barras (ex.: "situacao").
    Retorna uma figura Plotly para usar com st.plotly_chart.
    """
    if not itens:
        return None

    df = pd.DataFrame(itens)
    df["Início"] = df["inicio"].map(_para_data)
    df["Fim"] = df["fim"].map(_para_data)

    fig = px.timeline(
        df,
        x_start="Início",
        x_end="Fim",
        y=linha,
        color=cor,
        color_discrete_map=CORES,
        hover_name="nome",
        hover_data={"Início": "|%H:%M", "Fim": "|%H:%M", linha: False},
        title=titulo,
    )
    # Linhas em ordem cronológica, de cima para baixo
    # (o eixo y do Plotly desenha a primeira categoria embaixo, por isso a inversão)
    ordem = list(dict.fromkeys(df.sort_values("inicio", kind="stable")[linha]))
    fig.update_yaxes(categoryorder="array", categoryarray=ordem[::-1], autorange=True, title=None)
    fig.update_xaxes(tickformat="%H:%M", title=None)
    fig.update_traces(marker_line_width=1, marker_line_color="white")
    fig.update_layout(
        height=max(260, 42 * df[linha].nunique() + 120),
        margin=dict(l=10, r=10, t=50 if titulo else 20, b=10),
        legend_title_text="",
    )
    return fig
