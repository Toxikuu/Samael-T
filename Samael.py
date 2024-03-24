import os, sys, time
from platform import system

# check if first launch
if not os.path.exists(os.path.join(os.path.dirname(__file__), 'Setup', '.t')):
    print(" [!] First launch detected!")

    os.system(f'mkdir {os.path.join(os.path.dirname(__file__), "Setup")}')
    print(' [i] Created setup directory')

    match system():
        case 'Windows':
            print(f" [i] Detected system: {system()}")
            powershellpath = r"C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe"
            powershellcmd = f"Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/Toxikuu/Samael-T/main/Setup/setup.py' -OutFile '{os.path.join(os.path.dirname(__file__), Setup, setup.py)}'"
            os.system(f'{powershellpath} {powershellcmd}')

        case 'Linux':
            print(f" [i] Detected system: {system()}")
            os.system(f'curl -o {os.path.join(os.path.dirname(__file__), "Setup", "setup.py")} -L https://raw.githubusercontent.com/Toxikuu/Samael-T/main/Setup/setup.py')

    setupcmd = f"python {os.path.join(os.path.dirname(__file__), 'Setup', 'setup.py')}"
    # print(setupcmd)
    os.system(setupcmd)
    os.remove(__file__)
    sys.exit()

import math, configparser, re, shutil, toml, asyncio, json
from Utils.utils import *
from Configs.colors import *
from pprint import pprint as pp
from rich import print
from platform import system
 
# init vars
version = 'T'
discord = 'https://discord.gg/N3rVjjVEsv'

# startup
splash()
global t
t = readtoml(paths.toml)
y = readyaml()
kb = readtoml(paths.kb)
checked = []

def reload_t():
    global dev, delim, apikey
    dev = t['dev']['dev']
    delim = t['delimiter']['delimiter_type']
    apikey = t['apikey']['apikey']
    if delim == 0: delim = '▌'
    else: delim = '?'
    return dev, delim, apikey
dev, delim, apikey = reload_t()

if dev: pp(toml); pp(y)
if dev: print('Delimiter:', delim)

samtree()
clearfile(paths.rec)

def readchat():
    if t['paths']['chat'] != '':
        paths.chat = t['paths']['chat']
    return follow(open(paths.chat, 'r'))

chatlines = readchat()
if dev: print(f"Using chat path: {paths.chat}")

def get_target(line):
    # /sc
    if f"{mcchat} {delim}" in line and f"{mcchat} {delim} W/L: " not in line and "Lvl:" in line:

        iso1 = (line[line.index('[CHAT]')+7:line.index('Lvl:')]).strip()+'$' # 1 = isolation 1

        if dev: print("\n$\niso1:", iso1)

        if '[' in iso1 and ']' in iso1:
            iso2 = (iso1[iso1.index('] ')+2:iso1.index('$')]).strip() # 2 = name

            if dev: print("Isolated name:", iso2)

            iso3 = (iso1[iso1.index('['):iso1.index(']')+1]).strip() # 3 = rank
            if '§' in iso3:
                iso3 = re.sub('§.', '', iso3) 

            if dev: print("Isolated rank:", iso3)

            print(f"Statslol: {iso3} {iso2}")

        else: # nons
            iso2 = (iso1[iso1.index(delim)+1:iso1.index('$')].strip())
            iso3 = '[NON]'
            if dev: print("Isolated non:", iso2)

            print(f"Statslol: {iso3} {iso2}")
        
    # nicks
    if f"{mcchat} Lilith > Found" in line and " likely nicked players: Possibly " in line and "Possibly \n" not in line:
        iso2 = str((line[line.index("Possibly ")+9:line.index('\n', (line.index("Possibly ")+9)+1)]).strip(', '))
        iso3 = '[?]'
        if dev: print(f'Nick found: {iso2}')
        if iso2 != '':
            print(f"statslol {iso3} {iso2}")
            if dev: print(f'Skipped statslol() since name_nick = <{iso5}>')
        
    try: return iso3, iso2
    except: return None, None

def get_cmd(line):
    if f"{mcchat} -" in line and f"{mcchat} -----" not in line:
        cmd = line.replace(mcchat, '')
        cmd = cmd[cmd.index('-'):]
        print(f'\nDetected command: {cmd}')
        return cmd
    else: 
        return None

async def header(rank, name):
    if name is not None and name != '':
        cls()
        uuid = await igntouuid(name)
        if uuid is not None:
            print(f'[bold]Checking: {rank} {name}')
            print(f'[{c.grey}]UUID: {uuid}')
            await getping(uuid)
            sect()
            return uuid
        else: return None
    else: return None
    # add guild shit later

async def samprint(Hys):
    # PRINT STATS
    verdict_score = 0
    for key, value in Hys.items():
        tag = get_category(y, key, value)
        if tag != None:
            if tag == 'Safe' and t["options"]["show_safe"]:
                print(f'{tags.safe} || {key}: [{c.safe}]{value}')
            if tag == 'Risky' and t["options"]["show_risky"]:
                print(f'{tags.risky}  || {key}: [{c.risky}]{value}')
                verdict_score += .5
            if tag == 'Danger' and t["options"]["show_danger"]:
                print(f'{tags.danger} || {key}: [{c.danger}]{value}')
                verdict_score += 3
            if tag == 'Dodge' and t["options"]["show_dodge"]:
                print(f'{tags.dodge}  || {key}: [{c.dodge}]{value}')
                verdict_score += 6
            if tag == 'Fuck' and t["options"]["show_fuck"]:
                print(f'{tags.fuck} || {key}: [{c.fuck}]{value}')
                verdict_score += 12
            
            # time.sleep(0.001)
    sect()
    return verdict_score

async def display_flags(active_flags, note, verdict_score):
    displays = {
        "fl_name": f"[{c.lightrisky}] >> [{c.black} on {c.risky}] NAME FLAG [/][{c.lightrisky}] << ",
        "fl_proj": f"[{c.lightrisky}] >> [{c.black} on {c.risky}] Projectile Trail Disabled [/][{c.lightrisky}] << ",
        "fl_api": f"[{c.lightrisky}] >> [{c.black} on {c.risky}] API OFF [/][{c.lightrisky}] << ",
        "fl_bl": f"[{c.lightdodge}] >> [{c.black} on {c.dodge}] BLACKLISTED [/][{c.lightdodge}] << ",
        "fl_sl": f"[{c.lightsafe}] >> [{c.black} on {c.safe}] SAFELISTED [/][{c.lightsafe}] << ",
        "fl_wl": f"[{c.lightrisky}] >> [{c.black} on {c.risky}] WEIRDLISTED [/][{c.lightrisky}] << ",
        "fl_Sbl": f"[{c.lightdodge}] >> [{c.black} on {c.dodge}] [$] BLACKLISTED [/][{c.lightdodge}] << ",
        "fl_Ssl": f"[{c.lightsafe}] >> [{c.black} on {c.safe}] [$] SAFELISTED [/][{c.lightsafe}] << ",
        "fl_Swl": f"[{c.lightrisky}] >> [{c.black} on {c.risky}] [$] WEIRDLISTED [/][{c.lightrisky}] << ",
        "fl_notes": f"[{c.white}] >> [{c.black} on {c.notes}] {note} [/][{c.white}] << ",
    }

    for key, value in displays.items():
        if key in active_flags:
            print(value)

            if key.startswith("fl_name"):
                verdict_score += 5
            elif key.startswith("fl_bl") or key.startswith("fl_Sbl"):
                verdict_score += 10
            elif key.startswith("fl_sl"):
                verdict_score -= 10
            elif key.startswith("fl_Ssl"):
                verdict_score -= 5
            elif key.startswith("fl_wl") or key.startswith("fl_Swl"):
                verdict_score += 5

    sect()
    return verdict_score

def final_verdict(verdict_score):
    verdict = get_verdict(y, verdict_score)
    if verdict == "You're straight chilling af":
        f_verdict = f"[{c.black} on {c.sosafe}] {verdict} "
        f_verdict_score = f"[{c.sosafe}]{verdict_score}"
        vnum = 1
    elif verdict == "Prolly stay":
        f_verdict = f"[{c.black} on {c.safe}] {verdict} "
        f_verdict_score = f"[{c.safe}]{verdict_score}"
        vnum = 2
    elif verdict == "Sorta scary":
        f_verdict = f"[{c.black} on {c.risky}] {verdict} "
        f_verdict_score = f"[{c.risky}]{verdict_score}"
        vnum = 3
    elif verdict == "Dodge":
        f_verdict = f"[{c.black} on {c.danger}] {verdict} "
        f_verdict_score = f"[{c.danger}]{verdict_score}"
        vnum = 4
    elif verdict == "DODGE NOW":
        f_verdict = f"[{c.black} on {c.dodge}] {verdict} "
        f_verdict_score = f"[{c.dodge}]{verdict_score}"
        vnum = 5
    elif verdict == "FUCK!!":
        f_verdict = f"[{c.black} on {c.fuck}] {verdict} "
        f_verdict_score = f"[{c.fuck}]{verdict_score}"
        vnum = 6
    elif verdict == "Error":
        f_verdict = f"[{c.black} on {c.debug}] {verdict} "
        f_verdict_score = f"[{c.debug}]{verdict_score}"

    print(f"Verdict score: {f_verdict_score}")
    print(f"Verdict: {f_verdict}")
    sect()
    return vnum

async def sam():

    uuid = await header(rank, name)
    if uuid != None:

        Hys, hy = await statsxd(y, t, uuid, apikey)
        vscore = await samprint(Hys)
        active_flags, flagged, note = await check_flags(name, uuid, Hys, t, vscore, hy)
        if flagged: vscore = await display_flags(active_flags, note, vscore)
        vnum = final_verdict(vscore)

        if t["ingame"]["show_verdict_message"]:
            await ingame_verdict(vnum)

        checked.append(name)
        if len(checked) > 10:
            checked.pop(0)

    await cmds(cmd)
    await remove_duplicates()
    await track(line)
    await autolist()

# ingame verdict
async def ingame_verdict(vnum):
    if system() == 'Linux':
        for i in range(6):
            if vnum == i+1:
                key = kb["athk"][f"vnum{i+1}"]
                linux_hotkey(key)
                if dev: print(f"ATHK: {key}")

    if system() == 'Windows':
        for i in range(6):
            if vnum == i+1:
                key = kb["athk"][f"vnum{i+1}"]
                windows_hotkey(key)
                if dev: print(f"ATHK: {key}")

# handle ping
async def getping(uuid):
    if t["apikey"]["polsu_apikey"].strip() == '':
        print(f"[{c.grey}]No polsu key")
        return None
    pingdata = await polsu_ping(uuid, t["apikey"]["polsu_apikey"])
    pingjson = json.loads(pingdata)

    if pingjson['success']:
        min_ping = pingjson['data']['stats']['min']
        max_ping = pingjson['data']['stats']['max']
        avg_ping = pingjson['data']['stats']['avg']

        if avg_ping < 30:
            print(f"[{c.grey}]Ping: [{c.fuck}]{avg_ping}")
        elif avg_ping < 60:
            print(f"[{c.grey}]Ping: [{c.dodge}]{avg_ping}")
        elif avg_ping < 90:
            print(f"[{c.grey}]Ping: [{c.danger}]{avg_ping}")
        elif avg_ping < 120:
            print(f"[{c.grey}]Ping: [{c.risky}]{avg_ping}")
        elif avg_ping < 150:
            print(f"[{c.grey}]Ping: [{c.safe}]{avg_ping}")
        else:
            print(f"[{c.grey}]Ping: [{c.sosafe}]{avg_ping}")

    else:
        print(f"[{c.grey}]Ping: Unknown!")

# commands
async def cmds(cmd):
    if cmd != None and cmd != '':

        if cmd == '-v\n':
            print(f'[i] \[i] Samael version: {meta.version}')

        if '-s ' in cmd:
            target = cmd[cmd.index(' '):].strip()

            if '^' in target:
                for i in range(10):
                    if target == '^'*i: target = checked[-i]

            await add_to_list(target, paths.sl)

        if '-b ' in cmd:
            target = cmd[cmd.index(' '):].strip()

            if '^' in target:
                for i in range(10):
                    if target == '^'*i: target = checked[-i]

            await add_to_list(target, paths.bl)

        if '-w ' in cmd:
            target = cmd[cmd.index(' '):].strip()

            if '^' in target:
                for i in range(10):
                    if target == '^'*i: target = checked[-i]

            await add_to_list(target, paths.wl)

        if '-rs ' in cmd:
            target = cmd[cmd.index(' '):].strip()

            if '^' in target:
                for i in range(10):
                    if target == '^'*i: target = checked[-i]

            await remove_from_list(target, paths.sl)

        if '-rb ' in cmd:
            target = cmd[cmd.index(' '):].strip()

            if '^' in target:
                for i in range(10):
                    if target == '^'*i: target = checked[-i]

            await remove_from_list(target, paths.bl)

        if '-rw ' in cmd:
            target = cmd[cmd.index(' '):].strip()

            if '^' in target:
                for i in range(10):
                    if target == '^'*i: target = checked[-i]

            await remove_from_list(target, paths.wl)

        if '-note ' in cmd or '-n ' in cmd:
            target = cmd[cmd.index(' '):cmd.index('"')].strip()
            tar = target

            if '^' in target:
                for i in range(10):
                    if target == '^'*i: target = checked[-i]; tar = '^'*i

            note = cmd[cmd.index(tar)+len(tar):].strip()
            await make_note(target, note)

        if '-rn ' in cmd:
            target = cmd[cmd.index(' '):].strip()

            if '^' in target:
                for i in range(10):
                    if target == '^'*i: target = checked[-i]

            with open(paths.notes, 'r') as f:
                lines = f.readlines()
            
            for line in lines:
                if await igntouuid(target) in line:
                    lines.pop(lines.index(line))

            with open(paths.notes, 'w') as f:
                f.writelines(lines)
            

async def track(line):
    # won opponent
    if f"{mcchat}   " and "WINNER!  " in line:
        iso = line[line.index('WINNER!')+len("WINNER!"):].strip()

        if '[' in iso and ']' in iso:
            iso = iso[iso.index(']')+1:].strip()

        with open(paths.rec, 'a') as f:
            f.write(f"W: {await igntouuid(iso)}\n")
            print(f"[i] \[i] Recorded a win against {iso}")

    if f"{mcchat}   " in line and "WINNER!\n" in line:
        iso = line[line.index(t["user"]["nick"])+len(t["user"]["nick"]):line.index("WINNER!")].strip()

        if '[' in iso and ']' in iso:
            iso = iso[iso.index(']')+1:].strip()

        with open(paths.rec, 'a') as f:
            f.write(f"L: {await igntouuid(iso)}\n")
            print(f"[i] \[i] Recorded a loss against {iso}")

async def autolist():
    wonuuids, lostuuids = record_to_list(paths.rec)

    for uuid in wonuuids:
        if countOf(wonuuids, uuid) > 1:
            with open(paths.rec, 'r') as f:
                lines = readlines(f)
                lines = [line for line in lines if line.strip() != f'W: {uuid}']                    
            with open(paths.rec, 'w') as f:
                f.writelines(lines)
            wonuuids.pop(wonuuids.index(uuid))

            with open(paths.sl, 'a') as f:
                f.write(uuid+'\n')
                print(f'[i] \[i] Wrote {uuid} to safelist!')

    for uuid in lostuuids:
        if countOf(lostuuids, uuid) > 0:
            with open(paths.bl, 'a') as f:
                f.write(uuid+'\n')
                print(f'[i] \[i] Wrote {uuid} to blacklist!')

            with open(paths.rec, 'r') as f:
                lines = readlines(f)
                lines = [line for line in lines if line.strip() != f'L: {uuid}']                    
            with open(paths.rec, 'w') as f:
                f.writelines(lines)
            lostuuids.pop(lostuuids.index(uuid))

    # print("Won uuids:", wonuuids)
    # print("Lost uuids:", lostuuids)

# handle lines
for line in chatlines:
    get_target(line)
    rank, name = get_target(line)
    cmd = get_cmd(line)
    
    # silly little commands that cant be in the cmds function cus programming is fucking weird
    if cmd is not None and cmd != '':
        if '-reload' in cmd:
            t = readtoml(paths.toml)
            y = readyaml()
            dev, delim, apikey = reload_t()
            print("[i] \[i] Reloaded Samael")

        if '-api ' in cmd:
            apikey = cmd[cmd.index(' '):].strip()
            asyncio.run(update_toml("apikey", "apikey", apikey))
            print("[i] \[i] Updated apikey")

        if '-crash' in cmd:
            asyncio.run(update_toml("dev", "crash", not t["dev"]["crash"]))
            print("[i] \[i] Set crash to", not t["dev"]["crash"])
            t = readtoml(paths.toml)
    
    if t["dev"]["crash"]:
        asyncio.run(sam())
    else:
        try: asyncio.run(sam())
        except: continue
