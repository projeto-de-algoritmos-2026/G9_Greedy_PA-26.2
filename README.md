## Grupo 9 - 26.2 - Greedy

## Alunos
|Matrícula | Aluno |
| -- | -- |
| 232003652 | João Paulo Barbosa Pereira Nunes |
| 251023184 | João Pedro da Nóbrega Souza Cordeiro |


## Sobre

O **Organizador da Semana Acadêmica** é um app em Streamlit que usa algoritmos gulosos para resolver os problemas de organizar um evento universitário fictício, a Semana Acadêmica de Computação. Cada aba do app resolve um problema com um algoritmo diferente:

| Aba | Problema | Algoritmo | Responsável |
| -- | -- | -- | -- |
| Minha agenda | Assistir o maior número de palestras sem conflito de horário | Interval Scheduling | João Paulo |
| Alocação de salas | Encaixar todas as palestras usando o menor número de salas | Interval Partitioning | João Paulo |
| Tarefas da equipe | Ordenar as tarefas de preparação para minimizar o maior atraso | Scheduling to Minimize Lateness | João Pedro |
| Exportar programação | Comprimir o texto da programação final | Codificação de Huffman | João Pedro |

Em todas as abas os dados podem ser editados na própria tela, e o resultado do guloso pode ser conferido com uma solução de força bruta.

## Screenshots

## Instalação

**Linguagem:** Python 3.10 ou superior
**Bibliotecas:** Streamlit, pandas, Plotly e pytest (todas no `requirements.txt`)

### Como executar

### 1. Clonar o repositório

```bash
git clone https://github.com/projeto-de-algoritmos-2026/G9_Greedy_PA-26.2.git
cd G9_Greedy_PA-26.2
```

### 2. Criar o ambiente virtual e instalar as dependências

```bash
python3 -m venv .venv
source .venv/bin/activate        # no Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Rodar o app

```bash
streamlit run app.py
```

O app abre no navegador em `http://localhost:8501`.

### 4. Rodar os testes

```bash
python -m pytest
```

## Uso

1. Abra o app e escolha uma das quatro abas no topo.
2. Em cada aba, abra o painel de dados para ver ou editar as palestras e tarefas de exemplo (é possível alterar, adicionar ou remover linhas).
3. O resultado é recalculado na hora: métricas, gráfico e tabela.
4. No fim de cada aba, use o botão de **força bruta** para confirmar que o guloso chegou na resposta ótima.

Cada algoritmo também pode ser executado pelo terminal, com os dados de exemplo:

```bash
python -m algoritmos.scheduling
python -m algoritmos.partitioning
python -m algoritmos.lateness
python -m algoritmos.huffman
```

## Outros

### Funcionalidades

#### Interval Scheduling (Minha agenda)

**Problema:** dado um conjunto de palestras com horário de início e fim, escolher o maior número possível delas sem conflito.

**Guloso:** ordena as palestras pelo horário de **término** e percorre a lista escolhendo cada palestra que começa depois (ou no mesmo horário) que a última escolhida terminou. Escolher sempre a que termina primeiro deixa o maior tempo livre para as próximas.

**Complexidade:** O(n log n), por causa da ordenação.

**No app:** gráfico com as palestras escolhidas em destaque, comparação com critérios que falham (começa primeiro e menor duração, com contraexemplos) e conferência com força bruta testando todos os subconjuntos.

#### Interval Partitioning (Alocação de salas)

**Problema:** encaixar todas as palestras usando o menor número de salas, sem duas palestras ao mesmo tempo na mesma sala.

**Guloso:** ordena as palestras pelo horário de **início** e coloca cada uma na sala que fica livre mais cedo, se ela já estiver livre; se nenhuma estiver, abre uma sala nova. Uma heap guarda o horário em que cada sala fica livre.

**Por que é ótimo:** nenhuma solução usa menos salas que a **profundidade** (o maior número de palestras acontecendo ao mesmo tempo), e o guloso usa exatamente esse número.

**Complexidade:** O(n log n), pela ordenação e pelas operações na heap.

**No app:** número de salas, momento de pico, gráfico com uma linha por sala e conferência com força bruta.

#### Scheduling to Minimize Lateness (Tarefas da equipe)

**Problema:** a equipe executa uma tarefa por vez, sem pausas. Cada tarefa tem duração e prazo, e o atraso é quanto ela termina depois do prazo. O objetivo é minimizar o **maior** atraso.

**Guloso:** ordena as tarefas pelo **prazo mais próximo** (Earliest Deadline First) e executa nessa ordem, sem intervalos.

**Por que é ótimo:** qualquer ordem pode ser transformada na ordem por prazo trocando pares de tarefas "invertidas", e cada troca não aumenta o atraso máximo.

**Complexidade:** O(n log n), por causa da ordenação.

**No app:** atraso máximo, tarefas atrasadas em vermelho no gráfico, tabela com a ordem de execução e conferência com força bruta testando todas as ordens.

#### Codificação de Huffman (Exportar programação)

**Problema:** comprimir um texto usando códigos binários de tamanho variável, sem que nenhum código seja prefixo de outro.

**Guloso:** conta a frequência de cada caractere e coloca todos numa heap. Retira sempre os dois nós de **menor frequência**, junta num nó novo com a soma e devolve para a heap, até sobrar a raiz. O caminho da raiz até cada caractere é o código dele (esquerda = 0, direita = 1).

**Complexidade:** O(n log n), em que n é o número de caracteres distintos.

**No app:** tamanho original e comprimido, tabela de códigos, desenho da árvore, conferência da decodificação e download dos bits.

### Estrutura do projeto

```
app.py                     app Streamlit com as 4 abas
abas/
    comum.py               editor de palestras compartilhado
    aba_agenda.py          aba 1: Interval Scheduling
    aba_salas.py           aba 2: Interval Partitioning
    aba_tarefas.py         aba 3: Minimize Lateness
    aba_huffman.py         aba 4: Huffman
algoritmos/
    scheduling.py          Interval Scheduling
    partitioning.py        Interval Partitioning
    lateness.py            Scheduling to Minimize Lateness
    huffman.py             Codificação de Huffman
    verificacao.py         critérios alternativos e força bruta dos intervalos
visual/
    gantt.py               gráfico de Gantt (abas 1, 2 e 3)
    arvore.py              desenho da árvore de Huffman
dados/
    palestras.csv          palestras de exemplo
    tarefas.csv            tarefas de exemplo
tests/                     testes de todos os algoritmos
```
