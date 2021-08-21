import utime

def ___prn_nl():
    print("\n" * 4)

def headstart():
    sleep(1)
    ___prn_nl()
    print("""wiegand extended demo micropython port
(c) 2021 linuxgemini""")

def sleep(sec: int = 1):
    utime.sleep_ms(sec * 1000)

def sleep_ms(ms: int = 100):
    utime.sleep_ms(ms)

def afterload():
    print("loaded")

def rev(s: str) -> str:
    return "" if not(s) else rev(s[1::])+s[0]

def hex_rev(s: str) -> str:
    n = 2
    l = [s[i:i+n] for i in range(0, len(s), n)]
    l.reverse()
    return "".join(l)
