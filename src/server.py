
import time
import datetime
import logging
import requests
import threading
from flask import Flask, request, render_template, jsonify
from db import insert_joke, get_jokes, get_total_jokes

# Configure the logger
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Next fetch time in seconds
NEXT_FETCH_TIME = 3600

# Create a Flask app
app = Flask(__name__)
bot_status = {
    'last_fetch': None,
    'next_fetch_in': NEXT_FETCH_TIME,
}


@app.route('/get-total-jokes')
def get_total_amount():
    total_jokes_data = get_total_jokes()
    return jsonify({'total_jokes': total_jokes_data})

@app.route('/fetch-jokes')
def fetch_joke():
    headers = {'Accept': 'application/json'}
    response = requests.get('https://icanhazdadjoke.com/', headers=headers)
    if response.status_code == 200:
        joke = response.json().get('joke')
        insert_joke(joke)
        logger.info(f"Inserted joke: {joke}")
        with app.app_context():
            return jsonify(joke)
    else:
        logger.error(f"Failed to fetch joke. Status Code: {response.status_code}")
        return jsonify({'error': 'Failed to fetch joke'}), 500

@app.route('/recycle-jokes')
def serve_joke():
    # Cycle through existing jokes in DB
    count = request.args.get('count', default=1, type=int)
    jokes = get_jokes(count)
    return jsonify(jokes) if jokes else ('No jokes available', 404)

@app.route('/')
def home():
    joke = get_jokes(1)[0]
    return render_template('index.html', 
                           initial_joke=joke,
                           bot_status=bot_status,
                           )

def run_bot():
    while True:
        update_bot_status()
        fetch_joke()
        time.sleep(NEXT_FETCH_TIME)

def update_bot_status():
    global bot_status
    now_time = datetime.datetime.now()
    bot_status['last_fetch'] = now_time.strftime("%m/%d/%Y, %H:%M:%S")
    bot_status['next_fetch_in'] = NEXT_FETCH_TIME

if __name__ == "__main__":
    # Run the bot in a separate thread
    bot_thread = threading.Thread(target=run_bot, daemon=True)
    bot_thread.start()

    # Run the Flask app
    app.run(host='0.0.0.0', port=80, debug=True)