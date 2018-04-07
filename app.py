from flask import Flask, jsonify

from local_lookup import lookup, eve_xml, zkill

app = Flask(__name__, static_url_path='')


@app.route("/characters/information/<character_names>")
def character_information_route(character_names):
    character_names = character_names.split(",")
    character_id_map = eve_xml.get_character_ids(character_names)
    character_losses = zkill.get_character_losses(character_id_map)
    processed_data = lookup.process_character_losses(character_id_map, character_losses)

    return jsonify(processed_data)


@app.route('/lookup')
def root():
    return app.send_static_file('lookup.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0')
