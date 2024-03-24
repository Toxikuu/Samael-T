import Chromify as Ch

class chc:
    debug = Ch.Color("#FFA07A")
    sosafe = Ch.Color("#66CDAA")
    safe = Ch.Color("#ADFF2F")
    risky = Ch.Color("#FFFF00")
    danger = Ch.Color("#FF0000")
    dodge = Ch.Color("#FF00FF")
    fuck = Ch.Color("#7B68EE")
    scream = Ch.Color("#00BFFF")
    black = Ch.Color("#000000")
    white = Ch.Color("#FFFFFF")
    grey = Ch.Color("#708090")
    samaelred = Ch.Color("#FF4F4F")

class c:
    debug = "#FFA07A"
    sosafe = "#66CDAA"
    safe = "#ADFF2F"
    lightsafe = "#77FF81"
    risky = "#FFFF00"
    lightrisky = "#FDFF77"
    danger = "#FF0000"
    dodge = "#FF00FF"
    lightdodge = "#ff98ff"
    fuck = "#7B68EE"
    scream = "#00BFFF"
    notes = "#49FFBA"
    black = "#000000"
    white = "#FFFFFF"
    grey = "#708090"
    samaelred = "#FF4F4F"

class gr:
    def fg(attr, text):
        if attr == 'debug':
            return Ch.gradient(chc.grey, chc.debug, text)
        elif attr == 'sosafe':
            return Ch.gradient(chc.sosafe, chc.safe, text)
        elif attr == 'safe':
            return Ch.gradient(chc.safe, chc.risky, text)
        elif attr == 'risky':
            return Ch.gradient(chc.risky, chc.danger, text)
        elif attr == 'danger':
            return Ch.gradient(chc.danger, chc.dodge, text)
        elif attr == 'dodge':
            return Ch.gradient(chc.dodge, chc.fuck, text)
        elif attr == 'fuck':
            return Ch.gradient(chc.fuck, chc.scream, text)

    def bg(attr, text):
        if attr == 'debug':
            return Ch.gradient(chc.grey, chc.debug, text, background=True)
        elif attr == 'sosafe':
            return Ch.gradient(chc.sosafe, chc.safe, text, background=True)
        elif attr == 'safe':
            return Ch.gradient(chc.safe, chc.risky, text, background=True)
        elif attr == 'risky':
            return Ch.gradient(chc.risky, chc.danger, text, background=True)
        elif attr == 'danger':
            return Ch.gradient(chc.danger, chc.dodge, text, background=True)
        elif attr == 'dodge':
            return Ch.gradient(chc.dodge, chc.fuck, text, background=True)
        elif attr == 'fuck':
            return Ch.gradient(chc.fuck, chc.scream, text, background=True)       

