"""CE-02 live twin bridge: MAVLink in -> shadow model -> residuals + online estimates.

Listens for ArduPilot MAVLink (UDP, the ground radio / mavlink-router output), and on
every VFR_HUD + SYS_STATUS pair:
  * shadow prediction from the frozen twin (twin/perf.py at the D-32 best values):
      P_pred = (D(V) * V + W * climb) / eta + P_hotel ;  glide sink_pred = D(V) * V / W
  * residuals (measured - predicted) for battery power and, in glides, sink rate
  * online estimators (recursive least squares with forgetting):
      k_D  : drag multiplier, observable from motor-off glides  (sink = k_D * D V / W)
      hotel: electronics power, observable directly in motor-off glides (battery power = hotel)
      eta  : overall propulsion efficiency, from powered flight once k_D and hotel are known
    -> these are the live replacements for PROVISIONAL P-01 (eta) and P-04 (cd_misc)
  * live remaining range / endurance from measured Wh/km at the current airspeed

Run:  python3 twin/live/bridge.py --url udpin:0.0.0.0:14550 [--log out.jsonl]
Test: tests/test_live_bridge.py drives it with twin/live/sim_aircraft.py (synthetic truth).
"""
import argparse, json, math, os, sys, time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import perf  # noqa: E402

G = 9.80665


class RLS1:
    """Scalar recursive least squares y = theta * x with forgetting factor."""
    def __init__(self, theta0, p0=1.0, lam=0.995):
        self.theta, self.P, self.lam, self.n = theta0, p0, lam, 0
    def update(self, x, y):
        k = self.P * x / (self.lam + x * self.P * x)
        self.theta += k * (y - x * self.theta)
        self.P = (self.P - k * x * self.P) / self.lam
        self.n += 1
        return self.theta
    def sigma(self, noise_var):
        return math.sqrt(max(self.P * noise_var, 0.0))


class Shadow:
    def __init__(self, twin=None):
        self.T = twin or perf.Twin()
        self.W = self.T.m * G
        self.hotel = perf.A("p_hotel_w")
        self.eta0 = perf.A("eta_provisional")
        self.E_wh = perf.A("pack_wh") * perf.A("usable_frac")
        self._cache = {}
        self.kD = RLS1(1.0, p0=0.5)          # drag multiplier (1.0 = twin best estimate)
        self.inv_eta = RLS1(1 / self.eta0, p0=5.0)  # estimate 1/eta (linear in the data)
        self.hotel_est = RLS1(self.hotel, p0=1.0)   # electronics power, observable directly when the motor is off
        self.used_wh = 0.0; self.t_last = None; self.log = []

    def drag(self, V):
        key = round(V, 1)
        if key not in self._cache:
            self._cache[key] = self.T.trim(max(key, 5.0))["D"]
        return self._cache[key]

    def step(self, t, V, climb, throttle, volt, amp):
        P = volt * amp
        if self.t_last is not None:
            self.used_wh += P * (t - self.t_last) / 3600
        self.t_last = t
        D = self.drag(V)
        out = dict(t=t, V=V, climb=climb, throttle=throttle, P_meas=P)
        if throttle < 0.02:                                   # motor off: glide -> drag
            sink_pred = D * V / self.W
            out["sink_pred"], out["resid_sink"] = sink_pred, -climb - sink_pred
            if V > 5.5:
                self.kD.update(sink_pred, -climb)
            self.hotel_est.update(1.0, P)                     # motor off: battery power = electronics
        else:                                                 # powered -> 1/eta, given k_D
            hot = self.hotel_est.theta if self.hotel_est.n >= 10 else self.hotel
            p_air = self.kD.theta * D * V + self.W * climb
            P_pred = p_air / self.eta0 + hot
            out["P_pred"], out["resid_P"] = P_pred, P - P_pred
            if p_air > 0.5 and self.kD.n >= 10:
                self.inv_eta.update(p_air, P - hot)
        out["k_D"], out["eta"], out["hotel_W"] = self.kD.theta, 1 / self.inv_eta.theta, self.hotel_est.theta
        rem_wh = max(self.E_wh - self.used_wh, 0.0)
        if throttle >= 0.02 and V > 3:
            out["remaining_min"] = rem_wh / max(P, 0.1) * 60
            out["remaining_km"] = out["remaining_min"] * 60 * V / 1000
        self.log.append(out)
        return out


def run(url, log_path=None, duration=None, stop=None):
    from pymavlink import mavutil
    m = mavutil.mavlink_connection(url, source_system=255)
    sh = Shadow(); hud = None; t0 = time.time()
    fh = open(log_path, "w") if log_path else None
    while True:
        if stop is not None and stop.is_set(): break
        if duration and time.time() - t0 > duration: break
        msg = m.recv_match(type=["VFR_HUD", "SYS_STATUS", "SYSTEM_TIME"], blocking=True, timeout=1.0)
        if msg is None: continue
        if msg.get_type() == "VFR_HUD":
            hud = msg
        elif msg.get_type() == "SYS_STATUS" and hud is not None:
            ts = getattr(msg, "_timestamp", time.time())
            o = sh.step(ts, hud.airspeed, hud.climb, hud.throttle / 100.0,
                        msg.voltage_battery / 1000.0, msg.current_battery / 100.0)
            if fh: fh.write(json.dumps(o) + "\n")
    if fh: fh.close()
    return sh


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", default="udpin:0.0.0.0:14550"); ap.add_argument("--log")
    ap.add_argument("--duration", type=float)
    a = ap.parse_args()
    sh = run(a.url, a.log, a.duration)
    print(json.dumps({"samples": len(sh.log), "k_D": sh.kD.theta, "eta": 1 / sh.inv_eta.theta}, indent=1))
