# Conway’s Game of Life (Image-Seeded, Python)

This project is an implementation of **Conway’s Game of Life** in Python using a **sparse cell representation** and a **Tkinter-based visualiser**.  
Initial states are loaded directly from an image file, where **pure white pixels represent living cells**.

The focus of this implementation is clarity, correctness, and reasonable performance for large sparse grids.

---

## Features

- Sparse set-based representation (only alive cells are stored)
- Image-based seeding (`seed.png`)
- Exact Conway’s Game of Life rule implementation
- Adjustable simulation speed
- Custom pixel-grid renderer using Tkinter
- Origin-centred infinite grid view
- Efficient batch rendering to avoid redraw flicker

---

## Rules Implemented

This follows the standard Conway’s Game of Life rules:

- A live cell with **2 or 3 neighbours** survives
- A dead cell with **exactly 3 neighbours** becomes alive
- All other cells die or remain dead

Only pixels that are exactly **(255, 255, 255)** in the seed image are considered alive.  
Everything else is treated as dead.


---

## How It Works

### Image Loading

The simulation reads `seed.png` and scans every pixel:

- White pixels → alive
- Non-white pixels → dead

The image can optionally be sampled at lower resolution and cropped to its content to reduce empty space.

### Simulation Loop

The main loop:

1. Advances the Game of Life by one step  
2. Clears the screen  
3. Renders all alive cells  
4. Repeats after a fixed time delay  

The update rate is controlled via `STEP_MS` in `main.py`.

---

## Running the Project

### Requirements

- Python 3.10+
- Pillow (PIL)



