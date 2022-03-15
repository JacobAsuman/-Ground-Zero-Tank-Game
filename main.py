import pygame
import time
import math
from player import player
from projectile import projectile

pygame.init()

pygame.display.set_caption("Ground Zero 2.0")
window_width = 1280
window_height = 720
p1Body = pygame.image.load(r"C:\JacobAsumanMonkeyGame\stinky monke.data\Images\TankBody2.png")
p1Barrel = pygame.image.load(r"C:\JacobAsumanMonkeyGame\stinky monke.data\Images\TankBarrel2.png")
p2Body = pygame.image.load(r"C:\JacobAsumanMonkeyGame\stinky monke.data\Images\TankBody3.png")
p2Barrel = pygame.image.load(r"C:\JacobAsumanMonkeyGame\stinky monke.data\Images\TankBarrel3.png")
black = (0, 0, 0)
white = (255, 255, 255)
blue = (0, 0, 255)
red = (255, 0, 0)
orange = (255, 69, 0)
d_orange = (255, 140, 0)
player1 = player()
player2 = player()
projectile1 = projectile()
screen = pygame.display.set_mode((window_width, window_height))
clock = pygame.time.Clock()
font_style = pygame.font.SysFont(None, 25)


def drawBody(image, image2, x, y):
    screen.blit(image, (x, y))
    screen.blit(image2, (x, y))


def drawHealth(health, x, y):
    pygame.draw.rect(screen, red, [x - 32, y - 60, health, 15])


def drawPower(x, y, width, height):
    pygame.draw.rect(screen, orange, [x, y, width, height])


def drawFuel(fuel, x, y):
    pygame.draw.rect(screen, blue, [x - 32, y - 40, fuel, 15])


def drawMarker(x, y):
    pygame.draw.rect(screen, red, [x, y, 5, 5])


def displayText(msg, colour, x, y):
    r = font_style.render(msg, True, colour)
    screen.blit(r, [x, y])


def moveProjectile(x, y, xspeed, yspeed):
    x -= xspeed
    y -= yspeed


def main():
    pygame.init()
    start = time.time()
    screen.fill(black)
    player1.x = 250
    player1.y = 588
    player2.x = 800
    player2.y = 588
    xRight1 = 0
    xLeft1 = 0
    xRight2 = 0
    xLeft2 = 0
    powerX = 850
    powerY = 640
    PwrWidth = 360
    p1Turn = True
    p2Turn = False
    markX = 300
    markY = 300
    roundCount = 1
    game_over = False
    gravity = 0
    ammo = 1
    p1Win = False
    p2Win = False

    while not game_over:
        player1.x -= xLeft1
        player1.x += xRight1
        player2.x -= xLeft2
        player2.x += xRight2
        projectiles = []

        power = (0.1 + ((PwrWidth / 16) / 12))
        p1_angle = math.atan((markY - player1.y) / (markX - player1.x))
        p2_angle = math.atan((markY - player2.y) / (markX - player2.x))

        if p1Turn and not p1Win:
            if markX > player1.x:
                projectile1.xSpeed = (math.cos(p1_angle) * 5)
                projectile1.ySpeed = (math.sin(p1_angle) * 5)
            else:
                projectile1.xSpeed = (math.cos(p1_angle) * -5)
                projectile1.ySpeed = (math.sin(p1_angle) * -5)
        elif p2Turn and not p2Win:
            if markX > player2.x:
                projectile1.xSpeed = (math.cos(p2_angle) * 5)
                projectile1.ySpeed = (math.sin(p2_angle) * 5)
            else:
                projectile1.xSpeed = (math.cos(p2_angle) * -5)
                projectile1.ySpeed = (math.sin(p2_angle) * -5)

        projectile1.magnitude = math.sqrt(
            (projectile1.xSpeed * projectile1.xSpeed) + (projectile1.ySpeed * projectile1.ySpeed))
        projectile1.xSpeed /= projectile1.magnitude
        projectile1.ySpeed /= projectile1.magnitude
        projectile1.xSpeed *= power
        projectile1.ySpeed *= power
        elapsed = round((time.time()) - start)
        if player1.health == 0:
            p1Win = True
        elif player2.health == 0:
            p2Win = True
        if elapsed > 0:
            if elapsed % 10 == 0:
                roundCount += 1
                print("Round incremented!")
                time.sleep(0.1)
                start = time.time()
            else:
                roundCount = roundCount
        if roundCount % 2 == 0:
            p2Turn = True
            p1Turn = False
        else:
            p1Turn = True
            p2Turn = False
        mouseX, mouseY = pygame.mouse.get_pos()
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                game_over = True
                break
            if event.type == pygame.MOUSEBUTTONDOWN:
                if powerX < mouseX < (powerX + 360) and 640 < mouseY < 700:
                    PwrWidth = (mouseX - 850)
                    print(PwrWidth)
                if mouseY < 640 and ammo == 1:  # can only change the aim before shooting, not during
                    markX = mouseX
                    markY = mouseY

        if p1Turn:
            if player1.fuel > 0:
                if keys[pygame.K_a] and player1.x > 0:
                    xLeft1 = 0.5
                    player1.fuel -= 0.1
                else:
                    xLeft1 = 0
                if keys[pygame.K_d] and player1.x < 1248:
                    xRight1 = 0.5
                    player1.fuel -= 0.1
                else:
                    xRight1 = 0
            else:
                xLeft1 = 0
                xRight1 = 0
            if keys[pygame.K_SPACE]:
                bomb_x = player1.x + 15
                bomb_y = player1.y - 10
                ammo = 0

        if p2Turn:
            if player2.fuel > 0:
                if keys[pygame.K_a] and player2.x > 0:
                    xLeft2 = 0.5
                    player2.fuel -= 0.1
                else:
                    xLeft2 = 0
                if keys[pygame.K_d] and player2.x < 1248:
                    xRight2 = 0.5
                    player2.fuel -= 0.1
                else:
                    xRight2 = 0
            else:
                xLeft2 = 0
                xRight2 = 0
            if keys[pygame.K_SPACE]:
                bomb_x = player2.x + 15
                bomb_y = player2.y - 10
                ammo = 0
        screen.fill(black)
        if p1Win:
            displayText("Player 1 Wins!", white, 300, 300)
        if p2Win:
            displayText("Player 2 wins!", white, 300, 300)
        if ammo == 0:
            projectiles.append(projectile1)
            pygame.draw.circle(screen, white, (bomb_x, bomb_y), 5, 5)
            gravity += 0.003
            print("gravity: " + str(gravity))
            projectile1.ySpeed += gravity
            bomb_x += projectile1.xSpeed
            bomb_y += projectile1.ySpeed

            print("bomb x speed: " + str(round(projectile1.xSpeed)))
            print("bomb y speed: " + str(round(projectile1.ySpeed)))
            print("bomb x coord: " + str(bomb_x))
            print("bomb y coord: " + str(bomb_y))
            if bomb_y >= 620:  # code executed if bomb lands at ground level
                projectiles.pop()
                ammo = 1
                gravity = 0
                roundCount += 1
                start = time.time()
                if player1.x - 20 < bomb_x < player1.x + 20:
                    player1.health -= 20
                    print("hit!")
                elif player2.x - 20 < bomb_x < player2.x + 20:
                    player2.health -= 20
                player1.fuel = 100
                player2.fuel = 100

        # print(p1_angle)
        # print(roundCount)
        if p1Turn:
            displayText("V", white, player1.x + 13, player1.y - 80)
        elif p2Turn:
            displayText("V", white, player2.x + 13, player2.y - 80)
        displayText("Round " + str(roundCount), white, 50, 50)
        displayText("Time Elapsed: " + str(elapsed), white, 50, 100)
        pygame.draw.rect(screen, white, [0, 620, 1280, 720])  # draws ground
        pygame.draw.rect(screen, d_orange, [(powerX - 13), (powerY - 11), 385, 80])  # box around the power bar
        drawPower(powerX, powerY, PwrWidth, 60)  # draws power bar
        drawMarker(markX, markY)
        drawBody(p1Body, p1Barrel, player1.x, player1.y)  # draws player 1
        drawHealth(player1.health, player1.x, player1.y)  # draws player 1's health
        drawFuel(player1.fuel, player1.x, player1.y)
        drawBody(p2Body, p2Barrel, player2.x, player2.y)  # draws player 2
        drawHealth(player2.health, player2.x, player2.y)  # draws player 2's health bar
        drawFuel(player2.fuel, player2.x, player2.y)
        pygame.display.update()

    clock.tick(30)


main()
