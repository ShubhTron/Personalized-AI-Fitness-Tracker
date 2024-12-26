import cv2
import mediapipe as mp
import numpy as np

# yeh kuch nhi mediapipe ko initialize kiya hai
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose


# func bna diya to calculate angle 3 points le liye to calc angle
def calculate_angle(a, b, c):
    a = np.array(a)  # shoulder ke side wala
    b = np.array(b)  # elbow wala ( jo hamara joint hoga )
    c = np.array(c)  # teersa jo haath p ho

    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)
    #basically b point se x axis m distance calculate aur y axis m distance calculate kiya hai c[1] - c ki y axis ka coordinate
    # similarly a se bhi kiya hai aur angle ka formula laga diya hai

    if angle > 180.0:
        angle = 360 - angle

    return angle

# Vars
counter = 0
stage = None  # 'down' or 'up'

# capture hogi hamari video
cap = cv2.VideoCapture(0)

# pose model use hoga
with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        ret, image = cap.read()
        # ab yeh saara toh normal media pipe usage hai taaki jo open cv image lera
        # BGR to RGB karo kyunki Open CV BGR p kaam karta aur mediapipe RGB m :)
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image_rgb.flags.writeable = False

        # Process the frame with MediaPipe Pose
        results = pose.process(image_rgb)

        # Convert back to BGR
        image = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)

        if results.pose_landmarks:
            landmarks = results.pose_landmarks.landmark

            # yeh ham directly landmark id aur body part ke table se bhi kar sakte the value leke but aise better hai
            # link : https://miro.medium.com/v2/resize:fit:1400/1*JJCbfzhTySIqKr1L5pDkpQ.png
            shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                        landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
            elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                     landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
            wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                     landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
            # baad m add kiya kyunki shi nhi lera tha rep counting
            hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                   landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
            knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
                    landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]

            angle = calculate_angle(shoulder, elbow, wrist)

            body_alignment_angle = calculate_angle(shoulder, hip, knee)

            # Isse Screen p display hoga
            cv2.putText(image, str(int(angle)),
                        tuple(np.multiply(elbow, [640, 480]).astype(int)),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

            # Push-up logic
            if angle > 160:  # Arm fully extended
                if stage == 'down':
                    counter += 1  # Count a completed push-up
                    stage = 'up'
            if angle < 30:  # Arm fully bent
                stage = 'down'

            # Rep counter display
            cv2.putText(image, f'Reps: {counter}',
                        (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

            # Progress bar based on the arm angle (from bent to extended)
            bar_percentage = np.interp(angle, [30, 160], [0, 100])
            cv2.rectangle(image, (10, 60), (110, 80), (0, 255, 0), 3)  # Outer bar
            cv2.rectangle(image, (10, 60), (int(bar_percentage) + 10, 80), (0, 255, 0), -1)  # Inner progress bar

            # Provide posture feedback based on body alignment
            if body_alignment_angle < 160:
                cv2.putText(image, 'Hips Too High, Lower Down!',
                            (10, 450),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
            elif body_alignment_angle > 195:
                cv2.putText(image, 'Hips Too Low, Tighten Core!',
                            (10, 450),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

            # Provide feedback based on shoulder movement (up and down)
            shoulder_height = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y
            hip_height = landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y

            # Detect if shoulders are dropping too low or too high
            if shoulder_height - hip_height > 0.2:  # Shoulders dropping too low
                cv2.putText(image, 'Raise Shoulders!',
                            (10, 400),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

            # Pose ke Landmarks ko show kardo
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        cv2.imshow("AI Virtual Trainer", image)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
