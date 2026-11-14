#!/usr/bin/env python3
# Writes an Unreal pak, version 11 (UE 4.26 - 5.x), stored (no compression, no encryption): the layout FFRS-Switch.pak has.
# Usage: mkpak.py <out.pak> <folder>      every file under <folder>, at its path relative to it (mount point ../../../)
import hashlib, os, struct, sys
MAGIC, M64 = 0x5A6F12E1, (1 << 64) - 1
def fstr(s): b = s.encode('ascii') + b'\0'; return struct.pack('<i', len(b)) + b
def fnv64(path, seed):
    h = (0xcbf29ce484222325 + seed) & M64
    for c in path.lower().encode('utf-16-le'): h = ((h ^ c) * 0x100000001b3) & M64
    return h
def build(out, files, seed=0x1283072a):
    """files: {path relative to the mount point: bytes}"""
    data, enc, offs = bytearray(), bytearray(), {}
    for path in sorted(files):
        b = files[path]; off = len(data)
        assert off < 1 << 32 and len(b) < 1 << 32
        data += struct.pack('<qqqI', 0, len(b), len(b), 0) + hashlib.sha1(b).digest() + struct.pack('<BI', 0, 0) + b   # the FPakEntry in front of the data (53 bytes)
        offs[path] = len(enc); enc += struct.pack('<III', 0xe0000000, off, len(b))   # offset, raw size and stored size in 32 bits; no blocks, no method
    dirs = {'/': []}
    for path in sorted(files):
        d, n = path.rsplit('/', 1) if '/' in path else ('', path)
        parts = d.split('/') if d else []
        for i in range(1, len(parts) + 1): dirs.setdefault('/'.join(parts[:i]) + '/', [])
        dirs[d + '/' if d else '/'].append((n, offs[path]))
    fdi = struct.pack('<i', len(dirs))
    for d in sorted(dirs):
        fdi += fstr(d) + struct.pack('<i', len(dirs[d]))
        for n, o in dirs[d]: fdi += fstr(n) + struct.pack('<i', o)
    phi = struct.pack('<i', len(files)) + b''.join(struct.pack('<Qi', fnv64(p, seed), offs[p]) for p in sorted(files)) + fdi   # the hashes, then the directory index the engine keeps
    def primary(po, do):
        return (fstr('../../../') + struct.pack('<iQ', len(files), seed) + struct.pack('<iQQ', 1, po, len(phi)) + hashlib.sha1(phi).digest()
                + struct.pack('<iQQ', 1, do, len(fdi)) + hashlib.sha1(fdi).digest() + struct.pack('<i', len(enc)) + bytes(enc) + struct.pack('<i', 0))
    ioff = len(data); isz = len(primary(0, 0)); pri = primary(ioff + isz, ioff + isz + len(phi))
    foot = bytes(16) + b'\0' + struct.pack('<IIQQ', MAGIC, 11, ioff, isz) + hashlib.sha1(pri).digest() + bytes(160)
    with open(out, 'wb') as f: f.write(bytes(data) + pri + phi + fdi + foot)
if __name__ == '__main__':
    out, root = sys.argv[1:3]; files = {}
    for d, _, ns in os.walk(root):
        for n in ns:
            if n.startswith('.'): continue
            p = os.path.join(d, n); files[os.path.relpath(p, root).replace(os.sep, '/')] = open(p, 'rb').read()
    build(out, files); print(out, len(files), 'files', os.path.getsize(out), 'bytes')
