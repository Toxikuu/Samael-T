# Configuration
import toml, os, sys
from platform import system

SamaelDir = os.path.dirname(os.path.dirname(__file__))
ConfigsDir = os.path.join(SamaelDir, 'Configs')

with open(os.path.join(ConfigsDir, 'Config.toml'), 'r') as f:
    t = toml.load(f)

print(" [*] If you don't have one of these, just press enter to leave it blank.")

t['apikey']['apikey'] = input(' [-] Enter your hypixel apikey:\n > ')
t['apikey']['polsu_apikey'] = input(' [-] Enter your polsu apikey:\n > ')
t['user']['username'] = input(' [-] Enter your minecraft username\n > ')
t['user']['nick'] = input(' [-] Enter your hypixel nick:\n > ')

if system() == 'Linux':
    t['delimiter']['delimiter_type'] = 0
else:
    t['delimiter']['delimiter_type'] = 1

print(" [-] Enter the number of your minecraft client:")
print("  1. Lunar")
print("  2. Badlion")
print("  3. Other")
print("  4. Manually enter chat path")

while True:
    mcclient = input('')
    try:
        mcclient = int(mcclient)
        if 1 <= mcclient <= 4:
            break
        else:
            print(' [i] Invalid input! Please enter a number between 1 and 7.')
    except ValueError:
        print(' [i] Invalid input! Please enter a valid number.')

match mcclient:
    case 1:
        t['paths']['chat'] = os.path.join(os.path.expanduser('~'), '.lunarclient', 'offline', 'multiver', 'logs', 'latest.log')
    case 2:
        t['paths']['chat'] = os.path.join(os.path.expanduser('~'), '.minecraft', 'logs', 'blclient', 'minecraft', 'latest.log')
    case 3:
        t['paths']['chat'] = os.path.join(os.path.expanduser('~'), '.minecraft', 'logs', 'latest.log')
    case _:
        t['paths']['chat'] = input(' [-] Enter the absolute path of your latest.log\n > ')

with open(os.path.join(ConfigsDir, 'Config.toml'), 'w') as f:
    toml.dump(t, f)

match system():
    case 'Windows':
            print(" [*] You may now launch Samael with '{SamaelDir}/venv/Scripts/python.exe {SamaelDir}/Samael.py' using your terminal")
    
    case 'Linux':
            print(f" [*] You may now launch Samael with '{SamaelDir}/venv/bin/python {SamaelDir}/Samael.py' using your terminal")
        
print(" [*] Feel free to make an alias or function to shorten this in your shell.")
