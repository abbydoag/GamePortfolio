import pygame
from pygame import mixer #audio
import random
import sys

pygame.init()

#pantalla y sonido fondo
width = 600
height = 500
screen = pygame.display.set_mode((width, height))
background = pygame.image.load('./Assets/Background.png')
mixer.music.load('./Assets/Background-OST.mp3')
mixer.music.play(-1) #en loop

#Titulo e Icono en barra)?
pygame.display.set_caption(' Rebel Base Defender')
icon = pygame.image.load('./Assets/Logo.png')
pygame.display.set_icon(icon)

#JUgador
playerImg = pygame.image.load('./Assets/MilleniumFalcon.png')
#posicion en eje X y eje Y (inicial) y cambios en X
playerX = width//2 -playerImg.get_width()//2
playerY = height - playerImg.get_height()-10
playerX_change = 0
#Enemigos
enemyImg = pygame.image.load('./Assets/TIE.png')
enemyNum = 3
enemyImgs = [enemyImg]* enemyNum
enemyX = [random.randint(20, width-enemyImg.get_width()-20) for _ in range(enemyNum)]
enemyY = [random.randint(0, 0) for _ in range(enemyNum)]
enemyY_change = [1]*enemyNum
explosionImg = pygame.image.load('./Assets/boom.png')
#explosion_sound = mixer.Sound('./Assets/Explosion.mp3')
isExploding = False
explosionX = 0
explosionY = 0
#Ataque jugador
attackImg = pygame.image.load('./Assets/Laser-shot.png')
attack_sound = mixer.Sound('./Assets/Blaster-Shot.mp3')
attackX = 0
attackY = playerY
attackX_change = 0
attackY_change = 22
attack_state = "ready"  #ready = listo para disparar, fire = disparando (en mvoimiento)

#score and texts
current_score = 0
font = pygame.font.Font('8-bit-pusab.ttf', 10) #font para pygame, tamaño
textX = 470
textY = 15
pause_font = pygame.font.Font('8-bit-pusab.ttf', 15)
gameOver_font = pygame.font.Font('8-bit-pusab.ttf', 20)
pause_text = pause_font.render("PAUSED", True, (255,255,255))

#"Dibujo"
def game_score(x, y):                               #que salga   #color
    score = font.render("Score: "+str(current_score), True, (255,255,255))
    screen.blit(score, (x, y))
def player(x, y):
    #Ahora puede manipularse la posición en X y Y
    screen.blit(playerImg, (x, y))
def enemy(x,y, i):
    screen.blit(enemyImgs[i], (x, y))
def fire_attack(x, y):
    global attack_state
    #estado para disparar
    attack_state = "fire"
    screen.blit(attackImg, (x, y+10)) #para que no se vea raro el disparo
    
def isColliding(enemyX, enemyY, attackX, attackY):
        collision_rad = 27
        #enemigo-ataque
        distanceX = enemyX-attackX
        distanceY = enemyY-attackY
        distance = (distanceX**2 + distanceY**2)**0.5
        return distance <= collision_rad
def game_over():
    over_text = gameOver_font.render("Game Over", True, (255,255,255))
    screen.blit(over_text, (200,240))
#GAME LOOP (todo lo que pasa en la pantalla del juego se pone dentro de este loop)
running = True
paused = False
while running: 
    screen.blit(background, (0,0))   
    #Mantener ventana abierta y poder cerrarla
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    #controles (if keystroke is pressed check for right or left y disparos)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                #cambio (izq)
                playerX_change = -3.4
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                #cambio (der)
                playerX_change = 3.4
            elif event.key == pygame.K_UP or event.key == pygame.K_w:
                #varios disparos
                if attack_state == "ready":
                    #guarda la posicion actual de la nave, asi si nos movemos no el movimiento de la nave
                    attack_sound.play()
                    attackX = playerX
                    fire_attack(attackX, attackY)
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                paused = not paused
                if paused:
                    mixer.music.pause()
                else:
                    mixer.music.unpause()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key ==pygame.K_a or event.key == pygame.K_d:
                playerX_change = 0 
    if not paused:
        #cambio en posicion
        playerX += playerX_change
        #player boundaries
        if playerX <= 15:
            playerX = 15
        elif playerX >= 488:
            playerX = 488
        #mov enemigo (orden de cada uno)
        for i in range(enemyNum):
            #Game over
            if enemyY[i] > playerY:
                for j in range(enemyNum):
                    enemyY[j] = 2000
                game_over()
                break
            enemyY[i] += enemyY_change[i]
            #impacto y respawn enemigo
            impact = isColliding(enemyX[i], enemyY[i], attackX, attackY)
            if impact:
                #explosion_sound.play()
                attackY = playerY
                attack_state = "ready"
                explosionX = enemyX[i]
                explosionY = enemyY[i]
                enemyX[i] = random.randint(20,480)
                enemyY[i] = random.randint(0,0)
                isExploding = True
                explosion_time = 3
                current_score += 1
                break
            enemy(enemyX[i],enemyY[i], i)
        if isExploding:
            screen.blit(explosionImg, (explosionX, explosionY))
            explosion_time -= 1
            if explosion_time == 0:
                isExploding = False
        #ataque "recarga" y movimiento
        if attackY <= 0:
            attackY = playerY
            attack_state = "ready"
        if attack_state == "fire":
            fire_attack(attackX, attackY)
            attackY -= attackY_change
    else:
        screen.blit(pause_text, (240,250))
    #llamando al jugador (va despues del color o lo que modifica el fondo, si no lo taparía)
    player(playerX,playerY)
    game_score(textX, textY)

    pygame.display.update()
#liberando recursos
pygame.quit()
sys.exit()