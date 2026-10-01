# AirDraw 🎨

AirDraw is a touchless computer-vision drawing application built with Python, OpenCV and MediaPipe. It tracks a user's hand in real time and lets them draw in the air using finger gestures.

## Features

- Real-time webcam processing
- MediaPipe hand tracking
- 21 hand-landmark visualization
- Index-finger drawing
- Index + middle finger selection gesture
- Multiple drawing colors
- Eraser
- Clear canvas
- Undo / redo
- Save drawings as PNG
- Keyboard shortcuts

## Technology Stack

- Python
- OpenCV
- MediaPipe
- NumPy

## Project Structure

```text
AirDraw/
├── main.py
├── requirements.txt
├── README.md
├── .gitignore
├── src/
│   ├── config.py
│   ├── drawing.py
│   └── hand_tracker.py
├── screenshots/
└── drawings/
```

## Installation

### 1. Create a virtual environment

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

### 2. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Run

```bash
python main.py
```

## Gestures

| Gesture | Action |
|---|---|
| Index finger up | Draw |
| Index + middle fingers up | Select toolbar |
| No drawing gesture | Stop drawing |

## Keyboard Shortcuts

| Key | Action |
|---|---|
| Q | Quit |
| C | Clear |
| U | Undo |
| R | Redo |
| S | Save PNG |
| E | Eraser |

## How to Use

1. Start the application.
2. Show one hand to the webcam.
3. Raise only your index finger and move it to draw.
4. Raise index + middle fingers to enter selection mode.
5. Move the index fingertip over a color circle and select it.
6. Select the eraser or other tools from the top toolbar.
7. Press `S` or select Save to export the drawing.
8. Saved drawings appear in the `drawings` folder.

## Troubleshooting

### Camera does not open

Try changing:

```python
cv2.VideoCapture(0)
```

to:

```python
cv2.VideoCapture(1)
```

### MediaPipe installation problem

Make sure your virtual environment is activated:

```bash
venv\Scripts\activate
```

Then run:

```bash
pip install --upgrade pip
pip install mediapipe opencv-python numpy
```

## Future Improvements

- Two-hand gestures
- Shape recognition
- Text recognition
- Custom brush sizes
- Neon/glow brushes
- Gesture-controlled UI animations
- Export to SVG
- Voice commands
- Web-based version

## Author

Built as a Computer Vision and Human-Computer Interaction portfolio project.
