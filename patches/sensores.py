import ctypes
import struct
import subprocess
import time

libc = ctypes.CDLL("/usr/lib/libSystem.B.dylib")
FMT = "<4I32B32BII3Q"


def read():
    size = ctypes.c_size_t(struct.calcsize(FMT))
    buf = ctypes.create_string_buffer(size.value)
    if libc.sysctlbyname(b"debug.xepm.sensors", buf, ctypes.byref(size), None, 0) != 0:
        raise SystemExit("sensores indisponiveis")
    v = struct.unpack(FMT, buf.raw[:struct.calcsize(FMT)])
    core = v[4:36]
    kind = v[36:68]
    return {"pkg": v[3], "tj": v[2], "unit": v[68], "epkg": v[70], "eia": v[71], "egt": v[72],
            "p": [core[i] for i in range(32) if kind[i] == 0x40],
            "e": [core[i] for i in range(32) if kind[i] == 0x20], "kind": kind[:v[1]]}


def sample(label, seconds):
    a = read()
    t = time.time()
    time.sleep(seconds)
    b = read()
    dt = time.time() - t
    u = 2.0 ** -a["unit"]
    print("%-13s pacote %5.1f W | CPU %5.1f W | GPU %4.1f W | temp %3d C | P max %3s | E max %3s" % (
        label, (b["epkg"] - a["epkg"]) * u / dt, (b["eia"] - a["eia"]) * u / dt, (b["egt"] - a["egt"]) * u / dt,
        b["pkg"], max(b["p"] or [0]), max(b["e"] or [0])))


first = read()
print("TjMax", first["tj"], "| tipos por thread:", "".join("P" if k == 0x40 else "E" if k == 0x20 else "?" for k in first["kind"]))
sample("parado", 4)
spin = subprocess.Popen(["/bin/sh", "-c", "while :; do :; done"])
for i in range(3):
    sample("1 thread %ds" % ((i + 1) * 8), 8)
spin.kill()
spins = [subprocess.Popen(["/bin/sh", "-c", "while :; do :; done"]) for _ in range(12)]
for i in range(3):
    sample("12 thr %ds" % ((i + 1) * 8), 8)
for s in spins:
    s.kill()
