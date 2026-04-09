"""
Telemetry Logger - Listens on socket (port 5001) for log requests
Writes to log.txt
"""
import json
import socket
from pathlib import Path


class TelemetryLogger:
    def __init__(self):
        self.log_file = Path(__file__).parent / "log.txt"
        self.running = False
        self.socket_server = None
        self.processed_count = 0
    
    def write_log(self, timestamp, button, state):
        """Write single entry to log.txt"""
        with open(self.log_file, 'a') as f:
            log_line = f"{timestamp} | Button: {button} | State: {state}\n"
            f.write(log_line)
            print(f"[Telemetry] Logged: {log_line.strip()}")
        
        self.processed_count += 1
    
    def socket_listen(self):
        """Listen for incoming log requests on port 5001"""
        self.socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket_server.bind(("localhost", 5001))
        self.socket_server.listen(5)
        
        print("[Telemetry] Listening on port 5001...")
        
        while self.running:
            try:
                self.socket_server.settimeout(1)
                client, addr = self.socket_server.accept()
                
                # Receive log data
                data = client.recv(1024).decode('utf-8')
                client.close()
                
                if data:
                    try:
                        log_data = json.loads(data)
                        self.write_log(
                            log_data.get("timestamp"),
                            log_data.get("button"),
                            log_data.get("state")
                        )
                    except json.JSONDecodeError:
                        print("[Telemetry] Invalid JSON received")
            except socket.timeout:
                continue
            except:
                break
    
    def start(self):
        """Start the logger listening on socket"""
        self.running = True
        print("[Telemetry] Started")
        self.socket_listen()
    
    def stop(self):
        """Stop the logger"""
        self.running = False
        if self.socket_server:
            self.socket_server.close()
        print(f"[Telemetry] Stopped (processed {self.processed_count} events)")


if __name__ == "__main__":
    logger = TelemetryLogger()
    
    try:
        logger.start()
    except KeyboardInterrupt:
        print("\n[Telemetry] Shutting down...")
        logger.stop()