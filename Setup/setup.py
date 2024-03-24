import os, sys
from platform import system
print("\n [i] Setup script started!")

SamaelDir = os.path.join(os.path.expanduser('~'), 'Samael')

# Determine install location
while True:
    print(f" [i] Using directory '{SamaelDir}' for Samael")
    dircont = input(' [-] Is this ok? (y/n)\n')
    match dircont:
        case 'n':
            SamaelDir = input(" [-] Enter the absolute path to your desired Samael directory:\n > ")
            if not os.path.exists(SamaelDir):
                os.makedirs(SamaelDir)
        case 'y':
            print(" [i] Continuing!")
            break
        case _:
            print(f" [i] Invalid input!")

# Establish venv
print(f" [i] Creating venv...")
os.system(f"python -m venv {os.path.join(SamaelDir, 'venv')}")
print(f" [i] Created venv successfully")

venvbin = os.path.join(SamaelDir, 'venv', 'bin')
venvpip = os.path.join(venvbin, 'pip')
venvpython = os.path.join(venvbin, 'python')
print(f" [i] Established venv/bin/ paths")

# Install python modules to venv
print(f" [i] Installing modules:")
modules = ['toml', 'pyyaml', 'rich', 'Chromify', 'requests', 'httpx']

for module in modules:
    print(f'   #{modules.index(module)+1}. {module}')

for module in modules:
    print(f' [i] Installing module: {module}')
    os.system(f'{venvpip} install {module}')
    print(' [i] Installed!\n')

print(" [i] Installed all necessary modules to venv!")

# Create Samael file tree
print(" [i] Initializing Samael file tree...")
ListsDir = os.path.join(SamaelDir, 'Lists')
ConfigsDir = os.path.join(SamaelDir, 'Configs')
UtilsDir = os.path.join(SamaelDir, 'Utils')
SetupDir = os.path.join(SamaelDir, 'Setup')

dirs = [ListsDir, ConfigsDir, UtilsDir, SetupDir]
for  dir_ in dirs:
    os.system(f"mkdir {dir_}")

# Create lists
lists = ['Blacklist.log', 'Notes.log', 'Record.log', 'Safelist.log', 'Weirdlist.log']
for list_ in lists:
    list_f = os.path.join(ListsDir, list_)
    try:
        with open(list_f, 'x'): print(f" [i] Created list: {list_}")
    except FileExistsError: print(f" [i] List: {list_} already exists")

# Download Samael files from github
print(" [i] Downloading Samael files from github...")
repopaths = ['Samael.py', 'Configs/Config.toml', 'Configs/Settings.yaml', 'Configs/Keybinds.toml', 'Configs/colors.py', 'Utils/utils.py', 'Setup/setup.py', 'Setup/autocfg.py']

for repopath in repopaths:
    github_url = f"https://raw.githubusercontent.com/Toxikuu/Samael-T/main/{repopath}"

    if repopath.startswith('Configs/'):
        local_dir = ConfigsDir
    elif repopath.startswith('Utils/'):
        local_dir = UtilsDir
    elif repopath.startswith('Setup'):
        local_dir = SetupDir
    else:
        local_dir = SamaelDir

    match system():
        case 'Windows':
            powershellpath = r"C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe"
            powershellcmd = f"Invoke-WebRequest -Uri '{github_url}' -OutFile '{os.path.join(local_dir, os.path.basename(repopath))}'"

        case 'Linux':
                os.system(f'curl -o {os.path.join(local_dir, os.path.basename(repopath))} -L {github_url}')

autocfgcmd = f'{os.path.join(SamaelDir, "venv", "bin", "python")} {os.path.join(SamaelDir, "Setup", "autocfg.py")}'
print(autocfgcmd)
os.system(autocfgcmd)

# FINAL THING
dottpath = os.path.join(SetupDir, '.t')
with open(dottpath, 'x'):
    print(' [i] Setup complete!')

# Self Destruct
import shutil
shutil.rmtree(os.path.dirname(__file__))
input('Press enter to exit...')
