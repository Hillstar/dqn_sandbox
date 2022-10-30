import pygame
from os import path

import Boundary as BD
import Car

FPS = 60
DEBUG_ENABLED = False
SAVE_FILE = "scene.txt"
SAVE_CAR_DATA = False

def PRINT_DEBUG(arg):
    if not DEBUG_ENABLED:
        return
    if isinstance(arg, str):
        print(arg)
    elif isinstance(arg, list): # list of objects
        for obj in arg:
            print(obj.rect)

# PYGAME INIT
pygame.init()
window = pygame.display.set_mode((1200, 800))
clock = pygame.time.Clock()

# OBJECTS INIT
user_car = Car.car()
objects = []
selected_obj = None



def add_obj():
    global objects
    global selected_obj
    PRINT_DEBUG("ADD")
    objects.append(BD.boundary())
    selected_obj = objects[-1]

def delete_obj():
    global objects
    global selected_obj
    PRINT_DEBUG("DELETE")
    objects.remove(selected_obj)
    selected_obj = None

def load_scene():
    PRINT_DEBUG("LOAD SCENE")
    if not path.exists(SAVE_FILE):
        PRINT_DEBUG("SAVE FILE NOT FOUND")
        return

    global user_car

    with open(SAVE_FILE) as f:
        lines = [line.rstrip('\n') for line in f]
    
    for line in lines:
        args = line.split()

        center = (int(args[1]), int(args[2]))
        size = (int(args[3]), int(args[4]))

        if SAVE_CAR_DATA and args[0] == "car":
            user_car = Car.car(center, size)
        elif args[0] == "obj":
            objects.append(BD.boundary(center, size))

    PRINT_DEBUG(objects)

def save_scene():
    PRINT_DEBUG("SAVE SCENE")
    f = open(SAVE_FILE, "w")
    if SAVE_CAR_DATA:
        f.write(f"car {user_car.rect.left} {user_car.rect.top} {user_car.rect.width} {user_car.rect.height}\n")
    for obj in objects:
        f.write(f"obj {obj.rect.left} {obj.rect.top} {obj.rect.width} {obj.rect.height}\n")
    f.close()

    PRINT_DEBUG(objects)


load_scene()
run = True
while run:
    pygame.time.delay(10)
    dt = clock.tick(FPS)/1000
    #PRINT_DEBUG(clock.get_fps())

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                if not selected_obj:
                    add_obj()

            if event.key == pygame.K_q:
                if selected_obj != None:
                    delete_obj()
            
            if event.key == pygame.K_r:
                if selected_obj != None:
                    selected_obj.rotate()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: # left mouse button
                if selected_obj != None:
                    selected_obj = None # Drop object
                else: # Select object
                    x_mouse, y_mouse = pygame.mouse.get_pos()
                    for obj in objects:
                        if obj.rect.collidepoint((x_mouse, y_mouse)):
                            selected_obj = obj
                            break

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        user_car.rect.centerx -= int(user_car.move_speed * dt)

    if keys[pygame.K_RIGHT]:
        user_car.rect.centerx += int(user_car.move_speed * dt)

    if keys[pygame.K_UP]:
        user_car.rect.centery -= int(user_car.move_speed * dt)

    if keys[pygame.K_DOWN]:
        user_car.rect.centery += int(user_car.move_speed * dt)

    window.fill(0)

    if selected_obj:
        selected_obj.rect.center = pygame.mouse.get_pos()

    for obj in objects:
        collide = obj.rect.colliderect(user_car)
        color = (255, 0, 0) if collide else (255, 255, 255)
        pygame.draw.rect(window, color, obj.rect)

    pygame.draw.rect(window, (0, 255, 0), user_car.rect, 6, 1)

    pygame.display.flip()
    pygame.display.update()
    clock.tick(FPS)

save_scene()
pygame.quit()
exit()