# Projeto de Organização de Computadores

Este repositório contém os arquivos desenvolvidos para a disciplina de Organização de Computadores, ministrada pelo professor Juan Colonna. O projeto é dividido em duas partes principais: a simulação de um computador personalizado no Logisim e um montador (assembler) desenvolvido em Python.

## Estrutura do Projeto

A estrutura do projeto é organizada da seguinte forma:

```
.
├── logisim/
│   ├── luiz_gabriel_antunes_sena_novo.circ
│   └── luiz_gabriel_antunes_sena.circ
├── montador/
│   ├── dist/
│   │   └── .gitkeep
│   └── src/
│       ├── exem.asm
│       ├── programa.asm
│       ├── vector_swap.asm
│       ├── assembler.py
│       └── montador.py
├── program.pc
└── README.md
````


## Parte 1: Simulação no Logisim

A pasta `logisim/` contém os arquivos `.circ` do Logisim que representam a arquitetura de um computador personalizado, desenvolvida ao longo das aulas da disciplina.

* `luiz_gabriel_antunes_sena_novo.circ`: Versão mais recente ou revisada do projeto do computador no Logisim.
* `luiz_gabriel_antunes_sena.circ`: Versão original ou anterior do projeto do computador no Logisim.

Para utilizar, basta abrir um desses arquivos com o software Logisim e explorar a arquitetura do computador simulado.

## Parte 2: Montador (Assembler) em Python

A pasta `montador/` contém o código-fonte de um montador desenvolvido em Python. Este montador é capaz de compilar códigos escritos em uma linguagem Assembly específica para o computador simulado no Logisim, gerando um arquivo binário que pode ser carregado e executado na simulação.

### Conteúdo da Pasta `montador/`

* `src/`: Contém os arquivos-fonte do montador e exemplos de programas em Assembly.
    * `assembler.py`: Contém a lógica principal do processo de montagem.
    * `montador.py`: O script principal para executar o montador.
    * `exem.asm`: Exemplo de código Assembly.
    * `programa.asm`: Exemplo de código Assembly.
    * `vector_swap.asm`: Exemplo de código Assembly que realiza a troca de vetores.
* `dist/`: Destino para os arquivos binários gerados pelo montador (atualmente contém apenas o `.gitkeep`).

### Como Usar o Montador

1.  **Navegue até a pasta `montador/src`**:
    ```bash
    cd montador/src
    ```

2.  **Execute o montador**:
    Utilize o script `montador.py` para compilar seus arquivos `.asm`. Você precisará especificar o arquivo de entrada e o de saída.

    Exemplo:
    ```bash
    python montador.py programa.asm programa.m
    ```
    O arquivo gerado poderá então ser carregado no Logisim para execução no computador simulado.

    **Observação**: Consulte o código-fonte de `montador.py` e `assembler.py` para entender as opções de linha de comando e o formato dos arquivos Assembly esperados.
---

**Desenvolvido por:** Luiz Gabriel Antunes Sena

**Disciplina:** Organização de Computadores

**Professor:** Juan Colonna