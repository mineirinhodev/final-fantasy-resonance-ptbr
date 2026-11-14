# FINAL FANTASY RESONANCE → Brazilian Portuguese: translator's guide

You translate game text from **English** into **Brazilian Portuguese (pt-BR)**. Each input file is
`chunks/in/<name>.json`; you write `chunks/out/<name>.json`.

## Input

```
{"file": "t012",
 "glossary": {"Mythril Sword": "Espada de Mithril", ...},      (only in t-files)
 "groups": [ {"ns": "ST_C01_101_01", "items": [ {"id": 1234, "en": "...", "es": "..."}, ... ]}, ... ]}
```

- `en` is the source. `es` is the official Spanish text of the same line: use it **only** to settle gender,
  number, who is being addressed and ambiguous words. Never translate from the Spanish, never copy its wording
  (no "portunhol"), and ignore it where it is empty or says something else.
- `ns` is the string table: it tells you what the text is (`ST_C01_…` main story dialogue of chapter 1 in scene
  order, `ST_ChrEv…` / `ST_SubEv…` character and side events, `ST_SkillDescription`, `ST_EquipmentName`, `ST_UI_…`
  interface words, `…Summary` quest log prose, and so on). Items of one group are consecutive lines of one scene:
  read the group as a conversation before translating it.
- `glossary` lists names that occur in this file with the translation already in the game. **Use them exactly**
  (adjusting only case, plural and article).

## Output

One JSON object, every `id` of the input as a string key, the translation as the value, nothing else:

```
{"1234": "…", "1235": "…"}
```

Write it with the Write tool (UTF-8, real accented letters, `\r\n` and `\n` as JSON escapes). Then run

```
python3 tools/check.py <name>
```

and fix everything it reports, until it prints `OK`. Do not edit anything outside `chunks/out/`.

## Hard rules (the checker enforces them)

1. Every id translated; no id added.
2. Keep **verbatim**: `{Placeholders}` (never translate the name inside the braces), tags such as
   `<text style="italic">…</>`, `<text style="bold">…</>`, `<IA tag="…"/>`, and the marker `[TEMP]`.
   The words between an opening tag and `</>` are translated.
3. Line breaks: the same kind (`\r\n` stays `\r\n`, `\n` stays `\n`) and the **same number** of them. They are
   manual wraps of a text box: move the break to where the Portuguese sentence divides naturally and keep the lines
   of similar length. No line much longer than the longest line of the English text (about +25% at most): if the
   Portuguese runs long, rephrase more concisely.
4. Keep leading / trailing spaces and the full-width space `　` where the source has them.
5. Typography as in the source: curly quotes “ ” ‘ ’, the ellipsis as the source writes it (`...` or `…`),
   dashes `—`. Portuguese has no `¿` or `¡`.
6. Names in lowercase or plural in the source (`silver keys`, `suits of crystal armor`) are grammatical forms
   inserted into sentences: translate in the same form (`chaves de prata`, `armaduras de cristal`), without article.
7. Title case: Portuguese capitalizes only the first word and proper nouns in sentences and descriptions. Names of
   items, equipment, skills, enemies and places keep capitals on the main words (`Espada de Mithril`,
   `Golpe Poderoso`, `Templo da Terra`); prepositions and articles stay lowercase.

## Style

- Natural, idiomatic Brazilian Portuguese, the register of a professional game localization: `você` (never `tu`
  / `vós`), contractions and spoken rhythm in dialogue (`tá` / `pra` only for clearly rough or childish speakers),
  formal speech for nobles, soldiers addressing superiors and the like (`senhor`, `Vossa Majestade`, `Alteza`).
  Keep each character's voice: archaic stays elevated, slang stays slang, jokes and puns are recreated, not explained.
- Translate meaning, not words. Interjections become Portuguese ones (`Ugh` → `Argh` / `Aff`, `Huh?` → `Hã?`,
  `Hmph` → `Hmpf`, `Phew` → `Ufa`, `Whoa` → `Uau` / `Opa`, `Tsk` stays).
- Interface text is short and imperative-free where Portuguese UI convention uses the infinitive
  (`Save` → `Salvar`, `Load` → `Carregar`, `Equip` → `Equipar`, `Back` → `Voltar`, `Confirm` → `Confirmar`).
- Skill and effect descriptions: terse and uniform. `Deals fire damage to one enemy.` → `Causa dano de fogo a um
  inimigo.` `Restores HP to all allies.` → `Restaura HP de todos os aliados.` `for {Effect1Turn} turns` →
  `por {Effect1Turn} turnos`. `Increases ATK by {Effect1Param1}%` → `Aumenta ATK em {Effect1Param1}%`.

## Terminology

Keep unchanged (series terms and proper nouns):

- Names of people, espers / summons, places, nations and organizations (Rain, Lasswell, Fina, Grandshelt, Olderion,
  Ifrit, Ramuh…), and words the setting coins (Gil, Esper, Vision, Chocobo, Moogle, Mog, Magicite → `Magicita`
  is the exception, Mythril → `Mithril`).
- Stat and system abbreviations: HP, MP, LB, EXP, ATK, DEF, MAG, SPR, Lv.
- Traditional spell names: Fire / Fira / Firaga, Blizzard / Blizzara / Blizzaga, Thunder / Thundara / Thundaga,
  Water…, Aero…, Stone…, Cure / Cura / Curaga, Raise, Esuna, Dispel, Protect, Shell, Haste, Slow, Stop, Regen,
  Reflect, Bio, Holy, Flare, Meteor, Ultima, Libra, Osmose, Drain, Banish. Descriptive skill names are translated
  (`Power Strike` → `Golpe Poderoso`).

Translate consistently:

| English | Portuguese |
|---|---|
| Potion / Hi-Potion / X-Potion | Poção / Hiperpoção / Megapoção |
| Ether / Elixir / Megalixir | Éter / Elixir / Megalixir |
| Phoenix Down | Pena de Fênix |
| Antidote / Eye Drops / Echo Herbs / Gold Needle / Remedy / Tent | Antídoto / Colírio / Ervas de Eco / Agulha de Ouro / Panaceia / Tenda |
| Poison / Blind / Sleep / Silence / Paralysis / Confusion / Petrify / Disease | Veneno / Cegueira / Sono / Silêncio / Paralisia / Confusão / Petrificação / Doença |
| Stagger, Staggered / Break | Atordoamento, Atordoado / Quebra |
| fire / ice / lightning / water / wind / earth / light / dark (elements) | fogo / gelo / raio / água / vento / terra / luz / trevas |
| Limit Burst | Limit Burst |
| White Magic / Black Magic / Green Magic | Magia Branca / Magia Negra / Magia Verde |
| ability, abilities / skill / passive | habilidade(s) / técnica / passiva |
| equipment / weapon / armor / accessory | equipamento / arma / armadura / acessório |
| sword / greatsword / katana / dagger / staff / rod / bow / spear / axe / hammer / fist / whip / gun / mace / harp / throwing weapon | espada / espadão / katana / adaga / cajado / cetro / arco / lança / machado / martelo / manopla / chicote / arma de fogo / maça / harpa / arma de arremesso |
| shield / helm / hat / armor (heavy) / robe / clothes | escudo / elmo / chapéu / armadura / manto / traje |
| party / ally, allies / enemy, enemies / foe | grupo / aliado(s) / inimigo(s) / inimigo |
| quest / side quest / main quest | missão / missão secundária / missão principal |
| chapter / prologue / epilogue | capítulo / prólogo / epílogo |
| turn / chain / critical hit / evade / counter | turno / cadeia / golpe crítico / esquiva / contra-ataque |
| save / load / autosave / options / settings | salvar / carregar / salvamento automático / opções / configurações |
| inn / shop / colosseum / bulletin board / airship | estalagem / loja / coliseu / quadro de avisos / aeronave |
| knight / soldier / king / queen / prince / princess / sage / veritas | cavaleiro / soldado / rei / rainha / príncipe / princesa / sábio / Veritas |
| the Sworn Six of Paladia / Veritas of the Dark (…) | os Seis Juramentados de Paladia / Veritas das Trevas (…da Luz, do Fogo, da Água, da Terra, do Raio…) |
| crystal / Earth Crystal / Earth Shrine | cristal / Cristal da Terra / Templo da Terra |

## Decisions already made in the names (follow them)

- `skill(s)` → `técnica(s)` (Técnicas de Aileen), `abilities` → `habilidades`, Spellblade → Lâmina Mágica, Dualcast → Magia Dupla,
  Job → Classe, Mastery → Maestria (MR / MRP stay), Counter → Contra-Ataque, Evasion → Esquiva, Summon → Invocar.
- Every Final Fantasy spell and status-spell name stays in English (also Arise, Reraise, Gravity, Death, Berserk, Bravery, Faith,
  Deprotect, Deshell, Sleepga…). Status conditions in prose are translated (Veneno, Sono…); Charm → Encanto, Doom → Sentença.
- Nationalities → `de` + place (Hessian soldier → soldado de Hess, Aldorian → de Aldore, Zoldaadian → de Zoldaad, Mysidian → de Mysidia).
- Places: Shrine → Templo, Sanctum → Santuário, Cave / Cavern → Caverna, Town of X → Cidade de X, Village of X → Vila de X,
  Kingdom → Reino, Grandshelt Isles → Ilhas de Grandshelt, Aquapolis → Aquápolis, Colosseum → Coliseu. Mysidia keeps its spelling.
- Classic enemies keep their names (Bomb, Goblin, Cactuar, Tonberry, Malboro, Behemoth, Flan…); Magitek, Mechabo, Vision, Esper stay.
- Dark: creatures → Sombrio (Bahamut Sombrio); the element / the Veritas → das Trevas. Warrior of Light → Guerreiro da Luz.
- Sizes (S)/(M)/(L)/(XL) → (P)/(M)/(G)/(GG). Quest Accepted / Completed → Missão Aceita / Concluída. Clear → Concluir.
- Magicite Shard → Estilhaço de Magicita, Resonance Stone → Pedra de Ressonância, X-Potion → Megapoção, Phoenix Pinion → Asa de Fênix.
