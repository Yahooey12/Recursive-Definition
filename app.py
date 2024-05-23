from flask import Flask, request, jsonify, render_template
import requests
import random

app = Flask(__name__)

def get_definition(word):
    if len(word) < 3:
        return word
    else:
        url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            if data:
                try:
                    synonym = data[0]['meanings'][0]['synonyms'][0]
                    return synonym
                except:
                    print("error :((((")
                    return word
                

        return word

@app.route('/')
def home():
    return render_template('index.html')

def generate_random_sentence():
    with open('random-sentences.txt', 'r') as file:
        sentences = file.readlines()
        return random.choice(sentences).strip()

@app.route('/define', methods=['POST'])
def define():
    print("GAME IS GAME")
    #sentence = request.json.get('sentence')
    global original_sentence
    original_sentence = generate_random_sentence()
    if not original_sentence:
        return jsonify({'error': 'No sentence provided'}), 400

    words = original_sentence.split()
    definitions = [get_definition(word) for word in words]
    definitions = [get_definition(word) for word in definitions] #Make it into a game!!! give users the weird sentence and they have to workout the original!!!!
    definition_sentence = ' '.join(definitions)
    return jsonify({'definition_sentence': definition_sentence})

@app.route('/game', methods=['POST'])
def game():
    data = request.json
    guess_sentence = data.get('sentence')

    print(guess_sentence)

    if not guess_sentence:
        return jsonify({'error': 'No sentence provided'}), 400

    # Fetch the synonym sentence based on the user's guess
    synonym_sentence = " ".join([get_definition(word) for word in guess_sentence.split()])

    print(f"Guess sentence: {guess_sentence}. Original Sentence: {original_sentence}")

    # Here you can implement your game logic to determine if the guess matches the synonym sentence.
    # For simplicity, we'll directly compare the guess and the synonym sentence.
    if guess_sentence.lower() == original_sentence.lower():
        result = {'status': 'win', 'message': 'Congratulations! You guessed it right!', 'original_sentence': original_sentence}
    else:
        result = {'status': 'lose', 'message': 'Sorry, wrong guess.', 'original_sentence': original_sentence}

    print(result)
    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)
