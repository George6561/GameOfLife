from pathlib import Path

from GameOfLife import GameOfLife
from PixelGridWindow import PixelGridWindow

STEP_MS = 120


def render(window: PixelGridWindow, life: GameOfLife) -> None:
    window.begin_batch()
    window.clear()
    window.set_pixels(life.alive, color="black")
    window.end_batch()


def tick(window: PixelGridWindow, life: GameOfLife) -> None:
    life.step()
    render(window, life)
    window.root.after(STEP_MS, tick, window, life)


if __name__ == "__main__":
    here = Path(__file__).parent
    seed_path = here / "seed.png"

    life = GameOfLife.from_image(
        str(seed_path),
        sample_step=1,
        crop_to_content=True
    )

    window = PixelGridWindow(
        cell_size=4,
        title="Game of Life",
        origin_centered=True
    )

    render(window, life)
    window.root.after(STEP_MS, tick, window, life)
    window.mainloop()
