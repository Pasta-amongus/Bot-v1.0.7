from flask import Flask
import logging
import os
from threading import Thread

app = Flask(__name__)
os.environ['WERKZEUG_RUN_MAIN'] = 'true'
log = logging.getLogger('werkzeug')
log.disabled = True
app.logger.disabled = True
app.env = "development"

@app.route('/')
def home():
    return str(open("repl.html", "r").read())

def run():
  app.run(host='0.0.0.0',port=8080)

def keep_alive():  
    t = Thread(target=run)
    t.start()
