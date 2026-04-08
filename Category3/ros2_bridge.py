"""
ROS2 Bridge - Polls dashboard state every 2 seconds via socket
Relays to telemetry logger via socket
"""
import json
import os
import socket
import sys
import threading
import time
from datetime import datetime
from pathlib import Path


DASHBOARD_HOST = "localhost"
DASHBOARD_PORT = 5000
TELEMETRY_HOST = "localhost"
TELEMETRY_PORT = 5001
POLL_SECONDS = 2


class ROS2Bridge:
    def __init__(self):
        self.running = False
        self.last_state = None
        self.last_button = None

    def _can_connect(self, host, port, timeout=0.5):
        """Return True if a TCP endpoint is reachable."""
        try:
            with socket.create_connection((host, port), timeout=timeout):
                return True
        except OSError:
            return False

    def read_dashboard_state(self):
        """Connect to dashboard socket and get current UI state."""
        try:
            with socket.create_connection((DASHBOARD_HOST, DASHBOARD_PORT), timeout=1.0) as sock:
                data = sock.recv(2048).decode("utf-8")

            state_data = json.loads(data)
            return state_data.get("state"), state_data.get("button")
        except Exception as exc:
            return None, None

    def send_to_telemetry(self, button, state):
        """Send log data to telemetry logger via socket."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        payload = {
            "timestamp": timestamp,
            "button": button,
            "state": state,
        }

        try:
            with socket.create_connection((TELEMETRY_HOST, TELEMETRY_PORT), timeout=1.0) as sock:
                sock.sendall(json.dumps(payload).encode("utf-8"))
            print(f"[ROS2 Bridge] Sent to Telemetry: Button={button}, State={state}")
        except Exception as exc:
            print(f"[ROS2 Bridge] Error sending to Telemetry: {exc}")

    def poll_and_relay(self):
        """Poll dashboard every 2 seconds and relay changes."""
        print("[ROS2 Bridge] Starting polling loop...")
        consecutive_failures = 0
        max_failures_before_warn = 3
        
        while self.running:
            state, button = self.read_dashboard_state()

            if state is not None:
                consecutive_failures = 0
                if state != self.last_state or button != self.last_button:
                    print(f"[ROS2 Bridge] State change detected: Button={button}, State={state}")
                    self.send_to_telemetry(button, state)
                    self.last_state = state
                    self.last_button = button
            else:
                consecutive_failures += 1
                if consecutive_failures == max_failures_before_warn:
                    print(
                        "[ROS2 Bridge] Dashboard unreachable. "
                        "Check if dashboard.service is running: sudo systemctl status dashboard.service"
                    )

            time.sleep(POLL_SECONDS)

    def start(self):
        """Start bridge polling."""
        self.running = True
        thread = threading.Thread(target=self.poll_and_relay, daemon=True)
        thread.start()
        print("[ROS2 Bridge] Started")

    def stop(self):
        """Stop bridge."""
        self.running = False
        print("[ROS2 Bridge] Stopped")


if __name__ == "__main__":
    bridge = ROS2Bridge()
    bridge.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[ROS2 Bridge] Shutting down...")
        bridge.stop()