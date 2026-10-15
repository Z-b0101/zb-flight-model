"""Synthetic 'physical twin' for testing the live bridge (CE-02 VC-L1a).

Flies a scripted profile (climb, cruise at 7 and 10.5 m/s, motor-off glides) with TRUE
parameters that differ from the twin's best estimates, adds sensor noise, and emits the
ArduPilot MAVLink messages the bridge reads (VFR_HUD, SYS_STATUS, ATTITUDE) over UDP.
It stands in for ArduPlane SITL / the real aircraft until those are available.
"""
import math, os, random, sys, time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import perf  # noqa: E402

G = 9.80665
PROFILE = [  # (seconds, V m/s, climb m/s, motor_on)
    (20, 10.0, 2.0, True), (40, 7.0, 0.0, True), (25, 7.5, None, False), (40, 10.5, 0.0, True),
    (25, 8.5, None, False), (40, 7.0, 0.0, True), (20, 9.0, None, False), (30, 7.0, 0.0, True),
]


def truth_stream(eta_true=0.38, kD_true=1.12, hotel_true=1.2, rate_hz=5.0, noise=True, seed=1):
    rnd = random.Random(seed); T = perf.Twin(); W = T.m * G; t = 0.0
    cache = {}
    def D(V):
        k = round(V, 1)
        if k not in cache: cache[k] = T.trim(k)["D"]
        return cache[k]
    for dur, V, climb, on in PROFILE:
        for _ in range(int(dur * rate_hz)):
            Vm = V + (rnd.gauss(0, 0.15) if noise else 0)
            if on:
                c = climb
                P = (kD_true * D(V) * V + W * c) / eta_true + hotel_true
                thr = 0.3 + 0.03 * P
            else:
                c = -kD_true * D(V) * V / W; P = hotel_true; thr = 0.0
            cm = c + (rnd.gauss(0, 0.05) if noise else 0)
            volt = 11.4 + (rnd.gauss(0, 0.02) if noise else 0)
            amp = P / 11.4 + (rnd.gauss(0, 0.03) if noise else 0)
            yield t, Vm, cm, thr, volt, max(amp, 0.0)
            t += 1 / rate_hz


def send(url="udpout:127.0.0.1:14550", speedup=50.0, **kw):
    from pymavlink import mavutil
    m = mavutil.mavlink_connection(url, source_system=1, source_component=1)
    for t, V, c, thr, volt, amp in truth_stream(**kw):
        m.mav.vfr_hud_send(V, V, 0, int(thr * 100), 120.0, c)
        m.mav.sys_status_send(0, 0, 0, 500, int(volt * 1000), int(amp * 100), -1, 0, 0, 0, 0, 0, 0)
        time.sleep(0.2 / speedup)


if __name__ == "__main__":
    send()
