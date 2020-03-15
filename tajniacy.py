import numpy as np
import random
from flask import Flask, render_template, jsonify, send_from_directory

def get_words(fname):
    with open(fname, 'r') as infile:
        return [l.strip() for l in infile.readlines()]

def build_board(words):
    random.shuffle(words)
    return np.array(words[:25], dtype=object).reshape(5, 5)

def build_layout():
    ixs = list(range(25))
    random.shuffle(ixs)
    
    starter  = ixs[:9]
    follower = ixs[9:9+8]
    killer   = ixs[9+8]

    layout = np.zeros((25), dtype=np.uint8)

    for ix in starter:
        layout[ix] = 1

    for ix in follower:
        layout[ix] = 2

    layout[killer] = 3
    
    return layout.reshape(5, 5)

app = Flask(__name__)

INT_TO_COLOR = {
    1: 'blue',
    2: 'red',
    3: 'black',
    0: 'gray',
}
    
class Game:
    def __init__(self, words):
        self.words  = build_board(words)
        self.layout = build_layout()
        self.tapped = np.zeros((5, 5), dtype=np.bool)
        self.round = 'start'

    def get_state(self):
        layout = []

        for row in range(5):
            layout.append([])
            for col in range(5):
                color  = INT_TO_COLOR[self.layout[row, col]]
                tapped = bool(self.tapped[row, col])
                word   = self.words[row, col]

                layout[-1].append({
                    'color' : color,
                    'word'  : word,
                    'tapped': tapped
                })

        return jsonify(layout)

    def accept_click(self, i, j):
        self.tapped[i, j] = True

        return jsonify(success=True)

if __name__ == '__main__':
    word_list = get_words('slowa.txt')

    game = Game(word_list)

    @app.route('/player')
    def get_player_board():
        return send_from_directory('static', 'player_board.html')

    @app.route('/leader')
    def get_leader_board():
        return send_from_directory('static', 'leader_board.html')

    @app.route('/click/<int:i>/<int:j>')
    def accept_click(i, j):
        return game.accept_click(i, j)

    @app.route('/state')
    def get_state():
        return game.get_state()

    @app.route('/player_script')
    def get_player_script():
        return send_from_directory('static', 'player_script.js')

    @app.route('/leader_script')
    def get_leader_script():
        return send_from_directory('static', 'leader_script.js')

    @app.route('/style')
    def get_style():
        return send_from_directory('static/styles', 'board.css')

    app.run()
