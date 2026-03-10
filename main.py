import cv2
import pyautogui
from hand_tracking import HandDetector
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import math

# Disable PyAutoGUI fail-safe
pyautogui.FAILSAFE = False

# Get screen dimensions
screen_width, screen_height = pyautogui.size()

# Initialize volume control
try:
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    volume_range = volume.GetVolumeRange()
    min_vol, max_vol = volume_range[0], volume_range[1]
    volume_enabled = True
except Exception as e:
    print(f"Volume control not available: {e}")
    volume_enabled = False
    min_vol, max_vol = 0, 100

# Initialize webcam
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Cannot access webcam")
    exit()

cap.set(3, 640)
cap.set(4, 480)

print(f"Webcam opened: {cap.get(3)}x{cap.get(4)}")

# Initialize hand detector
try:
    detector = HandDetector(max_hands=1)
    print("Hand detector initialized successfully")
except Exception as e:
    print(f"Error initializing detector: {e}")
    exit()

# Variables
smoothing = 5
prev_x, prev_y = 0, 0
click_threshold = 40
action_cooldown = 0
paused = False

print("\n=== AI Hand Gesture Control System ===")
print("\nGestures:")
print("1 finger (index) = Move cursor")
print("2 fingers (index+middle) = Scroll mode")
print("Pinch (thumb+index close) = Left click")
print("Pinch (thumb+middle close) = Right click")
print("Pinch (thumb+index) in volume mode = Volume control")
print("5 fingers (open palm) = Pause/Resume")
print("\nPress ESC or 'q' to exit\n")

while True:
    success, frame = cap.read()
    if not success:
        break
    
    frame = cv2.flip(frame, 1)
    
    try:
        frame = detector.find_hands(frame)
        x, y = detector.get_finger_position(frame)
        fingers = detector.count_fingers(frame)
        
        if action_cooldown > 0:
            action_cooldown -= 1
        
        # Pause/Resume gesture (5 fingers)
        if fingers == 5 and action_cooldown == 0:
            paused = not paused
            action_cooldown = 20
            status = "PAUSED" if paused else "RESUMED"
            cv2.putText(frame, status, (200, 240), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3)
        
        if paused:
            cv2.putText(frame, "SYSTEM PAUSED", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        elif x and y:
            # Mouse movement (1 finger)
            if fingers == 1:
                screen_x = int((x / 640) * screen_width)
                screen_y = int((y / 480) * screen_height)
                current_x = prev_x + (screen_x - prev_x) / smoothing
                current_y = prev_y + (screen_y - prev_y) / smoothing
                pyautogui.moveTo(current_x, current_y)
                prev_x, prev_y = current_x, current_y
                cv2.putText(frame, "MOVE", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
            # Scroll mode (2 fingers)
            elif fingers == 2:
                if y < 240:
                    pyautogui.scroll(10)
                    cv2.putText(frame, "SCROLL UP", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
                else:
                    pyautogui.scroll(-10)
                    cv2.putText(frame, "SCROLL DOWN", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
            
            # Volume control (3 fingers)
            elif fingers == 3:
                distance, p1, p2 = detector.get_distance(frame, 8, 4)
                if distance and volume_enabled:
                    vol = int((distance - 20) / 200 * (max_vol - min_vol) + min_vol)
                    vol = max(min_vol, min(max_vol, vol))
                    volume.SetMasterVolumeLevel(vol, None)
                    vol_percent = int((vol - min_vol) / (max_vol - min_vol) * 100)
                    cv2.putText(frame, f"VOLUME: {vol_percent}%", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
                    cv2.line(frame, p1, p2, (255, 255, 0), 3)
                elif not volume_enabled:
                    cv2.putText(frame, "VOLUME: Not Available", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
            
            # Left click (pinch thumb+index)
            distance_thumb_index, p1, p2 = detector.get_distance(frame, 8, 4)
            if distance_thumb_index and distance_thumb_index < click_threshold and action_cooldown == 0 and fingers <= 2:
                pyautogui.click()
                action_cooldown = 15
                cv2.putText(frame, "LEFT CLICK", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
            
            # Right click (pinch thumb+middle)
            distance_thumb_middle, p3, p4 = detector.get_distance(frame, 12, 4)
            if distance_thumb_middle and distance_thumb_middle < click_threshold and action_cooldown == 0:
                pyautogui.rightClick()
                action_cooldown = 15
                cv2.putText(frame, "RIGHT CLICK", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 3)
            
            cv2.circle(frame, (x, y), 10, (0, 255, 0), cv2.FILLED)
            cv2.putText(frame, f"Fingers: {fingers}", (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        else:
            cv2.putText(frame, "No Hand Detected", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    
    except Exception as e:
        print(f"Error: {e}")
        cv2.putText(frame, "Error", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    
    cv2.imshow("AI Gesture Mouse", frame)
    
    key = cv2.waitKey(1) & 0xFF
    if key == 27 or key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
print("Program terminated")
