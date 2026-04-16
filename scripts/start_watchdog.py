import time
import sys
import os
from pathlib import Path

# Ensure project root is in path
sys.path.append(os.getcwd())

import modules.watchdog as watchdog

def run_watchdog_loop(interval_minutes=15):
    print("=============================================")
    print("   KOICHA WATCHDOG -- Active Monitoring    ")
    print("=============================================")
    print(f"Polling Interval: every {interval_minutes} minutes")
    print("Press Ctrl+C to stop.")
    
    try:
        while True:
            print(f"\n[{time.strftime('%H:%M:%S')}] Poking the inbox...")
            watchdog.poll_for_reviews()
            
            # Wait for the next interval
            time.sleep(interval_minutes * 60)
    except KeyboardInterrupt:
        print("\n[STOPPED] Watchdog is going to sleep. Goodbye!")

if __name__ == "__main__":
    # You can change the interval here
    run_watchdog_loop(interval_minutes=15)
