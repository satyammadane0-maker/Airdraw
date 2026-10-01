from pathlib import Path
from datetime import datetime
import cv2
import numpy as np


class DrawingCanvas:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.image = np.zeros((height, width, 3), dtype=np.uint8)

        self.undo_stack = []
        self.redo_stack = []

        Path("drawings").mkdir(exist_ok=True)

    def _snapshot(self):
        self.undo_stack.append(self.image.copy())
        if len(self.undo_stack) > 30:
            self.undo_stack.pop(0)
        self.redo_stack.clear()

    def draw_line(self, start, end, color, thickness=8):
        self._snapshot()
        cv2.line(self.image, start, end, color, thickness, cv2.LINE_AA)

    def clear(self):
        self._snapshot()
        self.image[:] = 0

    def undo(self):
        if not self.undo_stack:
            return
        self.redo_stack.append(self.image.copy())
        self.image = self.undo_stack.pop()

    def redo(self):
        if not self.redo_stack:
            return
        self.undo_stack.append(self.image.copy())
        self.image = self.redo_stack.pop()

    def save(self):
        filename = datetime.now().strftime("drawing_%Y%m%d_%H%M%S.png")
        path = Path("drawings") / filename

        # Convert black background to white for a clean saved drawing.
        output = self.image.copy()
        black = np.all(output == 0, axis=2)
        output[black] = (255, 255, 255)

        cv2.imwrite(str(path), output)
        return str(path)
