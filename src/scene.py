import pygame

from asyncio.windows_events import INFINITE
from pygame import Vector2 as v2
from os import path
from enum import Enum
from objects import Object_type, Player, Scene_object

FPS = 60
SCREEN_WIDTH = 380
SCREEN_HEIGHT = 380
DEBUG_ENABLED = False
SAVE_FILE = "scene.txt"
SAVE_CAR_DATA = False
MOVE_RESTRICTIONS = True

def PRINT_DEBUG(arg):
    if not DEBUG_ENABLED:
        return
    if isinstance(arg, str):
        print(arg)
    elif isinstance(arg, list): # list of objects
        for obj in arg:
            print(obj.rect)

class Move_type(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3

class Scene():
    def __init__(self):
        # PYGAME INIT
        pygame.init()
        self.window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()

        # OBJECTS INIT
        self.player = Player()
        self.scene_objects = []

        # SCENE ENV INIT
        self.run_scene = True
        self.selected_obj = None
        # self.boundary_hit = False
        # self.finish_hit = False
        # self.dist_to_finish = 0
        # self.dist_to_nearst_bnd = INFINITE

    def __del__(self):
        pygame.quit()

    def add_obj(self, obj_type, center = (300, 300)):
        if obj_type == Object_type.SCENE_OBJECT: # rework here to single line and dynamic arg puting
            color = (100, 255, 255)
            hit_color = (255, 50, 50)
            PRINT_DEBUG("ADD BOUNDARY")
        else: # CHECK_POINT
            color = (50, 35, 200)
            hit_color = (220, 220, 220)
            PRINT_DEBUG("ADD FINISH")

        self.scene_objects.append(Scene_object(obj_type = obj_type.value, center = center, color = color, hit_color = hit_color))
        self.selected_obj = self.scene_objects[-1]

    def delete_obj(self):
        PRINT_DEBUG("DELETE")
        self.scene_objects.remove(self.selected_obj)
        self.selected_obj = None

    def load_scene(self):
        PRINT_DEBUG("LOAD SCENE")
        if not path.exists(SAVE_FILE):
            PRINT_DEBUG("SAVE FILE NOT FOUND")
            return

        with open(SAVE_FILE) as f:
            lines = [line.rstrip('\n') for line in f]
        
        for line in lines:
            args = line.split()
            args = [ int(arg) for arg in args ]
            
            obj_type = args[0]
            center = (args[1], args[2])
            size = (args[3], args[4])
            color = (args[5], args[6], args[7])
            hit_color = (args[8], args[9], args[10])

            if obj_type == Object_type.PLAYER.value and SAVE_CAR_DATA:
                self.player = Player(center = center, size = size)
            elif obj_type == Object_type.SCENE_OBJECT.value or obj_type == Object_type.CHECK_POINT.value:
                self.scene_objects.append(Scene_object(obj_type = obj_type, center = center, size = size, color = color, hit_color = hit_color))

        if not SAVE_CAR_DATA:
            self.player.reset_position()

        PRINT_DEBUG(self.scene_objects)

    def save_scene(self):
        PRINT_DEBUG("SAVE SCENE")
        f = open(SAVE_FILE, "w")
        if SAVE_CAR_DATA:
            f.write(f"{Object_type.PLAYER} {self.player.rect.left} {self.player.rect.top} {self.player.rect.width} {self.player.rect.height}\n")
        for obj in self.scene_objects:
            f.write(f"{obj.type} {obj.rect.centerx} {obj.rect.centery} {obj.rect.width} {obj.rect.height} " \
                f"{obj.color[0]} {obj.color[1]} {obj.color[2]} {obj.hit_color[0]} {obj.hit_color[1]} {obj.hit_color[2]}\n")
        f.close()

        PRINT_DEBUG(self.scene_objects)

    def restart_scene(self):
        # SCENE ENV REINIT
        # self.boundary_hit = False
        # self.finish_hit = False
        # self.distance_to_finish = 0
        # self.distance_to_nearst_bnd = INFINITE
        self.run_scene = True
        self.selected_obj = None
        self.scene_objects = []
        self.load_scene()

    def get_collisions(self):
        for obj in self.scene_objects:
            collide = obj.rect.colliderect(self.player)
            if collide: 
                #self.boundary_hit = True
                obj.hit = True
            # else:
            #     obj.hit = False

            #if collide and obj.type == Object_type.CHECK_POINT:
                #self.finish_hit = True

        #PRINT_DEBUG(f"F {self.dist_to_finish}")
        #PRINT_DEBUG(f"NB = {self.dist_to_nearst_bnd}")

    def render_scene(self):
        self.window.fill(0)

        for obj in self.scene_objects:
            color = obj.get_color()
            pygame.draw.rect(self.window, color, obj.rect)
        
        pygame.draw.rect(self.window, self.player.color, self.player.rect, 8, 1)

        pygame.display.flip()
        self.clock.tick(FPS)

    def get_screen_pixels(self):
        return pygame.surfarray.pixels3d(self.window)
    
    def get_screen_size(self):
        return self.window.get_size()

    def _perform_move_restrictions(self, action, dt):
        move_step = self.player.move_speed * dt
        if action is Move_type.LEFT and self.player.rect.left < 0:
            self.player.rect.centerx += int(move_step)

        if action is Move_type.RIGHT and self.player.rect.right > self.window.get_width():
            self.player.rect.centerx -= int(move_step)

        if action is Move_type.UP and self.player.rect.top < 0:
            self.player.rect.centery += int(move_step)

        if action is Move_type.DOWN and  self.player.rect.bottom > self.window.get_height():
            self.player.rect.centery -= int(move_step)

    def _move_player(self, action):
        dt = 0.03 #clock.tick(FPS)/1000
        move_step = self.player.move_speed * dt
        if action is Move_type.LEFT:
            self.player.rect.centerx -= int(move_step)

        if action is Move_type.RIGHT:
            self.player.rect.centerx += int(move_step)

        if action is Move_type.UP:
            self.player.rect.centery -= int(move_step)

        if action is Move_type.DOWN:
            self.player.rect.centery += int(move_step)

        if MOVE_RESTRICTIONS:
            self._perform_move_restrictions(action, dt)

    def handle_player_movement_keys(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self._move_player(Move_type.LEFT)

        if keys[pygame.K_RIGHT]:
            self._move_player(Move_type.RIGHT)

        if keys[pygame.K_UP]:
            self._move_player(Move_type.UP)

        if keys[pygame.K_DOWN]:
            self._move_player(Move_type.DOWN)

    def handle_management_keys(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run_scene = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    if not self.selected_obj:
                        self.add_obj(Object_type.SCENE_OBJECT)

                if event.key == pygame.K_2:
                    if not self.selected_obj:
                        self.add_obj(Object_type.CHECK_POINT)
            
                if event.key == pygame.K_d:
                    if self.selected_obj != None:
                        self.delete_obj()
                
                if event.key == pygame.K_r:
                    if self.selected_obj != None:
                        self.selected_obj.rotate()

                if event.key == pygame.K_f:
                    self.restart_scene()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # left mouse button
                    if self.selected_obj != None:
                        self.selected_obj = None # Drop object
                    else: # Select object
                        x_mouse, y_mouse = pygame.mouse.get_pos()
                        for obj in self.scene_objects:
                            if obj.rect.collidepoint((x_mouse, y_mouse)):
                                self.selected_obj = obj
                                break
        if self.selected_obj:
            self.selected_obj.rect.center = pygame.mouse.get_pos()

    # def calc_distances(self):
    #     dists = []
    #     for obj in self.scene_objects:

    #         if obj.type == Object_type.FINISH:
    #             self.dist_to_finish = pygame.math.Vector2.distance_to(v2(obj.rect.center), v2(self.player.rect.center))
    #         else:
    #             dists.append(pygame.math.Vector2.distance_to(v2(obj.rect.center), v2(self.player.rect.center)))
    #             self.dist_to_nearst_bnd = min(dists)

    #     PRINT_DEBUG(f"F {self.dist_to_finish}\n")
    #     PRINT_DEBUG(f"NB = {self.dist_to_nearst_bnd}")