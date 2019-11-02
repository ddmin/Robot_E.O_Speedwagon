# Interface for the Stand JSON file
import json
import random
import difflib


def format_link(stand):
    # Stand names that overlap with people
    EXCEPTIONS = ['Weather Report', 'Sugar Mountain']
    if stand in EXCEPTIONS:
        stand = stand + ' (Stand)'

    if stand == 'Oye Como Va, Mi Ritmo':
        stand = 'Boku no Rhythm wo Kiitekure'

    BASE = "https://jojo.fandom.com/wiki/"
    return BASE + '_'.join(stand.split())


# doesn't capitalize certain words
def mod_cap(s):
    EXCEPTIONS = ['a', 'to', 'of', 'no', 'wo', 'in', 'the']
    if s not in EXCEPTIONS:
        return s.capitalize()
    return s

# capitalize each word
def caps(s):
    string = s.split()[0].capitalize() + ' '
    return string + ' '.join(list(map(lambda x: mod_cap(x.lower()), s.split()[1:])))

# return stand name based on user input
def match_stand(stands, stand_name):

    if stand_name == 'THE WORLD':
        return 'THE WORLD'

    # normalize names
    stand_name = caps(stand_name)

    # alias dictionary
    aliases = {
                'Ger': 'Gold Experience Requiem',
                'D4c': 'Dirty Deeds Done Dirt Cheap',
               }

    # Check for aliases
    if stand_name in aliases:
        return aliases[stand_name]

    # if exact name
    if stand_name in stands:
        return stand_name

    # find closest match
    match = difflib.get_close_matches(stand_name, stands, n=1, cutoff=0.4)

    if not match:
        print("Even Speedwagon doesn't know!")
        print("Here's a random 「STAND」:")
        print()
        return random.choice(stands)
    else:
        print("Yare Yare Daze, that name isn't in the database.")
        print("Here's my guess:")
        print()

    return match[0]


def format_info(stand):
    STANDS_JSON = '/home/ddmin/Code/Python/JoJo/stands.json'
    STANDS_TXT = '/home/ddmin/Code/Python/JoJo/stands.txt'

    with open(STANDS_JSON) as f:
        data = json.load(f)

    with open(STANDS_TXT) as f:
        stands = f.read().split('\n')[:-1]

    stand = match_stand(stands, stand)
    d = data[stand]

    info = ''

    info += f'#「{stand}」\n'
    info += f'\tStand User: {d["Stand User"]}\n'
    info += f'\tType: {" / ".join(d["Type"])}\n\n'

    info += '## Stats\n'
    info += f'| Destructive Power | {d["Stats"][0]["Destructive Power"]} |\n'
    info += f'|:-:|:-:|\n'
    info += f'| Speed | {d["Stats"][0]["Speed"]} |\n'
    info += f'| Range | {d["Stats"][0]["Range"]} |\n'
    info += f'| Persistence | {d["Stats"][0]["Persistence"]} |\n'
    info += f'| Precision | {d["Stats"][0]["Precision"]} |\n'
    info += f'| Developmental Potential | {d["Stats"][0]["Developmental Potential"]} |\n'

    info += '## Abilities\n'

    a = ''
    for ability in d["Abilities"]:
        a += f'\t* {ability}\n'
    info += a

    info += f'\n ^(Information from {format_link(stand)})'

    return info

def main():
    print('Enter「STAND」name:')
    stand = input('> ')

    print()
    print(format_info(stand))


if __name__ == '__main__':
    main()
