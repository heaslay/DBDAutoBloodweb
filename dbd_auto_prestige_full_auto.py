import time
import threading
from utils import detect_ui_scale, execute_full_auto, check_for_updates, Clicker, resource_path

__version__ = "v1.1.0"

def get_input_with_timeout(prompt, timeout, default):
    user_input = [default]

    def ask_input():
        user_input[0] = input(prompt)

    input_thread = threading.Thread(target=ask_input)
    input_thread.daemon = True
    input_thread.start()
    input_thread.join(timeout)

    if input_thread.is_alive():
        print(f"\n ⚙️ No input detected within {timeout} seconds. Defaulting to {default} prestige.\n")
        return default
    return user_input[0]

if __name__ == '__main__':
    start_time = time.time()

    print("\n================ Auto-Prestige Configuration ================\n")
    print("\n------------------------------------------------------------")
    print("💡 Prestige Setup:")
    print("› Enter how many prestiges to perform.")
    print("› Enter 0 to cancel and exit.")
    print("› If no input is given within 5 seconds, defaults to 1 prestige.")
    print("------------------------------------------------------------\n")

    while True:
        user_response = get_input_with_timeout("Enter number of prestiges (0 to cancel): ", timeout=5, default="1")
        try:
            num_prestiges = int(user_response)
            if num_prestiges < 0:
                raise ValueError
            elif num_prestiges == 0:
                print("\n🚪 Operation cancelled by user. Exiting.\n")
                exit(0)
            break
        except ValueError:
            print("❌ Invalid input. Please enter a positive whole number or 0 to exit.\n")

    print("Please switch to the Dead By Daylight application within 5 seconds...")
    time.sleep(5)
    detected_ui_scale, auto_purchase_coords = detect_ui_scale(resource_path('images/auto_purchase_node_withBG.png'))
    clicker = Clicker(auto_purchase_coords)

    for i in range(1, num_prestiges + 1):
        print(f"\nStarting Prestige {i}/{num_prestiges}...")
        execute_full_auto(clicker)
        #time.sleep(2)

    check_for_updates(__version__)
    end_time = time.time()
    total_time = end_time - start_time
    minutes, seconds = divmod(total_time, 60)
    print(f"\n✅ All {num_prestiges} prestige(s) completed. Exiting...")
    time.sleep(2)
    print(f"🕒 Total execution time: {int(minutes)} minutes and {seconds:.2f} seconds.\n")
    exit(0)