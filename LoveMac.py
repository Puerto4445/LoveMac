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
            f"\n[!] Goodbye...\n",
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
    """  
    Cambia la dirección MAC de la interfaz de red proporcionada.  

    Args:  
        interface (str): La interfaz de red.  
        mac (str): La nueva dirección MAC.  

    Returns:  
        None  
    """  
    if Valid_input(interface, mac):
        for _ in tqdm(range(100), desc="Progreso"):
            time.sleep(0.1)
        subprocess.run(["ifconfig", interface, "down"])
        subprocess.run(["ifconfig", interface, "hw", "ether", mac])
        subprocess.run(["ifconfig", interface, "up"])

        print(
            colored(f"\n[+] New MAC available", "green", attrs=["bold"])
        )
    else:
        print(colored(f"\n[!] MAC not available ", "red"))


def arg():
    """  
    Obtiene los argumentos requeridos para la ejecución del script.  

    Returns:  
        argparse.Namespace: Los argumentos proporcionados.  
    """
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
