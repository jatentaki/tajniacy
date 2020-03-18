import random, time
import numpy as np
from flask import Flask, render_template, jsonify, \
                  send_from_directory, redirect, request, url_for

from flask_socketio import SocketIO

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
                color  = int(self.layout[row, col])
                tapped = bool(self.tapped[row, col])
                word   = self.words[row, col]

                layout[-1].append({
                    'color' : color,
                    'word'  : word,
                    'tapped': tapped
                })

        return layout

    def accept_click(self, i, j):
        self.tapped[i, j] = True

if __name__ == '__main__':
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
    socketio = SocketIO(app)

    word_list = get_words('slowa.txt')

    games = {}

    @app.route('/game')
    def new_game():
        stamp = str(int(time.time()))
        games[stamp] = Game(word_list)
        print('New session', stamp)

        return redirect(url_for('get_player_board', session_id=stamp))

    @app.route('/player')
    def get_player_board():
        id = request.args.get('session_id')
        return render_template('board.html', session_id=id, player_type='player')

    @app.route('/leader')
    def get_leader_board():
        id = request.args.get('session_id')
        return render_template('board.html', session_id=id, player_type='leader')

    @app.route('/state')
    def get_state():
        id = request.args.get('session_id')
        return jsonify(games[id].get_state())

    @app.route('/style')
    def get_style():
        return send_from_directory('static/styles', 'board.css')

    @socketio.on('click_event')
    def handle_click_event(json, methods=['POST', 'GET']):
        game = games[json['session_id']]
        game.accept_click(json['i'], json['j'])
        socketio.emit('click_response', game.get_state())

    socketio.run(app, debug=True)
