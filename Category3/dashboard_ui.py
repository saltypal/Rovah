"""
Dashboard UI - Simple Tkinter interface with +/- buttons
Serves state via socket (localhost:5000)
"""
import tkinter as tk
from tkinter import ttk
import json
import socket
import threading
from pathlib import Path


class DashboardUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Rover Dashboard")
        self.root.geometry("300x200")
        
        # Initialize state
        self.state = 0
        self.last_button = None
        
        # Socket server
        self.socket_server = None
        self.running = False
        
        # UI Elements
        label = ttk.Label(root, text="Dashboard Control", font=("Arial", 14, "bold"))
        label.pack(pady=10)
        
        state_label = ttk.Label(root, text=f"State: {self.state}", font=("Arial", 20))
        self.state_label = state_label
        state_label.pack(pady=20)
        
        button_frame = ttk.Frame(root)
        button_frame.pack(pady=10)
        
        minus_btn = ttk.Button(button_frame, text="−", command=self.decrement, width=5)
        minus_btn.grid(row=0, column=0, padx=10)
        
        plus_btn = ttk.Button(button_frame, text="+", command=self.increment, width=5)
        plus_btn.grid(row=0, column=1, padx=10)
        
        status = ttk.Label(root, text="Ready", foreground="green")
        self.status = status
        status.pack(pady=10)
        
        # Start socket server in background
        self.start_socket_server()
        
        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
    
    def increment(self):
        self.state += 1
        self.last_button = "+"
        self.update_display()
    
    def decrement(self):
        self.state -= 1
        self.last_button = "-"
        self.update_display()
    
    def update_display(self):
        self.state_label.config(text=f"State: {self.state}")
    
    def get_state(self):
        """Return current state as JSON"""
        data = {
            "state": self.state,
            "button": self.last_button
        }
        return json.dumps(data)
    
    def start_socket_server(self):
        """Start socket server listening on port 5000"""
        self.running = True
        thread = threading.Thread(target=self.socket_listen, daemon=True)
        thread.start()
        print("[Dashboard] Socket server started on port 5000")
    
    def socket_listen(self):
        """Listen for connections on port 5000"""
        self.socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket_server.bind(("localhost", 5000))
        self.socket_server.listen(5)
        
        while self.running:
            try:
                self.socket_server.settimeout(1)
                client, addr = self.socket_server.accept()
                print(f"[Dashboard] Client connected: {addr}")
                
                # Send state as JSON
                state_json = self.get_state()
                client.sendall(state_json.encode('utf-8'))
                client.close()
            except socket.timeout:
                continue
            except:
                break
    
    def on_close(self):
        """Handle window close"""
        self.running = False
        if self.socket_server:
            self.socket_server.close()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = DashboardUI(root)
    root.mainloop()
