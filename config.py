import json

json_file = open('config.json', 'r')
config = json.load(json_file)
json_file.close()


def save_config():
    global config
    json_file = open('config.json', 'w')
    json.dump(config, json_file)
    json_file.close()
