import cv2
import numpy as np
import sqlite3
from flask import Flask, request, jsonify, render_template
from ai_model import process_frame  # Assume this handles calorie calculations
from datetime import datetime
from weight_loss_calculator import weight_loss_prediction  # Import the prediction function
from waitress import serve

app = Flask(__name__)

# Global variables
previous_exercise = None  # Store the last exercise type

# Database setup
def init_db():
    conn = sqlite3.connect('fitness_tracker.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS progress (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            calories REAL NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def log_progress(calories):
    conn = sqlite3.connect('fitness_tracker.db')
    cursor = conn.cursor()
    date_str = datetime.now().strftime("%Y-%m-%d %H:%M")
    cursor.execute('INSERT INTO progress (date, calories) VALUES (?, ?)', (date_str, calories))
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_video', methods=['POST'])
def process_video():
    global previous_exercise  # Declare as global to modify it

    if 'image' not in request.files or 'exercise_type' not in request.form:
        return jsonify({'error': 'Invalid request'}), 400

    file = request.files['image']
    exercise_type = request.form['exercise_type']

    image = np.frombuffer(file.read(), np.uint8)
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)

    if image is None:
        return jsonify({'error': 'Failed to decode image'}), 400


    feedback, rep_count, progress_percentage, calorie_burned_current_exercise = process_frame(image, exercise_type, previous_exercise)

    previous_exercise = exercise_type

    return jsonify({
        'feedback': feedback,
        'rep_count': rep_count,
        'progress': progress_percentage,
        'calories': calorie_burned_current_exercise,
        'total_calories_burned': calorie_burned_current_exercise
    })

@app.route('/save_progress', methods=['POST'])
def save_progress():
    data = request.json
    date_time = data['date_time']
    total_calories_burned = data['total_calories_burned']

    log_progress(total_calories_burned)

    return jsonify({'message': 'Progress saved successfully!'})

@app.route('/get_history', methods=['GET'])
def get_history():
    conn = sqlite3.connect('fitness_tracker.db')
    cursor = conn.cursor()

    cursor.execute("SELECT date, calories FROM progress ORDER BY date DESC")
    rows = cursor.fetchall()

    # Convert rows into a list of dictionaries for easy JSON serialization
    history_data = [{'date': row[0], 'calories': row[1]} for row in rows]

    conn.close()

    return jsonify(history_data)

@app.route('/weight_loss_prediction', methods=['POST'])
def weight_loss():
    """
    Predict weight loss based on user input.
    """
    try:
        # Get JSON data from the POST request
        data = request.json
        weight = float(data['weight'])
        height = float(data['height'])
        age = int(data['age'])
        gender = data['gender'].strip().lower()
        activity_level = data['activity_level'].strip().lower()
        calorie_deficit = float(data['calorie_deficit'])
        duration_weeks = int(data['duration_weeks'])

        # Calculate weight loss prediction
        result = weight_loss_prediction(weight, height, age, gender, activity_level, calorie_deficit, duration_weeks)

        return jsonify({
            'initial_weight': result['initial_weight'],
            'final_weight': result['final_weight'],
            'total_weight_loss': result['total_weight_loss'],
            'bmr': result['bmr'],
            'tdee': result['tdee']
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400



if __name__ == '__main__':
    init_db()  # Initialize the database when starting the app
    app.run(host="0.0.0.0", port=5000, debug=True)