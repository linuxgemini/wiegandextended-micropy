import utime

def ___prn_nl():
    print("\n" * 4)

def headstart():
    utime.sleep(1)
    ___prn_nl()
    print("""wiegand extended demo micropython port
(c) 2021 linuxgemini""")

def sleep1sec():
    utime.sleep(1)

def afterload():
    print("loaded")

def rev(s: str) -> str:
    return "" if not(s) else rev(s[1::])+s[0]

def hex_rev(s: str) -> str:
    n = 2
    l = [s[i:i+n] for i in range(0, len(s), n)]
    l.reverse()
    return "".join(l)
