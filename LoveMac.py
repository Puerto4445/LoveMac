#!/usr/bin/python3
import argparse
import re
from termcolor import colored
import subprocess
import sys
import signal
from tqdm import tqdm
import time
from pyfiglet import Figlet


def Print_Figlet(text):
    """BANNER"""
    figlet = Figlet(font="5lineoblique")
    ascii_art = figlet.renderText(text)
    lolcat_process = subprocess.Popen(["lolcat"], stdin=subprocess.PIPE)
    lolcat_process.communicate(input=ascii_art.encode())


def close_correct(sig, frame):
    """CIERRE CONTROLADO"""
    print(
        colored(
            f"\nTe vas tan rapido amor?...\n",
            "light_blue",
            "on_light_grey",
            attrs=["dark"],
        )
    )
    sys.exit(1)


signal.signal(signal.SIGINT, close_correct)


def Valid_input(interface, mac):
    """VALIDAR MAC"""
    valid_interface = re.match(r"^[e][n|t][s|h]\d{1,2}$", interface)
    valid_mac = re.match(r"^([A-Fa-f0-9]{2}[:]){5}[A-Fa-f0-9]{2}$", mac)
    return valid_interface and valid_mac


def Changer_MAC(interface, mac):
    """CAMBIADOR MAC"""
    if Valid_input(interface, mac):
        for i in tqdm(range(100), desc="Progreso"):
            time.sleep(0.1)
        subprocess.run(["ifconfig", interface, "down"])
        subprocess.run(["ifconfig", interface, "hw", "ether", mac])
        subprocess.run(["ifconfig", interface, "up"])

        print(
            colored(f"\n[+] Nueva direccion MAC disponible.", "green", attrs=["bold"])
        )
    else:
        print(colored(f"\n[!] No se ha podido camibar la MAC", "red"))


def arg():
    """ARGUMENTOS REQUERIDOS"""
    parser = argparse.ArgumentParser(description="Cambiar MAC de una intefaz de red")
    parser.add_argument(
        "-i", "--interface", required=True, dest="interface", help="Interfaz de red"
    )
    parser.add_argument(
        "-m", "--MAC", required=True, dest="mac", help="Nueva direccion MAC"
    )
    return parser.parse_args()


def main():
    Print_Figlet("LOVEMAC")
    print("\n@puerto4444")
    print("-" * 30)
    argumentos = arg()
    Changer_MAC(argumentos.interface, argumentos.mac)


if __name__ == "__main__":
    main()
