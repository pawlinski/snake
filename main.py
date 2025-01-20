import math
import random
import pygame
import tkinter as tk
from tkinter import messagebox

# TODO: stwórz klasę -> kostka weża
# TODO: stwórz klasę -> wąż
# funkcja rysowania siatki
def draw_grid(w, rows, surface):
    size_between = w // rows # dzielenie bez wartości po przecinku

    x = 0
    y = 0
    for l in range(rows): # dla każdej linii w ilości rzędów
        x = x + size_between
        y = y + size_between
        pygame.draw.line(surface, (255, 255, 255), (x, 0), (x, w)) # rysuje linię poziomą
        pygame.draw.line(surface, (255, 255, 255), (0, y), (w, y)) # rysuje linię pionową

# funkcja rysowania okna
def draw_window(surface):
    surface.fill((0, 255, 0)) # RGB
    draw_grid(size, rows, surface)
    pygame.display.update()
# TODO: stwórz funkcję rysowania jabłka
# TODO: stwórz funkcję dla okna informacyjnego

def main():
    """main usuchamia się na początku gry/progrmu i jest odpowiedzialny za jego działanie, flow, etc."""
    global size, rows # widoczne poza funkcją
    # obszar gry
    size = 500
    rows = 20

    # inicjalizacja obszaru gry
    window = pygame.display.set_mode((size, size))

    # TODO: s = snake((color), (pozycja startowa))

    # jeżeli True, gra działa
    flag = True
    clock = pygame.time.Clock()

    while flag:
        for event in pygame.event.get(): # dla wszystkich eventów które się wydarzają
            if event.type == pygame.QUIT: # naciśnięty x
                flag = False

        pygame.time.delay(50) # zwolnienie gry o 50 milisekund (im mniej tym gra szybsza)
        clock.tick(10) # wąż porusza się 10 kostek na sekundę (im mniej tym gra wolniejsza) dlatego dodatkowo delay jest ustawione

        draw_window(window) # rysuje planszę

main()