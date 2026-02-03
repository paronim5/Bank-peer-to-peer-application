import tkinter as tk
from tkinter import scrolledtext, messagebox
import subprocess
import threading
import sys
import os
import signal
import queue
import time

class NodeMonitor(tk.Tk):
    """
    GUI application for monitoring and controlling the Bank Node.
    
    Provides a dashboard to start/stop the node process and view real-time logs.
    Inherits from `tkinter.Tk`.
    """
    def __init__(self):
        """
        Initialize the NodeMonitor GUI.
        
        Sets up the window, grid configuration, process management variables,
        and initializes UI components.
        
        Side Effects:
            - Creates a Tkinter window.
            - Sets up a periodic callback for log processing.
            - Binds the window close event.
        """
        super().__init__()
        self.title("Bank Node Monitor")
        self.geometry("800x600")
        
        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        
        # Process handle
        self.process = None
        self.log_queue = queue.Queue()
        self.is_running = False
        
        # UI Components
        self._create_widgets()
        
        # Periodic check for queue updates
        self.after(100, self._process_log_queue)
        
        # Handle close
        self.protocol("WM_DELETE_WINDOW", self._on_close)

    def _create_widgets(self):
        """
        Create and arrange the GUI widgets.
        
        Constructs the header (status, control button), info label, and
        scrolled text area for logs.
        
        Side Effects:
            - Adds widgets to the Tkinter window.
        """
        # 1. Header Frame (Status + Controls)
        header_frame = tk.Frame(self, pady=10)
        header_frame.grid(row=0, column=0, sticky="ew")
        
        # Status Indicator
        self.status_canvas = tk.Canvas(header_frame, width=20, height=20, highlightthickness=0)
        self.status_canvas.pack(side=tk.LEFT, padx=(20, 5))
        self.status_light = self.status_canvas.create_oval(2, 2, 18, 18, fill="red")
        
        self.status_label = tk.Label(header_frame, text="Status: STOPPED", font=("Arial", 12, "bold"))
        self.status_label.pack(side=tk.LEFT, padx=5)
        
        # Control Button
        self.btn_control = tk.Button(header_frame, text="Start Node", command=self._toggle_node, 
                                     bg="#4CAF50", fg="white", font=("Arial", 10, "bold"), width=15)
        self.btn_control.pack(side=tk.RIGHT, padx=20)

        # 2. Info Label
        info_label = tk.Label(self, text="Real-time Logs:", font=("Arial", 10))
        info_label.grid(row=1, column=0, sticky="w", padx=20)
        
        # 3. Log Area
        self.log_area = scrolledtext.ScrolledText(self, state='disabled', height=20, font=("Consolas", 9))
        self.log_area.grid(row=2, column=0, sticky="nsew", padx=20, pady=(0, 20))
        
        # Define tags for coloring
        self.log_area.tag_config("INFO", foreground="black")
        self.log_area.tag_config("ERROR", foreground="red")
        self.log_area.tag_config("WARNING", foreground="#FF8C00") # Dark Orange

    def _toggle_node(self):
        """
        Toggle the running state of the bank node.
        
        If the node is running, stops it. If stopped, starts it.
        
        Side Effects:
            - Calls `_stop_node` or `_start_node`.
        """
        if self.is_running:
            self._stop_node()
        else:
            self._start_node()

    def _start_node(self):
        """
        Start the bank node as a subprocess.
        
        Launches `main.py` in a separate process and starts a thread to
        capture its output.
        
        Side Effects:
            - Spawns a new subprocess (`subprocess.Popen`).
            - Starts a background thread (`_read_output`).
            - Updates UI state.
        """
        if self.process:
            return
            
        try:
            # Find main.py relative to this script
            current_dir = os.path.dirname(os.path.abspath(__file__))
            main_script = os.path.join(current_dir, "main.py")
            
            # Start process with unbuffered output (-u)
            self.process = subprocess.Popen(
                [sys.executable, "-u", main_script],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=1,
                cwd=os.path.dirname(current_dir) # Run from project root
            )
            
            self.is_running = True
            self._update_ui_state(True)
            
            # Start log reading thread
            self.thread = threading.Thread(target=self._read_output, daemon=True)
            self.thread.start()
            
            self._log("SYSTEM", "Node started successfully.")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start node: {e}")
            self._stop_node()

    def _stop_node(self):
        """
        Stop the running bank node.
        
        Terminates the subprocess if it exists.
        
        Side Effects:
            - Terminates the subprocess.
            - Updates UI state.
        """
        if self.process:
            self._log("SYSTEM", "Stopping node...")
            self.process.terminate()
            self.process = None
            
        self.is_running = False
        self._update_ui_state(False)
        self._log("SYSTEM", "Node stopped.")

    def _update_ui_state(self, running):
        """
        Update the UI elements to reflect the node's running state.
        
        Changes the status indicator color, text, and button label.
        
        Args:
            running (bool): True if the node is running, False otherwise.
            
        Side Effects:
            - Modifies widget properties (text, color).
        """
        if running:
            self.status_canvas.itemconfig(self.status_light, fill="#00FF00") # Green
            self.status_label.config(text="Status: RUNNING")
            self.btn_control.config(text="Stop Node", bg="#F44336") # Red
        else:
            self.status_canvas.itemconfig(self.status_light, fill="red")
            self.status_label.config(text="Status: STOPPED")
            self.btn_control.config(text="Start Node", bg="#4CAF50") # Green

    def _read_output(self):
        """
        Read stdout from the subprocess and enqueue lines.
        
        Intended to run in a separate thread to prevent blocking the GUI.
        Reads lines from the process stdout and puts them into `self.log_queue`.
        
        Side Effects:
            - Reads from a file descriptor (stdout).
            - Modifies `self.log_queue`.
        """
        if not self.process:
            return
            
        try:
            for line in iter(self.process.stdout.readline, ''):
                if line:
                    self.log_queue.put(line)
                else:
                    break
        except Exception as e:
            self.log_queue.put(f"[Monitor Error] {e}\n")
        finally:
            # Process ended
            if self.is_running: # If we didn't intentionally stop it
                self.log_queue.put("[SYSTEM] Node process exited unexpectedly.\n")
                # We can't update UI directly from thread, so we'll handle state change in _process_log_queue if needed
                # But for now, simple is better.
                pass

    def _process_log_queue(self):
        """
        Process the log queue and update the text area.
        
        Scheduled periodically on the main thread.
        Dequeues messages and appends them to the log display.
        Also checks if the subprocess has died unexpectedly.
        
        Side Effects:
            - Updates the `log_area` widget.
            - Schedules itself to run again (`after`).
        """
        while not self.log_queue.empty():
            line = self.log_queue.get_nowait()
            self._append_log(line)
            
        # Check if process died unexpectedly
        if self.is_running and self.process and self.process.poll() is not None:
            self._stop_node()
            
        self.after(100, self._process_log_queue)

    def _log(self, level, message):
        timestamp = time.strftime("%H:%M:%S")
        formatted = f"[{timestamp}] [{level}] {message}\n"
        self._append_log(formatted)

    def _append_log(self, text):
        self.log_area.config(state='normal')
        
        # Simple coloring based on content
        tag = "INFO"
        if "ERROR" in text or "CRITICAL" in text or "Exception" in text:
            tag = "ERROR"
        elif "WARNING" in text:
            tag = "WARNING"
            
        self.log_area.insert(tk.END, text, tag)
        self.log_area.see(tk.END) # Auto-scroll
        self.log_area.config(state='disabled')

    def _on_close(self):
        """
        Handle the window close event.
        
        Prompts for confirmation if the node is running. Stops the node
        before destroying the window.
        
        Side Effects:
            - May stop the subprocess.
            - Destroys the Tkinter window.
        """
        if self.is_running:
            if messagebox.askokcancel("Quit", "Node is running. Stop node and quit?"):
                self._stop_node()
                self.destroy()
        else:
            self.destroy()

if __name__ == "__main__":
    app = NodeMonitor()
    app.mainloop()
