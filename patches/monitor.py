"""Monitor passivo: consumo, temperatura, pausa e motivo de limite a cada 2 s, por ate 6 minutos."""
import ctypes
import struct
import time

libc = ctypes.CDLL("/usr/lib/libSystem.B.dylib")
FMT = "<4I32B32BII3Q"
BITS = {0: "PROCHOT", 1: "TERM", 5: "TERM-MED", 6: "VR-TERM", 7: "VR-COR", 8: "OUTRO", 10: "PL1", 11: "PL2", 12: "TURBO"}


def sensors():
    size = ctypes.c_size_t(struct.calcsize(FMT))
    buf = ctypes.create_string_buffer(size.value)
    if libc.sysctlbyname(b"debug.xepm.sensors", buf, ctypes.byref(size), None, 0) != 0:
        raise SystemExit("sensores indisponiveis")
    v = struct.unpack(FMT, buf.raw[:struct.calcsize(FMT)])
    return v[3], v[68], v[70], v[71]


def integer(name):
    value = ctypes.c_int(0)
    size = ctypes.c_size_t(4)
    if libc.sysctlbyname(name, ctypes.byref(value), ctypes.byref(size), None, 0) != 0:
        return -1
    return value.value & 0xFFFFFFFF


pkg_t, unit, e_pkg, e_ia = sensors()
u = 2.0 ** -unit
t0 = t = time.time()
print("dytc=0x%08x boot_err=%d msr_pl1=%d msr_pl2=%d trip=%d resume=%d" % (
    integer(b"debug.xepm.dytc"), integer(b"debug.xepm.dytc_boot_err"), integer(b"debug.xepm.msr_pl1"),
    integer(b"debug.xepm.msr_pl2"), integer(b"debug.xepm.trip_c"), integer(b"debug.xepm.resume_c")), flush=True)
while time.time() - t0 < 360:
    time.sleep(2)
    temp, _, a, b = sensors()
    now = time.time()
    dt = now - t
    lim = integer(b"debug.xepm.lim64f")
    active = ",".join(n for bit, n in BITS.items() if lim >> bit & 1) or "-"
    print("%3d pkg=%5.1f ia=%5.1f t=%3d hot=%d %s" % (
        now - t0, (a - e_pkg) * u / dt, (b - e_ia) * u / dt, temp, integer(b"debug.xepm.hold_hot"), active), flush=True)
    e_pkg, e_ia, t = a, b, now
