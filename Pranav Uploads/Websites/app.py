from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# In-memory storage for received data
received_data = []

@app.route('/receive_data', methods=['POST'])
def receive_data():
    data = request.get_json()  # Parse JSON data from the request
    if data:
        received_data.append(data)
        print(f"Received data: {data}")
        return jsonify({'status': 'success'})
    else:
        return jsonify({'status': 'error', 'message': 'Invalid JSON data'}), 400

@app.route('/')
def index():
    return render_template('index.html', data=received_data)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')