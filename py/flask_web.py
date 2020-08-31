import json
from flask import Flask, jsonify, request, send_from_directory
from utils import addPath
addPath("voc")
import orm
from voc import VOC

config_file = "../config/config.json"
config = None
with open(config_file) as f:
    config = json.load(f)

app = Flask(__name__, static_url_path=config["static_url"], static_folder=config["static_dir"])
voc = VOC(config["temp_dir"], config["temp_url"])

@app.route('/test')
def test():
    t = {
        'a': 1,
        'b': 2,
        'c': [3, 4, 5]
    }
    return jsonify(t)

@app.route('/config/<path:filename>')
def staticp(filename):
    return send_from_directory('../config',filename)

@app.route('/lookup')
def lookup():
    word = request.args.get('word', default='', type=str)
    print(word)
    res = voc.lookup(word)
    res["orm"] = orm.lookup(word)
    return jsonify(res)

@app.route("/update",  methods=['POST'])
def update():
    word = request.form.get('word')
    note = request.form.get('note')
    print("Word: {}, Note: {}".format(word, note))
    count, now = orm.update(word, note)
    return jsonify({"res":count == 1,"note":note, "last_update":now})

'''
@app.route('/match')
def match():
    word = request.args.get('word', default='', type=str)
    tags = request.args.getlist('tags')
    print(word)
    print(tags)
    res = aca.match(word, tags)
    return jsonify(res)
'''
if __name__ == '__main__':
    app.debug = True
    print(config)
    app.run(host='0.0.0.0', port=config["port"])