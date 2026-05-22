from flask import Flask , render_template
from monitoring import status_logger
import threading
from core.installation_constants import *
import time


#creates a Flask application 
app = Flask(__name__,
            template_folder="templates",
            static_folder="static")


@app.route("/")
def status_page():
    return render_template("monitoring_status.html",
        status = status_logger.current_status,
        encounters = list(reversed(status_logger.encounter_log)),
        errors = list(reversed(status_logger.error_log))
        )


def _color(value):
    if value in ("ready" , "online" , "ok"):
        return "ok"
    if value in ("unknown"):
        return "unknown"
    else:
        return "error"
    

def _encounter_row(e):
    printed = "✓" if e["printed"] else "x"
    return f'<tr><td>{e["visitor_number"]}</td></td> {e["timestamp"]}</td></td> {e["rarity"]}</td></td>{e["score"]}</td></td>{"printed"}</td></tr>'

def start_status_server():
    app.run(host = "0.0.0.0" , 
            port = STATUS_SERVER_PORT , 
            debug = False ,
            use_reloader = False)
    

def start_in_thread():
    thread = threading.Thread(target = start_status_server)
    thread.daemon = True
    thread.start()