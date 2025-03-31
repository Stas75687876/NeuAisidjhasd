from flask import Flask, render_template, request, jsonify
from datetime import datetime
import random

app = Flask(__name__)

# Verbesserte Fragen für den Steckbrief
questions = [
    {
        "id": "name",
        "text": "Wie heißt du?",
        "icon": "👤"
    },
    {
        "id": "age",
        "text": "Wie alt bist du?",
        "icon": "🎂"
    },
    {
        "id": "birthday",
        "text": "Wann hast du Geburtstag?",
        "icon": "🎈"
    },
    {
        "id": "color",
        "text": "Was ist deine Lieblingsfarbe?",
        "icon": "🎨"
    },
    {
        "id": "animal",
        "text": "Was ist dein Lieblingstier?",
        "icon": "🐾"
    },
    {
        "id": "subject",
        "text": "Was ist dein Lieblingsfach in der Schule?",
        "icon": "📚"
    },
    {
        "id": "hobby",
        "text": "Was machst du gerne in deiner Freizeit?",
        "icon": "⚽"
    },
    {
        "id": "food",
        "text": "Was isst du am liebsten?",
        "icon": "🍕"
    },
    {
        "id": "dream",
        "text": "Was möchtest du später einmal werden?",
        "icon": "✨"
    },
    {
        "id": "friend",
        "text": "Wer ist dein bester Freund oder deine beste Freundin?",
        "icon": "🤝"
    },
    {
        "id": "music",
        "text": "Was ist deine Lieblingsmusik oder dein Lieblingslied?",
        "icon": "🎵"
    },
    {
        "id": "movie",
        "text": "Was ist dein Lieblingsfilm oder deine Lieblingsserie?",
        "icon": "🎬"
    },
    {
        "id": "special",
        "text": "Was macht dich besonders?",
        "icon": "🌟"
    }
]

# Verbesserte Farbthemen für Jungen und Mädchen
themes = {
    "boy": {
        "primary": "#1E88E5",  # Kräftiges Blau
        "secondary": "#64B5F6",  # Helles Blau
        "gradient": "linear-gradient(135deg, #1E88E5 0%, #64B5F6 100%)",  # Blau Verlauf
        "accent": "#0D47A1",  # Dunkles Blau
        "emoji": "🦸‍♂️",  # Superheld
        "decorative_emojis": [
            "🦸‍♂️", "⚡", "🚀", "🦁", "🐯", "🎮", "⚽", "🏈", "🎯",
            "🛡️", "⚔️", "🏃‍♂️", "🦾", "🤖", "🎪", "🌟", "✨", "💫"
        ]
    },
    "girl": {
        "primary": "#EC407A",  # Helles Pink
        "secondary": "#F48FB1",  # Zartes Rosa
        "gradient": "linear-gradient(135deg, #EC407A 0%, #F48FB1 100%)",  # Pink Verlauf
        "accent": "#C2185B",  # Dunkles Pink
        "emoji": "👸",  # Prinzessin
        "decorative_emojis": [
            "👸", "🦄", "🎀", "🌸", "🌺", "🦋", "💝", "🎭", "🌈",
            "⭐", "🌟", "✨", "💫", "🎪", "🎨", "🎭", "🧚‍♀️", "🎠"
        ]
    }
}

# Wortliste für das Passwort-Spiel
password_words = [
    # Schule
    "schule", "klasse", "lehrer", "freunde", "lernen", "pause", "bücher", 
    "tafel", "kreide", "hefte", "stifte", "mathe", "deutsch", "sport", 
    "kunst", "musik", "computer", "wissen", "rechnen", "lesen", "schreiben",
    "schüler", "stundenplan", "hausaufgabe", "prüfung", "zeugnis", "direktor", 
    "klassenzimmer", "schulhof", "bibliothek", "mensa", "grundschule",
    
    # Tiere
    "katze", "hund", "maus", "pferd", "elefant", "tiger", "löwe", "giraffe",
    "affe", "zebra", "pinguin", "fisch", "vogel", "adler", "biene", "frosch",
    
    # Lebensmittel
    "apfel", "banane", "orange", "erdbeere", "pizza", "nudeln", "kartoffel",
    "wasser", "milch", "käse", "brot", "kuchen", "schokolade", "eis", "gemüse",
    
    # Natur
    "baum", "blume", "wald", "wiese", "berg", "fluss", "meer", "sonne",
    "mond", "stern", "himmel", "wolke", "regen", "schnee", "wind", "blatt"
]

# Kategorien für das Passwort-Spiel (für Hinweise)
password_categories = {
    "schule": "Schule", "klasse": "Schule", "lehrer": "Schule", "freunde": "Schule", 
    "lernen": "Schule", "pause": "Schule", "bücher": "Schule", "tafel": "Schule", 
    "kreide": "Schule", "hefte": "Schule", "stifte": "Schule", "mathe": "Schule", 
    "deutsch": "Schule", "sport": "Schule", "kunst": "Schule", "musik": "Schule", 
    "computer": "Schule", "wissen": "Schule", "rechnen": "Schule", "lesen": "Schule", 
    "schreiben": "Schule", "schüler": "Schule", "stundenplan": "Schule", 
    "hausaufgabe": "Schule", "prüfung": "Schule", "zeugnis": "Schule", 
    "direktor": "Schule", "klassenzimmer": "Schule", "schulhof": "Schule", 
    "bibliothek": "Schule", "mensa": "Schule", "grundschule": "Schule",
    
    "katze": "Tiere", "hund": "Tiere", "maus": "Tiere", "pferd": "Tiere", 
    "elefant": "Tiere", "tiger": "Tiere", "löwe": "Tiere", "giraffe": "Tiere",
    "affe": "Tiere", "zebra": "Tiere", "pinguin": "Tiere", "fisch": "Tiere", 
    "vogel": "Tiere", "adler": "Tiere", "biene": "Tiere", "frosch": "Tiere",
    
    "apfel": "Lebensmittel", "banane": "Lebensmittel", "orange": "Lebensmittel", 
    "erdbeere": "Lebensmittel", "pizza": "Lebensmittel", "nudeln": "Lebensmittel", 
    "kartoffel": "Lebensmittel", "wasser": "Lebensmittel", "milch": "Lebensmittel", 
    "käse": "Lebensmittel", "brot": "Lebensmittel", "kuchen": "Lebensmittel", 
    "schokolade": "Lebensmittel", "eis": "Lebensmittel", "gemüse": "Lebensmittel",
    
    "baum": "Natur", "blume": "Natur", "wald": "Natur", "wiese": "Natur", 
    "berg": "Natur", "fluss": "Natur", "meer": "Natur", "sonne": "Natur",
    "mond": "Natur", "stern": "Natur", "himmel": "Natur", "wolke": "Natur", 
    "regen": "Natur", "schnee": "Natur", "wind": "Natur", "blatt": "Natur"
}

# Hauptseite (Menü)
@app.route('/')
def index():
    return render_template('index.html')

# Steckbrief-Bereich
@app.route('/steckbrief')
def steckbrief():
    return render_template('steckbrief.html', questions=questions, themes=themes)

@app.route('/generate_profile', methods=['POST'])
def generate_profile():
    data = request.json
    answers = data.get('answers', {})
    theme = data.get('theme', 'girl')  # Standard ist Mädchen-Theme
    return render_template('profile.html', 
                         answers=answers, 
                         questions=questions, 
                         datetime=datetime,
                         theme=themes[theme])

# Passwort-Spiel
@app.route('/spiel')
def spiel():
    return render_template('spiel.html')

@app.route('/get_word', methods=['GET'])
def get_word():
    word = random.choice(password_words)
    category = password_categories.get(word, "Allgemein")
    return jsonify({
        "word": word,
        "category": category,
        "length": len(word)
    })

# Stundenplan
@app.route('/stundenplan')
def stundenplan():
    weekdays = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag"]
    periods = ["1. Stunde", "2. Stunde", "3. Stunde", "4. Stunde", "5. Stunde", "6. Stunde"]
    subjects = [
        "Deutsch", "Mathematik", "Englisch", "Sachunterricht", "Sport", 
        "Kunst", "Musik", "Religion", "Werken", "Pause"
    ]
    return render_template('stundenplan.html', weekdays=weekdays, periods=periods, subjects=subjects)

# Mathe-Spiel
@app.route('/mathe-spiel')
def mathe_spiel():
    return render_template('mathe_spiel.html')

@app.route('/generate_math_problem', methods=['GET'])
def generate_math_problem():
    difficulty = request.args.get('difficulty', 'easy')
    
    if difficulty == 'easy':
        num1 = random.randint(1, 10)
        num2 = random.randint(1, 10)
        op = random.choice(['+', '-'])
    elif difficulty == 'medium':
        num1 = random.randint(10, 30)
        num2 = random.randint(10, 30)
        op = random.choice(['+', '-', '*'])
    else:  # hard
        num1 = random.randint(20, 50)
        num2 = random.randint(20, 50)
        op = random.choice(['+', '-', '*', '/'])
        if op == '/':
            # Stellen sicher, dass die Division ohne Rest aufgeht
            num2 = random.randint(1, 10)
            num1 = num2 * random.randint(1, 10)
    
    problem = f"{num1} {op} {num2}"
    result = eval(problem)
    
    # Bei Division immer als Ganzzahl zurückgeben
    if op == '/':
        result = int(result)
    
    return jsonify({
        "problem": problem,
        "result": result
    })

if __name__ == '__main__':
    app.run(debug=True) 