# Scheduling to Minimize Lateness.


import csv
from pathlib import Path


def minimize_lateness(tarefas, inicio=0):
    """Recebe uma lista de dicts {"nome", "duracao", "prazo"} (minutos).

    Retorna (agenda, atraso_maximo), em que agenda é uma lista de dicts
    {"nome", "inicio", "fim", "prazo", "atraso"}. O atraso de uma tarefa
    é fim menos prazo, ou zero se ela terminou dentro do prazo.
    """
    ordenadas = sorted(tarefas, key=lambda t: t["prazo"])

    agenda = []
    tempo = inicio
    atraso_maximo = 0
    for tarefa in ordenadas:
        fim = tempo + tarefa["duracao"]
        atraso = max(0, fim - tarefa["prazo"])
        agenda.append({
            "nome": tarefa["nome"],
            "inicio": tempo,
            "fim": fim,
            "prazo": tarefa["prazo"],
            "atraso": atraso,
        })
        atraso_maximo = max(atraso_maximo, atraso)
        tempo = fim

    return agenda, atraso_maximo


def carregar_tarefas(caminho):
    """Lê o CSV de tarefas e converte duração e prazo para int."""
    with open(caminho, encoding="utf-8") as arquivo:
        return [
            {"nome": linha["nome"], "duracao": int(linha["duracao"]), "prazo": int(linha["prazo"])}
            for linha in csv.DictReader(arquivo)
        ]


if __name__ == "__main__":
    caminho = Path(__file__).resolve().parent.parent / "dados" / "tarefas.csv"
    tarefas = carregar_tarefas(caminho)
    agenda, atraso_maximo = minimize_lateness(tarefas)

    print(f"Tarefas: {len(tarefas)}")
    print(f"Atraso máximo: {atraso_maximo} min\n")
    for t in agenda:
        situacao = f"atrasou {t['atraso']} min" if t["atraso"] else "no prazo"
        print(f"  {t['inicio']:>4} a {t['fim']:<4} (prazo {t['prazo']:>3})  {t['nome']}: {situacao}")
