# main.py

import os
import sys
import subprocess


def banner():
    print(r"""
  ___ ___ ___   _                      _             _____         _ _   _ _   
 |_ _/ __/ __| | |   ___ __ _ _ _ _ _ (_)_ _  __ _  |_   _|__  ___| | |_(_) |_ 
  | | (__\__ \ | |__/ -_) _` | '_| ' \| | ' \/ _` |   | |/ _ \/ _ \ | / / |  _|
 |___\___|___/ |____\___\__,_|_| |_||_|_|_||_\__, |   |_|\___/\___/_|_\_\_|\__|
                                             |___/                             

       by d00dz
""")

def main_menu():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        banner()
        print("Main Menu:")
        print("1. OPC")
        print("2. TODO1")
        print("3. TODO2")
        print("0. Exit")

        choice = input("Select an option: ")

        if choice == "1":
            opc_menu()
        elif choice == "2":
            run_script("")
        elif choice == "3":
            run_script("")
        elif choice == "0":
            print("Bye!")
            sys.exit()
        else:
            print("Not a valid option.")
            input("Press Enter to continue...")

def opc_menu():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("OPC Menu:")
        print("1. Run Server")
        print("2. Run Client")
        print("3. Attacks")
        print("0. Back")

        choice = input("Select an option: ")

        if choice == "1":
            run_script("./opc-ua/server.py")
        elif choice == "2":
            run_script("./opc-ua/client.py")
        elif choice == "3":
            opc_attacks_menu()
        elif choice == "0":
            break
        else:
            print("Not a valid option.")
            input("Press Enter to continue...")

def opc_attacks_menu():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("OPC Menu:")
        print("1. Write on Rogue Sensor")
        print("2. Scan the network for OPC servers")
        print("3. Bruteforce credentials")
        print("0. Back")

        choice = input("Select an option: ")

        if choice == "1":
            run_script("./opc-ua/writer.py")
        elif choice == "2":
            run_script("./opc-ua/scanner.py")
        elif choice == "3":
            run_script("./opc-ua/bruteforce.py")
        elif choice == "0":
            break
        else:
            print("Not a valid option.")
            input("Press Enter to continue...")

def run_script(script_name):
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"Running {script_name}...\n")
    try:
        subprocess.run(['python', script_name], check=True)
    except FileNotFoundError:
        print(f"Error: File not found {script_name}")
    except subprocess.CalledProcessError as e:
        print(f"Script ended with an error: {e}")
    input("\nPress Enter to go back to Menu...")

if __name__ == "__main__":
    main_menu()