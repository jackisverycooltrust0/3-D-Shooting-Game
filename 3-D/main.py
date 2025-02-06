from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import random

game_engine = Ursina()

# Create the ground, walls, barrier
# Increase the ground size
platform = Entity(model="plane", scale=(200, 1, 200), color=color.yellow.tint(-2), texture="white_cube", texture_scale=(200, 200), collider="box")

# Adjust wall positions and scales
wall1 = Entity(model="cube", scale=(200, 42, 1), color=color.orange, collider="box", x=0, z=-2)
wall2 = Entity(model="cube", scale=(200, 42, 1), color=color.orange, collider="box", x=0, z=42)

wall3 = Entity(model="cube", scale=(200, 42, 1), color=color.orange, collider="box", x=-20, z=20, rotation_y=90)
wall4 = Entity(model="cube", scale=(200, 42, 1), color=color.orange, collider="box", x=20, z=20, rotation_y=90)

# Load a new texture for the walls
wall_texture = load_texture("brick_texture.jpg")  # Replace with your texture file

# Apply the new texture to the walls
wall1.texture = wall_texture
wall2.texture = wall_texture
wall3.texture = wall_texture
wall4.texture = wall_texture

player = FirstPersonController(model="cube", y=0, origin_y=5)

bullets = []
moving_targets = []

# Create 11 random moving targets
for _ in range(11):  # Changed from 6 to 11
    x = random.randrange(-19, 19, 2)  # Adjusted range for larger arena
    y = random.randrange(1, 6, 1)
    z = random.randrange(3, 41, 2)  # Adjusted range for larger arena
    target = Entity(model="cube", color=color.white, texture="target.jpg", scale=(1, 1, 0.1), position=(x, y, z), collider="box", dx=0.05)
    target.collider = BoxCollider(target, size=(2.5, 2.5, 2.5))
    moving_targets.append(target)

# Make a gun for the player
gun = Entity(parent=camera, model="Blaster/3D/Blaster.obj", color=color.red, origin_y=0.5, scale=(0.1, 0.1, 0.1), position=(2, -1, 2.5), collider="box", rotation=(0, -90, 0))

player.gun = gun

# Add a bullet counter
bullet_cap = 25
bullets_remaining = bullet_cap

def input(key):
    global bullets, bullets_remaining
    if key == "left mouse down" and player.gun and bullets_remaining > 0:
        bullet = Entity(parent=gun, model="cube", scale=1, position=(0, 0.5, 0), speed=3, collider="box", rotation_y=90)
        bullets.append(bullet)
        gun.blink(color.white)
        bullet.world_parent = scene
        bullets_remaining -= 1  # Decrease bullet count
        print(f"Bullets remaining: {bullets_remaining}")

    if bullets_remaining == 0:
        print("Out of bullets!")

def update():
    if held_keys["escape"]:
        print("Escape")
        application.quit()
    for target in moving_targets:
        target.x += target.dx
        if target.x > 19:  
            target.dx *= -1

        if target.x < -19:  
            target.x = -19
            target.dx *= -1

    # Get the bullet moving
    global bullets
    if len(bullets) > 0:
        for b in bullets:
            b.position += b.forward * 8
            hit_info = b.intersects()
            if hit_info.hit:
                if hit_info.entity in moving_targets:
                    moving_targets.remove(hit_info.entity)
                    destroy(hit_info.entity)
                    if len(moving_targets) == 0:
                        message = Text(text='YOU WON', scale=2, origin=(0, 0), background=True, color=color.blue)
                        application.pause()

if __name__ == "__main__":
    game_engine.run()