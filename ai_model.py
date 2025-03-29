import cv2
import numpy as np
import mediapipe as mp

# Initialize Mediapipe Pose model
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# Global variables for rep counting
counter = 0
stage = None

# Calorie burn per rep (approximate values)
calories_per_rep = {
    "pushup": 0.29,
    "squat": 0.32,
    "mountain_climber": 0.16,
    "crunch": 0.14,
    "situp": 0.15,
    "bending_arm": 0.1,
}


def calculate_angle(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)

    # Calculate angle
    radians = (np.arctan2(c[1] - b[1], c[0] - b[0]) -
               np.arctan2(a[1] - b[1], a[0] - b[0]))
    angle = np.abs(radians * 180.0 / np.pi)
    if angle > 180.0:
        angle = 360 - angle
    return angle


def process_frame(image, exercise_type, previous_exercise):
    global counter, stage

    # Initialize pose estimation
    pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = pose.process(image_rgb)

    progress_percentage = 0  # Initialize progress
    calorie_burn = 0  # Initialize calorie burn

    if results.pose_landmarks:
        landmarks = results.pose_landmarks.landmark

        # Get key points
        left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                         landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
        right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                          landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
        left_elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                      landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
        right_elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,
                       landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
        left_wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                      landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
        right_wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,
                       landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]

        # Check if the selected exercise is different from the previous one

        # Process each exercise type (existing logic remains unchanged)
        if exercise_type == "pushup":

            if previous_exercise != exercise_type:
                counter = 0  # Reset counter for new exercise
                stage = None  # Reset stage for new exercise

            left_elbow_angle = calculate_angle(left_shoulder, left_elbow, left_wrist)
            right_elbow_angle = calculate_angle(right_shoulder, right_elbow, right_wrist)
            avg_elbow_angle = (left_elbow_angle + right_elbow_angle) / 2
            progress_percentage = np.interp(avg_elbow_angle, [30, 160], [100, 0])

            if avg_elbow_angle > 160:
                if stage == 'down':
                    counter += 1
                    stage = 'up'
            if avg_elbow_angle < 30:
                stage = 'down'

        elif exercise_type == "squat":

            if previous_exercise != exercise_type:
                counter = 0  # Reset counter for new exercise
                stage = None  # Reset stage for new exercise

            left_knee_angle = calculate_angle(left_shoulder, left_elbow, left_wrist)
            right_knee_angle = calculate_angle(right_shoulder, right_elbow, right_wrist)
            avg_knee_angle = (left_knee_angle + right_knee_angle) / 2
            progress_percentage = np.interp(avg_knee_angle, [60, 170], [100, 0])

            if avg_knee_angle > 160:
                if stage == 'down':
                    counter += 1
                    stage = 'up'
            if avg_knee_angle < 70:
                stage = 'down'

        elif exercise_type == "mountain_climber":

            if previous_exercise != exercise_type:
                counter = 0  # Reset counter for new exercise
                stage = None  # Reset stage for new exercise

            left_hip_angle = calculate_angle(left_shoulder, left_elbow, left_wrist)
            right_hip_angle = calculate_angle(right_shoulder, right_elbow, right_wrist)
            avg_hip_angle = (left_hip_angle + right_hip_angle) / 2
            progress_percentage = np.interp(avg_hip_angle, [30, 110], [100, 0])

            if avg_hip_angle > 90:
                if stage == 'down':
                    counter += 1
                    stage = 'up'
            if avg_hip_angle < 30:
                stage = 'down'


        elif exercise_type == "crunch":
            if previous_exercise != exercise_type:
                counter = 0  # Reset counter for new exercise
                stage = None  # Reset stage for new exercise
            # Get the angles related to the torso flexion for crunches
            left_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                        landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]

            right_hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,
                         landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]

            left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                             landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]

            right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                              landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
            # Calculate angle between the hip and shoulder for each side

            left_torso_angle = calculate_angle(left_shoulder, left_hip,
                                               [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,

                                                landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y])

            right_torso_angle = calculate_angle(right_shoulder, right_hip,
                                                [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,

                                                 landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y])

            avg_torso_angle = (left_torso_angle + right_torso_angle) / 2

            # Progress calculation based on torso angle (the more flexed, the higher the progress)

            progress_percentage = np.interp(avg_torso_angle, [30, 120], [100, 0])

            if avg_torso_angle > 90:

                if stage == 'down':
                    counter += 1

                    stage = 'up'

            if avg_torso_angle < 30:
                stage = 'down'

        elif exercise_type == "situp":

            if previous_exercise != exercise_type:
                counter = 0  # Reset counter for new exercise
                stage = None  # Reset stage for new exercise

            left_hip_angle = calculate_angle(left_shoulder, left_elbow, left_wrist)
            right_hip_angle = calculate_angle(right_shoulder, right_elbow, right_wrist)
            avg_hip_angle = (left_hip_angle + right_hip_angle) / 2
            progress_percentage = np.interp(avg_hip_angle, [30, 120], [100, 0])

            if avg_hip_angle > 100:
                if stage == 'down':
                    counter += 1
                    stage = 'up'
            if avg_hip_angle < 30:
                stage = 'down'

        elif exercise_type == "bending_arm":
            if previous_exercise != exercise_type:
                counter = 0  # Reset counter for new exercise
                stage = None  # Reset stage for new exercise
            counter += 1

        # Calculate calorie burn based on current counter value for the specific exercise type.
        calorie_burn += round(counter * calories_per_rep.get(exercise_type, 0), 2)

    feedback = "Great job!" if stage == 'up' else "Keep going!"
    return feedback, counter, int(progress_percentage), calorie_burn
