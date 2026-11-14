# FINAL FANTASY RESONANCE — Tradução PT-BR (não oficial)

Mod que traduz os textos de **FINAL FANTASY RESONANCE** (Nintendo Switch, title ID `0100606026F12000`) para
**português do Brasil**. O jogo não tem português; este mod coloca a tradução no lugar do texto em inglês.

- Interface, menus, itens, equipamentos, técnicas, tutoriais, missões e todos os diálogos da história.
- 20.103 textos traduzidos (cerca de 209 mil palavras no original).
- Acentos funcionam com as fontes do próprio jogo; nenhuma fonte é trocada.
- Vozes, vídeos e textos desenhados em imagens continuam como no original.

> **Aviso:** a tradução ainda **não passou por uma revisão completa linha a linha** dentro do jogo. Há um guia de
> estilo, um glossário e um verificador automático, mas espere inconsistências e frases estranhas aqui e ali.
> Correções são bem-vindas: veja [Como contribuir](#como-contribuir).

## Download

Baixe o arquivo `FFResonance-PTBR.zip` na página de [Releases](../../releases/latest).

Dentro dele há uma pasta `Traducao PT-BR` com esta estrutura:

```
Traducao PT-BR/
└── romfs/FFRS/Content/Paks/
    ├── FFRS-Switch_P.pak
    ├── FFRS-Switch_P.utoc
    └── FFRS-Switch_P.ucas     (vazio, mas necessário)
```

Os três arquivos precisam ficar juntos. Sem o `.utoc`, o jogo ignora o `.pak`.

## Instalação

Em qualquer caso, **deixe o idioma do jogo em inglês** (é o padrão): o português aparece no lugar dele.

### NX Library (Mac)

1. Copie a pasta `Traducao PT-BR` para
   `/Applications/NxNative_Data/AppSupport/0100606026F12000/mods/`
2. Abra o NX Library, entre em FINAL FANTASY RESONANCE → **Mods** e ligue `Traducao PT-BR`.
3. Inicie o jogo.

Este é o único ambiente em que o mod foi testado.

### Switch com Atmosphère

Copie a pasta `romfs` do zip para o cartão SD em

```
atmosphere/contents/0100606026F12000/romfs/
```

de modo que os arquivos fiquem em `atmosphere/contents/0100606026F12000/romfs/FFRS/Content/Paks/`. Não testado.

### Outros emuladores

Emuladores que aceitam mods no formato `romfs` costumam usar uma pasta de mods por jogo: abra-a pelo menu do emulador
(algo como "Abrir diretório de mods") e copie a pasta `Traducao PT-BR` inteira para lá. Não testado.

### Desinstalar

Desligue o mod no emulador ou apague a pasta. Nada no jogo nem no save é alterado.

## Compatibilidade

- Feito sobre a versão base do jogo (v0). Uma atualização que mude os textos pode deixar linhas novas em inglês ou
  trocadas; nesse caso o mod precisa ser refeito a partir dos arquivos da versão nova.
- O mod só substitui `FFRS/Content/Localization/Game/en/Game.locres`. Os outros idiomas não são tocados.

## Escolhas de tradução

Ficam como no original:

- nomes de personagens, lugares, nações e espers;
- magias clássicas da série (Fire / Fira / Firaga, Cure, Haste, Slow, Raise…);
- siglas e termos de sistema: HP, MP, LB, EXP, ATK, DEF, MAG, SPR, Gil, Vision, Limit Burst, buff / debuff;
- inimigos clássicos (Bomb, Goblin, Cactuar, Tonberry, Malboro, Behemoth…).

São traduzidos:

- itens e equipamentos (Poção, Pena de Fênix, Espada de Mithril…);
- técnicas com nome descritivo, estados alterados (Veneno, Sono, Silêncio…), elementos;
- interface, tutoriais, missões e diálogos.

O guia completo, com a tabela de termos, está em [`GUIA.md`](GUIA.md) (em inglês, porque é o texto dado aos tradutores).

## Limitações conhecidas

- O jogo guarda cada texto idêntico em inglês uma única vez, então a mesma frase em dois contextos recebe a mesma
  tradução. Os casos encontrados foram separados à mão (por exemplo "Slow", que é a magia e também a velocidade
  "Lento" nas opções); pode haver outros.
- O gênero de quem fala ou de quem ouve foi deduzido pelo contexto e pela versão oficial em espanhol; pode estar
  errado em algumas falas.
- Algumas linhas podem ficar mais largas que a caixa de texto.
- Só a tela de título e o menu de opções foram conferidos dentro do jogo. O restante foi validado apenas pelo
  verificador automático (variáveis, marcações e quebras de linha iguais às do original).

## Como contribuir

Achou um erro? Abra uma [issue](../../issues) com a frase como aparece no jogo (uma captura de tela ajuda) ou mande
um pull request.

A tradução fica em `chunks/out/*.json`. Cada arquivo é um objeto `{"id": "texto em português"}`, em que `id` é a
posição do texto na tabela do jogo. Arquivos `n…` são nomes e termos; arquivos `t…` são o restante, na ordem das
cenas. Para corrigir uma frase, procure-a nesses arquivos e edite o valor, mantendo:

- tudo o que está entre chaves (`{Effect1Turn}`) e as marcações (`<text style="italic">…</>`) exatamente iguais;
- a mesma quantidade de quebras de linha (`\r\n` / `\n`).

## Como remontar o mod

Este repositório **não contém arquivos do jogo**. Para remontar você precisa do seu próprio dump:

1. Extraia `FFRS/Content/Localization/Game/en/Game.locres` de `FFRS-Switch.pak` (RomFS do jogo; o pak usa compressão
   Oodle) e salve como `orig/en.locres`.
2. Rode:

   ```
   python3 tools/build.py "caminho/para/Traducao PT-BR"
   ```

   Requer apenas Python 3, sem dependências.

Scripts em `tools/`:

| Script | Função |
|---|---|
| `build.py` | aplica `chunks/out` sobre `orig/en.locres` e grava o `.pak`, o `.utoc` e o `.ucas` |
| `locres.py` | leitor / gravador do formato `.locres` (versão 3) |
| `mkpak.py` | gravador de `.pak` do Unreal (versão 11, sem compressão) |
| `export.py` | divide o texto original em arquivos de tradução `chunks/in` (precisa também de `orig/es.locres`) |
| `check.py` | compara `chunks/out` com `chunks/in`: ids, variáveis, marcações, quebras e largura das linhas |
| `unify.py` | passada única que unificou termos divergentes entre os arquivos |

### Detalhe técnico

O jogo usa Unreal Engine 5.6. Um pak de patch (`FFRS-Switch_P.pak`) sozinho é aberto e depois ignorado: o motor só
monta o pak quando existe um contêiner IoStore com o mesmo nome. Por isso o mod leva um `FFRS-Switch_P.utoc` com
cabeçalho válido e zero entradas, e um `FFRS-Switch_P.ucas` vazio.

## Aviso legal

Projeto de fã, sem fins lucrativos, sem vínculo com a Square Enix. FINAL FANTASY e FINAL FANTASY RESONANCE são marcas
e propriedade de seus respectivos donos. O mod não inclui o jogo nem seus arquivos originais e só funciona com uma
cópia sua, obtida legalmente. Os scripts em `tools/` estão sob a licença MIT (veja [`LICENSE`](LICENSE)).
