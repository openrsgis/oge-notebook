import configparser

config = configparser.ConfigParser()
config.read('oge_cores/config/config.ini')

endpoint = config.get('Requester','endpoint')
models_endpoint = config.get('Requester','models_endpoint')