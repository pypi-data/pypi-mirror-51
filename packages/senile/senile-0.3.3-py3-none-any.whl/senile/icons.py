"""
Icon themes for status.
"""

icon_themes = {
    'default': { 
        '👻': -1, 
        '✔️ ': 0,
        '⭕': 1,
        '🔴': 2,
        },
    'text': { 
        'h': -1, 
        'd': 0,
        'T': 1,
        'A': 2,
        },
    'senile': {
        '👓': -1, 
        '⚰️ ': 0,
        '📰': 1,
        '🧠': 2,
        },
    'love': {
        '💔': -1, 
        '💖': 0,
        '❤️ ': 1,
        '💘': 2,
        },
    'xmas': {
        '☃️ ': -1, 
        '🎁': 0,
        '🎄': 1,
        '🛷': 2,
        },
    'archery': { 
        '🐺': -1, 
        '🏅': 0,
        '🎯': 1,
        '🏹': 2,
        },
    }

def get_theme(name):
    return icon_themes.get(name, icon_themes['default'])

