#!/usr/bin/env python3
# Splits the English text table into translation files (chunks/in/<name>.json), each with the Spanish text as a reference.
# Usage: export.py names           the name / term namespaces (files n001…), translated first: their results are the glossary
#        export.py text            everything else (files t001…), each file with the glossary entries its text mentions
import collections, glob, json, os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
import locres
ROOT = os.path.join(os.path.dirname(__file__), '..')
NAMES = re.compile(r'(Name|NAME|Title|Word)')
JA = re.compile(r'[぀-ヿ㐀-鿿＀-￯]')
LIMIT = 14000
def nat(s): return [int(p) if p.isdigit() else p.lower() for p in re.split(r'(\d+)', s)]
def load():
    en = locres.load(open(f'{ROOT}/orig/en.locres', 'rb').read()); es = locres.load(open(f'{ROOT}/orig/es.locres', 'rb').read())
    est = {(ns, k): es['strings'][i][0] for _, ns, keys in es['namespaces'] for _, k, _, i in keys}
    owner, refs = {}, collections.defaultdict(list)
    for _, ns, keys in sorted(en['namespaces'], key=lambda n: nat(n[1])):
        for _, k, _, i in sorted(keys, key=lambda k: nat(k[1])):
            owner.setdefault(i, (ns, k)); refs[i].append(est[(ns, k)])
    return en, owner, refs
def wanted(t): return bool(re.search(r'[A-Za-z]', t)) and not JA.search(t)
def items(names):
    en, owner, refs = load(); groups = collections.OrderedDict()
    for i, (ns, k) in owner.items():
        t = en['strings'][i][0]
        if not wanted(t) or bool(NAMES.search(ns)) != names: continue
        es = next((r for r in refs[i] if not JA.search(r)), '')
        groups.setdefault(ns, []).append(dict(id=i, en=t, es=es))
    return groups
def glossary():
    en = locres.load(open(f'{ROOT}/orig/en.locres', 'rb').read())['strings']; g = {}
    for f in sorted(glob.glob(f'{ROOT}/chunks/out/n*.json')):
        for i, pt in json.load(open(f, encoding='utf-8')).items():
            e = en[int(i)][0]
            if 4 <= len(e) <= 40 and '\n' not in e and e != pt: g.setdefault(e, pt)
    return g
def main(mode):
    names = mode == 'names'; groups = items(names); gl = {} if names else glossary()
    files, cur, size = [], [], 0
    for ns, its in groups.items():
        n = sum(len(x['en']) for x in its)
        if size and size + n > LIMIT: files.append(cur); cur, size = [], 0
        part = []
        for x in its:   # a namespace longer than a file is cut between strings
            if size and size + len(x['en']) > LIMIT:
                if part: cur.append(dict(ns=ns, items=part)); part = []
                files.append(cur); cur, size = [], 0
            part.append(x); size += len(x['en'])
        if part: cur.append(dict(ns=ns, items=part))
    if cur: files.append(cur)
    for old in glob.glob(f'{ROOT}/chunks/in/{"n" if names else "t"}*.json'): os.remove(old)
    words = sorted(gl, key=len, reverse=True)
    for n, gs in enumerate(files, 1):
        name = f'{"n" if names else "t"}{n:03d}'; doc = dict(file=name)
        if gl:
            text = '\n'.join(x['en'] for g in gs for x in g['items']); found = {}
            for w in words:
                if w in text and re.search(r'(?<![A-Za-z])' + re.escape(w) + r'(?![a-z])', text): found[w] = gl[w]
                if len(found) >= 120: break
            doc['glossary'] = found
        doc['groups'] = gs
        with open(f'{ROOT}/chunks/in/{name}.json', 'w', encoding='utf-8') as f:
            f.write('{"file": %s,\n' % json.dumps(name))
            if gl: f.write('"glossary": %s,\n' % json.dumps(doc['glossary'], ensure_ascii=False))
            f.write('"groups": [\n')
            for gi, g in enumerate(gs):
                f.write('{"ns": %s, "items": [\n' % json.dumps(g['ns']))
                f.write(',\n'.join(json.dumps(x, ensure_ascii=False) for x in g['items']))
                f.write('\n]}%s\n' % (',' if gi < len(gs) - 1 else ''))
            f.write(']}\n')
    tot = sum(len(x['en']) for gs in files for g in gs for x in g['items'])
    print(mode, len(files), 'files,', sum(len(g['items']) for gs in files for g in gs), 'strings,', tot, 'chars')
if __name__ == '__main__': main(sys.argv[1])
