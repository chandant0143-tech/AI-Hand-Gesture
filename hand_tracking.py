import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import time

class HandDetector:
    """Hand detection and tracking using MediaPipe"""
    
    def __init__(self, max_hands=1, detection_confidence=0.5, tracking_confidence=0.5):
        # Download model if not exists
        import os
        import urllib.request
        
        model_path = 'hand_landmarker.task'
        if not os.path.exists(model_path):
            print("Downloading hand detection model...")
            url = 'https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task'
            urllib.request.urlretrieve(url, model_path)
            print("Model downloaded successfully")
        
        # Initialize MediaPipe hands detector
        base_options = python.BaseOptions(model_asset_path=model_path)
        options = vision.HandLandmarkerOptions(
            base_options=base_options,
            num_hands=max_hands,
            min_hand_detection_confidence=detection_confidence,
            min_tracking_confidence=tracking_confidence,
            running_mode=vision.RunningMode.VIDEO
        )
        self.detector = vision.HandLandmarker.create_from_options(options)
        self.results = None
        
        # Hand connections for drawing
        self.connections = [
            (0,1),(1,2),(2,3),(3,4),(0,5),(5,6),(6,7),(7,8),
            (5,9),(9,10),(10,11),(11,12),(9,13),(13,14),(14,15),
            (15,16),(13,17),(17,18),(18,19),(19,20),(0,17)
        ]
        
    def find_hands(self, frame, draw=True):
        """Detect hands in the frame and optionally draw landmarks"""
        # Convert BGR to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
        
        # Process frame with timestamp in milliseconds
        timestamp_ms = int(time.time() * 1000)
        self.results = self.detector.detect_for_video(mp_image, timestamp_ms)
        
        # Draw landmarks if detected
        if self.results.hand_landmarks and draw:
            height, width, _ = frame.shape
            for hand_landmarks in self.results.hand_landmarks:
                # Draw landmarks (circles)
                for landmark in hand_landmarks:
                    x = int(landmark.x * width)
                    y = int(landmark.y * height)
                    cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)
                
                # Draw connections (lines)
                for connection in self.connections:
                    start_idx, end_idx = connection
                    start = hand_landmarks[start_idx]
                    end = hand_landmarks[end_idx]
                    start_point = (int(start.x * width), int(start.y * height))
                    end_point = (int(end.x * width), int(end.y * height))
                    cv2.line(frame, start_point, end_point, (255, 255, 255), 2)
        
        return frame
    
    def get_finger_position(self, frame, finger_tip_id=8):
        """Get the position of a specific finger tip (default: index finger)"""
        height, width, _ = frame.shape
        
        if self.results and self.results.hand_landmarks:
            hand_landmarks = self.results.hand_landmarks[0]
            landmark = hand_landmarks[finger_tip_id]
            x = int(landmark.x * width)
            y = int(landmark.y * height)
            return x, y
        
        return None, None
    
    def get_distance(self, frame, point1_id=8, point2_id=4):
        """Calculate distance between two landmarks (default: index tip and thumb tip)"""
        height, width, _ = frame.shape
        
        if self.results and self.results.hand_landmarks:
            hand_landmarks = self.results.hand_landmarks[0]
            p1 = hand_landmarks[point1_id]
            p2 = hand_landmarks[point2_id]
            
            x1, y1 = int(p1.x * width), int(p1.y * height)
            x2, y2 = int(p2.x * width), int(p2.y * height)
            
            distance = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
            return distance, (x1, y1), (x2, y2)
        
        return None, None, None
    
    def count_fingers(self, frame):
        """Count number of extended fingers"""
        if not self.results or not self.results.hand_landmarks:
            return 0
        
        hand_landmarks = self.results.hand_landmarks[0]
        fingers = []
        
        # Thumb
        if hand_landmarks[4].x < hand_landmarks[3].x:
            fingers.append(1)
        else:
            fingers.append(0)
        
        # Other fingers
        for id in [8, 12, 16, 20]:
            if hand_landmarks[id].y < hand_landmarks[id-2].y:
                fingers.append(1)
            else:
                fingers.append(0)
        
        return sum(fingers)
    
    def get_distance(self, frame, point1_id=8, point2_id=4):
        """Calculate distance between two landmarks (default: index tip and thumb tip)"""
        height, width, _ = frame.shape
        
        if self.results and self.results.hand_landmarks:
            hand_landmarks = self.results.hand_landmarks[0]
            
            # Get coordinates of both points
            p1 = hand_landmarks[point1_id]
            p2 = hand_landmarks[point2_id]
            
            x1, y1 = int(p1.x * width), int(p1.y * height)
            x2, y2 = int(p2.x * width), int(p2.y * height)
            
            # Calculate Euclidean distance
            distance = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
            
            return distance, (x1, y1), (x2, y2)
        
        return None, None, None
