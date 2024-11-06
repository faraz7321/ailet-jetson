import os
import signal
import subprocess

def stop_script():
    try:
        # Find the PID(s) of the running script
        pids = subprocess.check_output(['pgrep', '-f', 'start_ailet.py']).decode().split()
        for pid in pids:
            # Terminate each process
            os.kill(int(pid), signal.SIGTERM)
            print(f"Process {pid} terminated.")
    except subprocess.CalledProcessError:
        print("No running process found for 'start.py'.")

if __name__ == "__main__":
    stop_script()
