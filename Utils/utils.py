import Chromify, requests, os, time, math, re, toml, yaml, asyncio, httpx
from pathlib import Path
from Configs.colors import c

mcchat = '[Client thread/INFO]: [CHAT]'

class meta:
    version = 'T'
    authors = 'Toxikuu, Hollow, Scycle'
    thx1 = 'Nolqk, Zani, Sedged, Yhuvko, Praxzz, Virse'
    thx2 = 'Plonk, i5tar, Nea, Nuclear'
    discord = 'https://discord.gg/N3rVjjVEsv'

class dirs:
    samael = os.path.dirname(os.path.dirname(__file__))
    lists = os.path.join(samael, 'Lists')
    configs = os.path.join(samael, 'Configs')

class paths:
    bl = os.path.join(dirs.lists, 'Blacklist.log')
    sl = os.path.join(dirs.lists, 'Safelist.log')
    wl = os.path.join(dirs.lists, 'Weirdlist.log')
    rec = os.path.join(dirs.lists, 'Record.log')
    notes = os.path.join(dirs.lists, 'Notes.log')
    logs = [bl, sl, wl, rec, notes]
    toml = os.path.join(dirs.configs, 'Config.toml')
    kb = os.path.join(dirs.configs, 'Keybinds.toml')
    yaml = os.path.join(dirs.configs, 'Settings.yaml')
    chat = os.path.join(Path.home(), '.lunarclient', 'offline', 'multiver', 'logs', 'latest.log')

class tags:
    safe = f'[{c.safe}]Safe[/]'
    risky = f'[{c.risky}]Risky[/]'
    danger = f'[{c.black} on {c.danger}]Danger[/]'
    dodge = f'[{c.black} on {c.dodge}]DODGE[/]'
    fuck = f'[{c.black} on {c.fuck}]FUCK!![/]'

async def uuidtoign(uuid):
    try:
        pdb = await req(f"https://playerdb.co/api/player/minecraft/{uuid}")
        ign = pdb["data"]["player"]["username"]
    except:
        from rich import print
        print(f"[{c.black} on {c.fuck}][i] \[!] Failed to access ign for {uuid}!")
    return ign

async def igntouuid(ign):
    if ign != '':
        try:
            pdb = await req(f"https://playerdb.co/api/player/minecraft/{ign}")
            uuid = pdb["data"]["player"]["raw_id"]
        except:
            from rich import print
            print(f"[{c.black} on {c.fuck}][i] \[!] Failed to access uuid for {ign}!")
        return uuid
    else:
        return None

async def add_to_list(ign, l):
    with open(l, 'a') as f:
        f.write(await igntouuid(ign)+'\n')
        print(f' [i] Added {ign} to {os.path.basename(l)}!')

async def remove_from_list(ign, l):
    uuid = await igntouuid(ign)
    with open(l, 'r') as f:
        lines = f.readlines()

    lines = [line for line in lines if uuid not in line]

    with open(l, 'w') as f:
        f.writelines(lines)
        print(f' [i] Removed {ign} from {os.path.basename(l)}!')

async def make_note(ign, note):
    with open(paths.notes, 'a') as f:
        f.write(f"Target: {ign} UUID: {await igntouuid(ign)} Note: {note}\n")
        print(f" [i] Noted {ign}!")

def cls():
    if os.name == 'nt':
        _ = os.system('cls')
    else:
        _ = os.system('clear')

def splash():
    Chromify.init()
    cls()

    slices = {
        'a': ' ______     ______     __    __     ______     ______     __        ',
        'b': '/\  ___\   /\  __ \   /\ "-./  \   /\  __ \   /\  ___\   /\ \       ',
        'c': '\ \___  \  \ \  __ \  \ \ \-./\ \  \ \  __ \  \ \  __\   \ \ \____  ',
        'd': ' \/\_____\  \ \_\ \_\  \ \_\ \ \_\  \ \_\ \_\  \ \_____\  \ \_____\ ',
        'e': '  \/_____/   \/_/\/_/   \/_/  \/_/   \/_/\/_/   \/_____/   \/_____/ \n',
        'f': ' [$] Version: ' + meta.version + ' ' * (54-len(meta.version)),
        'g': ' [$] Made by: ' + meta.authors + ' ' * (54-len(meta.authors)),
        'h': ' [$] Thanks: ' + meta.thx1 + ' ' * (55-len(meta.thx1)),
        'i': ' [$] More thanks: ' + meta.thx2 + ' ' * (50-len(meta.thx2)),
        'j': ' [$] Discord: ' + meta.discord + ' ' * (54-len(meta.discord)) + '\n',
    }

    for key in slices:
        print(Chromify.gradient(Chromify.Color('#FF0000'), Chromify.Color('#FF1493'), slices[key], background=False))

def readtoml(file):
    with open(file, 'r') as f:
        return toml.load(f)

def readyaml():
    with open(paths.yaml, 'r') as f:
        return yaml.safe_load(f)

def clearfile(file):
    with open(file, 'w') as f:
        f.write('')

def mkdir(dir):
    if not os.path.exists(dir):
        os.mkdir(dir)

def touch(path):
    if not os.path.exists(path):
        with open(path, 'x') as f: pass

def samtree():
    mkdir(dirs.lists)
    for log in paths.logs:
        if not os.path.exists(log): touch(log)

async def req(url):
    async with httpx.AsyncClient() as cli:
        r = await cli.get(url)
        return r.json()

async def get_hypixel_stats(apikey, uuid):
    if uuid != None:
        url = f"https://api.hypixel.net/player?key={apikey}&uuid={uuid}"
        data = await req(url)
        return data

def follow(file):
    file.seek(0,2)
    while True:
        line = file.readline()
        if not line:
            time.sleep(0.04)
            continue
        yield line

def countOf(list, x):
    count = 0
    for element in list:
        if element == x:
            count += 1
    return count

def div(value1, value2, precision):
    if value2 == 0: value2 = 1
    return round(value1/value2, precision)

def get_category(y, section, value):
        value = float(value)
        try: thresholds = y['Thresholds'][section]
        except KeyError: thresholds = None
        if thresholds != None:
            for category, (start, end) in thresholds.items():
                if start == None: start = 0
                if end == None: end = float('inf')

                if start <= value < end:
                    return category
            return "Danger"

def get_value_from_json(json_obj, path):
    # Split the path into individual keys
    keys = path.split('/$/')

    # Iterate through the keys to traverse the JSON object
    current = json_obj
    for key in keys:
        if isinstance(current, dict) and key in current:
            current = current[key]
        else:
            current = 0

    return current

def sect():
    print('-'*36)

async def statsxd(y, t, uuid, apikey):
    hy = await get_hypixel_stats(apikey, uuid)

    # hypath shortcuts
    sw_hypath = 'player/$/stats/$/SkyWars'
    bw_hypath = 'player/$/stats/$/Bedwars'
    d_hypath = 'player/$/stats/$/Duels'
    uhc_hypath = 'player/$/stats/$/UHC'
    sg_hypath = 'player/$/stats/$/HungerGames'
    pit_hypath = 'player/$/stats/$/Pit/$/pit_stats_pt1'
    ww_hypath = 'player/$/stats/$/WoolGames/$/wool_wars/$/stats'

    # hypaths dictionary
    hypaths = {
        'NWL' : 'player/$/networkExp',

        'SW star' : f'{sw_hypath}/$/levelFormattedWithBrackets',
        'SW kills' : f'{sw_hypath}/$/kills',
        'SW deaths' : f'{sw_hypath}/$/deaths',
        'SW wins' : f'{sw_hypath}/$/wins',
        'SW losses' : f'{sw_hypath}/$/losses',

        'BW star' : 'player/$/achievements/$/bedwars_level',
        'BW fks' : f'{bw_hypath}/$/final_kills_bedwars',
        'BW fds' : f'{bw_hypath}/$/final_deaths_bedwars',
        'Beds lost' : f'{bw_hypath}/$/beds_lost_bedwars',
        'Beds broken' : f'{bw_hypath}/$/beds_broken_bedwars',
        'BW kills' : f'{bw_hypath}/$/kills_bedwars',
        'BW deaths' : f'{bw_hypath}/$/deaths_bedwars',

        'Sumo wins' : f'{d_hypath}/$/sumo_duel_wins',
        'Sumo losses' : f'{d_hypath}/$/sumo_duel_losses',
        'Sumo bws' : f'{d_hypath}/$/best_sumo_winstreak',
        'Sumo cws' : f'{d_hypath}/$/current_sumo_winstreak',

        'UHCD1 wins' : f'{d_hypath}/$/uhc_duel_wins',
        'UHCD1 losses': f'{d_hypath}/$/uhc_duel_losses',
        'UHCD2 wins' : f'{d_hypath}/$/uhc_doubles_wins',
        'UHCD2 losses': f'{d_hypath}/$/uhc_doubles_losses',
        'UHCD4 wins': f'{d_hypath}/$/uhc_four_losses',
        'UHCD4 losses': f'{d_hypath}/$/uhc_four_losses',
        'UHCD bws': f'{d_hypath}/$/best_uhc_winstreak',
        'UHCD cws': f'{d_hypath}/$/current_uhc_winstreak',

        'Classic wins': f'{d_hypath}/$/classic_duel_wins',
        'Classic losses': f'{d_hypath}/$/classic_duel_losses',

        'Bow wins': f'{d_hypath}/$/bow_duel_wins',
        'Bow losses': f'{d_hypath}/$/bow_duel_losses',

        'Parkour wins': f'{d_hypath}/$/parkour_eight_wins',
        'Parkour losses': f'{d_hypath}/$/parkour_eight_losses',

        'Boxing wins': f'{d_hypath}/$/boxing_duel_wins',
        'Boxing losses': f'{d_hypath}/$/boxing_duel_losses',

        'Skywars1 wins': f'{d_hypath}/$/sw_duel_wins',
        'Skywars1 losses': f'{d_hypath}/$/sw_duel_losses',
        'Skywars2 wins': f'{d_hypath}/$/sw_doubles_wins',
        'Skywars2 losses': f'{d_hypath}/$/sw_doubles_losses',

        'Combo wins': f'{d_hypath}/$/combo_duel_wins',
        'Combo losses': f'{d_hypath}/$/combo_duel_losses',

        'TNT wins': f'{d_hypath}/$/bowspleef_duel_wins',
        'TNT losses': f'{d_hypath}/$/bowspleef_duel_losses',

        'Bridge1 wins': f'{d_hypath}/$/bridge_duel_wins',
        'Bridge1 losses': f'{d_hypath}/$/bridge_duel_losses',
        'Bridge2 wins': f'{d_hypath}/$/bridge_doubles_wins',
        'Bridge2 losses': f'{d_hypath}/$/bridge_doubles_losses',
        'Bridge3 wins': f'{d_hypath}/$/bridge_threes_wins',
        'Bridge3 losses': f'{d_hypath}/$/bridge_threes_losses',
        'Bridge4 wins': f'{d_hypath}/$/bridge_four_wins',
        'Bridge4 losses': f'{d_hypath}/$/bridge_four_losses',
        'Bridge2x4 wins': f'{d_hypath}/$/bridge_2v2v2v2_wins',
        'Bridge2x4 losses': f'{d_hypath}/$/bridge_2v2v2v2_losses',
        'Bridge3x4 wins': f'{d_hypath}/$/bridge_3v3v3v3_wins',
        'Bridge3x4 losses': f'{d_hypath}/$/bridge_3v3v3v3_losses',
        'BridgeCTF wins': f'{d_hypath}/$/capture_threes_wins',
        'BridgeCTF losses': f'{d_hypath}/$/capture_threes_losses',

        'Combo swings' : f'{d_hypath}/$/combo_duel_melee_swings',
        'Combo hits' : f'{d_hypath}/$/combo_duel_melee_hits',

        'NDB wins' : f'{d_hypath}/$/potion_duel_wins',
        'NDB losses' : f'{d_hypath}/$/potion_duel_losses',

        'OP1 wins' : f'{d_hypath}/$/op_duel_wins',
        'OP1 losses' : f'{d_hypath}/$/op_duel_losses',
        'OP2 wins' : f'{d_hypath}/$/op_doubles_wins',
        'OP2 losses' : f'{d_hypath}/$/op_doubles_losses',

        'MWD1 wins' : f'{d_hypath}/$/mw_duel_wins',
        'MWD1 losses' : f'{d_hypath}/$/mw_duel_losses',
        'MWD2 wins' : f'{d_hypath}/$/mw_doubles_wins',
        'MWD2 losses' : f'{d_hypath}/$/mw_doubles_losses',

        'UHC kills' : f'{uhc_hypath}/$/kills',
        'UHC kills2' : f'{uhc_hypath}/$/kills_solo',
        'UHC deaths' : f'{uhc_hypath}/$/deaths',
        'UHC deaths2' : f'{uhc_hypath}/$/deaths_solo',
        'UHC wins' : f'{uhc_hypath}/$/wins',
        'UHC games' : f'{uhc_hypath}/$/games_played',

        'Duels wins' : f'{d_hypath}/$/wins',
        'Duels losses' : f'{d_hypath}/$/losses',
        'Duels bws' : f'{d_hypath}/$/best_overall_winstreak',
        'Duels cws' : f'{d_hypath}/$/current_winstreak',
        'Duels swings' : f'{d_hypath}/$/melee_swings',
        'Duels hits' : f'{d_hypath}/$/melee_hits',

        'Combo swings' : f'{d_hypath}/$/combo_duel_melee_swings',
        'Combo hits' : f'{d_hypath}/$/combo_duel_melee_hits',
        'Combo wins': f'{d_hypath}/$/combo_duel_wins',
        'Combo losses': f'{d_hypath}/$/combo_duel_losses',

        'NDB wins' : f'{d_hypath}/$/potion_duel_wins',
        'NDB losses' : f'{d_hypath}/$/potion_duel_losses',

        'OP wins' : f'{d_hypath}/$/op_duel_wins',
        'OP losses' : f'{d_hypath}/$/op_duel_losses',

        'MWD wins' : f'{d_hypath}/$/mw_duel_wins',
        'MWD losses' : f'{d_hypath}/$/mw_duel_losses',

        'Blitzd wins' : f'{d_hypath}/$/blitz_duel_wins',
        'Blitzd losses' : f'{d_hypath}/$/blitz_duel_losses',

        'SG wins' : f'{sg_hypath}/$/wins',
        'SG games' : f'{sg_hypath}/$/games_played',
        'SG kills' : f'{sg_hypath}/$/kills',
        'SG deaths' : f'{sg_hypath}/$/deaths',

        'Pit kills' : f'{pit_hypath}/$/kills',
        'Pit deaths' : f'{pit_hypath}/$/deaths',
        'Pit max streak' : f'{pit_hypath}/$/max_streak',

        'WW wins' : f'{ww_hypath}/$/wins',
        'WW games' : f'{ww_hypath}/$/games_played',
        'WW kills' : f'{ww_hypath}/$/kills',
        'WW deaths' : f'{ww_hypath}/$/deaths'
    }

    # converts hypaths to stats
    hystats = {key: get_value_from_json(hy, value) for key, value in hypaths.items()}

    # Fixing Hypixel's shitty api
    hystats['NWL'] = round(((math.sqrt((2 * hystats['NWL']) + 30625) / 50) - 2.5), t["options"]["rounding_precision"])
    if hystats['SW star'] == 0:
        hystats['SW star'] = '[0*]'
    # if cfg.devmode: print('Raw SW star:', hystats['SW star'])
    sw_star_in = hystats['SW star']
    sw_star_out = (re.sub(r'§.', '', sw_star_in)).strip('[] ')
    sw_star_out = sw_star_out[:-1]
    # if cfg.devmode: print('Cleaned SW star:', sw_star_out)
    hystats['SW star'] = sw_star_out
    hystats['SW kdr'] = div(hystats['SW kills'], hystats['SW deaths'], t["options"]["rounding_precision"])
    hystats['SW wlr'] = div(hystats['SW wins'], hystats['SW losses'], t["options"]["rounding_precision"])

    hystats['BW fkdr'] = div(hystats['BW fks'], hystats['BW fds'], t["options"]["rounding_precision"])
    hystats['BW bblr'] = div(hystats['Beds broken'], hystats['Beds lost'], t["options"]["rounding_precision"])
    hystats['BW kdr'] = div(hystats['BW kills'], hystats['BW deaths'], t["options"]["rounding_precision"])
    hystats['BW fksperstar'] = div(hystats['BW fks'], hystats['BW star'], t["options"]["rounding_precision"])

    hystats['Sumo wlr'] = div(hystats['Sumo wins'], hystats['Sumo losses'], t["options"]["rounding_precision"])

    hystats['UHCD wins'] = (hystats['UHCD1 wins'] + hystats['UHCD2 wins'] + hystats['UHCD4 wins'])
    hystats['UHCD losses'] = (hystats['UHCD1 losses'] + hystats['UHCD2 losses'] + hystats['UHCD4 losses'])
    hystats['UHCD wlr'] = div(hystats['UHCD wins'], hystats['UHCD losses'], t["options"]["rounding_precision"])
    hystats['UHC kills'] = hystats['UHC kills'] + hystats['UHC kills2']
    hystats['UHC deaths'] = hystats['UHC deaths'] + hystats['UHC deaths2']
    hystats['UHC kdr'] = div(hystats['UHC kills'], hystats['UHC deaths'], t["options"]["rounding_precision"])

    hystats['UHC kdr'] = div(hystats['UHC kills'], hystats['UHC deaths'], t["options"]["rounding_precision"])
    hystats['UHC winrate'] = div(hystats['UHC wins'], hystats['UHC games'], t["options"]["rounding_precision"])
    hystats['Melee Acc'] = div(hystats['Duels hits'], hystats['Duels swings'], t["options"]["rounding_precision"])
    hystats['Combo Melee Acc'] = div(hystats['Combo hits'], hystats['Combo swings'], t["options"]["rounding_precision"])
    hystats['NDB wlr'] = div(hystats['NDB wins'], hystats['NDB losses'], t["options"]["rounding_precision"])

    hystats['OP wins'] = (hystats['OP1 wins'] + hystats['OP2 wins'])
    hystats['OP losses'] = (hystats['OP1 losses'] + hystats['OP2 losses'])
    hystats['OP wlr'] = div(hystats['OP wins'], hystats['OP losses'], t["options"]["rounding_precision"])

    hystats['MWD wins'] = (hystats['MWD1 wins'] + hystats['MWD2 wins'])
    hystats['MWD losses'] = (hystats['MWD1 losses'] + hystats['MWD2 losses'])
    hystats['MWD wlr'] = div(hystats['MWD wins'], hystats['MWD losses'], t["options"]["rounding_precision"])

    hystats['Bridge wins'] = (hystats['Bridge1 wins'] + hystats['Bridge2 wins'] + hystats['Bridge4 wins'] + hystats['Bridge2x4 wins'] + hystats['Bridge3x4 wins'] + hystats['BridgeCTF wins'])
    hystats['Bridge losses'] = (hystats['Bridge1 losses'] + hystats['Bridge2 losses'] + hystats['Bridge4 losses'] + hystats['Bridge2x4 losses'] + hystats['Bridge3x4 losses'] + hystats['BridgeCTF losses'])
    hystats['Bridge wlr'] = div(hystats['Bridge wins'], hystats['Bridge losses'], t["options"]["rounding_precision"])
    hystats['Classic wlr'] = div(hystats['Classic wins'], hystats['Classic losses'], t["options"]["rounding_precision"])
    hystats['Boxing wlr'] = div(hystats['Boxing wins'], hystats['Boxing losses'], t["options"]["rounding_precision"])
    hystats['Bow wlr'] = div(hystats['Bow wins'], hystats['Bow losses'], t["options"]["rounding_precision"])
    hystats['TNT wlr'] = div(hystats['TNT wins'], hystats['TNT losses'], t["options"]["rounding_precision"])
    hystats['Parkour wlr'] = div(hystats['Parkour wins'], hystats['Parkour losses'], t["options"]["rounding_precision"])
    hystats['Skywars wins'] = (hystats['Skywars1 wins'] + hystats['Skywars2 wins'])
    hystats['Skywars losses'] = (hystats['Skywars1 losses'] + hystats['Skywars2 losses'])
    hystats['Skywars wlr'] = div(hystats['Skywars wins'], hystats['Skywars losses'], t["options"]["rounding_precision"])
    hystats['Combo wlr'] = div(hystats['Combo wins'], hystats['Combo losses'], t["options"]["rounding_precision"])

    hystats['Blitzd wlr'] = div(hystats['Blitzd wins'], hystats['Blitzd losses'], t["options"]["rounding_precision"])
    hystats['Duels wlr'] = div(hystats['Duels wins'], hystats['Duels losses'], t["options"]["rounding_precision"])
    hystats['SG games'] = hystats['SG wins'] + hystats['SG games']
    hystats['SG winrate'] = div(hystats['SG wins'], hystats['SG games'], t["options"]["rounding_precision"])
    hystats['SG kdr'] = div(hystats['SG kills'], hystats['SG deaths'], t["options"]["rounding_precision"])
    hystats['Pit kdr'] = div(hystats['Pit kills'], hystats['Pit deaths'], t["options"]["rounding_precision"])
    hystats['WW winrate'] = div(hystats['WW wins'], hystats['WW games'], t["options"]["rounding_precision"])
    hystats['WW kdr'] = div(hystats['WW kills'], hystats['WW deaths'], t["options"]["rounding_precision"])

    # Error avoidance
    hystats = {key: 0 if (str(value)).strip() == '' else value for key, value in hystats.items()}
    hystats = {key: float(value) if value is not None else 0 for key, value in hystats.items()}
    hystats = {key: int(value) if isinstance(value, float) and value.is_integer() else value for key, value in hystats.items()}

    # Active stats dictionary
    active_keys = [key for key, value in y['Active'].items() if value]
    HyStats = {key: value for key, value in hystats.items() if key in active_keys}

    # Sorting
    active_keys_ordered = list(y['Active'].keys())
    Hys = {key: HyStats[key] for key in active_keys_ordered if key in HyStats}
    return Hys, hy

def get_verdict(y, value):
    verdicts = y["Verdicts"]
    for verdict, (start, end) in verdicts.items():
        if start == None: start = float('-inf')
        if end == None: end = float('inf')
        if start <= value < end:
            return verdict
    return "Error"

async def check_flags(name, uuid, Hys, t, verdict_score, hy):
    flags = {
        'fl_name': False,
        'fl_api': False,
        'fl_proj': False,
        'fl_bl': False,
        'fl_sl': False,
        'fl_wl': False,
        'fl_Sbl': False,
        'fl_Ssl': False,
        'fl_Swl': False,
        'fl_notes': False
    }
    fl = []
    
    # name flag
    if len(name) < 5:
        flags['fl_name'] = True
    for nameflag in t["nameflags"]["nameflags"]:
        if nameflag in name:
            flags['fl_name'] = True
    
    # api flag
    if Hys["Duels bws"] == 0 and Hys["Duels wins"] > 5:
        flags['fl_api'] = True

    # projectiles flag
    if get_value_from_json(hy, 'player/$/disabledProjectileTrails'):
        flags['fl_proj'] = True

    # blacklist
    with open(paths.bl, 'r') as f:
        for line in f.readlines():
            line = line.strip()
            if uuid != None:
                if line == uuid:
                    flags['fl_bl'] = True
                if uuid in line and '[$] ' in line:
                    flags['fl_Sbl'] = True

    # safelist
    with open(paths.sl, 'r') as f:
        for line in f.readlines():
            line = line.strip()
            if uuid != None:
                if line == uuid:
                    flags['fl_sl']= True
                if uuid in line and '[$] ' in line:
                    flags['fl_Ssl'] = True
    
    # weirdlist
    with open(paths.wl, 'r') as f:
        for line in f.readlines():
            line = line.strip()
            if uuid != None:
                if line == uuid:
                    flags['fl_wl'] = True
                if uuid in line and '[$] ' in line:
                    flags['fl_Swl'] = True

    # notes
    note = None
    with open(paths.notes, 'r') as f:
        for line in f.readlines():
            if uuid != None:
                if uuid in line:
                    note = line[line.index('Note: "')+7:line.index('"\n', line.index('Note: "')+1)]
                    flags['fl_notes'] = True

    for key, value in flags.items():
        if value: fl.append(key)

    if len(fl) > 0:
        return fl, True, note
    else:
        return None, False, None

async def remove_duplicates():
    ls = [paths.bl, paths.sl, paths.wl]
    for l in ls:
        with open(l, 'r') as f:
            lines = f.readlines()
    
        lines = list(dict.fromkeys(lines))

        with open(l, 'w') as f:
            f.writelines(lines)
    
async def update_toml(section, key, new_value):
    t = toml.load(paths.toml)
    t[section][key] = new_value

    f = open(paths.toml, 'w')
    toml.dump(t, f)
    f.close()

def record_to_list(filename):
    wonids = []
    lostids = []

    with open(filename, 'r') as f:
        lines = f.readlines()
    
    for line in lines:
        if 'W:' in line:
            wonids.append(line.replace('W:', '').strip())
        if 'L:' in line:
            lostids.append(line.replace('W:', '').strip())

    return wonids, lostids

def linux_hotkey(key):
    os.system(f"xte 'keydown {key}'")
    time.sleep(0.05)
    os.system(f"xte 'keyup {key}'")

def windows_hotkey(key):
    from keyboard import press_and_release as tap
    tap(key)

async def polsu_ping(uuid, apikey):
    import http.client

    conn = http.client.HTTPSConnection("api.polsu.xyz")

    headers = { 'API-Key': apikey }

    conn.request("GET", f"/polsu/ping?uuid={uuid}", headers=headers)

    res = conn.getresponse()
    data = res.read()
    if "error code: 1106" in str(data):
        print("Try disabling ipv6")

    return data.decode("utf-8")
