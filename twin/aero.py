"""ZiB twin v0.1 — reads the JSBSim model as the single aero/mass source and trims analytically."""
import re, math, numpy as np
XML = "/home/claude/twin/aircraft/zb_wing/zb_wing.xml"
G, RHO = 9.80665, 1.225

def _table(x, name):
    f = re.search(rf'<function name="{re.escape(name)}">(.*?)</function>', x, re.S).group(1)
    rows = re.search(r'<tableData>(.*?)</tableData>', f, re.S).group(1).split()
    a = np.array(rows, float).reshape(-1, 2)
    return a[:, 0], a[:, 1]

class Model:
    def __init__(self, path=XML):
        x = open(path).read()
        self.S = float(re.search(r'<wingarea unit="M2">([\d.]+)', x).group(1))
        self.b = float(re.search(r'<wingspan unit="M">([\d.]+)', x).group(1))
        mb = x[x.find('<mass_balance>'):x.find('</mass_balance>')]
        self.m = float(re.search(r'<emptywt unit="KG">([\d.]+)', mb).group(1)) + sum(
            float(w) for w in re.findall(r'<pointmass name="\w+">\s*<weight unit="KG">([\d.]+)', mb))
        self.aCL, self.CLt = _table(x, "aero/coefficient/CL")
        self.aCm, self.Cmt = _table(x, "aero/coefficient/Cm")
        self.aCD, self.CDt = _table(x, "aero/coefficient/CD")
        self.CLd, self.Cmd, self.CDdd = 0.012, -0.008, 1.3e-4
        self.Tmax = 1.5
    def CL(self, a, d): return np.interp(a, self.aCL, self.CLt) + self.CLd * d
    def Cm(self, a, d): return np.interp(a, self.aCm, self.Cmt) + self.Cmd * d
    def CD(self, a, d): return np.interp(a, self.aCD, self.CDt) + self.CDdd * d * d
    def trim(self, V):
        CLreq = self.m * G / (0.5 * RHO * V * V * self.S)
        lo, hi = -6.0, 15.0
        def f(a):  # elevon that zeros Cm, then lift residual
            d = np.interp(a, self.aCm, self.Cmt) / -self.Cmd * -1
            d = -np.interp(a, self.aCm, self.Cmt) / self.Cmd
            return self.CL(a, d) - CLreq, d
        if f(hi)[0] < 0: return None  # beyond CLmax: stalled
        for _ in range(80):
            mid = 0.5 * (lo + hi)
            if f(mid)[0] > 0: hi = mid
            else: lo = mid
        a = 0.5 * (lo + hi); _, d = f(a)
        q = 0.5 * RHO * V * V
        D = q * self.S * self.CD(a, d)
        return dict(V=V, alpha=a, elevon=d, CL=self.CL(a, d), CD=self.CD(a, d), LD=self.CL(a, d) / self.CD(a, d),
                    D=D, throttle=D / self.Tmax, P_air=D * V)

if __name__ == "__main__":
    M = Model(); print(f"mass {M.m*1000:.1f} g  S {M.S}  b {M.b}")
    for V in [4, 5, 6, 7, 8, 9, 10, 12, 14]:
        t = M.trim(V)
        print(V, "STALL" if t is None else " ".join(f"{k}={v:.3f}" for k, v in t.items() if k != "V"))
