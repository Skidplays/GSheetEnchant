from util.config import check_config, init_config, read_config
from util.data import get_helmets, get_json_data, write_to_sheet

from colorama import Fore, init

init(autoreset=True)

def main():
    if check_config is None:
        print(Fore.RED + 'Config not detected, creating one right now.')

    get_json_data()
    print(Fore.GREEN +'List of accounts ✓')
    #print(Fore.LIGHTWHITE_EX +'Storing accounts on google sheets...')

    get_helmets()
    print(Fore.GREEN + 'Helmets data ✓')

    write_to_sheet()
    print(Fore.GREEN + 'Done')

if __name__ == "__main__":
    main()