from PPlay.sound import Sound
from PPlay.collision import Collision
from PPlay.gameimage import *
from PPlay.sprite import Sprite
import os
from PPlay.window import Window
import random
import math

# Define a posição inicial da janela (x, y)
# os.environ['SDL_VIDEO_WINDOW_POS'] = "50,70"

janela = Window(1800, 920)
janela.set_title('Silent Eccho')
WIDTH, HEIGHT = janela.width, janela.height
teclado = Window.get_keyboard()
mouse = Window.get_mouse()
cenario = GameImage("background3.png")

#Música
musica = Sound("musicas/musicBoss.ogg")
musica.set_volume(20)
musica.stop()
musica.loop = True
musica.play()

espada = Sound("musicas/espada.ogg")

# Funções
def alternar_sprite(movendo, frente, tras):
    global estado, player, posX, posY, combate, contador, cont, correndo, rolando, esquerda

    # Correndo, andando e Parado
    if correndo == True and movendo and esquerda == False:
        playerCorrendo.set_position(posX, posY)
        player = playerCorrendo
    if correndo == True and movendo and esquerda == True:
        playerCorrendoEsquerda.set_position(posX, posY)
        player = playerCorrendoEsquerda
    elif movendo:
        if estado != "andando":
            estado = "andando"
            if frente:
                playerAndando.set_position(posX, posY)
                player = playerAndando
                esquerda = False
            elif tras:
                playerAndandoTras.set_position(posX, posY)
                player = playerAndandoTras
                esquerda = True
    else:
        if estado != "parado" and esquerda == False:
            estado = "parado"
            playerParado.set_position(posX, posY)
            player = playerParado
        elif estado != "parado" and esquerda == True:
            estado = "parado"
            playerParadoEsquerda.set_position(posX, posY)
            player = playerParadoEsquerda

    # Rolando
    if rolando == True and esquerda == False:
        posX += velocidade * janela.delta_time()
        playerRolando.set_position(posX, posY)
        player = playerRolando
        if cont > 1:
            playerParado.set_position(posX, posY)
            player = playerParado
            rolando = False
            contador = False
    if rolando == True and esquerda == True:
        posX -= velocidade * janela.delta_time()
        playerRolandoEsquerda.set_position(posX, posY)
        player = playerRolandoEsquerda
        if cont > 1:
            playerParadoEsquerda.set_position(posX, posY)
            player = playerParadoEsquerda
            rolando = False
            contador = False

    # Ataque
    if combate == True and esquerda == False:
        espada.set_volume(50)
        espada.stop()
        espada.play()
        playerAtaque.set_position(posX - 30, posY - 30)
        player = playerAtaque
        if cont > 0.7:
            playerParado.set_position(posX, posY)
            player = playerParado
            combate = False
            contador = False
    if combate == True and esquerda == True:
        espada.set_volume(50)
        espada.stop()
        espada.play()
        playerAtaqueEsquerda.set_position(posX - 30, posY - 30)
        player = playerAtaqueEsquerda
        if cont > 0.7:
            playerParadoEsquerda.set_position(posX, posY)
            player = playerParadoEsquerda
            combate = False
            contador = False

def listadeVidas(lista, col, lin):
    for i in range(lin):
        coluna = []
        for c in range(col):
            vida = Sprite("hud/vida.png", 1)
            vida.x = 80 * c
            vida.y = (vida.height + vida.height / 2) * i
            coluna.append(vida)
        lista.append(coluna)
    return lista

# Player
playerParado = Sprite("player/idle.png", 5)
playerParado.set_sequence_time(0, 4, 250)
playerParadoEsquerda = Sprite("player/IdleEsquerda.png", 5)
playerParadoEsquerda.set_sequence_time(0, 4, 250)
playerAndando = Sprite("player/Walk.png", 6)
playerAndando.set_sequence_time(0, 5, 200)
playerAndandoTras = Sprite("player/Walkback.png", 6)
playerAndandoTras.set_sequence_time(0, 5, 200)
playerAtaque = Sprite("player/attack.png", 10)
playerAtaque.set_sequence_time(0, 9, 100)
playerAtaqueEsquerda = Sprite("player/attackEsquerda.png", 10)
playerAtaqueEsquerda.set_sequence_time(0, 9, 100)
playerCorrendo = Sprite("player/Run.png", 6)
playerCorrendo.set_sequence_time(0, 5, 150)
playerCorrendoEsquerda = Sprite("player/RunEsquerda.png", 6)
playerCorrendoEsquerda.set_sequence_time(0, 5, 150)
playerRolando = Sprite("player/Roll.png", 11)
playerRolando.set_sequence_time(0, 10, 100)
playerRolandoEsquerda = Sprite("player/RollEsquerda.png", 11)
playerRolandoEsquerda.set_sequence_time(0, 10, 100)
playerWin = Sprite("player/win.png", 5)
playerWin.set_sequence_time(0, 4, 200)
playerHit = Sprite("player/hit.png", 6)
playerHit.set_sequence_time(0, 5, 80)

player = playerParado
player.set_position(100, 600)
posX = player.x
posY = player.y

# Variáveis
estado = "parado"
combate = False
contador = False
contador2 = False
rolando = False
esquerda = False
travado = False
cont2 = 0
cont = 0

# Boss
bossAndando = Sprite("boss/idle_esquerda.png", 6)  # Cria o inimigo
bossAndando.set_sequence_time(0, 5, 200)
bossAtirando = Sprite("boss/ataca_esquerda.png", 4)  # Cria o inimigo
bossAtirando.set_sequence_time(0, 3, 400)
bossDano = Sprite("boss/dano.png", 4)  # Cria o inimigo
bossDano.set_sequence_time(0, 3, 350)

boss = bossAndando
boss.set_position(1100, 150)

# TiroBoss
bolaFogo = Sprite("boss/bola_esquerda.png", 3)

bolaFogo.x = boss.x + 45
bolaFogo.y = boss.y + 30

atiraInimigo = False
velTiroInimigo = -600
contagemTiros = 0
recarga = 0
danoInimigo = 0
tempo = 10

# Hud
listaVida = []
linha = 1
colunas = 5
n = 4

vidaCheia = Sprite("hud/100porcento.png", 1)
vidaMeioCheia = Sprite("hud/75porcento.png", 1)
vidaMetade = Sprite("hud/50porcento.png", 1)
vidaMeioVazia = Sprite("hud/25porcento.png", 1)

vidaBoss = vidaCheia
vidaBoss.set_position(1300, 50)

moeda = Sprite("boss/Coin.png", 5)
moeda.set_sequence_time(0, 4, 150)

moeda.set_position(1300, 600)

while True:
    janela.update()

    if danoInimigo >= 75:
        tempo = 6
        vidaBoss = vidaMeioCheia
    if danoInimigo >= 150:
        tempo = 4
        vidaBoss = vidaMetade
    if danoInimigo >= 225:
        tempo = 2
        vidaBoss = vidaMeioVazia

    if not travado:
        movendoFrente = teclado.key_pressed("right") or teclado.key_pressed("d") or teclado.key_pressed(
            "up") or teclado.key_pressed("w") or teclado.key_pressed("down") or teclado.key_pressed("s")
        movendoTras = teclado.key_pressed("left") or teclado.key_pressed("a")
        movendo = movendoTras or movendoFrente

        # Movimentação-Player e Câmera
        if movendo:
            if teclado.key_pressed("d") or teclado.key_pressed("right"):
                posX += velocidade * janela.delta_time()
                playerAndando.set_position(posX, posY)
            if teclado.key_pressed("a") or teclado.key_pressed("left"):
                posX -= velocidade * janela.delta_time()
                playerAndandoTras.set_position(posX, posY)
            if teclado.key_pressed("w") or teclado.key_pressed("up"):
                posY -= velocidade * janela.delta_time()
                playerAndando.set_position(posX, posY)
            if teclado.key_pressed("s") or teclado.key_pressed("down"):
                posY += velocidade * janela.delta_time()
                playerAndando.set_position(posX, posY)

        if teclado.key_pressed("space"):
            contador = True
            rolando = True

        if teclado.key_pressed("left_shift"):
            velocidade = 500
            correndo = True
        else:
            velocidade = 250
            correndo = False

        # Ataque e Dano
        if mouse.is_button_pressed(1):
            playerAtaque.set_position(posX - 100, posY - 100)
            contador = True
            combate = True
            # Verifica colisão e alterna o sprite para dano
            if combate and Collision.collided(player, boss):
                boss = bossDano
                boss.set_position(1100, 150)
                danoInimigo += 1

    # Contador 1 e 2
    if contador == True:
        cont += janela.delta_time()
    elif contador == False:
        cont = 0
    if contador2 == True:
        cont2 += janela.delta_time()
    elif contador2 == False:
        cont2 = 0

    alternar_sprite(movendo, movendoFrente, movendoTras)

    cenario.draw()

    player.update()
    player.draw()

    boss.update()
    boss.draw()

    vidaBoss.draw()

    if listaVida == []:
        listaVida = listadeVidas(listaVida, colunas, linha)

    if listaVida != []:
        for linha in listaVida:
            for colunas in linha:
                colunas.draw()

    # Tiro Inimigo
    tiroInimigo = 1
    altura = random.randint(250, 550)

    if contagemTiros < 1430:
        if 0 <= danoInimigo <= 200:
            if tiroInimigo == 1 and atiraInimigo == False:
                atiraInimigo = True
                bolaFogo.x = boss.x - 45
                bolaFogo.y = boss.y + altura
            if atiraInimigo == True:
                vidaBoss.set_position(1300, 50)
                boss = bossAtirando
                boss.set_position(1100, 150)
                bolaFogo.x += velTiroInimigo * janela.delta_time()
                bolaFogo.draw()
                contagemTiros += 1
            if bolaFogo.x < 0:
                atiraInimigo = False
        elif 200 <= danoInimigo <= 300:
            if tiroInimigo == 1 and atiraInimigo == False:
                atiraInimigo = True
                bolaFogo.x = boss.x - 45
                bolaFogo.y = boss.y + altura
            if atiraInimigo == True:
                boss = bossAtirando
                boss.set_position(1100, 150)
                bolaFogo.x += velTiroInimigo * janela.delta_time()
                bolaFogo.draw()
                contagemTiros += 1
            if bolaFogo.x < 0:
                atiraInimigo = False
    else:
        atiraInimigo = False
        vidaBoss.set_position(1250, 80)

    # Recarga
    if contagemTiros == 1430:
        recarga += janela.delta_time()
        boss = bossAndando
        boss.set_position(1100, 150)
        if recarga > tempo:
            contagemTiros = 0
            recarga = 0

    # Colisão do Fogo
    if Collision.collided(player, bolaFogo) and atiraInimigo == True:
        player = playerHit
        playerHit.set_position(posX, posY)
        travado = True
        contador2 = True
        posX -= 1
        atiraInimigo = False
        # Remover apenas um coração
        for i in range(len(listaVida) - 1, -1, -1):  # Percorre as colunas de trás para frente
            if listaVida[i]:  # Verifica se a coluna tem corações
                listaVida[i].pop(n)  # Remove o primeiro coração da coluna
                n -= 1

    if cont2 > 0.5:
        travado = False
        player = playerParado
        playerParado.set_position(posX, posY)
        contador2 = False

    if n < 0:
        break

        # Colisão

    if player.y < 460:
        posY = posY + 3
    if player.y > (janela.height - 80):
        posY = posY - 3
    if player.x < -5:
        posX = posX + 2
    if danoInimigo < 300:
        if player.x > boss.x + 20:
            posX = posX - 2
    elif danoInimigo >= 300:
        boss.hide()
        vidaBoss.hide()
        moeda.draw()
        moeda.update()
        if Collision.collided(player, moeda):
            moeda.hide()
            player = playerWin
            playerWin.set_position(posX, posY)
            travado = True
            janela.draw_text("Você conseguiu meu pequeno gafanhoto!!", 380, 300, size=50, color="white", font_name="Comic Sans MS", bold=False,
                             italic=True)
            janela.draw_text("Agora Khan conseguiu voltar para o seu mundo e viver tranquilamente!!", 100, 400, size=50, color="white", font_name="Comic Sans MS", bold=False, italic=True)