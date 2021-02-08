import pygame
import os
import sys
import serial
from threading import Thread

class Ser(Thread): # Creates a thread to read the input of the joysticks in parallel
    def __init__(self):
        Thread.__init__(self)
        self.x = 539
        self.y = 494
        self.read = 1

    def run(self): # Cleans the input
        def clean(L):
            newL = []
            for i in range(len(L)):
                temp = L[i][2:]
                newL.append(temp[:len(L) - 6])
            return "".join(newL)

        try:
            arduino = serial.Serial('COM3', timeout=1)
        except:
            print('Vérifier le port série utilisé')

        while self.read:
            axe = [str(arduino.readline())]
            coords = list(map(int, clean(axe).split()))

            self.x = coords[0]
            self.y = 1023 - coords[1]


class Hitbox:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Player:
    def __init__(self, x=100, y=700, width=8, height=8, vel=8, number=1, lives=3):  #Vel = width or the display will bug
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = vel
        self.lives = lives
        if number == 1:
            self.hitbox = Hitbox(x + 16, y - 8)
            self.direction = "right"
            self.image = pygame.image.load("images/blue_motorcycle.png")
            self.cur_image = pygame.transform.rotate(self.image, 90)
            self.color = (9, 150, 238)
        else:
            self.hitbox = Hitbox(x - 32, y - 8)
            self.direction = "left"
            self.image = pygame.image.load("images/yellow_motorcycle.png")
            self.cur_image = pygame.transform.rotate(self.image, -90)
            self.color = (253, 204, 28)

        self.number = number

    def deplacement(self):
        keys = pygame.key.get_pressed()
        if self.number == 1: #J1
            if joysticks:
                x, y = thread.x, thread.y  # X and Y of the joystick
                if (not 450 < x < 550) or (not 450 < y < 550):
                    if not self.direction == "right":
                        if x < y < 1023 - x:
                            self.direction = "left"

                    if not self.direction == "left":
                        if 1023 - x < y < x:
                            self.direction = "right"

                    if not self.direction == "down":
                        if y > x and y > 1023 - x:
                            self.direction = "up"

                    if not self.direction == "up":
                        if y < 1023 - x and y < x:
                            self.direction = "down"

            else: # Moving with the arrows
                if not self.direction == "right":
                    if keys[pygame.K_LEFT]:
                        self.direction = "left"

                if not self.direction == "left":
                    if keys[pygame.K_RIGHT]:
                        self.direction = "right"

                if not self.direction == "down":
                    if keys[pygame.K_UP]:
                        self.direction = "up"

                if not self.direction == "up":
                    if keys[pygame.K_DOWN]:
                        self.direction = "down"

        else: #J2
            if not self.direction == "right":
                if keys[pygame.K_q]:
                    self.direction = "left"

            if not self.direction == "left":
                if keys[pygame.K_d]:
                    self.direction = "right"

            if not self.direction == "down":
                if keys[pygame.K_z]:
                    self.direction = "up"

            if not self.direction == "up":
                if keys[pygame.K_s]:
                    self.direction = "down"

        pygame.draw.rect(arena, (20, 20, 20),
                         (self.hitbox.x, self.hitbox.y, 32, 32))  # Supprime le carré d'avant

        pygame.draw.rect(arena, self.color, (self.x, self.y, self.width, self.height))

        # Lights:
        # multiplier = 1.5
        # if self.direction == "right" or self.direction == "left":
        #     for j in range(5):
        #         surf = pygame.Surface((self.width, self.height * multiplier))
        #         pygame.draw.rect(surf, (5, 5, 5), (0, 0, self.width, self.height * multiplier))
        #         surf.set_colorkey((0, 0, 0))
        #
        #         screen.blit(surf, (self.x, (self.y + (self.height - self.height * multiplier) // 2)),
        #                     special_flags=pygame.BLEND_RGB_ADD)
        #         multiplier += 0.05
        # else:
        #     for j in range(5):
        #         surf = pygame.Surface((self.width* multiplier, self.height ))
        #         pygame.draw.rect(surf, (5, 5, 5), (0, 0, self.width * multiplier, self.height))
        #         surf.set_colorkey((0, 0, 0))
        #
        #         screen.blit(surf, (self.x + (self.height - self.height * multiplier) // 2, self.y),
        #                     special_flags=pygame.BLEND_RGB_ADD)
        #         multiplier += 0.05

        if self.direction == "left":
            self.x -= self.vel

            self.cur_image = pygame.transform.rotate(self.image, -90)
            self.hitbox.x = self.x + self.width - 32
            self.hitbox.y = self.y - ((32 - self.height) // 2)

        if self.direction == "right":
            self.x += self.vel

            self.cur_image = pygame.transform.rotate(self.image, 90)
            self.hitbox.x = self.x
            self.hitbox.y = self.y - ((32 - self.height) // 2)

        if self.direction == "up":
            self.y -= self.vel

            self.cur_image = pygame.transform.rotate(self.image, 180)
            self.hitbox.x = self.x - ((32 - self.width) // 2)
            self.hitbox.y = self.y + self.height - 32

        if self.direction == "down":
            self.y += self.vel

            self.cur_image = pygame.transform.rotate(self.image, -180)
            self.hitbox.x = self.x - ((32 - self.width) // 2)
            self.hitbox.y = self.y

    def border(self):
        self.x %= w_arena
        self.y %= h_arena

    def draw(self):
        arena.blit(self.cur_image, (self.hitbox.x, self.hitbox.y))


def colliders(direction, x, y, width, height):  # Return a list of coliders with lines
    if direction == "right":
        x += 1  # Because we don't want the collider to be on the sprite
        return [(x + 31, y)] + [(x + 31, y + i) for i in range(7, 32, height)] + [(x+16, y-1), (x+16, y+32)]
    if direction == "left":
        x -= 1  # Because we don't want the collider to be on the sprite
        return [(x, y)] + [(x, y + i) for i in range(7, 32, height)] + [(x+16, y-1), (x+16, y+32)]
    if direction == "up":
        y -= 1  # Because we don't want the collider to be on the sprite
        return [(x, y)] + [(x + i, y) for i in range(7, 32, width)] + [(x-1, y+16), (x+32, y+16)]
    if direction == "down":
        y += 1  # Because we don't want the collider to be on the sprite
        return [(x, y + 31)] + [(x + i, y + 31) for i in range(7, 32, width)] + [(x-1, y+16), (x+32, y+16)]


def menu(screen):
    global joysticks
    global thread

    inmenu = True
    fullscreen = False
    background = pygame.image.load('images/titre_final_{}.jpg'.format(screen_type))
    boup = pygame.mixer.Sound("sounds/boup.wav")
    start_button = pygame.Rect(int(812 / 1920 * w_screen), int(698 / 1080 * h_screen), int(295 / 1920 * w_screen),
                           int(95 / 1080 * h_screen))

    joystick_button = pygame.Rect(int(1824 / 1920 * w_screen), int(30 / 1080 * h_screen), int(64 / 1920 * w_screen),
                                  int(64 / 1080 * h_screen))

    while inmenu:
        click = False
        for event in pygame.event.get():  # To have the full screen ans close it and catch events
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
            if event.type == pygame.VIDEORESIZE:
                if not fullscreen:
                    screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    fullscreen = not fullscreen
                    if fullscreen:
                        screen = pygame.display.set_mode((screen.get_width(), screen.get_height()), pygame.FULLSCREEN)
                    else:
                        screen = pygame.display.set_mode((w_screen,  h_screen-10), pygame.RESIZABLE)
                    pygame.time.delay(100)

        mx, my = pygame.mouse.get_pos()  # We're getting mx and my

        if start_button.collidepoint((mx, my)):
            if click:
                boup.play()

                inmenu = False

                if joysticks:

                    thread = Ser()
                    thread.start()

                game(screen, fullscreen)

        if joystick_button.collidepoint((mx, my)):
            if click:
                boup.play()

                joysticks = not joysticks

        if joysticks:
            joystick_image = pygame.image.load("images/joysticks_reflets.png")
        else:
            joystick_image = pygame.image.load("images/joysticks_reflets_barre.png")

        screen.blit(background, (0, 0))
        screen.blit(joystick_image, (joystick_button.left, joystick_button.top))

        pygame.display.flip()


def end(looser):
    if joysticks:
        thread.read = False

    if looser == 1:
        p = 2
    else:
        p = 1

    sound = pygame.mixer.Sound("sounds/explosion_1.mp3")

    image = pygame.image.load("images/player_{}_wins_{}.png".format(p, screen_type))
    screen.blit(image, (0, 0))
    pygame.display.update()
    pygame.time.delay(500)

    for f in range(1, 9):
        image = pygame.image.load("images/wins_animation_{}/p{}_win_{}.jpg".format(screen_type, p, f))
        screen.blit(image, (0, 0))
        pygame.display.update()
        pygame.time.delay(150)
        if f == 9:
            pygame.time.delay(300)

        if f == 4:
            sound.play()

    image = pygame.image.load("images/player_{}_wins_{}.png".format(p, screen_type))
    screen.blit(image, (0, 0))
    pygame.display.update()
    pygame.time.delay(2000)

    if play_again:
        menu(screen)


def showLives(screen, players, g, g_x, d_x, f_y):
    # w_frame, h_frame = g.get_width(), g.get_height()

    empty_heart = pygame.image.load("images/coeur_vide.png")
    for player in players:
        if player.number == 1:
            full_heart = pygame.image.load("images/coeur_bleu.png")
            x = g_x + 23
        else:
            full_heart = pygame.image.load("images/coeur_jaune.png")
            x = d_x + 23
        y = f_y + 29

        for i in range(3):
            if player.lives - i > 0:
                screen.blit(full_heart, (x + 64 * i, y))
            else:
                pygame.draw.rect(screen, (36, 36, 36), (x + 64 * i, y, 64, 64)) #Fais un carré pour cacher le keur perdu
                screen.blit(empty_heart, (x + 64 * i, y))


def game(screen, fullscreen = 0):
    player_1 = Player(number=1)
    player_2 = Player(x=1800, y=200, number=2)

    colors = [(9, 150, 238, 255), (253, 204, 28, 255)]

    explosion_sound = pygame.mixer.Sound("sounds/explosion_2.mp3")

    screen.fill((0, 0, 0))

    while min(player_1.lives, player_2.lives):
        play = 1
        arena.fill((20, 20, 20))  # Is creating the arena

        player_1 = Player(number=1, lives=player_1.lives)
        player_2 = Player(x=980, y=200, number=2, lives=player_2.lives)

        players = [player_1, player_2]

        while play:
            for event in pygame.event.get():  # To leave the game with the arrows
                if event.type == pygame.QUIT:
                    play = False
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.type == pygame.VIDEORESIZE:
                        if not fullscreen:
                            screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                    if event.key == pygame.K_f:
                        fullscreen = not fullscreen
                        if fullscreen:
                            screen = pygame.display.set_mode((screen.get_width(), screen.get_height()),
                                                             pygame.FULLSCREEN)
                        else:
                            screen = pygame.display.set_mode((w_screen,  h_screen-10),
                                                             pygame.RESIZABLE)


            # Makes the grey color of the bg
            pygame.draw.rect(screen, (5, 5, 5), (0, 0, w_screen, h_screen))

            # Shows the different lives on each side of the arena and their
            w = 240

            g = pygame.image.load("images/cadre_gauche.png")
            d = pygame.image.load("images/cadre_droit.png")
            g_x = (w_screen - w_arena - 2*w)//4
            d_x = (3*w_screen + w_arena - 2*w)//4
            f_y = 60

            screen.blit(g, (g_x, f_y))
            screen.blit(d, (d_x, f_y))
            showLives(screen, players, g, g_x, d_x, f_y)

            screen.blit(arena,
                        ((w_screen - w_arena) // 2, (h_screen - h_arena) // 2))  # Affiche l'arène au milieu de l'écran


            player_1.deplacement() # Makes the motorcycle move and delete the old rectangle from the previous location
            player_2.deplacement()

            player_1.border()  # Makes the motorcycle pass on the other side if needed
            player_2.border()

            player_1.draw()
            player_2.draw()


            # Collisions made by a line of colliders in front of the motorcycle and on the side
            for player in players:
                for collider in colliders(player.direction, player.hitbox.x, player.hitbox.y, player.width,
                                          player.height):

                    x = collider[0]
                    y = collider[1]
                    # pygame.draw.rect(arena, (255,0,0), (x, y, 1, 1)) #To make appear the colliders
                    for color in colors:
                        if arena.get_at((x % w_arena, y % h_arena)) == color: #If the player has touched a line
                            explosion_sound.play()

                            player.lives -= 1
                            play = False
                            if player.lives == 0:
                                looser = player.number
                                end(looser)
                            break
                    if not play: # Need improvement (do not spam break)
                        break
                if not play:
                    break

            pygame.display.update()
            pygame.time.delay(speed)  # The time of actualization/ the speed


pygame.init()

# Initialize the screen
w_screen, h_screen = pygame.display.Info().current_w, pygame.display.Info().current_h

if w_screen == 1920:
    screen_type = "1920"
elif w_screen == 1600:
    screen_type = "1600"

screen = pygame.display.set_mode((w_screen, h_screen), pygame.RESIZABLE)


# Initialize important variables
if screen_type == "1600":
    speed = 30 #the delay of actualization
else:
    speed = 25
joysticks = False
play_again = 1
thread = None

# Initialize and play the music
music = pygame.mixer.music.load("sounds/JOJO.mp3")
pygame.mixer.music.set_volume(0.4)
pygame.mixer.music.play(-1)

# Initialize the logo and title
pygame.display.set_caption("Tron: the ultimate video game of the death.")
icon = pygame.image.load("images/blue_motorcycle.png")
pygame.display.set_icon(icon)

# Initialize the arena which is as square of h_screen*h_screen
w_arena, h_arena = h_screen, h_screen
arena = pygame.Surface((w_arena, h_arena))

menu(screen)