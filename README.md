# NES Tennis Clone

A small single-player tennis game built with Python and Pygame. Move the
bottom paddle, choose a flat or lob serve, rally against the CPU, and score
using simplified tennis rules.

## Run locally

Python 3.10 or newer is recommended.

```bash
python -m venv .venv
```

Activate the environment:

```powershell
# Windows PowerShell
.venv\Scripts\Activate.ps1
```

```bash
# macOS or Linux
source .venv/bin/activate
```

Install and launch:

```bash
python -m pip install -r requirements.txt
python main.py
```

## Controls

| Action | Key |
|---|---|
| Move left | Left arrow |
| Move right | Right arrow |
| Flat serve | Space |
| Lob serve | Shift + Space |
| Quit | Close the game window |

## Project structure

- `main.py`: game loop, drawing and scoring events
- `ball.py`: ball motion, height and paddle collision logic
- `player.py`: player and CPU paddle representation
- `score.py`: simplified tennis scoring
- `config.py`: screen size, frame rate and movement speeds

The game currently uses idealized two-dimensional collisions and a simple CPU
that tracks the ball horizontally.
