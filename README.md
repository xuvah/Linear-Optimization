# Linear-Optimization

## Problema do Transporte - Pesquisa Operacional

Este repositório contém a implementação de um modelo de otimização linear para o problema do transporte, abordado na disciplina de Pesquisa Operacional da Universidade Federal de Minas Gerais (UFMG). O objetivo é otimizar a movimentação de múltiplos produtos de várias origens para diversos destinos, considerando restrições de oferta e demanda.

## Estrutura do Projeto

### Descrição Geral

Problema de otimização combinatória com diversas aplicações no mundo real, visando a movimentação eficiente de produtos de origens a destinos.

### Modelagem

- **Modelagem padrão baseada em Arenales.**
- **Modelagem expandida**, detalhada com tratamento de dados e algoritmo de modelagem.

### Tratamento de Dados e Bibliotecas Utilizadas

- **Gurobi**: Usado como solver de otimização.
- **Excel**: Facilita a leitura de dados e manipulação (simulando um cenário real).
- **Pandas**: Utilizado para manipulação de dados.

Leitura de dados a partir de um arquivo Excel (`Base_de_dados_PO.xlsx`) que contém as planilhas `Distâncias`, `Pesos k`, `Ofertas` e `Demandas b(j,k)`.

### Algoritmo de Modelagem

1. **Criação de modelos de otimização** e definição de variáveis de decisão.
2. Definição da **função objetivo**.
3. Adição de **restrições de oferta e demanda** para garantir a factibilidade do modelo.

### Resultados e Análise

- O modelo converge em tempo hábil e faz uso do **Dual Simplex** para resolver.
- Critério de parada baseado na otimalidade.
- **Pré-solve** aplicado para eliminar grande parte das linhas e colunas.
- Adaptações feitas para casos de infactibilidade.

## Requisitos

- **Gurobi**
- **Pandas**

## Como Executar

### Instalação de Dependências

```bash
pip install gurobipy pandas
