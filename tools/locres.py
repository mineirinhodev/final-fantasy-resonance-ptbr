# Unreal .locres reader / writer (versions 1-3: Compact, Optimized_CRC32, Optimized_CityHash64_UTF16)
import struct
MAGIC = bytes.fromhex('0E147475674A03FC4A15909DC3377F1B')
class R:
    def __init__(s, b, o=0): s.b, s.o = b, o
    def t(s, f):
        v = struct.unpack_from(f, s.b, s.o); s.o += struct.calcsize(f); return v if len(v) > 1 else v[0]
    def fstr(s):
        n = s.t('<i')
        if n < 0: v = s.b[s.o:s.o - 2 * n].decode('utf-16-le'); s.o -= 2 * n; return v[:-1]
        v = s.b[s.o:s.o + n].decode('utf-8', 'surrogateescape'); s.o += n; return v[:-1] if n else ''
def fstr(v, force_wide=False):
    if not v and not force_wide: return struct.pack('<i', 0)
    try:
        if force_wide: raise UnicodeEncodeError('ascii', v, 0, 1, 'wide')
        b = v.encode('ascii') + b'\0'; return struct.pack('<i', len(b)) + b
    except UnicodeEncodeError:
        b = (v + '\0').encode('utf-16-le'); return struct.pack('<i', -(len(b) // 2)) + b
def load(b):
    """{version, namespaces: [(ns hash, ns, [(key hash, key, source hash, string index)])], strings: [(text, refcount)]}"""
    assert b[:16] == MAGIC, 'legacy locres'
    r = R(b, 16); ver = r.t('<B'); soff = r.t('<q')
    s = R(b, soff); strings = []
    for _ in range(s.t('<i')):
        t = s.fstr(); strings.append((t, s.t('<i') if ver >= 2 else -1))
    d = dict(version=ver, strings=strings, namespaces=[])
    if ver >= 2: d['entries'] = r.t('<I')
    for _ in range(r.t('<I')):
        nh = r.t('<I') if ver >= 2 else None; ns = r.fstr(); keys = []
        for _ in range(r.t('<I')):
            kh = r.t('<I') if ver >= 2 else None; k = r.fstr(); sh = r.t('<I'); keys.append((kh, k, sh, r.t('<i')))
        d['namespaces'].append((nh, ns, keys))
    return d
def dump(d):
    ver = d['version']; out = [MAGIC, struct.pack('<B', ver), b'\0' * 8]
    if ver >= 2: out.append(struct.pack('<I', d['entries']))
    out.append(struct.pack('<I', len(d['namespaces'])))
    for nh, ns, keys in d['namespaces']:
        if ver >= 2: out.append(struct.pack('<I', nh))
        out.append(fstr(ns)); out.append(struct.pack('<I', len(keys)))
        for kh, k, sh, i in keys:
            if ver >= 2: out.append(struct.pack('<I', kh))
            out.append(fstr(k)); out.append(struct.pack('<Ii', sh, i))
    head = b''.join(out); body = [struct.pack('<i', len(d['strings']))]
    for t, rc in d['strings']:
        body.append(fstr(t))
        if ver >= 2: body.append(struct.pack('<i', rc))
    b = head + b''.join(body)
    return b[:17] + struct.pack('<q', len(head)) + b[25:]
