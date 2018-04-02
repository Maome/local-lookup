import logging

from local_lookup import lookup

from flask import Flask, jsonify, render_template

log = logging.getLogger('local_lookup')
app = Flask(__name__, static_url_path='')

@app.route('/lookup')
def empty():
    return render_template('lookup.html', characters={})

@app.route('/lookup/<names>')
def new_lookup(names):
    names = names.split(',')
    characters = [lookup.Character(name) for name in names]
    return render_template('lookup.html', characters=characters)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
