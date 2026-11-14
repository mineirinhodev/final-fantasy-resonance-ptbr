#!/usr/bin/env python3
# Checks translated files against their input: check.py <name>…   (chunks/in/<name>.json ↔ chunks/out/<name>.json); prints OK or the problems
import json, os, re, sys
ROOT = os.path.join(os.path.dirname(__file__), '..')
TOK = re.compile(r'\{[^{}]*\}|<[^<>]*>|\[TEMP\]')
JA = re.compile(r'[぀-ヿ㐀-鿿]')
def norm(t): return t.replace('”>', '">')   # one source tag is closed with a curly quote
def problems(name):
    src = {str(x['id']): x['en'] for g in json.load(open(f'{ROOT}/chunks/in/{name}.json', encoding='utf-8'))['groups'] for x in g['items']}
    path = f'{ROOT}/chunks/out/{name}.json'
    if not os.path.exists(path): return [f'{name}: no output file']
    try: out = json.load(open(path, encoding='utf-8'))
    except ValueError as e: return [f'{name}: not valid JSON ({e})']
    if not isinstance(out, dict): return [f'{name}: the output must be one JSON object of id → text']
    p = []
    miss = [i for i in src if i not in out]; extra = [i for i in out if i not in src]
    if miss: p.append(f'{name}: {len(miss)} ids missing: {", ".join(miss[:30])}{"…" if len(miss) > 30 else ""}')
    if extra: p.append(f'{name}: ids not in the input: {", ".join(extra[:30])}')
    same = 0
    for i, en in src.items():
        pt = out.get(i)
        if pt is None: continue
        if not isinstance(pt, str) or not pt.strip(): p.append(f'{name} id {i}: empty or not a string'); continue
        if sorted(TOK.findall(norm(en))) != sorted(TOK.findall(norm(pt))): p.append(f'{name} id {i}: placeholders / tags differ: source {TOK.findall(en)} ≠ yours {TOK.findall(pt)}')
        if en.count('\r\n') != pt.count('\r\n') or en.count('\n') != pt.count('\n'): p.append(f'{name} id {i}: line breaks differ (source {en.count(chr(13) + chr(10))} CRLF, {en.count(chr(10)) - en.count(chr(13) + chr(10))} LF; yours {pt.count(chr(13) + chr(10))} CRLF, {pt.count(chr(10)) - pt.count(chr(13) + chr(10))} LF)')
        if '\r' in pt.replace('\r\n', ''): p.append(f'{name} id {i}: a lone carriage return')
        if JA.search(pt) or '¿' in pt or '¡' in pt: p.append(f'{name} id {i}: Japanese characters or ¿ ¡ in the translation')
        if (en[:1] == ' ') != (pt[:1] == ' ') or (en[-1:] == ' ') != (pt[-1:] == ' '): p.append(f'{name} id {i}: leading / trailing space differs from the source')
        le = max(len(l) for l in en.split('\n')); lp = max(len(l) for l in pt.split('\n'))
        if lp > max(le * 1.35 + 6, 24) and '\n' in en: p.append(f'{name} id {i}: longest line {lp} characters, the source\'s is {le}: rebalance the lines or shorten')
        if len(pt) > max(len(en) * 1.7 + 12, 30): p.append(f'{name} id {i}: {len(pt)} characters for a source of {len(en)}: shorten')
        if pt == en and len(re.findall(r'\b[a-z]{3,}\b', en)) >= 3: same += 1; p.append(f'{name} id {i}: left in English')
    return p
if __name__ == '__main__':
    bad = 0
    for name in sys.argv[1:]:
        p = problems(name); bad += len(p)
        print('\n'.join(p[:60]) + (f'\n… and {len(p) - 60} more' if len(p) > 60 else '') if p else f'{name}: OK')
    sys.exit(1 if bad else 0)
