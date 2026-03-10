# AI Hand Gesture Control System

A Python-based computer vision system that enables hands-free computer control using hand gestures captured through a webcam. Built with MediaPipe, OpenCV, and PyAutoGUI.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![OpenCV](https://img.shields.io/badge/OpenCV-4.x-green)
![MediaPipe](https://img.shields.io/badge/MediaPipe-0.10%2B-orange)

## 🎯 Features

- **Mouse Control**: Move cursor with index finger
- **Left Click**: Pinch thumb and index finger
- **Right Click**: Pinch thumb and middle finger
- **Scroll**: Two fingers up/down
- **Volume Control**: Three fingers with pinch gesture
- **Pause/Resume**: Open palm (5 fingers)
- Real-time hand tracking with visual feedback
- Smooth cursor movement with jitter reduction

## 🎥 Demo

### Gesture Controls

| Gesture | Action | Fingers |
|---------|--------|----------|
| Index finger pointing | Move cursor | 1 |
| Index + Middle finger | Scroll up/down | 2 |
| Three fingers + pinch | Volume control | 3 |
| Thumb + Index pinch | Left click | - |
| Thumb + Middle pinch | Right click | - |
| Open palm | Pause/Resume | 5 |

## 🛠️ Technologies Used

- **Python 3.8+**: Programming language
- **OpenCV**: Webcam capture and image processing
- **MediaPipe**: Hand detection and landmark tracking
- **PyAutoGUI**: System mouse and keyboard control
- **Pycaw**: Windows audio control

## 📋 Prerequisites

- Python 3.8 or higher
- Webcam
- Windows OS (for volume control feature)

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/AI-Hand-Gesture-Control-System.git
cd AI-Hand-Gesture-Control-System
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

Or install individually:

```bash
pip install opencv-python mediapipe pyautogui pycaw comtypes
```

### 3. Run the program

```bash
python main.py
```

## 📖 Usage

1. Run the program using `python main.py`
2. Position your hand in front of the webcam
3. Perform gestures to control your computer:
   - **1 finger**: Move the cursor
   - **2 fingers**: Scroll (hand position determines direction)
   - **3 fingers**: Volume control mode
   - **Pinch gestures**: Click actions
   - **5 fingers**: Pause/Resume the system
4. Press **ESC** or **'q'** to exit

## 📁 Project Structure

```
AI-Hand-Gesture-Control-System/
│
├── main.py                 # Main program with gesture logic
├── hand_tracking.py        # Hand detection and tracking module
├── requirements.txt        # Project dependencies
├── README.md              # Project documentation
├── .gitignore             # Git ignore file
└── hand_landmarker.task   # MediaPipe model (auto-downloaded)
```

## 🔧 How It Works

1. **Video Capture**: Captures live video from webcam using OpenCV
2. **Hand Detection**: MediaPipe detects hand and identifies 21 landmarks
3. **Gesture Recognition**: Analyzes finger positions to identify gestures
4. **Coordinate Mapping**: Converts camera coordinates to screen coordinates
5. **Action Execution**: PyAutoGUI performs corresponding mouse/keyboard actions
6. **Smoothing**: Applies smoothing algorithm to reduce cursor jitter

## 🎓 Technical Details

### Hand Landmarks
MediaPipe detects 21 hand landmarks:
- Landmark 4: Thumb tip
- Landmark 8: Index finger tip
- Landmark 12: Middle finger tip
- Landmark 16: Ring finger tip
- Landmark 20: Pinky tip

### Gesture Detection Logic
- **Finger Counting**: Compares Y-coordinates of fingertips with knuckles
- **Pinch Detection**: Calculates Euclidean distance between fingertips
- **Smoothing**: Uses exponential moving average for cursor stability

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| Camera not opening | Close other apps using webcam |
| Import errors | Reinstall dependencies: `pip install -r requirements.txt` |
| Slow performance | Close background applications |
| Volume control not working | Ensure running on Windows with audio device |
| Hand not detected | Improve lighting, adjust hand distance |

## 🔮 Future Enhancements

- [ ] Add double-click gesture
- [ ] Implement drag and drop functionality
- [ ] Add gesture customization settings
- [ ] Support for two-hand gestures
- [ ] Cross-platform volume control
- [ ] Gesture recording and playback
- [ ] Performance optimization for low-end systems
- [ ] Add configuration file for custom settings

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is free to use for educational purposes.

## 👨‍💻 Author

**BCA Final Year Project**

## 🙏 Acknowledgments

- [MediaPipe](https://mediapipe.dev/) for hand tracking
- [OpenCV](https://opencv.org/) for computer vision
- [PyAutoGUI](https://pyautogui.readthedocs.io/) for system control

## 📧 Contact

For questions or feedback, please open an issue on GitHub.

---

⭐ Star this repository if you find it helpful!