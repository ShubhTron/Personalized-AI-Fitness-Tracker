import cv2
import mediapipe as mp
import numpy as np

# Initialize mediapipe utilities
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose


# Function to calculate the angle between three points
def calculate_angle(a, b, c):
    a = np.array(a)  # First point
    b = np.array(b)  # Middle point (joint)
    c = np.array(c)  # Last point

    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)

    if angle > 180.0:
        angle = 360 - angle

    return angle


# Variables to track push-up state and count
counter = 0  # Total reps counter
stage = None  # Whether the push-up is going 'down' or 'up'

# Allow user to choose camera position
camera_position = input("Enter 'front' for camera in front of you or 'side' for camera on your left: ").strip().lower()

# Open video capture
cap = cv2.VideoCapture(0)

# Use mediapipe pose model
with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        ret, image = cap.read()

        # Convert BGR to RGB
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image_rgb.flags.writeable = False

        # Process the frame with MediaPipe Pose
        results = pose.process(image_rgb)

        # Convert back to BGR
        image = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)

        # If landmarks are detected
        if results.pose_landmarks:
            landmarks = results.pose_landmarks.landmark

            if camera_position == 'side':
                # For left side view, track left side landmarks
                shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                            landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                         landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                         landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
                hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                       landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
                knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
                        landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]

            elif camera_position == 'front':
                # For front view, track both sides (left and right landmarks)
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

                # You can track hip and knee on both sides as well for front view if needed
                hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                       landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]

            # Calculate angles based on camera position
            if camera_position == 'side':
                # For side view, calculate elbow and body alignment angles
                elbow_angle = calculate_angle(shoulder, elbow, wrist)
                body_alignment_angle = calculate_angle(shoulder, hip, knee)

                # Display angle and count reps
                cv2.putText(image, str(int(elbow_angle)),
                            tuple(np.multiply(elbow, [640, 480]).astype(int)),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

                # Rep counting logic based on elbow angle
                if elbow_angle > 160:  # Arm fully extended
                    if stage == 'down':
                        counter += 1  # Count a completed push-up
                        stage = 'up'
                if elbow_angle < 30:  # Arm fully bent
                    stage = 'down'

            elif camera_position == 'front':
                # For front view, calculate elbow angles for both arms
                left_elbow_angle = calculate_angle(left_shoulder, left_elbow, left_wrist)
                right_elbow_angle = calculate_angle(right_shoulder, right_elbow, right_wrist)

                # Display the angle on the image
                cv2.putText(image, str(int(left_elbow_angle)),
                            tuple(np.multiply(left_elbow, [640, 480]).astype(int)),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
                cv2.putText(image, str(int(right_elbow_angle)),
                            tuple(np.multiply(right_elbow, [640, 480]).astype(int)),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

                # Rep counting logic based on both elbow angles
                if left_elbow_angle > 160 and right_elbow_angle > 160:  # Both arms fully extended
                    if stage == 'down':
                        counter += 1  # Count a completed push-up
                        stage = 'up'
                if left_elbow_angle < 30 and right_elbow_angle < 30:  # Both arms fully bent
                    stage = 'down'

            # Display rep count
            cv2.putText(image, f'Reps: {counter}',
                        (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

            bar_percentage = np.interp(left_elbow_angle, [30, 160], [0, 100])
            cv2.rectangle(image, (10, 60), (110, 80), (0, 255, 0), 3)  # Outer bar
            cv2.rectangle(image, (10, 60), (int(bar_percentage) + 10, 80), (0, 255, 0), -1)  # Inner progress bar

            # Display landmarks
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        # Show the image in the window
        cv2.imshow("AI Push-up Trainer", image)

        # Break the loop on 'q' key press
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

# Release the capture and close windows
cap.release()
cv2.destroyAllWindows()
