#!/usr/bin/python3  
import argparse  
import re  
import subprocess  
import sys  
import signal  
from termcolor import colored  
from pyfiglet import Figlet  

class MACChanger:  
    """  
    A class to handle MAC address changing functionality.  
    """  
    def __init__(self):  
        signal.signal(signal.SIGINT, self.close_correct)  
    @staticmethod  
    def print_banner(text):  
        """  
        Generate and print a colorful ASCII art banner.  

        Args:  
            text (str): Text to be displayed in the banner  
        """  
        figlet = Figlet(font="5lineoblique")  
        ascii_art = figlet.renderText(text)  
        
        try:  
            lolcat_process = subprocess.Popen(["lolcat"], stdin=subprocess.PIPE)  
            lolcat_process.communicate(input=ascii_art.encode())  
        except FileNotFoundError:  
            print(ascii_art)  

    @staticmethod  
    def validate_input(interface, mac):  
        """  
        Validate the network interface and MAC address.  

        Args:  
            interface (str): Network interface name  
            mac (str): MAC address to be set  

        Returns:  
            bool: True if both interface and MAC are valid, False otherwise  
        """  
        valid_interface = re.match(r"^[e][n|t][s|h]\d{1,2}$", interface)  
        valid_mac = re.match(r"^([A-Fa-f0-9]{2}[:]){5}[A-Fa-f0-9]{2}$", mac)  
        return bool(valid_interface and valid_mac)  

    def change_mac(self, interface, mac):  
        """  
        Change the MAC address of the specified network interface.  

        Args:  
            interface (str): Network interface name  
            mac (str): New MAC address  

        Returns:  
            bool: True if MAC change is successful, False otherwise  
        """  
        if not self.validate_input(interface, mac):  
            print(colored("\n[!] Invalid interface or MAC address", "red"))  
            return False  

        try:   
            subprocess.run(["ifconfig", interface, "down"], check=True)  
             
            subprocess.run(["ifconfig", interface, "hw", "ether", mac], check=True)  
             
            subprocess.run(["ifconfig", interface, "up"], check=True)  

            print(colored(f"\n[+] MAC address changed to {mac} on {interface}", "green", attrs=["bold"]))  
            return True  
        except subprocess.CalledProcessError as e:  
            print(colored(f"\n[!] Error changing MAC: {e}", "red"))  
            return False  

    @staticmethod  
    def close_correct(sig=None, frame=None):  
        """  
        Handle graceful exit when SIGINT is received.  

        Args:  
            sig: Signal number  
            frame: Current stack frame  
        """  
        print(  
            colored(  
                f"\n[!] Goodbye...\n",  
                "light_blue",  
                "on_light_grey",  
                attrs=["dark"],  
            )  
        )  
        sys.exit(1)  

    @staticmethod  
    def parse_arguments():  
        """  
        Parse command-line arguments.  

        Returns:  
            argparse.Namespace: Parsed arguments  
        """  
        parser = argparse.ArgumentParser(description="Change MAC address of a network interface")  
        parser.add_argument(  
            "-i", "--interface",   
            required=True,   
            dest="interface",   
            help="Network interface"  
        )  
        parser.add_argument(  
            "-m", "--MAC",   
            required=True,   
            dest="mac",   
            help="New MAC address"  
        )  
        return parser.parse_args()  

def main():  
    """  
    Main function to execute MAC address changing process.  
    """   
    mac_changer = MACChanger()  
    
    mac_changer.print_banner("LOVEMAC")  
    print("\n@puerto4444")  
    print("-" * 30)  
 
    args = MACChanger.parse_arguments()    
    mac_changer.change_mac(args.interface, args.mac)  

if __name__ == "__main__":  
    main()
