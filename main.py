import random
import pygame
import tkinter as tk
from tkinter import messagebox

# klasa -> kostka weża
class Cube:
    rows = 20
    def __init__(self, start, dirnx=1, dirny=0, color=(0, 0, 0)): # wąż od razu porusza się w prawo
        self.pos = start
        self.dirnx = dirnx
        self.dirny = dirny
        self.color = color

    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny) # przemieszczamy się o pozycję, czyli kostkę a nie piksel

    def draw(self, surface, eyes=False):
        dis = size // rows
        rw = self.pos[0] # rząd
        cm = self.pos[1] # kolumna

        pygame.draw.rect(surface, self.color, (rw * dis + 1, cm * dis + 1, dis -2 , dis -2)) # pomniejszamy kwadraty żeby była widoczna siatka

        # rysowanie oczu
        if eyes:
            center = dis // 2
            radius = 3
            circle_middle_1 = (rw * dis + center - radius * 2, cm * dis + 8) # środek oka 1
            circle_middle_2 = (rw * dis + dis - radius * 2, cm * dis + 8)  # środek oka 2
            pygame.draw.circle(surface, (255, 255, 255), circle_middle_1, radius)
            pygame.draw.circle(surface, (255, 255, 255), circle_middle_2, radius)


# klasa -> wąż
class Snake:
    body = [] # ciało węża
    turns = {}

    def __init__(self, color, pos):
        self.color = color
        self.head = Cube(pos) # tworzymy głowę w konkretnej pozycji
        self.body.append(self.head) # do ciała dodajemy kolejne głowy
        self.dirnx = 0 # kierunek poruszania się węża - watości -1, 0, 1
        self.dirny = 1

    def move(self): # ruch węża
        for event in pygame.event.get():  # dla wszystkich eventów które się wydarzają
            if event.type == pygame.QUIT:  # naciśnięty x
                pygame.quit() # zamiast flag = False

            keys = pygame.key.get_pressed() # zbiór wszystkich naciśniętych klawiszy w grze

            if keys[pygame.K_LEFT]:
                self.dirnx = -1
                self.dirny = 0
                self.turns[self.head.pos[:]] = [self.dirnx, self.dirny] # zapisuje pozycję zmiany kierunku do słownika
            elif keys[pygame.K_RIGHT]:
                self.dirnx = 1
                self.dirny = 0
                self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
            elif keys[pygame.K_UP]:
                self.dirnx = 0
                self.dirny = -1
                self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
            elif keys[pygame.K_DOWN]:
                self.dirnx = 0
                self.dirny = 1
                self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

        for i, c in enumerate(self.body): # przechodzi po każdym indeksie (i) i kostce (c) w body
            # [:] kopiuje element, a nie przypisuje do tego samego
            p = c.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0], turn[1]) # przemieszczamy kostkę na pozycję
                if i == len(self.body) - 1:
                    self.turns.pop(p)
            else: # poruszanie, kiedy pozycja nie znajduje się w turns (czyli do przodu)
                # sprawdzanie, czy dotarliśmy do krawędzi ekranu
                if c.dirnx == -1 and c.pos[0] <= 0: # jeżeli dotkniemy lewej strony
                    c.pos = (c.rows - 1, c.pos[1]) # to przerzuca kostkę na prawą
                elif c.dirnx == 1 and c.pos[0] >= c.rows - 1:
                    c.pos = (0, c.pos[1])
                elif c.dirny == 1 and c.pos[1] >= c.rows - 1:
                    c.pos = (c.pos[0], 0)
                elif c.dirny == -1 and c.pos[1] <= 0:
                    c.pos = (c.pos[0], c.rows - 1)
                else:
                    c.move(c.dirnx, c.dirny) # poruszamy się jeżeli nie dotknęliśmy krawędzi ekranu

    def reset(self, pos): # reset w przypadku zginięcia
        self.head = Cube(pos)  # tworzymy głowę w konkretnej pozycji
        self.body = [] # usuwamy elementy z ciała węża
        self.body.append(self.head)  # do ciała dodajemy kolejne głowy
        self.turns = {} # usuwamy info o skrętach
        self.dirnx = 0  # kierunek poruszania się węża - watości -1, 0, 1
        self.dirny = 1

    def add_cube(self): # powiększanie o jedną kostkę
        tail = self.body[-1] # ostatnia pozycja ciała węża
        dx, dy = tail.dirnx, tail.dirny

        if dx == 1 and dy == 0: # jeżeli ostatni element porusza się w prawo...
            self.body.append(Cube((tail.pos[0] - 1, tail.pos[1]))) # dołączy element po lewej stronie
        elif dx == -1 and dy == 0:
            self.body.append((Cube((tail.pos[0] + 1, tail.pos[1]))))
        elif dx == 0 and dy == 1:
            self.body.append((Cube((tail.pos[0], tail.pos[1] - 1))))
        elif dx == 0 and dy == -1:
            self.body.append((Cube((tail.pos[0], tail.pos[1] + 1))))

        self.body[-1].dirnx = dx # nadajemy nowemu ostatniemu elementowi kierunek poruszania taki jak miał poprzedni ostatni element
        self.body[-1].dirny = dy

    def draw(self, surface): # rysowanie węża
        for i, c in enumerate(self.body):
            if i == 0: # jeżeli jesteśmy na pierwszej pozycji w naszym ciele
                c.draw(surface, True) # rysuj kostkę z oczami
            else:
                c.draw(surface) # rysuj kostkę bez oczu

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
    s.draw(surface)
    apple.draw(surface)
    draw_grid(size, rows, surface)
    pygame.display.update()

# funkcja rysowania jabłka
def random_apple(snake):
    position = snake.body # pobieramy pozycję, żeby nie rysować jabłka na wężu

    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        if len(list(filter(lambda z: z.pos == (x, y), position))) > 0: # otrzymamy listę zawierającą przefiltrowaną inną listę, która sprawdzi czy którakolwiek z pozycji x, y znajduje się w zbiorze position
            continue # jeżeli jest to wychodzi z pętli i ponownie generuje x, y
        else:
            break # jeżeli nie ma to przerywamy i wychodzimy z pętli while
    return (x, y)

# funkcja dla okna informacyjnego
def message_box(subject, content):
    root = tk.Tk()
    root.attributes("-topmost", 1) # umieszcza okno na górze
    root.withdraw() # umieszcza okno na pierwszym planie
    messagebox.showinfo(subject, content)

    try:
        root.destroy()
    except:
        pass

def main():
    # This will attempt to initialize all the pygame modules for you. Not all pygame modules need to be initialized, but this will automatically initialize the ones that do. You can also easily initialize each pygame module by hand. For example to only initialize the font module you would just call.
    pygame.init()
    pygame.display.init()
    """main usuchamia się na początku gry/progrmu i jest odpowiedzialny za jego działanie, flow, etc."""
    global size, rows, s, apple # widoczne poza funkcją
    # obszar gry
    size = 500
    rows = 20
    score = 0

    # inicjalizacja obszaru gry
    window = pygame.display.set_mode((size, size))

    s = Snake((0, 0, 0), (10, 10)) # tworzy obiekt węża
    apple = Cube(random_apple(s), color=(255, 0, 0)) # tworzy obiekt jabłka

    # jeżeli True, gra działa
    flag = True
    clock = pygame.time.Clock()

    while flag:
        # pygame.event.poll() # pobiera eventy nawet bez naciśnięcia klawiszy żeby gra działała (do testowania)

        pygame.time.delay(50) # zwolnienie gry o 50 milisekund (im mniej tym gra szybsza)
        clock.tick(10) # wąż porusza się 10 kostek na sekundę (im mniej tym gra wolniejsza) dlatego dodatkowo delay jest ustawione

        s.move()

        if s.body[0].pos == apple.pos: # jeżeli głowa węża jest na pozycji jabłka
            s.add_cube() # powiększamy węża o jeden element
            score += 1 # dodajemy punkt
            apple = Cube(random_apple(s), color=(255, 0, 0)) # tworzymy nowe jabłko

        # wykrywamy kolizję i ją obsługujemy
        for x in range(len(s.body)): # dla każdego elementu body
            if s.body[x].pos in list(map(lambda z: z.pos, s.body[x+1:])): # sprawdza czy dany element body jest równy któremukolwiek elenetowi body
                message_box("GAME OVER", f"Zagraj ponownie\nZdobyłeś {score} punktów")
                s.reset((10, 10)) # reset węża do pozycji 10, 10
                break

        draw_window(window) # rysuje planszę

main()