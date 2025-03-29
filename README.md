# AI Fitness Tracker

**AI Fitness Tracker** is an innovative web application designed to help users track their fitness journey in real-time. By leveraging cutting-edge technologies like AI, machine learning, and computer vision, this app provides personalized feedback on exercise form, calorie burn predictions, and tailored recovery recommendations.

---

## Features

1. **Real-Time Exercise Tracking**
   - Tracks exercise repetitions using OpenCV and MediaPipe.
   - Provides instant feedback on body posture and form (e.g., correcting push-up angles).

2. **Calorie Burn Prediction**
   - Uses a built-in AI model and Streamlit interface to estimate calories burned based on activity.

3. **Weight Loss Predictor**
   - Features a predictive model integrated into Streamlit to estimate potential weight loss based on user data.

4. **Progress Monitoring**
   - Stores daily stats such as date, time, exercise type, calorie burn, and streaks.
   - Visualizes consistency with a streak system.

5. **Personalized Recommendations**
   - Chatbot-powered suggestions for diet adjustments and recovery strategies for muscle soreness, using Dialogflow for conversational AI.

---

## Tech Stack

- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Python Flask
- **Database**: SQLite (or preferred database for production)
- **Computer Vision**: OpenCV, MediaPipe
- **AI/ML Models**: TensorFlow/Keras (for pose detection and calorie predictions)
- **Streamlit**: For interactive calorie and weight loss prediction tools
- **Dialogflow**: For chatbot implementation

---

## Installation

### Prerequisites
- Python 3.8 or later
- pip package manager
- Virtual environment (optional but recommended)

### Steps
1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/ai-fitness-tracker.git
   cd ai-fitness-tracker
   ```

2. Set up a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the Flask server:
   ```bash
   python app.py
   ```

5. Open your browser and go to:
   ```
   http://127.0.0.1:5000
   ```

6. For Streamlit applications (Calorie Burn Prediction & Weight Loss Predictor):
   ```bash
   streamlit run streamlit_app.py
   ```

---

## Usage

1. Log in or create an account.
2. Select an exercise and start performing it in front of your webcam.
3. View real-time feedback on your form and track reps.
4. Check daily stats, including calories burned and streaks.
5. Use the Streamlit tools for detailed calorie burn predictions and weight loss forecasts.
6. Chat with the built-in AI assistant for personalized fitness advice.

---

## Roadmap

- Add support for more exercises and pose tracking.
- Integrate advanced calorie prediction models.
- Expand chatbot capabilities for mental health and wellness advice.
- Develop a mobile app version for on-the-go tracking.

---

## Contribution

Contributions are welcome! Please follow these steps:

1. Fork this repository.
2. Create a feature branch:
   ```bash
   git checkout -b feature-name
   ```
3. Commit changes and push to your fork:
   ```bash
   git commit -m "Add feature-name"
   git push origin feature-name
   ```
4. Open a pull request on the main repository.

---

## Acknowledgments

- **OpenCV and MediaPipe** for enabling robust real-time computer vision.
- **Flask Framework** for creating a seamless web application.
- **Streamlit** for interactive and user-friendly prediction tools.
- **Dialogflow** for providing conversational AI capabilities.
- **Fitness enthusiasts** who inspired the need for real-time feedback and personalized fitness solutions.

---

## Contact

For questions or suggestions, feel free to contact:

- **Name**: Shubh Sharma
- **Email**: k.sharmashubh123@gmail.com
- **LinkedIn**: [Shubh Sharma](https://linkedin.com/in/shubh-sharma-a39276143/)

Happy Tracking! 🏋️‍♂️

---


## Images 
**Real Time Rep Counter**


---
![Real Time Rep Counter](https://github.com/user-attachments/assets/4163a884-5b60-455b-ba9e-5f23d0cfa08a)


**Weight Loss Predictor**


---
![Weight Loss Predictor](https://github.com/user-attachments/assets/950f50d3-7f21-44f5-ade6-f327a5937a06)



**Calorie Burn Predictor**


---
![Calorie Burn Predictor](https://github.com/user-attachments/assets/f830af79-6886-4c2d-8164-e8d7598e3997)



**Backend**


---
![SQLite3](https://github.com/user-attachments/assets/5f8424ef-30f5-4283-881c-c1c622658217)


**Chatbot**


---
![Chatbot 2](https://github.com/user-attachments/assets/0b85002f-f4cd-4578-a033-0cd7828b5014)



