import unittest
import subprocess
import time
import socket
import os
import shutil
import sys

class TestProxy(unittest.TestCase):
    SERVER1_PORT = 65525
    SERVER2_PORT = 65526
    DATA_DIR1 = "tests/temp_data_node1"
    DATA_DIR2 = "tests/temp_data_node2"
    p1 = None
    p2 = None
    
    @classmethod
    def setUpClass(cls):
        # Clean up previous runs
        if os.path.exists(cls.DATA_DIR1):
            shutil.rmtree(cls.DATA_DIR1)
        if os.path.exists(cls.DATA_DIR2):
            shutil.rmtree(cls.DATA_DIR2)
            
        # Start Server 1
        cls.p1 = subprocess.Popen(
            [sys.executable, "tests/run_test_node.py", "--port", str(cls.SERVER1_PORT), "--data-dir", cls.DATA_DIR1],
            cwd=os.path.abspath(os.path.join(os.path.dirname(__file__), "..")),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Start Server 2
        cls.p2 = subprocess.Popen(
            [sys.executable, "tests/run_test_node.py", "--port", str(cls.SERVER2_PORT), "--data-dir", cls.DATA_DIR2],
            cwd=os.path.abspath(os.path.join(os.path.dirname(__file__), "..")),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Wait for servers to start
        time.sleep(3)

    @classmethod
    def tearDownClass(cls):
        if cls.p1:
            cls.p1.terminate()
            cls.p1.wait()
        if cls.p2:
            cls.p2.terminate()
            cls.p2.wait()
        
        # Clean up
        # if os.path.exists(cls.DATA_DIR1):
        #     shutil.rmtree(cls.DATA_DIR1)
        # if os.path.exists(cls.DATA_DIR2):
        #     shutil.rmtree(cls.DATA_DIR2)

    def send_command(self, port, command):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(5)
            s.connect(("127.0.0.1", port))
            if not command.endswith("\n"):
                command += "\n"
            s.sendall(command.encode())
            data = s.recv(1024)
            return data.decode().strip()

    def test_01_proxy_balance(self):
        # 1. Create account on Server 2 (Directly)
        try:
            response = self.send_command(self.SERVER2_PORT, "AC")
            self.assertIn("AC", response)
            # Parse account ID: AC <number>/<ip>
            parts = response.split(" ")[1].split("/")
            account_num = parts[0]
            # ip = parts[1] # "127.0.0.1" usually
        except ConnectionRefusedError:
            self.fail("Could not connect to Server 2")
        
        # 2. Deposit funds to initialize balance on Server 2 (Directly)
        # AD <number>/<ip> <amount>
        response = self.send_command(self.SERVER2_PORT, f"AD {account_num}/127.0.0.1 500")
        self.assertIn("AD", response)

        # 3. Check balance on Server 2 (Directly)
        response = self.send_command(self.SERVER2_PORT, f"AB {account_num}/127.0.0.1")
        self.assertIn("AB 500", response)
        
        # 4. Check balance on Server 1 (Proxy to Server 2)
        # We specify port in IP: 127.0.0.1:65526
        # Account ID: <account_num>/127.0.0.1:65526
        try:
            response = self.send_command(self.SERVER1_PORT, f"AB {account_num}/127.0.0.1:{self.SERVER2_PORT}")
            self.assertIn("AB 500", response)
        except ConnectionRefusedError:
             self.fail("Could not connect to Server 1")
             
        # Store account num for other tests if needed, but tests should be independent or use class var
        self.__class__.account_num = account_num
        
    def test_02_proxy_deposit(self):
         if not hasattr(self, 'account_num'):
             self.test_01_proxy_balance()
         
         account_num = self.account_num
         
         # 1. Deposit to account on Server 2 via Server 1
         response = self.send_command(self.SERVER1_PORT, f"AD {account_num}/127.0.0.1:{self.SERVER2_PORT} 200")
         self.assertIn("AD", response)
         
         # 2. Verify balance on Server 2
         response = self.send_command(self.SERVER2_PORT, f"AB {account_num}/127.0.0.1")
         self.assertIn("AB 700", response)
         
    def test_03_proxy_withdraw(self):
         if not hasattr(self, 'account_num'):
             self.test_01_proxy_balance()
             
         account_num = self.account_num
         
         # 1. Withdraw from account on Server 2 via Server 1
         response = self.send_command(self.SERVER1_PORT, f"AW {account_num}/127.0.0.1:{self.SERVER2_PORT} 100")
         self.assertIn("AW", response)
         
         # 2. Verify balance on Server 2
         response = self.send_command(self.SERVER2_PORT, f"AB {account_num}/127.0.0.1")
         self.assertIn("AB 600", response)

if __name__ == "__main__":
    unittest.main()
