from scene import Scene

scene = Scene()
scene.load_scene()

while scene.run_scene:
    scene.get_collisions()
    scene.render_scene()
    scene.handle_player_movement_keys()
    scene.handle_management_keys()

scene.save_scene()
del scene
