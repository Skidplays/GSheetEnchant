from configparser import ConfigParser
import os
from colorama import Fore

config = ConfigParser()
def check_config():
    if not os.path.exists('config.ini'):
        return None
    else:
        config.read('config.ini')
        return config['settings']['league']

def init_config():
    initial_option = input(Fore.YELLOW+ 'Please enter initial league name').lower()
    print(Fore.WHITE)
    config['settings'] = {
    'league': initial_option
    }
    config.write(open('config.ini', 'w'))
    return initial_option

def read_config():
    config.read('config.ini')
    return config['settings']['league']