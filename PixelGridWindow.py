import tkinter as tk
from typing import Dict, Iterable, Optional, Tuple

Coord = Tuple[int, int]


class PixelGridWindow:
    def __init__(
        self,
        cell_size: int = 4,
        grid_color: str = "#d0d0d0",
        background: str = "white",
        title: str = "Pixel Grid",
        start_width: int = 900,
        start_height: int = 650,
        origin_centered: bool = True,
    ):
        self.cell_size = int(cell_size)
        self.grid_color = grid_color
        self.background = background

        self.root = tk.Tk()
        self.root.title(title)
        self.root.geometry(f"{start_width}x{start_height}")

        self.canvas = tk.Canvas(self.root, bg=self.background, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        self._cells: Dict[Coord, str] = {}

        self.view_x = 0
        self.view_y = 0
        self._origin_centered = origin_centered

        # NEW: allow batching
        self._batch_depth = 0
        self._dirty = True

        self.canvas.bind("<Configure>", self._on_resize)
        self.root.after(0, self._initial_draw)

    # -------------------------
    # Batching API (NEW)
    # -------------------------
    def begin_batch(self) -> None:
        self._batch_depth += 1

    def end_batch(self) -> None:
        if self._batch_depth > 0:
            self._batch_depth -= 1
        if self._batch_depth == 0 and self._dirty:
            self._redraw()

    def _mark_dirty(self) -> None:
        self._dirty = True
        if self._batch_depth == 0:
            self._redraw()

    # -------------------------
    # Public API
    # -------------------------
    def set_pixel(self, x: int, y: int, color: str = "black") -> None:
        self._cells[(int(x), int(y))] = color
        self._mark_dirty()

    def set_pixels(self, pixels: Iterable[Coord], color: str = "black") -> None:
        # Fast: set a whole bunch then redraw once
        self.begin_batch()
        c = color
        for (x, y) in pixels:
            self._cells[(int(x), int(y))] = c
        self.end_batch()

    def clear(self) -> None:
        self._cells.clear()
        self._mark_dirty()

    def set_view_center(self, cx: int, cy: int) -> None:
        w = max(1, self.canvas.winfo_width())
        h = max(1, self.canvas.winfo_height())
        cols_visible = max(1, w // self.cell_size)
        rows_visible = max(1, h // self.cell_size)
        self.view_x = int(cx) - cols_visible // 2
        self.view_y = int(cy) - rows_visible // 2
        self._mark_dirty()

    def mainloop(self) -> None:
        self.root.mainloop()

    # -------------------------
    # Drawing internals
    # -------------------------
    def _initial_draw(self) -> None:
        if self._origin_centered:
            self.set_view_center(0, 0)
        else:
            self._redraw()

    def _on_resize(self, _event) -> None:
        self._mark_dirty()

    def _visible_cell_bounds(self) -> Tuple[int, int, int, int]:
        w = max(1, self.canvas.winfo_width())
        h = max(1, self.canvas.winfo_height())
        cols_visible = (w + self.cell_size - 1) // self.cell_size
        rows_visible = (h + self.cell_size - 1) // self.cell_size
        x0 = self.view_x
        y0 = self.view_y
        x1 = self.view_x + cols_visible - 1
        y1 = self.view_y + rows_visible - 1
        return x0, y0, x1, y1

    def _redraw(self) -> None:
        self._dirty = False
        self.canvas.delete("all")

        w = max(1, self.canvas.winfo_width())
        h = max(1, self.canvas.winfo_height())

        # grid lines
        cols_visible = (w + self.cell_size - 1) // self.cell_size
        rows_visible = (h + self.cell_size - 1) // self.cell_size

        for c in range(cols_visible + 1):
            x = c * self.cell_size
            self.canvas.create_line(x, 0, x, h, fill=self.grid_color)

        for r in range(rows_visible + 1):
            y = r * self.cell_size
            self.canvas.create_line(0, y, w, y, fill=self.grid_color)

        # visible colored cells
        x0, y0, x1, y1 = self._visible_cell_bounds()

        for (cx, cy), color in self._cells.items():
            if cx < x0 or cx > x1 or cy < y0 or cy > y1:
                continue

            sx0 = (cx - self.view_x) * self.cell_size + 1
            sy0 = (cy - self.view_y) * self.cell_size + 1
            sx1 = sx0 + self.cell_size - 2
            sy1 = sy0 + self.cell_size - 2
            self.canvas.create_rectangle(sx0, sy0, sx1, sy1, fill=color, outline=color)
