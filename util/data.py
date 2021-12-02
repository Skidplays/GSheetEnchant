from typing import Counter
import requests
import concurrent.futures
from tqdm import tqdm
from util.config import read_config
from util.sheets import update_sheets
from util.item import Player

ALL_CHARACTERS_LIST = "https://poe.ninja/api/data/d1a91d2df1f6b52a1f5888f1d593abe4/getbuildoverview"
# overview(league), type(exp,depthsolo)(optional), language(en,pt,ru,th,ge,fr,es,ko)(optional)
SPECIFIC_CHARACTER = "https://poe.ninja/api/data/7ced296e802fa437db07d9827a75b7f7/GetCharacter"
# account, name, overview(league), language(en,pt,ru,th,ge,fr,es,ko)(optional), type(exp,depthsolo)(optional)
PLAYER_LIST = []
LEAGUE = read_config().lower()

def get_json_data():
    #Create link
    payload = {'overview': LEAGUE,'type': 'exp', 'language': 'en'}

    try:
        r = requests.get(ALL_CHARACTERS_LIST, params= payload, timeout=5)
        r.raise_for_status()
    except requests.exceptions.HTTPError as errh:
        print ("Http Error:",errh)
    except requests.exceptions.ConnectionError as errc:
        print ("Error Connecting:",errc)
    except requests.exceptions.Timeout as errt:
        print ("Timeout Error:",errt)
    except requests.exceptions.RequestException as err:
        print ("Oops: Something Else",err)

    data = r.json()
    #Send to gsheet
    accounts = data.get('accounts')
    names = data.get('names')
    update_sheets(2, accounts, 'A')
    update_sheets(2, names, 'B')
    #zip into (acc, name) and return for futher processing
    return zip(accounts, names), len(accounts)

def get_individual_data(account: str, name: str):
    payload = {'account': account, 'name': name, 'overview': LEAGUE,'type': 'exp', 'language': 'en'}

    try:
        r = requests.get(SPECIFIC_CHARACTER, params=payload)
        r.raise_for_status()
    except requests.exceptions.HTTPError as errh:
        print ("Http Error:",errh)
    except requests.exceptions.ConnectionError as errc:
        print ("Error Connecting:",errc)
    except requests.exceptions.Timeout as errt:
        print ("Timeout Error:",errt)
    except requests.exceptions.RequestException as err:
        print ("Oops: Something Else",err)

    data = r.json()

    #Filter to helmets only

    for i in range(len(data['items'])):
        if(data['items'][i]['itemData']['inventoryId']) == 'Helm':
            helmet_name = data['items'][i]['itemData']['name']
            helmet_base = data['items'][i]['itemData']['baseType']
            ilv = data['items'][i]['itemData']['ilvl']
            if(data['items'][i]['itemClass']) == 3: #Is unique
                unique = True
            else:
                unique = False
                
            if 'enchantMods' in data['items'][i]['itemData']:
                enchantment = data['items'][i]['itemData']['enchantMods'][0]
            else:
                enchantment = ""

    player = Player(account, name, helmet_name, helmet_base, ilv, unique, enchantment)
    PLAYER_LIST.append(player)

def get_helmets():
    list_of_player, count = get_json_data()
    accounts, names = zip(*list_of_player)

    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        list(tqdm(executor.map(get_individual_data, accounts, names), total=count))

def write_to_sheet():
    helm_list = []
    enchant_list = []
    for i in PLAYER_LIST:
        helm_list.append(i.display_name)
        enchant_list.append(i.enchantment)
    
    update_sheets(3, helm_list, 'A')
    update_sheets(3, enchant_list, 'B')