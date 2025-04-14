import time
from utils import detect_ui_scale, execute_autoprestige, check_for_updates, Clicker

__version__ = "v1.0.1"

if __name__ == '__main__':
    start_time = time.time() #- debug, testing for time (section start)
    print("Please switch to the Dead By Daylight application within 5 seconds.")
    time.sleep(5)

    # Detect UI scale and setup Clicker class
    detected_ui_scale, auto_purchase_coords = detect_ui_scale('images/auto_purchase_node_withBG.png')
    clicker = Clicker(auto_purchase_coords)

    # Execute the auto-prestige process
    execute_autoprestige(clicker)

    # Check for updates after execution
    check_for_updates(__version__)
    end_time = time.time()
    total_time = end_time - start_time
    minutes, seconds = divmod(total_time, 60)
    print(f"Execution finished in {int(minutes)} minutes and {seconds:.2f} seconds.") #- debug, testing for time (section end)