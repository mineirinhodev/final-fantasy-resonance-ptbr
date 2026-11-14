#!/usr/bin/env python3
# Builds the mod from the translated files: build.py [<mod folder>]
#   chunks/out/*.json (id → Portuguese text) replace the strings of orig/en.locres; the table goes into FFRS-Switch_P.pak as the game's English text
#   (FFRS/Content/Localization/Game/en/Game.locres), beside an empty IoStore container of the same name: Unreal 5.6 mounts a pak only with its .utoc.
# The game then shows Portuguese whenever its language is English (the default).
import glob, json, os, struct, sys
sys.path.insert(0, os.path.dirname(__file__))
import locres, mkpak
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
def table():
    d = locres.load(open(f'{ROOT}/orig/en.locres', 'rb').read()); n = 0
    for f in sorted(glob.glob(f'{ROOT}/chunks/out/*.json')):
        for i, pt in json.load(open(f, encoding='utf-8')).items():
            i = int(i)
            if isinstance(pt, str) and pt.strip() and pt != d['strings'][i][0]: d['strings'][i] = (pt, d['strings'][i][1]); n += 1
    return d, n
# Keys that share their English string with a kept spell name but mean something else: (namespace, key) → text of their own
OWN = {('ST_UI_Option_Common', 'RadioButton_Late'): 'Lento', ('ST_UI_Libra', 'UI_Libra_Race_Stone'): 'Pedra', ('ST_UI_BattleDamageProp', 'UIBtlProp_InstantDeath'): 'Morte'}
def own(d):
    left = dict(OWN)
    for n, (nh, ns, keys) in enumerate(d['namespaces']):
        for k, (kh, key, sh, i) in enumerate(keys):
            if (ns, key) in left:
                t, rc = d['strings'][i]; d['strings'][i] = (t, rc - 1) if rc > 1 else (t, rc)
                d['strings'].append((left.pop((ns, key)), 1)); keys[k] = (kh, key, sh, len(d['strings']) - 1)
    assert not left, f'keys not found: {left}'
def utoc():   # an IoStore table of contents (version 8) without chunks
    h = b'-==--==--==--==-' + struct.pack('<BBHIIIIIIIII', 8, 0, 0, 144, 0, 0, 12, 0, 32, 65536, 0, 1) + struct.pack('<Q', (1 << 64) - 1) + bytes(16) + struct.pack('<BBHIQII', 0, 0, 0, 0, (1 << 64) - 1, 0, 0) + bytes(40)
    assert len(h) == 144; return h
def main(mod):
    d, n = table(); own(d); b = locres.dump(d); assert locres.load(b)['strings'] == d['strings']
    paks = os.path.join(mod, 'romfs/FFRS/Content/Paks'); os.makedirs(paks, exist_ok=True)
    mkpak.build(os.path.join(paks, 'FFRS-Switch_P.pak'), {'FFRS/Content/Localization/Game/en/Game.locres': b})
    open(os.path.join(paks, 'FFRS-Switch_P.utoc'), 'wb').write(utoc()); open(os.path.join(paks, 'FFRS-Switch_P.ucas'), 'wb').write(b'')
    print(f'{n} of {len(d["strings"])} strings translated → {paks}')
if __name__ == '__main__': main(sys.argv[1] if len(sys.argv) > 1 else f'{ROOT}/out/mod')
