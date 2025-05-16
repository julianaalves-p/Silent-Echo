from pydoc import importfile
import subprocess
from PPlay.sound import Sound
from PPlay.sprite import Sprite
from PPlay.window import *
from PPlay.gameimage import *

#Janela
x = 1280
y = 900
janela = Window(x,y)
janela.set_title('Silent Eccho')

# Música
musica = Sound("musicas/musicMenu.ogg")
musica.set_volume(30)
musica.loop = True
musica.play()

# Fundo
fundo = GameImage("imagens/fundoMenu.jpg")

# Logo, Marca e Caveirinha
logo = GameImage("imagens/LogoJogo.png")
logo.x = 360
logo.y = 50
marca = GameImage("imagens/LogoMarca.png")
marca.x = 1100
marca.y = 770
caveirinhas = Sprite("imagens/caveirinhas.png")

# Botões
iniciarJogo = GameImage("imagens/Iniciar.png")

sair = GameImage("imagens/Sair.png")

sair.x = iniciarJogo.x = 470
iniciarJogo.y = 560

sair.y = 650
caveirinhas.x = 0
caveirinhas.y = 0

#Teclado
keyboard = Window.get_keyboard()
mouse = Window.get_mouse()

while True:
    janela.set_background_color('Black')

    musica.play()

    if mouse.is_over_object(iniciarJogo):
        caveirinhas.x = iniciarJogo.x - 75
        caveirinhas.y = iniciarJogo.y
        caveirinhas.unhide()
        if mouse.is_button_pressed(1):
            musica.stop()
            subprocess.run(["python", "fase1.py"])
            break

    if mouse.is_over_object(sair):
        caveirinhas.x = sair.x - 75
        caveirinhas.y = sair.y
        caveirinhas.unhide()
        if mouse.is_button_pressed(1):
            janela.close()

    fundo.draw()
    logo.draw()
    marca.draw()
    iniciarJogo.draw()
    sair.draw()
    caveirinhas.draw()
    caveirinhas.hide()

    janela.update()