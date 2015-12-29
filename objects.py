from pygame import *
from time import sleep
import graphics
tile_w, tile_h = 0, 0
map_w, map_h = 0, 0
solids_in_use = False

def give_tile_data(w, h, mw, mh):
    global tile_w, tile_h, map_w, map_h
    tile_w, tile_h = w, h
    map_w, map_h = mw, mh

active_objects = []  # this includes placed objects, Handler's self.objects MUST be updated to this after placing.

solid = []

class Player_items:
    def __init__(self):
        self.wires = 50


class Handler:
    global solid, active_objects
    def __init__(self, obj):
        global active_objects
        active_objects = obj
        self.graphic = graphics.Objects()
    def main_loop(self, block=(0,0), counter=0):
        global solid
        if "door" in active_objects[counter]:
            # TODO: door stuff
            pass
        if "wall" in active_objects[counter]:
            solid.append(block)
            # TODO: solidise
        if "wire" in active_objects[counter]:
            # TODO: Wire stuff
            pass
        return active_objects[counter]

class Player:
    global solid, tile_w, tile_h
    def __init__(self):
        # TODO: Start positions
        self.x = 500
        self.y = 200
        self.current = "north"
        self.items = Player_items()
    def check_collisions(self, pos):  # TODO: fix slow warp through block thing
        try:
            solids_in_use = True
            tmp = True
            for i in range(0, len(solid)):
                if pos[0] > solid[i][0] - 32 and pos[0] < solid[i][0] + tile_w:
                    if pos[1] + 32 > solid[i][1] and pos[1] < solid[i][1] + tile_w:
                        solids_in_use = False
                        tmp = False
            solids_in_use = False
            return tmp
        except:
            return False
    def move(self, keys):
        global solid, tile_w, tile_h
        cant_move = False
        if keys[K_w] or keys[K_UP]:
            if self.check_collisions((self.x, self.y-5)):
                self.y -= 1
                sleep(0.001)
        if keys[K_s] or keys[K_DOWN]:
            if self.check_collisions((self.x, self.y+5)):
                self.y += 1
                sleep(0.001)
        if keys[K_a] or keys[K_LEFT]:
            if self.check_collisions((self.x-5, self.y)):
                self.x -= 1
                sleep(0.001)
        if keys[K_d] or keys[K_RIGHT]:
            if self.check_collisions((self.x+5, self.y)):
                self.x += 1
                sleep(0.001)
        if keys[K_e]:
            if "none" in active_objects[detect_item((self.x, self.y))]:
                if self.items.wires > 0:
                    if create_wire((self.x, self.y)):
                        self.items.wires -=1
                        sleep(0.3)
            elif "wire" in active_objects[detect_item((self.x, self.y))]:
                if remove_wire((self.x, self.y)):
                    self.items.wires +=1
                sleep(0.3)
    def render(self):
        return self.current, (self.x, self.y)

def get_wire_direction(position):
    global tile_w, tile_h, map_w, map_h, active_objects
    try:
        x = int(position[0]/tile_w) * tile_w
    except ZeroDivisionError:
        x = 0
    try:
        y = int(position[1]/tile_h) * tile_h
    except ZeroDivisionError:
        y = 0
    if "wire" in active_objects[detect_item((x+tile_w+10, y))] and "wire" in active_objects[detect_item((x, y+tile_h+10))]:
        return "es"
    elif "wire" in active_objects[detect_item((x+tile_w+10, y))] and "wire" in active_objects[detect_item((x, y-tile_h+10))]:
        return "ne"
    elif "wire" in active_objects[detect_item((x-tile_w+10, y))] and "wire" in active_objects[detect_item((x, y-tile_h+10))]:
        return "nw"
    elif "wire" in active_objects[detect_item((x-tile_w+10, y))] and "wire" in active_objects[detect_item((x, y+tile_h+10))]:
        return "sw"
    elif "wire" in active_objects[detect_item((x+tile_w+10, y))] or "wire" in active_objects[detect_item((x-tile_w+10, y))]:
        return "ew"
    else:
        return "ns"


def detect_item(position):
    global tile_w, tile_h, map_w, map_h
    try:
        x = int(position[0]/tile_w) * tile_w
    except ZeroDivisionError:
        x = 0
    try:
        y = int(position[1]/tile_h) * tile_h
    except ZeroDivisionError:
        y = 0
    x_order = int(x/tile_w)
    y_order = int(y/tile_h)
    order = (y_order * map_w) + x_order
    return order

def create_wire(position, type="electric_insulated"):  # TODO: wiretypes
    global active_objects
    order = detect_item(position)
    if active_objects[order] == "none":
        active_objects[order] = "electric_insulated_wire"
        return True
    else:
        return False  # attempted place on other item

def remove_wire(position):
    global active_objects
    order = detect_item(position)
    if "wire" in active_objects[order]:
        active_objects[order] = "none"
        return True
    else:
        return False  # not on a wire