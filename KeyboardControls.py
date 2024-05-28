from main import LabyrinthSolverAPI
import keyboard as kb

game_on = True


def stop_game():
    global game_on
    game_on = False

Labyrinth = LabyrinthSolverAPI(side=10, drm=True, win_callback=stop_game)

for hotkey in ("up", "left", "down", "right"):
    kb.add_hotkey(hotkey, Labyrinth.move, args=(hotkey, ), timeout=0.5)

kb.add_hotkey('esc', stop_game)

while game_on:
    pass
