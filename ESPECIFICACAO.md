# Especificacao da linguagem DrStone

Esta e a especificacao inicial da linguagem DrStone, versao 0.1. Um programa
DrStone descreve amostras minerais por meio de propriedades e solicita sua
identificacao.

## Exemplo

```stone
mineral amostra1 {
    cor = "incolor"
    dureza = 7
    densidade = 2.65
    brilho = "vitreo"
}

identificar amostra1
```

Arquivos escritos em DrStone usam a extensao `.stone` e codificacao UTF-8. A
linguagem diferencia letras maiusculas de minusculas. Assim, `amostra1` e
`Amostra1` sao identificadores diferentes.

## Palavras reservadas

| Palavra | Funcao |
| --- | --- |
| `mineral` | Inicia a declaracao de uma amostra mineral. |
| `identificar` | Solicita a identificacao de uma amostra declarada. |

Palavras reservadas nao podem ser usadas como nomes de amostras ou propriedades.

O lexer tambem reconhece `cor`, `dureza`, `densidade` e `brilho` como palavras
do dominio, produzindo tokens especificos para tornar o resultado da analise
lexica mais didatico. Outros nomes de propriedade continuam sendo reconhecidos
como identificadores comuns.

## Identificadores

Identificadores nomeiam amostras e propriedades. Eles devem:

- comecar com uma letra sem acento (`A-Z` ou `a-z`) ou sublinhado (`_`);
- continuar com letras, algarismos (`0-9`) ou sublinhados;
- nao ser uma palavra reservada.

Forma simplificada:

```text
[A-Za-z_][A-Za-z0-9_]*
```

Exemplos validos: `amostra1`, `dureza`, `cor_primaria`, `_codigo`.

Exemplos invalidos: `1amostra`, `cor-principal`, `mineral`.

## Numeros

Numeros podem ser inteiros ou decimais, positivos ou negativos. O separador
decimal e o ponto.

Forma simplificada:

```text
-?[0-9]+(\.[0-9]+)?
```

Exemplos validos: `7`, `0`, `2.65`, `10.0`, `-2.65`.

Nesta versao, o sinal negativo e aceito para permitir que a analise semantica
valide limites. O sinal positivo, a notacao cientifica e a virgula decimal nao
sao aceitos.

## Strings

Strings representam valores textuais e devem aparecer entre aspas duplas. Elas
nao podem ocupar mais de uma linha.

```stone
cor = "incolor"
brilho = "vitreo"
```

As sequencias de escape previstas sao:

| Sequencia | Significado |
| --- | --- |
| `\"` | Aspas duplas dentro da string. |
| `\\` | Barra invertida. |
| `\n` | Quebra de linha no valor da string. |
| `\t` | Tabulacao no valor da string. |

## Operadores

A versao 0.1 possui apenas o operador `=`, usado para associar um valor a uma
propriedade.

```stone
dureza = 7
```

O operador representa atribuicao de propriedade, nao comparacao matematica.

## Simbolos

| Simbolo | Funcao |
| --- | --- |
| `{` | Abre o bloco de propriedades de uma amostra. |
| `}` | Fecha o bloco de propriedades de uma amostra. |
| Quebra de linha | Separa declaracoes e propriedades. |

Espacos e tabulacoes podem ser usados para identacao e ao redor de `=`. A
identacao melhora a leitura, mas nao altera o significado do programa.

Cada propriedade deve ocupar sua propria linha. A chave de abertura deve ficar
na linha da declaracao, e a chave de fechamento deve ficar em uma nova linha.
Ponto e virgula nao faz parte da sintaxe.

## Comentarios

Um comentario comeca com `#` e continua ate o fim da linha. Comentarios podem
ocupar uma linha inteira ou aparecer depois de uma instrucao.

```stone
# Amostra encontrada em uma rocha ignea
mineral amostra1 {
    dureza = 7       # Escala de Mohs
    brilho = "vitreo"
}
```

O marcador `#` dentro de uma string e parte do texto e nao inicia um comentario.

## Gramatica simplificada

A gramatica abaixo usa uma notacao semelhante a EBNF. Chaves indicam repeticao,
colchetes indicam um elemento opcional e `|` indica alternativas.

```ebnf
programa             = { fim_de_linha | comando }, EOF ;

comando              = declaracao_mineral
                     | comando_identificar ;

declaracao_mineral   = "mineral", identificador, "{", fim_de_linha,
                       { fim_de_linha | propriedade, fim_de_linha },
                       "}" ;

propriedade          = identificador, "=", valor ;

comando_identificar  = "identificar", identificador,
                       [ fim_de_linha ] ;

valor                = numero | string ;

identificador        = ( letra | "_" ),
                       { letra | digito | "_" } ;

numero               = [ "-" ], digito, { digito },
                       [ ".", digito, { digito } ] ;

string               = '"', { caractere | escape }, '"' ;

escape               = '\\"' | '\\\\' | '\\n' | '\\t' ;
fim_de_linha         = NEWLINE ;
```

Comentarios e espacos horizontais nao aparecem na gramatica porque serao
tratados durante a analise lexica. A quebra de linha, por outro lado, e
significativa e separa propriedades e comandos.

## Regras estruturais e semanticas iniciais

- Uma amostra deve ser declarada antes de ser identificada.
- O nome de cada amostra deve ser unico no programa.
- Uma propriedade nao pode ser repetida dentro da mesma amostra.
- Uma amostra deve possuir pelo menos uma propriedade.
- As quatro propriedades basicas possuem tokens proprios. Outros nomes de
  propriedade sao identificadores, e o analisador semantico decidira se sao
  reconhecidos e quais tipos de valor aceitam.
- O comando `identificar` recebe exatamente um identificador de amostra.

Essas regras complementam a gramatica: algumas construcoes podem ser
sintaticamente validas, mas rejeitadas posteriormente pela analise semantica.
