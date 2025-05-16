from os import remove

from PPlay.sound import Sound
import subprocess
from PPlay.collision import Collision
from PPlay.gameimage import *
from PPlay.sprite import Sprite
import os
from PPlay.window import Window
import random
import math

janela = Window(1800, 920)
janela.set_title('Silent Eccho')
WIDTH, HEIGHT = janela.width, janela.height
teclado = Window.get_keyboard()
mouse = Window.get_mouse()
cenario = GameImage("background1.png")

#Música
musica = Sound("musicas/music2.ogg.ogg")
musica.set_volume(20)
musica.stop()
musica.loop = True
musica.play()

espada = Sound("musicas/espada.ogg")

class Inimigo:
    def __init__(self, x, y):
        # Atributos gerais
        self.vida = 50
        self.estado = "andando"  # Pode ser "andando", "dano", "atacando", etc.

        # Sprites do inimigo
        self.sprite_andando = Sprite("monstros2/correr_esquerda.png", 8)
        self.sprite_andando.set_sequence_time(0, 7, 150)

        self.sprite_dano = Sprite("monstros2/takehit_esquerda.png", 3)
        self.sprite_dano.set_sequence_time(0, 2, 150)

        self.sprite_atacando = Sprite("monstros2/ataque_esquerda.png", 6)
        self.sprite_atacando.set_sequence_time(0, 5, 150)

        # Sprite ativo inicial
        self.sprite = self.sprite_andando
        self.sprite.set_position(x, y)

    def set_position(self, x, y):
        """Atualiza a posição de todos os sprites, mantendo a posição sincronizada."""
        self.sprite_andando.set_position(x, y)
        self.sprite_dano.set_position(x, y)
        self.sprite_atacando.set_position(x, y)
        self.sprite = self.sprite_andando  # Redefine o sprite inicial como "andando"

    def update(self):
        self.sprite.update()

    def draw(self):
        self.sprite.draw()

    def trocar_estado(self, novo_estado):
        """Troca o estado do inimigo e mantém a posição do sprite atual."""
        x, y = self.sprite.x, self.sprite.y  # Captura a posição atual do sprite
        if novo_estado == "dano":
            self.sprite = self.sprite_dano
        elif novo_estado == "andando":
            self.sprite = self.sprite_andando
        elif novo_estado == "atacando":
            self.sprite = self.sprite_atacando

        self.sprite.set_position(x, y)  # Garante que a posição seja preservada
        self.sprite.set_curr_frame(0)  # Reinicia a animação no novo estado
        self.estado = novo_estado

# Funções
def alternar_sprite(movendo, frente, tras):
    global estado, player, posX, posY, combate, contador, cont, correndo, rolando, esquerda

    #Correndo, andando e Parado
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

    #Rolando
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

    #Ataque
    if combate == True and esquerda == False:
        espada.set_volume(50)
        espada.stop()
        espada.play()
        playerAtaque.set_position(posX-30, posY-30)
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
        playerAtaqueEsquerda.set_position(posX-30, posY-30)
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
player.set_position(100, 500)
posX = player.x
posY = player.y

# Variáveis
estado = "parado"
combate = False
contador = False
contador2 = False
contador3 = False
contador4 = False
rolando = False
esquerda = False
travado = False
ataque = False
cont = 0
cont2 = 0
cont3 = 0
cont4 = 0
wave = 1

dano = 0
inimigos = []
flechas_inimigos = []
tempo_spawn = 0
quant = 0
quantidade = random.randint(3, 5)
velocidade = 150
velmonstro = 100

# Hud
listaVida = []
linha = 1
colunas = 5
n = 4

# Monstros
atiraInimigo = False
tiro = 0

moeda = Sprite("boss/Coin.png", 5)
moeda.set_sequence_time(0, 4, 150)

moeda.set_position(1300, 600)

# Crie uma imagem preta para a transição
transicao = GameImage("transicao.png")
transicao_opacidade = 0  # Opacidade inicial
transicao_ativa = False
tempo_transicao = 0
duracao_transicao = 2  # Tempo da transição em segundos

while True:
    janela.update()

    movendoFrente = teclado.key_pressed("right") or teclado.key_pressed("d") or teclado.key_pressed("up") or teclado.key_pressed("w") or teclado.key_pressed("down") or teclado.key_pressed("s")
    movendoTras = teclado.key_pressed("left") or teclado.key_pressed("a")
    movendo = movendoTras or movendoFrente

    # Movimentação-Player e Câmera
    if not travado:
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
            velocidade = 300
            correndo = True
        else:
            velocidade = 150
            correndo = False

    # Ataque e Dano
    if mouse.is_button_pressed(1):
        playerAtaque.set_position(posX - 100, posY - 100)
        contador = True
        combate = True

    # Colisão
    if player.y < 400:
        posY = posY + 1
    if player.y > (janela.height - 80):
        posY = posY - 1
    if player.x < 0:
        posX = posX + 1


    # Contador
    if contador == True:
        cont += janela.delta_time()
    elif contador == False:
        cont = 0
    if contador2 == True:
        cont2 += janela.delta_time()
    elif contador2 == False:
        cont2 = 0
    if contador3 == True:
        cont3 += janela.delta_time()
    elif contador3 == False:
        cont3 = 0
    if contador4 == True:
        cont4 += janela.delta_time()
    elif contador4 == False:
        cont4 = 0

    alternar_sprite(movendo, movendoFrente, movendoTras)

    # Atualize o tempo de spawn
    tempo_spawn += janela.delta_time()

    cenario.draw()

    player.update()
    player.draw()

    """janela.draw_text(str(n), 150, 150, size=30, color="white", font_name="Comic Sans MS", bold=False, italic=True)
    janela.draw_text(str(tempo_spawn), 150, 100, size=30, color="white", font_name="Comic Sans MS", bold=False,italic=True)"""

    if listaVida == []:
        listaVida = listadeVidas(listaVida, colunas, linha)

    if listaVida != []:
        for linha in listaVida:
            for colunas in linha:
                colunas.draw()

    # Condição para gerar um inimigo a cada 2 segundos
    if tempo_spawn >= 2:
        if quant < quantidade:
            tempo_spawn = 0
            x = janela.width + 50
            y = random.randint(500, 700)
            inimigo = Inimigo(x, y)  # Cria um inimigo com posição inicial
            inimigos.append(inimigo)
        quant += 1

    # Atualize a posição dos inimigos
    inimigos_a_remover = []  # Lista para armazenar inimigos que serão removidos

    for inimigo in inimigos:
        if inimigo.vida <= 0:
            inimigos_a_remover.append(inimigo)
            continue

        # Movimentação do inimigo
        dx = player.x - inimigo.sprite.x
        dy = player.y - inimigo.sprite.y
        distancia = math.sqrt(dx ** 2 + dy ** 2)
        if distancia > 500:
            dx /= distancia
            dy /= distancia
            novo_x = inimigo.sprite.x + dx * velmonstro * janela.delta_time()
            novo_y = inimigo.sprite.y + dy * velmonstro * janela.delta_time()
            inimigo.set_position(novo_x, novo_y)  # Atualiza posição sincronizada
            inimigo.trocar_estado("andando")
        else:
            inimigo.trocar_estado("atacando")
            # Atira flecha com chance aleatória
            if random.random() < 0.01:# 10% de chance de atirar a cada iteração
                if tiro < 5:
                    nova_flecha = Sprite("monstros2/flecha_esquerda.png", 2)  # Crie o sprite da flecha
                    nova_flecha.set_sequence_time(0, 1, 100)
                    nova_flecha.set_position(inimigo.sprite.x, inimigo.sprite.y)
                    vel_flecha = 300  # Velocidade da flecha
                    tiro += 1
                    flechas_inimigos.append({
                        "flecha": nova_flecha,
                        "dx": dx / distancia * vel_flecha,
                        "dy": dy / distancia * vel_flecha,
                    })
                else:
                    contador3 = True
                    if cont3 > 4:
                        tiro = 0
                        contador3 = False

        # Processar dano ao inimigo
        if combate and cont > 0.5 and Collision.collided(player, inimigo.sprite) and inimigo.sprite.x - player.x < 20:
            inimigo.vida -= 1
            inimigo.trocar_estado("dano")

        # Voltar ao estado "andando" após um tempo
        if cont2 > 2:
            inimigo.trocar_estado("andando")

        inimigo.update()
        inimigo.draw()

    # Atualiza as flechas inimigas
    for dados_flecha in flechas_inimigos[:]:
        flecha = dados_flecha["flecha"]
        flecha.x -= vel_flecha * janela.delta_time()
        flecha.y += dados_flecha["dy"] * janela.delta_time()
        flecha.draw()

        # Remove flechas que saíram da tela
        if flecha.x < 0 or flecha.x > janela.width or flecha.y < 0 or flecha.y > janela.height:
            flechas_inimigos.remove(dados_flecha)

        # Colisão da flecha com o jogador
        if Collision.collided(player, flecha):
            for i in range(len(listaVida) - 1, -1, -1):  # Remove o coração
                if listaVida[i]:
                    listaVida[i].pop()
                    n -= 1
                    break
            flechas_inimigos.remove(dados_flecha)  # Remove a flecha que acertou o jogador

    if n < 0:
        travado = True
        transicao_ativa = True  # Ativa a transição
        tempo_transicao = 0  # Reseta o tempo da transição
        transicao_opacidade = 0
        contador3 = False

    # Remove os inimigos marcados para remoção
    for inimigo in inimigos_a_remover:
        inimigos.remove(inimigo)

    if (inimigos == []) and quant >= quantidade:
        if wave <= 2:
            quant = 0
        wave += 1

    if wave > 3 and inimigos == []:
        moeda.draw()
        moeda.update()
        if Collision.collided(player, moeda):
            moeda.hide()
            player = playerWin
            playerWin.set_position(posX, posY)
            travado = True
            transicao_ativa = True  # Ativa a transição
            tempo_transicao = 0  # Reseta o tempo da transição
            transicao_opacidade = 0
            contador = False

    # Lógica da transição
    if transicao_ativa:
        tempo_transicao += janela.delta_time()
        transicao_opacidade = min(255, int((tempo_transicao / duracao_transicao) * 255))  # Calcula a opacidade
        # Define a opacidade da imagem de transição
        transicao.set_alpha(transicao_opacidade)
        transicao.draw()
        if n >= 0:
            contador = True
        else:
            contador4 = True
            janela.draw_text("Você Morreu!", 450, 300, size=140, color="white", font_name="Comic Sans MS", bold=False, italic=True)
            janela.draw_text("Tente Novamente em alguns segundos!", 200, 480, size=80, color="white", font_name="Comic Sans MS", bold=False, italic=True)

        # Quando a transição terminar
        if transicao_ativa and cont >= 3:
            subprocess.run(["python", "faseFinal.py"])
            break  # Sai do loop da fase atual
        elif transicao_ativa and cont4 >= 3:
            subprocess.run(["python", "fase2.py"])
            break