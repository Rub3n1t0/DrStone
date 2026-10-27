# Especificação da linguagem DrStone

**Versão:** 0.1 — **Entrega:** especificação da linguagem (20/10).

Documento organizado em cinco partes, com quebras sugeridas para impressão em cinco páginas. A paginação final depende do renderizador de Markdown.

## 1. Propósito, público-alvo e exemplo completo

DrStone é uma linguagem de domínio específico para descrever amostras minerais e solicitar sua identificação por comparação com um catálogo. Seu público-alvo são estudantes de programação, compiladores e mineralogia que desejam representar observações de forma simples e acompanhar as etapas de análise léxica, sintática, semântica e interpretação. Implementada em Python, oferece declarações de amostras, propriedades e um comando de identificação. O resultado indica compatibilidade com referências do catálogo, sem constituir uma determinação laboratorial conclusiva.

### Programa completo, comentado linha a linha

```stone
# Descreve uma amostra e solicita sua identificação no catálogo.
mineral amostra1 {       # Declara a amostra amostra1 e abre seu bloco.
    cor = "incolor"      # Registra a cor observada como texto.
    dureza = 7          # Registra a dureza na escala de Mohs.
    densidade = 2.65    # Registra o valor numérico da densidade.
    brilho = "vitreo"   # Registra o brilho como texto.
}                       # Encerra a declaração da amostra.
identificar amostra1    # Compara a amostra com os minerais do catálogo.
```

O nome `amostra1` identifica uma amostra do programa, não uma espécie já conhecida. As propriedades podem aparecer em qualquer ordem. Ao menos uma deve ser fornecida; não é obrigatório preencher as quatro.

Salve o exemplo em UTF-8, por exemplo como `examples/amostra1.stone`, e execute na raiz do repositório:

```text
python -m drstone.main examples/amostra1.stone
```

Com o catálogo atual, o exemplo apresenta `Quartzo` como mineral mais compatível e compatibilidade `4/4`. A saída mostra a amostra, suas propriedades e os critérios coincidentes. Os candidatos são ordenados pela quantidade de coincidências; empates preservam a ordem do catálogo. Basta uma propriedade coincidir para existir um candidato. Se nenhuma coincidir, a saída informa `Nenhum mineral compatível encontrado.`; isso não constitui erro semântico.

### Convenções gerais

Arquivos usam extensão `.stone`. O código diferencia maiúsculas de minúsculas: `amostra1` e `Amostra1` são nomes distintos. A indentação é livre. A abertura `{` fica na linha da declaração; cada propriedade e o fechamento `}` ocupam linhas próprias. Comandos consecutivos exigem quebra de linha; a última linha pode terminar diretamente no fim do arquivo. Linhas vazias e comentários são permitidos. Não há ponto e vírgula.

<div style="page-break-after: always;"></div>

## 2. Especificação léxica e tabela de tokens

O lexer produz os 14 tipos definidos em `drstone/tokens.py`. Cada token registra tipo, lexema, valor literal quando aplicável, linha e coluna, ambas iniciadas em 1.

| Token | Lexema ou padrão | Papel |
| --- | --- | --- |
| `MINERAL` | `mineral` | Inicia a declaração de uma amostra. |
| `IDENTIFICAR` | `identificar` | Solicita a identificação. |
| `COR` | `cor` | Nome de propriedade textual. |
| `DUREZA` | `dureza` | Nome de propriedade numérica. |
| `DENSIDADE` | `densidade` | Nome de propriedade numérica. |
| `BRILHO` | `brilho` | Nome de propriedade textual. |
| `IDENTIFIER` | `[A-Za-z_][A-Za-z0-9_]*`, exceto os seis lexemas acima | Nome de amostra ou propriedade. |
| `NUMBER` | `-?[0-9]+(\.[0-9]+)?` | Literal inteiro ou decimal. |
| `STRING` | Texto entre aspas duplas | Literal textual, com escapes. |
| `EQUALS` | `=` | Associa um valor à propriedade. |
| `LBRACE` | `{` | Abre o bloco de propriedades. |
| `RBRACE` | `}` | Fecha o bloco de propriedades. |
| `NEWLINE` | Quebra de linha | Separa propriedades e comandos. |
| `EOF` | Fim da entrada, sem lexema | Encerra a sequência de tokens. |

O lexer percorre o nome inteiro antes de consultar as palavras especiais: `mineralogia`, por exemplo, é um único `IDENTIFIER`. Os tokens específicos de `cor`, `dureza`, `densidade` e `brilho` impedem seu uso como nomes de amostras na implementação atual. Outros nomes de propriedade chegam ao parser como `IDENTIFIER` e são rejeitados posteriormente pela semântica.

Espaços e tabulações fora de strings são descartados. Comentários começam com `#` e seguem até o fim da linha, preservando o token `NEWLINE`. Dentro de strings, `#` é texto. Quebras `CRLF` e `CR` são normalizadas para `LF`.

### Literais e escapes

Números usam ponto decimal, sem sinal positivo ou notação científica. Exemplos: `7`, `2.65`, `0` e `-2.65`. O sinal negativo integra o literal; não é um operador aritmético. A semântica decide se o valor é permitido para a propriedade.

Strings permitem Unicode, inclusive texto acentuado, e não atravessam fisicamente uma linha. Os escapes aceitos são `\"` (aspas), `\\` (barra invertida), `\n` (quebra de linha no valor) e `\t` (tabulação no valor). Escapes diferentes e strings sem fechamento geram erro léxico. Strings vazias são aceitas; não há vocabulário fechado de cores ou brilhos.

<div style="page-break-after: always;"></div>

## 3. Gramática em EBNF

Nesta notação, `,` significa concatenação, `|` alternativa, `[ ... ]` opção e `{ ... }` repetição zero ou mais vezes. Terminais entre aspas são lexemas. Os nomes em maiúsculas representam categorias de tokens.

```ebnf
programa       = { NEWLINE }, [ sequencia ], EOF ;
sequencia      = comando, [ NEWLINE, { NEWLINE }, [ sequencia ] ] ;
comando        = declaracao | identificacao ;
declaracao     = "mineral", IDENTIFIER, "{", NEWLINE,
                 { NEWLINE | propriedade, NEWLINE }, "}" ;
identificacao  = "identificar", IDENTIFIER ;
propriedade    = nome_propriedade, "=", valor ;
nome_propriedade = "cor" | "dureza" | "densidade" | "brilho"
                   | IDENTIFIER ;
valor          = NUMBER | STRING ;
```

A sequência recursiva exige pelo menos um `NEWLINE` entre comandos e permite linhas vazias adicionais. O último comando dispensa essa quebra. A gramática aceita programa vazio e bloco vazio; a análise semântica rejeita uma declaração sem propriedades.

As categorias léxicas têm a formação abaixo. A regra `nome` origina `IDENTIFIER` somente quando não corresponde às seis palavras com token próprio. Os terminais de `escape` representam os dois caracteres presentes no código-fonte.

```ebnf
nome           = ( letra | "_" ), { letra | digito | "_" } ;
numero         = [ "-" ], digito, { digito },
                 [ ".", digito, { digito } ] ;
texto          = '"', { caractere_textual | escape }, '"' ;
escape         = '\"' | '\\' | '\n' | '\t' ;
letra          = ? uma letra ASCII de A a Z ou de a a z ? ;
digito         = "0" | "1" | "2" | "3" | "4"
               | "5" | "6" | "7" | "8" | "9" ;
caractere_textual = ? caractere diferente de aspas duplas,
                     barra invertida e quebra de linha ? ;
```

`numero` origina `NUMBER`; `texto` origina `STRING`. Comentários e espaços horizontais são tratados pelo lexer, antes do parser. As produções sintáticas correspondem ao parser recursivo descendente manual de `drstone/parser.py`.

Não existem expressões compostas: depois de `=` deve existir exatamente um literal numérico ou textual. Nomes de amostras não podem ser usados como valores de propriedades. O operador `=` representa associação de propriedade, sem comparação matemática ou alteração posterior da amostra.

<div style="page-break-after: always;"></div>

## 4. Verificação semântica escolhida

A verificação central é a **validação de tipos e limites das propriedades**. Uma estrutura gramaticalmente correta pode conter dados inadequados ao domínio. Após construir a AST e antes de interpretar qualquer comando, o analisador verifica cada propriedade. Não existe conversão implícita: `"7"` é uma string e não substitui o número `7`.

| Propriedade | Tipo aceito | Restrição implementada |
| --- | --- | --- |
| `cor` | String | Qualquer texto, inclusive vazio. |
| `brilho` | String | Qualquer texto, inclusive vazio. |
| `dureza` | Inteiro ou decimal | Entre 1 e 10, inclusive. |
| `densidade` | Inteiro ou decimal | Maior ou igual a zero. |

A implementação aceita densidade zero e não verifica unidades. Usar g/cm³ é a convenção recomendada para comparar medidas com o catálogo; a unidade não é escrita no literal. Exigir densidade estritamente positiva demandaria alterar a implementação.

### Programa que passa

```stone
mineral pedra {
    dureza = 7
    densidade = 2.65
    brilho = "vitreo"
}
identificar pedra
```

Os tipos e valores são permitidos. A amostra é registrada e pode ser identificada. Com o catálogo atual, o resultado indica `Quartzo`, com compatibilidade `3/3`.

### Programa rejeitado e mensagem pretendida

```stone
mineral pedra {
    dureza = 11
}
identificar pedra
```

O lexer aceita `11` como número e o parser aceita a atribuição. A semântica rejeita o valor fora da escala de Mohs. A mensagem pretendida, já produzida pela interface de linha de comando, é:

```text
Erro semântico: Linha 2, coluna 5: dureza deve estar entre 1 e 10
```

A posição aponta para o início de `dureza`, considerando quatro espaços de indentação. A execução termina com código 1 e não identifica a amostra.

### Regras complementares

O analisador percorre os comandos na ordem do arquivo e mantém uma tabela de amostras declaradas. Cada nome deve ser único e precisa existir antes de ser usado em `identificar`. Cada amostra exige ao menos uma propriedade. Propriedades repetidas ou diferentes das quatro conhecidas são rejeitadas. A validação para no primeiro erro. Essas regras estão em `drstone/semantic.py`.

<div style="page-break-after: always;"></div>

## 5. Construções consideradas e não incluídas

**Nota para a equipe:** o repositório não registra o histórico das discussões. As três decisões abaixo são propostas de justificativa coerentes com a versão implementada e precisam ser validadas pela equipe antes de serem apresentadas como decisões efetivamente tomadas.

### 5.1. Expressões aritméticas em propriedades

**Construção considerada:** permitir cálculos como `densidade = 5.30 / 2` diretamente na declaração.

**Decisão proposta:** manter apenas literais numéricos e textuais. Operadores exigiriam precedência, novos nós na AST e verificações como divisão por zero e incompatibilidade de operandos. O objetivo inicial é descrever observações; o usuário pode informar o resultado da medição já calculado. Essa exclusão mantém o foco nas etapas do interpretador e na validação de propriedades minerais.

### 5.2. Condicionais e laços de repetição

**Construção considerada:** incluir comandos equivalentes a `se`, `senao` e `enquanto`, para decidir quais amostras identificar e repetir análises.

**Decisão proposta:** executar declarações e identificações em sequência. O fluxo de controle exigiria expressões booleanas, comparações e blocos aninhados. Para analisar várias amostras, a versão atual permite várias declarações e comandos `identificar`. Isso atende ao uso previsto sem ampliar o projeto para uma linguagem de propósito geral.

### 5.3. Funções definidas pelo usuário

**Construção considerada:** declarar funções com parâmetros e retorno para reutilizar procedimentos de análise.

**Decisão proposta:** manter a comparação com o catálogo como operação interna acionada por `identificar`. Funções exigiriam chamadas, verificação de argumentos, escopos locais e tratamento de retorno. Essas estruturas aumentariam o esforço sem serem necessárias para representar as quatro propriedades previstas. O escopo inicial prioriza uma implementação manual completa e compreensível do fluxo léxico, sintático e semântico.

### Rastreabilidade

Esta especificação se baseia na revisão local `d89e9d4` do [repositório DrStone](https://github.com/Rub3n1t0/DrStone).

| Parte | Arquivos de referência |
| --- | --- |
| Tokens e literais | `drstone/tokens.py`, `drstone/lexer.py` |
| Gramática e AST | `drstone/parser.py`, `drstone/ast_nodes.py` |
| Tipos, limites e nomes | `drstone/semantic.py` |
| Identificação e CLI | `drstone/interpreter.py`, `drstone/main.py` |
| Validação dos exemplos | `tests/test_semantic.py`, `tests/test_interpreter.py` |

Construções futuras devem ser acompanhadas de atualização da gramática, dos tokens e das regras semânticas.
