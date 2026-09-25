# DrStone

DrStone e um projeto academico de uma pequena linguagem de programacao voltada
para a identificacao de rochas e minerais. O projeto sera implementado em Python
e apresentara manualmente as principais etapas de um compilador/interpretador.

## Estrutura inicial

```text
drstone/
    lexer.py
    tokens.py
    parser.py
    ast_nodes.py
    semantic.py
    interpreter.py
    minerals.py
    main.py
examples/
    quartzo.stone
    calcita.stone
    desconhecido.stone
tests/
    test_lexer.py
    test_parser.py
    test_semantic.py
    test_interpreter.py
    test_minerals.py
    test_main.py
README.md
```

## Responsabilidade dos arquivos

- `drstone/tokens.py`: definira os tipos de token e os dados associados a cada
  token reconhecido na linguagem.
- `drstone/lexer.py`: convertera o texto de um programa em uma sequencia de
  tokens.
- `drstone/parser.py`: verificara a estrutura gramatical dos tokens e construira
  a AST.
- `drstone/ast_nodes.py`: reunira as classes que representam os nos da AST.
- `drstone/semantic.py`: validara regras semanticas, como tipos, propriedades e
  referencias a minerais.
- `drstone/interpreter.py`: percorrera a AST para executar o programa e produzir
  o resultado da identificacao.
- `drstone/minerals.py`: armazena 100 gemas/variedades importadas da base
  gemologica, alem de seis referencias genericas mantidas para compatibilidade.
- `drstone/main.py`: e o ponto de entrada e coordena todas as etapas do
  interpretador.
- `examples/quartzo.stone`: contera um programa de exemplo para quartzo.
- `examples/calcita.stone`: contera um programa de exemplo para calcita.
- `examples/desconhecido.stone`: contera um caso sem identificacao conhecida.
- `tests/test_lexer.py`: testara a conversao de texto em tokens.
- `tests/test_parser.py`: testara a analise sintatica e a construcao da AST.
- `tests/test_interpreter.py`: testara a execucao dos programas e seus resultados.

## Execucao

Na raiz do projeto, execute um programa `.stone` com:

```text
python -m drstone.main examples/quartzo.stone
```

Tambem e possivel informar as propriedades diretamente na linha de comando:

```text
python -m drstone.main --dureza 7 --densidade 2.65 --brilho vitreo --cor incolor
```

O nome da amostra e `amostra` por padrao. Para altera-lo, use `--nome`:

```text
python -m drstone.main --nome pedra --dureza 7 --densidade 2.65
```

O modo direto aceita qualquer combinacao com ao menos uma das propriedades
`--dureza`, `--densidade`, `--cor` e `--brilho`. Ele utiliza o mesmo fluxo de
analise do arquivo `.stone`.

## Fluxo

```text
Arquivo .stone -> Lexer -> Tokens -> Parser -> AST
               -> Analise semantica -> Interpretador -> Resultado
```

O projeto implementa manualmente lexer, parser recursivo descendente, AST,
analise semantica e interpretacao.

A sintaxe oficial inicial esta descrita em [`ESPECIFICACAO.md`](ESPECIFICACAO.md).
