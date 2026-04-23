#!/usr/bin/env python3
"""Standalone test script for the HDMIAnalyserController APIs.

Usage:
    1. Edit tests/hdmiAnalyser_test_config.yml and set your M42h IP address.
    2. Run:  python3 tests/hdmiAnalyser_test.py [path/to/config.yml]

The script exercises each public API on the controller and prints
PASSED / FAILED for every call so you can quickly verify which
operations work against real hardware.
"""

import os
import sys
import json
import yaml

# Add the framework path to system
dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(dir_path, ".."))

from framework.core.logModule import logModule
from framework.core.hdmiAnalyserController import HDMIAnalyserController

# ── Helpers ─────────────────────────────────────────────────────────────

_pass_count = 0
_fail_count = 0

def run_test(name, func):
    """Run *func*, print PASSED/FAILED, and track counts."""
    global _pass_count, _fail_count
    try:
        func()
        print(f"  PASSED: {name}")
        _pass_count += 1
    except Exception as e:
        print(f"  FAILED: {name} — {e}")
        _fail_count += 1

def print_dict(label, d):
    """Pretty-print a dict result."""
    print(f"    {label}: {json.dumps(d, indent=6, default=str)}")

# ── Main ────────────────────────────────────────────────────────────────

if __name__ == "__main__":

    # Load config
    default_cfg = os.path.join(dir_path, "hdmiAnalyser_test_config.yml")
    cfg_path = sys.argv[1] if len(sys.argv) > 1 else default_cfg

    with open(cfg_path, "r") as f:
        cfg = yaml.safe_load(f)

    config = cfg.get("hdmiAnalyserController", cfg)

    if not config.get("host"):
        print("ERROR: Set the 'host' field in", cfg_path)
        sys.exit(1)

    LOG = logModule("hdmi analyser test", logModule.DEBUG)
    LOG.setFilename(os.path.abspath('./logs/'), 'hdmiAnalyser-%sTest.log' % config.get('type'))

    print("=" * 60)
    print("HDMI Analyser API Test")
    print("=" * 60)
    print(f"Config: {json.dumps(config, default=str)}")
    print()

    # ── Create controller ───────────────────────────────────────────
    controller = HDMIAnalyserController(LOG, config)

    # ── 1. Connect ──────────────────────────────────────────────────
    print("[Connection]")
    run_test("connect()", lambda: controller.connect())

    # ── 2. Link status ──────────────────────────────────────────────
    print("\n[Link Status]")
    def _link_status():
        status = controller.get_link_status()
        print_dict("link_status", status)
    run_test("get_link_status()", _link_status)

    # ── 3. Video format — set and read back ─────────────────────────
    print("\n[Video Format]")
    def _set_video_1080p():
        controller.set_video_format("1080p60")
    run_test("set_video_format('1080p60')", _set_video_1080p)

    def _start_output():
        controller.start_output()
    run_test("start_output()", _start_output)

    def _get_video_status():
        status = controller.get_video_status()
        print_dict("video_status", status)
    run_test("get_video_status()", _get_video_status)

    # ── 4. HDR mode ─────────────────────────────────────────────────
    print("\n[HDR Mode]")
    def _set_hdr_hdr10():
        controller.set_hdr_mode("HDR10")
    run_test("set_hdr_mode('HDR10')", _set_hdr_hdr10)

    def _set_hdr_sdr():
        controller.set_hdr_mode("SDR")
    run_test("set_hdr_mode('SDR')", _set_hdr_sdr)

    # ── 5. ALLM ─────────────────────────────────────────────────────
    print("\n[ALLM]")
    run_test("set_allm(True)", lambda: controller.set_allm(True))
    run_test("set_allm(False)", lambda: controller.set_allm(False))

    # ── 6. VRR ──────────────────────────────────────────────────────
    print("\n[VRR]")
    run_test("set_vrr(True, base_refresh_rate=48)",
             lambda: controller.set_vrr(True, base_refresh_rate=48))
    run_test("set_vrr(False)", lambda: controller.set_vrr(False))

    # ── 7. AVI InfoFrame ────────────────────────────────────────────
    print("\n[AVI InfoFrame]")
    def _get_avi():
        info = controller.get_avi_info()
        print_dict("avi_info", info)
    run_test("get_avi_info()", _get_avi)

    # ── 8. SPD InfoFrame ────────────────────────────────────────────
    print("\n[SPD InfoFrame]")
    run_test("set_spd_info('TestVendor', 'TestProduct')",
             lambda: controller.set_spd_info("TestVendor", "TestProduct"))

    def _get_spd():
        info = controller.get_spd_info()
        print_dict("spd_info", info)
    run_test("get_spd_info()", _get_spd)

    # ── 9. Audio status ─────────────────────────────────────────────
    print("\n[Audio]")
    def _get_audio():
        status = controller.get_audio_status()
        print_dict("audio_status", status)
    run_test("get_audio_status()", _get_audio)

    # ── 10. HDCP ────────────────────────────────────────────────────
    print("\n[HDCP]")
    run_test("set_hdcp_mode('none')", lambda: controller.set_hdcp_mode("none"))

    def _get_hdcp():
        status = controller.get_hdcp_status()
        print_dict("hdcp_status", status)
    run_test("get_hdcp_status()", _get_hdcp)

    run_test("set_hdcp_mode('2.3')", lambda: controller.set_hdcp_mode("2.3"))
    run_test("set_hdcp_mode('none')", lambda: controller.set_hdcp_mode("none"))

    # ── 11. HPD ─────────────────────────────────────────────────────
    print("\n[Hot-Plug]")
    run_test("set_hpd(False)", lambda: controller.set_hpd(False))
    run_test("set_hpd(True, duration=200)",
             lambda: controller.set_hpd(True, duration=200))

    # ── 12. EDID ────────────────────────────────────────────────────
    print("\n[EDID]")
    def _get_edid():
        edid = controller.get_edid()
        print(f"    edid length: {len(edid)} bytes")
    run_test("get_edid()", _get_edid)
    run_test("restore_default_edid()", lambda: controller.restore_default_edid())

    # ── 13. Background colour ───────────────────────────────────────
    print("\n[Background Colour]")
    def _get_bg():
        colour = controller.get_background_color()
        print(f"    background_color: {colour}")
    run_test("get_background_color()", _get_bg)

    # ── 14. Snapshot (combined status) ──────────────────────────────
    print("\n[Snapshot]")
    def _snapshot():
        snap = controller.snapshot()
        print_dict("snapshot", snap)
    run_test("snapshot()", _snapshot)

    # ── 15. Change format to 4K and read back ──────────────────────
    print("\n[4K Format Test]")
    def _set_4k():
        controller.set_video_format("2160p60", colour_space="YCbCr709",
                                    subsampling="420", bit_depth=10)
    run_test("set_video_format('2160p60', cs=YCbCr709, ss=420, depth=10)", _set_4k)
    run_test("get_video_status() after 4K", _get_video_status)

    # ── 16. Stop output ─────────────────────────────────────────────
    print("\n[Stop Output]")
    run_test("stop_output()", lambda: controller.stop_output())

    # ── 17. Disconnect ──────────────────────────────────────────────
    print("\n[Disconnect]")
    run_test("disconnect()", lambda: controller.disconnect())

    # ── Summary ─────────────────────────────────────────────────────
    total = _pass_count + _fail_count
    print()
    print("=" * 60)
    print(f"Results: {_pass_count}/{total} passed, {_fail_count}/{total} failed")
    print("=" * 60)
