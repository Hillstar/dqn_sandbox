import pygame
from os import path

import game_classes as GC
from game_classes import Object_type

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
user_car = GC.Car()
objects = []
selected_obj = None



def add_obj(type):
    global objects
    global selected_obj

    if type == Object_type.BOUNDARY:
        PRINT_DEBUG("ADD BOUNDARY")
        objects.append(GC.Boundary())
    elif type == Object_type.FINISH:
        PRINT_DEBUG("ADD FINISH")
        objects.append(GC.Finish())
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
        args = [ int(arg) for arg in args ]

        center = (args[1], args[2])
        size = (args[3], args[4])

        if args[0] == Object_type.CAR.value and SAVE_CAR_DATA:
            user_car = GC.Car(center, size)
        elif args[0] == Object_type.BOUNDARY.value:
            objects.append(GC.Boundary(center, size))
        elif args[0] == Object_type.FINISH.value:
            objects.append(GC.Finish(center, size))

    PRINT_DEBUG(objects)

def save_scene():
    PRINT_DEBUG("SAVE SCENE")
    f = open(SAVE_FILE, "w")
    if SAVE_CAR_DATA:
        f.write(f"{Object_type.CAR} {user_car.rect.left} {user_car.rect.top} {user_car.rect.width} {user_car.rect.height}\n")
    for obj in objects:
        f.write(f"{obj.type.value} {obj.rect.left} {obj.rect.top} {obj.rect.width} {obj.rect.height}\n")
    f.close()

    PRINT_DEBUG(objects)


load_scene()
run = True
game_over = False

while run and not game_over:
    pygame.time.delay(10)
    dt = clock.tick(FPS)/1000
    #PRINT_DEBUG(clock.get_fps())

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                if not selected_obj:
                    add_obj(Object_type.BOUNDARY)

            if event.key == pygame.K_f:
                if not selected_obj:
                    add_obj(Object_type.FINISH)
        
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
        color = (255, 0, 0) if collide else obj.color
        pygame.draw.rect(window, color, obj.rect)

        if collide and obj.type == Object_type.FINISH:
            game_over = True


    pygame.draw.rect(window, user_car.color, user_car.rect, 8, 1)

    pygame.display.flip()
    pygame.display.update()
    clock.tick(FPS)

if game_over:
    PRINT_DEBUG("YOU WON!!!")

save_scene()
pygame.quit()
exit()