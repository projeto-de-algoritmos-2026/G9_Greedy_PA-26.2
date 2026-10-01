"""Interval Scheduling (Pessoa A).

Problema: escolher o maior número de palestras sem conflito de horário.
Guloso: ordenar por horário de término e pegar a próxima compatível.
Complexidade: O(n log n) pela ordenação; a varredura é O(n).
"""

import csv
from pathlib import Path


def interval_scheduling(palestras):
    """Recebe uma lista de dicts {"nome", "inicio", "fim"} (minutos).

    Retorna a lista de palestras escolhidas, em ordem de horário.
    Palestras que encostam (uma termina às 10h e a outra começa às 10h)
    são consideradas compatíveis.
    """
    ordenadas = sorted(palestras, key=lambda p: p["fim"])

    escolhidas = []
    fim_ultima = float("-inf")
    for palestra in ordenadas:
        if palestra["inicio"] >= fim_ultima:
            escolhidas.append(palestra)
            fim_ultima = palestra["fim"]

    return escolhidas


def carregar_palestras(caminho):
    """Lê o CSV de palestras e converte início e fim para int."""
    with open(caminho, encoding="utf-8") as arquivo:
        return [
            {"nome": linha["nome"], "inicio": int(linha["inicio"]), "fim": int(linha["fim"])}
            for linha in csv.DictReader(arquivo)
        ]


def formatar_hora(minutos):
    """Converte minutos desde 00:00 para o formato HH:MM."""
    return f"{minutos // 60:02d}:{minutos % 60:02d}"


if __name__ == "__main__":
    caminho = Path(__file__).resolve().parent.parent / "dados" / "palestras.csv"
    palestras = carregar_palestras(caminho)
    agenda = interval_scheduling(palestras)

    print(f"Palestras disponíveis: {len(palestras)}")
    print(f"Máximo sem conflito: {len(agenda)}\n")
    for p in agenda:
        print(f"  {formatar_hora(p['inicio'])} às {formatar_hora(p['fim'])}  {p['nome']}")
