import pygame
from os import path
from time import sleep
import random

HUDs_to_render = []
comp = 0

class Hud:
    def __init__(self, position, text, timeout=0, style="default"):
        self.txt = text
        self.colour = (0,0,0)
        self.font = pygame.font.Font(path.join("assets", "fonts", "ShareTechMono-Regular.ttf"), 25)
        self.hud = self.font.render(self.txt, 1, self.colour)
        HUDs_to_render.append((self.hud, position))
        if timeout > 0:
            self.timeout(timeout)

    def timeout(self, timeout):
        sleep(timeout)
        for i in range(0, len(HUDs_to_render)):
            if self.hud in HUDs_to_render[i]:
                HUDs_to_render.pop(i)

class Computer_ui:
    global comp
    def __init__(self):
        self.cs = pygame.Surface((400,400))
        self.colour = (249,249,249)
        self.font = pygame.font.Font(path.join("assets", "fonts", "ShareTechMono-Regular.ttf"), 25)
        self.run = True
        self.txt = "[USR943@GOVSYS~]$  "
    def main(self):
        global comp
        for i in range(20, random.randint(21, 100)):
            self.txt = "[USR943@GOVSYS~]$  "
            self.hud = self.font.render(self.txt, 1, self.colour)
            self.txt += self.randtxt()
            self.cs.blit(self.hud, (0,0))
            comp = self.cs
        comp = 0
    def randtxt(self):
        letters = [
            "q",
            "w",
            "e",
            "r",
            "t",
            "y",
            "u",
            "i",
            "o",
            "p",
            "a",
            "s",
            "d",
            "f",
            "g",
            "h",
            "j",
            "k",
            "l",
            "z",
            "x",
            "c",
            "v",
            "b",
            "n",
            "m"
        ]
        word = ""
        for i in range(1, random.randint(1, 12)):
            word += letters[random.randint(0, 25)]
        return word
