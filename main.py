import cv2
import numpy as np
from src.hand_tracker import HandTracker
from src.config import COLORS, TOOLS, TOOLBAR_HEIGHT
from src.drawing import DrawingCanvas

CAMERA_WIDTH = 1280
CAMERA_HEIGHT = 720


def fingers_up(landmarks):
    """Return [thumb, index, middle, ring, pinky] as 0/1."""
    if landmarks is None:
        return [0, 0, 0, 0, 0]

    # For a mirrored webcam, these x comparisons work well for the thumb.
    thumb = int(landmarks[4][0] > landmarks[3][0])

    # Finger is considered up when its tip is above the PIP joint.
    index = int(landmarks[8][1] < landmarks[6][1])
    middle = int(landmarks[12][1] < landmarks[10][1])
    ring = int(landmarks[16][1] < landmarks[14][1])
    pinky = int(landmarks[20][1] < landmarks[18][1])

    return [thumb, index, middle, ring, pinky]


def draw_toolbar(frame, selected_color, selected_tool):
    cv2.rectangle(frame, (0, 0), (CAMERA_WIDTH, TOOLBAR_HEIGHT), (25, 25, 25), -1)

    x = 15
    for name, color in COLORS.items():
        radius = 22
        center = (x + radius, 38)
        cv2.circle(frame, center, radius, color, -1)

        if selected_tool == name:
            cv2.circle(frame, center, radius + 4, (255, 255, 255), 2)

        x += 55

    # Tool buttons
    tools = [
        ("E", "eraser"),
        ("C", "clear"),
        ("U", "undo"),
        ("R", "redo"),
        ("S", "save"),
    ]

    for label, tool in tools:
        cv2.rectangle(frame, (x, 12), (x + 48, 62), (60, 60, 60), -1)
        cv2.putText(frame, label, (x + 14, 47),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        if selected_tool == tool:
            cv2.rectangle(frame, (x, 12), (x + 48, 62), (255, 255, 255), 2)
        x += 58

    cv2.putText(
        frame,
        f"Color: {selected_color} | Tool: {selected_tool}",
        (15, 90),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.65,
        (255, 255, 255),
        2,
    )


def toolbar_action(x, y, canvas):
    """Handle a selection click. Returns (color_name, tool_name, changed)."""
    if y > TOOLBAR_HEIGHT:
        return None, None, False

    # Color circles
    start_x = 15
    for name in COLORS:
        cx = start_x + 22
        if (x - cx) ** 2 + (y - 38) ** 2 <= 27 ** 2:
            return name, "pen", True
        start_x += 55

    tool_start = start_x
    tools = [("eraser", 0), ("clear", 1), ("undo", 2), ("redo", 3), ("save", 4)]
    for tool, i in tools:
        left = tool_start + i * 58
        if left <= x <= left + 48 and 12 <= y <= 62:
            return None, tool, True

    return None, None, False


def main():
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_HEIGHT)

    if not cap.isOpened():
        print("ERROR: Could not open webcam.")
        print("Try changing cv2.VideoCapture(0) to cv2.VideoCapture(1) in main.py.")
        return

    tracker = HandTracker()
    canvas = DrawingCanvas(CAMERA_WIDTH, CAMERA_HEIGHT - TOOLBAR_HEIGHT)

    selected_color = "blue"
    selected_tool = "pen"
    previous_point = None
    status = "Show your hand"

    print("AirDraw started.")
    print("Q = quit | C = clear | U = undo | R = redo | S = save | E = eraser")

    while True:
        success, frame = cap.read()
        if not success:
            break

        frame = cv2.flip(frame, 1)

        # Keep toolbar area separate from drawing area.
        results = tracker.find_hands(frame, draw=True)
        landmarks = tracker.get_landmarks(results, frame.shape)

        draw_fingers = fingers_up(landmarks)

        # Gesture: index + middle up = selection mode.
        selection_mode = draw_fingers[1] == 1 and draw_fingers[2] == 1

        # Gesture: index only = drawing mode.
        drawing_mode = draw_fingers[1] == 1 and draw_fingers[2] == 0

        if landmarks:
            index_tip = landmarks[8]
            x, y = index_tip

            # Visual cursor
            cursor_color = (255, 255, 255) if selection_mode else COLORS[selected_color]
            cv2.circle(frame, (x, y), 10, cursor_color, 2)

            if selection_mode:
                status = "Selection mode"
                color_name, tool, changed = toolbar_action(x, y, canvas)

                if changed:
                    if color_name:
                        selected_color = color_name
                        selected_tool = "pen"
                    elif tool == "clear":
                        canvas.clear()
                        previous_point = None
                    elif tool == "undo":
                        canvas.undo()
                        previous_point = None
                    elif tool == "redo":
                        canvas.redo()
                        previous_point = None
                    elif tool == "save":
                        path = canvas.save()
                        status = f"Saved: {path}"
                        previous_point = None
                    elif tool == "eraser":
                        selected_tool = "eraser"
                        previous_point = None

            elif drawing_mode:
                status = "Drawing"
                if y > TOOLBAR_HEIGHT:
                    canvas_y = y - TOOLBAR_HEIGHT
                    current_point = (x, canvas_y)

                    if previous_point is not None:
                        color = (255, 255, 255) if selected_tool == "eraser" else COLORS[selected_color]
                        thickness = 35 if selected_tool == "eraser" else 8
                        canvas.draw_line(previous_point, current_point, color, thickness)

                    previous_point = current_point
            else:
                status = "Move hand"
                previous_point = None
        else:
            status = "No hand detected"
            previous_point = None

        # Composite canvas under/with webcam image.
        frame[TOOLBAR_HEIGHT:, :] = cv2.addWeighted(
            frame[TOOLBAR_HEIGHT:, :], 0.75,
            canvas.image, 0.95,
            0
        )

        draw_toolbar(frame, selected_color, selected_tool)

        cv2.putText(
            frame,
            status,
            (CAMERA_WIDTH - 380, 90),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 255),
            2,
        )

        cv2.putText(
            frame,
            "Index = Draw | Index+Middle = Select | Q = Quit",
            (15, CAMERA_HEIGHT - 15),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            (255, 255, 255),
            2,
        )

        cv2.imshow("AirDraw - Computer Vision Drawing", frame)

        key = cv2.waitKey(1) & 0xFF

        if key == ord("q"):
            break
        elif key == ord("c"):
            canvas.clear()
            previous_point = None
        elif key == ord("u"):
            canvas.undo()
            previous_point = None
        elif key == ord("r"):
            canvas.redo()
            previous_point = None
        elif key == ord("s"):
            path = canvas.save()
            status = f"Saved: {path}"
        elif key == ord("e"):
            selected_tool = "eraser"
            previous_point = None

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
