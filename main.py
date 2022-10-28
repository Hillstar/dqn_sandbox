import pygame
import Boundary as BD
import Car

FPS = 60
DEBUG_ENABLED = False

def PRINT_DEBUG(msg):
    if DEBUG_ENABLED:
        print(msg)

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
    # TODO
    PRINT_DEBUG("LOAD SCENE")
    return

def save_scene():
    # TODO
    PRINT_DEBUG("SAVE SCENE")
    return

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
        user_car.h_cdt -= int(user_car.move_speed * dt)

    if keys[pygame.K_RIGHT]:
        user_car.h_cdt += int(user_car.move_speed * dt)

    if keys[pygame.K_UP]:
        user_car.v_cdt -= int(user_car.move_speed * dt)

    if keys[pygame.K_DOWN]:
        user_car.v_cdt += int(user_car.move_speed * dt)

    window.fill(0)

    if selected_obj:
        selected_obj.rect.center = pygame.mouse.get_pos()

    for obj in objects:
        collide = obj.rect.colliderect(user_car)
        color = (255, 0, 0) if collide else (255, 255, 255)
        pygame.draw.rect(window, color, obj.rect)

    user_car.rect.center = (user_car.h_cdt, user_car.v_cdt)
    pygame.draw.rect(window, (0, 255, 0), user_car, 6, 1)

    pygame.display.flip()
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
exit()