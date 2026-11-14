#!/usr/bin/env python3
# One pass over chunks/out/*.json that makes the translators' renderings of recurring terms agree (run once after all files are translated; safe to rerun)
import glob, json, os, re
ROOT = os.path.join(os.path.dirname(__file__), '..')
ALL = [  # (pattern, replacement) on every string
    (r'Veritas da Chama', 'Veritas do Fogo'), (r'Carne Molenga', 'Carne Pastosa'), (r'Caverna de Rubi\b', 'Caverna dos Rubis'), (r'Cristais de Visão', 'Cristais de Vision'),
    (r'expulsa-Victoria', 'evic-toria'), (r'Vovozinha', 'Babushka'), (r'Pântano Sem Volta', 'Pântano Sem Retorno'), (r'adamandélion', 'adamandelion'),
    (r'Sétima Alvorada', 'Sétimo Alvorecer'), (r'potência de atordoamento', 'poder de atordoamento'), (r'Potência de atordoamento', 'Poder de atordoamento'),
    (r'Selo Divino', 'Sinete Divino'), (r'selo divino', 'sinete divino'), (r'pique-esconde', 'pega-pega'), (r'pique-pega', 'pega-pega'), (r'Pique-esconde', 'Pega-pega'),
    (r'magi-antena', 'magitena'), (r'Magi-antena', 'Magitena'), (r'\bgil\b', 'Gil'), (r'atordoamento abrangente', 'atordoamento total'),
    (r'Estilhaço de Tabuleta', 'Fragmento de Tábula'), (r'Estilhaços de Tabuleta', 'Fragmentos de Tábula'), (r'estilhaço de tabuleta', 'fragmento de tábula'), (r'estilhaços de tabuleta', 'fragmentos de tábula'),
    (r'Fragmentos de Tábua', 'Fragmentos de Tábula'), (r'fragmentos de tábua\b', 'fragmentos de tábula'), (r'tábua quebrada', 'tábula quebrada'),
    (r'Fortalecimentos e Enfraquecimentos', 'Buffs e Debuffs'), (r'fortalecimentos ou enfraquecimentos', 'buffs ou debuffs'), (r'Fortalecimento e Enfraquecimento', 'Buff e Debuff'),
]
BUFF = {'14956', '14959', '14972', '14955', '14949', '14958', '14950', '14884', '16082', '16078', '15674', '15939', '21516', '21621', '21610'}   # bônus / penalidade → buff / debuff
VISION = set('1388 1402 1408 1395 1404 1415 1403 1467 1466 1517 1507 1499 1502 1508 13499 13603 13798 14235 14435 14516 14411 17320 20282 20281 20292 20298 20356 20358 20360 20359 20363 20366 20414 20416 20430 20455 20458 20472'.split())   # the game's Visions, written as a common noun
ONE = {'20995': 'Quebrador', '20994': 'Médico', '21559': 'Ganha um buff após consumir a presa.'}
def fix(i, t):
    for a, b in ALL: t = re.sub(a, b, t)
    if i in BUFF:
        for a, b in (('das penalidades', 'dos debuffs'), ('penalidades', 'debuffs'), ('penalidade', 'debuff'), ('bônus', 'buffs')): t = t.replace(a, b)
    if i in VISION: t = re.sub(r'\b[Vv]isões\b', 'Visions', re.sub(r'\b[Vv]isão\b', 'Vision', t))
    if i == '5136': t = t.replace('do <text style="italic">Invencível', 'da <text style="italic">Invincible')
    if i == '5500': t = re.sub(r'\bo (<text style="italic">)Invencível', r'a \1Invincible', t)
    return ONE.get(i, t)
n = 0
for f in sorted(glob.glob(f'{ROOT}/chunks/out/*.json')):
    d = json.load(open(f, encoding='utf-8')); e = {i: fix(i, t) for i, t in d.items()}
    if e != d:
        n += sum(e[i] != d[i] for i in d); json.dump(e, open(f, 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
print(n, 'strings changed')
