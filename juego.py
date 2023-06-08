from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import random

app = Ursina()

class Voxel(Button):
    def __init__(self, position=(0, 0, 0)):
        super().__init__(
            parent=scene,
            position=position,
            model='cube',
            origin_y=0.5,
            texture='brick',
            color=color.rgb(255, 255, 255),
            highlight_color=color.lime,
        )

plataform = 16
cubes_remaining = plataform * plataform
lives = 3

platform_cubes = []

for z in range(plataform):
    for x in range(plataform):
        voxel = Voxel(position=(x, 0, z))
        platform_cubes.append(voxel)

player = FirstPersonController()

falling_cubes = []
falling_speed = 0.1
timer = 0.0

time_text = Text(text="Time: 0", position=(-0.85, 0.45))
lives_text = Text(text="Lives: 3", position=(-0.85, 0.4))

def start_game():
    global player
    player = FirstPersonController()

    destroy(start_button)
    destroy(high_scores_button)
    destroy(quit_button)
    destroy(config_button)

    app.on_update = update

def show_high_scores():
    print("Mostrando puntuaciones más altas")

def quit_game():
    application.quit()

def show_config():
    print("Mostrando configuración")

start_button = Button(
    text="Jugar",
    color=color.gray,
    scale=(0.2, 0.1),
    position=(0, 0.1),
    on_click=start_game
)

high_scores_button = Button(
    text="Puntuación más alta",
    color=color.gray,
    scale=(0.2, 0.1),
    position=(0, -0.1),
    on_click=show_high_scores
)

quit_button = Button(
    text="Salir",
    color=color.gray,
    scale=(0.2, 0.1),
    position=(0, -0.3),
    on_click=quit_game
)

config_button = Button(
    text="Configuración",
    color=color.gray,
    scale=(0.2, 0.1),
    position=(-0.8, 0.45),
    on_click=show_config
)

def update():
    global cubes_remaining, falling_speed, timer, lives

    timer += time.dt

    if timer > 5.0:
        falling_speed += 0.01
        timer = 0.0

    if random.random() < 0.01 + timer * 0.01:
        x = random.randint(0, plataform - 1)
        z = random.randint(0, plataform - 1)
        falling_cube = Voxel(position=(x, 10, z))
        falling_cubes.append(falling_cube)

    for falling_cube in falling_cubes:
        falling_cube.y -= falling_speed

        if player.intersects(falling_cube):
            falling_cubes.remove(falling_cube)
            destroy(falling_cube)
            lives -= 1
            lives_text.text = f"Lives: {lives}"
            if lives == 0:
                print("¡Has perdido!")
                application.quit()

        if falling_cube.y < -1:
            falling_cubes.remove(falling_cube)
            destroy(falling_cube)

    if player.y < -10:
        print("¡Has perdido!")
        application.quit()

    if cubes_remaining == 0:
        print("¡Has ganado!")
        application.quit()

    time_text.text = f"Time: {int(timer)}"

app.run()

