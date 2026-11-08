# Leitura do kext (so leitura, sem chamada entre CPUs):
#   python3 -I cpu-gpu.py estado        pedido HWP por CPU, chave autonomo, GPU agora
#   python3 -I cpu-gpu.py gpu 20        amostra a GPU por 20 s (MHz e repouso RC6)
import ctypes
import struct
import sys
import time

libc = ctypes.CDLL("/usr/lib/libSystem.B.dylib")


def raw(name, size):
    n = ctypes.c_size_t(size)
    buf = ctypes.create_string_buffer(size)
    if libc.sysctlbyname(name.encode(), buf, ctypes.byref(n), None, 0) != 0:
        raise SystemExit("sem %s (kext antigo?)" % name)
    return buf.raw[:n.value]


def num(name):
    v = ctypes.c_int()
    n = ctypes.c_size_t(4)
    return v.value if libc.sysctlbyname(name.encode(), ctypes.byref(v), ctypes.byref(n), None, 0) == 0 else None


MHZ = 50.0 / 3


def gpu():
    v = struct.unpack("<8I", raw("debug.xepm.gpu", 32))
    cap = v[2]
    req = v[4]
    ratio = ((req >> 14) & 0x1FF) if (req & 0xF) else (req >> 23)
    return {"cagf": ((v[1] >> 11) & 0x1FF) * MHZ, "rp0": (cap & 0xFF) * 50.0, "rp1": ((cap >> 8) & 0xFF) * 50.0,
            "rpn": ((cap >> 16) & 0xFF) * 50.0, "rc6": v[3], "pedido": ratio * MHZ, "pedidos": v[5]}


def estado():
    print("hwp_auto =", num("debug.xepm.hwp_auto"), "| route =", num("debug.xepm.route"))
    q = struct.unpack("<64Q", raw("debug.xepm.hwp_last", 512))
    print("CPU tipo  XCPM: min max des epp  ->  gravado: min max des epp")
    for c in range(12):
        a, b = q[c], q[32 + c]
        f = lambda x: "%3d %3d %3d %3d" % (x & 0xFF, (x >> 8) & 0xFF, (x >> 16) & 0xFF, (x >> 24) & 0xFF)
        print("%3d  %s   %s  ->  %s" % (c, "P" if c < 4 else "E", f(a), f(b)))
    g = gpu()
    print("GPU agora %.0f MHz | RP0 %.0f RP1 %.0f RPn %.0f | ultimo pedido da Apple %.0f MHz (%d pedidos)" % (
        g["cagf"], g["rp0"], g["rp1"], g["rpn"], g["pedido"], g["pedidos"]))


def amostra(seg):
    a = gpu()
    t0 = time.time()
    mhz = []
    while time.time() - t0 < seg:
        time.sleep(0.05)
        mhz.append(gpu()["cagf"])
    b = gpu()
    dt = time.time() - t0
    rc6 = ((b["rc6"] - a["rc6"]) & 0xFFFFFFFF) * 1.28e-6 / dt * 100
    ativo = sorted(m for m in mhz if m > 0)
    print("GPU por %.0f s: repouso RC6 %.0f%% | amostras ativas %d de %d" % (dt, rc6, len(ativo), len(mhz)))
    if ativo:
        p = lambda k: ativo[min(len(ativo) - 1, int(len(ativo) * k))]
        print("MHz ativa: min %.0f | mediana %.0f | p90 %.0f | max %.0f (RP0 %.0f)" % (
            ativo[0], p(0.5), p(0.9), ativo[-1], b["rp0"]))
    print("pedidos da Apple no periodo: %d" % (b["pedidos"] - a["pedidos"]))


if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[1] == "gpu":
        amostra(float(sys.argv[2]))
    else:
        estado()
