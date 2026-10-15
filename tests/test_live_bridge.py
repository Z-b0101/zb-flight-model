"""CE-02 VC-L1a: live-bridge estimators recover the 'physical twin' truth.

1. In-process: the synthetic truth stream (eta 0.38, drag x1.12, hotel 1.2 W) is fed straight
   to the Shadow model; the estimators must recover eta within +/-0.03 and k_D within +/-5%.
2. End-to-end over real MAVLink/UDP (pymavlink): sim_aircraft -> UDP -> bridge.run().
"""
import os, sys, threading, time
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "twin")); sys.path.insert(0, os.path.join(REPO, "twin", "live"))
import bridge, sim_aircraft  # noqa: E402

TRUTH = dict(eta_true=0.38, kD_true=1.12, hotel_true=1.4)   # 1.4 W = budget + CE-02 link


def test_estimators_recover_truth_in_process():
    sh = bridge.Shadow()
    for s in sim_aircraft.truth_stream(**TRUTH):
        o = sh.step(*s)
    assert abs(o["k_D"] - 1.12) / 1.12 < 0.05
    assert abs(o["eta"] - 0.38) < 0.03
    assert sh.kD.n > 100 and sh.inv_eta.n > 100
    assert abs(o["hotel_W"] - 1.4) < 0.05          # electronics power separated from eta


def test_end_to_end_over_mavlink_udp():
    port = 14571
    stop = threading.Event(); result = {}
    th = threading.Thread(target=lambda: result.setdefault("sh", bridge.run(f"udpin:127.0.0.1:{port}", stop=stop)))
    th.start(); time.sleep(0.5)
    sim_aircraft.send(f"udpout:127.0.0.1:{port}", speedup=200.0, **TRUTH)
    time.sleep(1.0); stop.set(); th.join(timeout=5)
    sh = result["sh"]
    assert len(sh.log) > 800                       # most of the 240 s x 5 Hz stream arrived
    assert abs(sh.log[-1]["eta"] - 0.38) < 0.04
    assert abs(sh.log[-1]["k_D"] - 1.12) / 1.12 < 0.07
