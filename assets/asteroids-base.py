# -*- coding: utf-8 -*-

# Importando as bibliotecas necessárias.
import pygame
from os import path
import random
import time

# Estabelece a pasta que contem as figuras.
img_dir = path.join(path.dirname(__file__), 'img')

#SND
snd_dir = path.join(path.dirname(__file__), 'snd')

# Dados gerais do jogo.
WIDTH = 480 # Largura da tela
HEIGHT = 600 # Altura da tela
FPS = 60 # Frames por segundo

# Define algumas variáveis com as cores básicas
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

#Classe Mob que representa os meteoros

class Mob(pygame.sprite.Sprite):
    
    #construtor
    def __init__(self):
        
        #Construtor da classe pai (Sprite)
        pygame.sprite.Sprite.__init__(self)
        
        #Carregando imagem
        meteoro_img = pygame.image.load(path.join(img_dir, "meteorBrown_med1.png"))
        self.image = meteoro_img
        
        #transformando imagem
        self.image = pygame.transform.scale(meteoro_img, (50, 38))
        
        #Transparente
        self.image.set_colorkey(BLACK)
        
        #Posicionamento
        self.rect = self.image.get_rect()
        
        self.rect.x = random.randrange(0, WIDTH)
        
        self.rect.y = random.randrange(-100, -40)
        
        #Speed
        self.speedx = random.randrange(-3, 3)
        
        self.speedy = random.randrange(2, 9)
        
        #Melhora colisão
        self.radius = int(self.rect.width * .85/2)
        
    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        
        #Se o meteoro sair do rect:
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedx = random.randrange(-3, 3)
            self.speedy = random.randrange(2, 9)
        
#Grupo Mobs:
all_mobs = pygame.sprite.Group()  

#Classe jogador que representa nave

class Player(pygame.sprite.Sprite):
    
    #construtor da classe
    def __init__(self, player_img):
        
        #Construtor da classe pai (Sprite)
        pygame.sprite.Sprite.__init__(self)
        
        #Carregando a imagem de fundo
        self.image = player_img
        
        #Diminuindo o tamanho da imagem
        self.image = pygame.transform.scale(player_img, (50, 38))
        
        #Deixando transparente
        self.image.set_colorkey(BLACK)
        
        #Detalhes sobre o posicionamento
        self.rect = self.image.get_rect()
        
        #Centraliza embaixo da tela
        self.rect.centerx = WIDTH/2
        self.rect.bottom = HEIGHT - 10
        
        #velocidade da nave
        self.speedx = 0
        
        #Raio 
        self.radius = 25
        
    #Metodo que atualiza a posição da navinha
    def update(self):
        self.rect.x += self.speedx
        
        #mantem dentro da tela
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
            
class Bullet(pygame.sprite.Sprite):
    
    def __init__(self, x, y):
        
        pygame.sprite.Sprite.__init__(self)
        
        bullet_img = pygame.image.load(path.join(img_dir, "laserRed16.png"))
        self.image = bullet_img
        
        self.image.set_colorkey(BLACK)
        
        self.rect = self.image.get_rect()
        
        self.speedy = -10
        self.rect.bottom = y
        self.rect.centerx = x
        
    def update(self):
        self.rect.y += self.speedy
        
        if self.rect.bottom < 0:
            self.kill()

#Carrega os assets
def load_assets(img_dir, snd_dir):
    assets = {}
    assets["player_img"] = pygame.image.load(path.join(img_dir, 'playerShip1_orange.png')).convert()
    assets["mob_img"] = pygame.image.load(path.join(img_dir, 'meteorBrown_med1.png')).convert()
    assets["bullet_img"] = pygame.image.load(path.join(img_dir, 'laserRed16.png')).convert()
    assets["background"] = pygame.image.load(path.join(img_dir, 'starfield.png')).convert()
    assets["boom_sound"] = pygame.mixer.Sound(path.join(snd_dir, 'expl3.wav')).convert()
    assets["destroy_sound"] = pygame.mixer.Sound(path.join(snd_dir, 'expl6.wav')).convert()
    assets["pew_sound"] = pygame.mixer.Sound(path.join(snd_dir, 'pew.wav')).convert()   
    return assets


# Inicialização do Pygame.
pygame.init()
pygame.mixer.init()

# Tamanho da tela.
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Nome do jogo
pygame.display.set_caption("Asteroids")

#Carrega todos os assets uma vez só, e guarda em um dicionário
assets = load_assets(img_dir, snd_dir)

# Variável para o ajuste de velocidade
clock = pygame.time.Clock()

# Carrega o fundo do jogo
background = assets["background"]
background_rect = background.get_rect()

#Som
pygame.mixer.music.load(path.join(snd_dir, 'tgfcoder-FrozenJam-Seamlessloop.ogg'))
pygame.mixer.music.set_volume(0.4)
boom_sound = assets["boom_sound"]
pew_sound = assets["pew_sound"]
destroy_sound = assets["destroy_sound"]

#Cria uma nave. O construtor será chamado automaticamete
player = Player(assets["player_img"])

#Cria um grupo de sprites e adiciona a nave
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

all_bullets = pygame.sprite.Group()


for i in range(8):
    m = Mob()
    all_mobs.add(m)
    all_sprites.add(m)  



# Comando para evitar travamentos.
try:
    
    # Loop principal.
    pygame.mixer.music.play(loops = -1)
    running = True
    while running:
        
        # Ajusta a velocidade do jogo.
        clock.tick(FPS)
        
        # Processa os eventos (mouse, teclado, botão, etc).
        for event in pygame.event.get():
            
            # Verifica se foi fechado
            if event.type == pygame.QUIT:
                running = False
                
            #Verifica se apertou alguma tecla    
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.speedx = -8
                if event.key == pygame.K_RIGHT:
                    player.speedx = 8
                if event.key == pygame.K_SPACE:
                    bullet = Bullet(player.rect.centerx, player.rect.top)
                    all_sprites.add(bullet)
                    all_bullets.add(bullet)
                    pew_sound.play()
                
             #Verifica se soltou alguma tecla
            if event.type == pygame.KEYUP:
                #Dependendo da tecla altera a velocidade
                if event.key == pygame.K_LEFT:
                    player.speedx = 0
                if event.key == pygame.K_RIGHT:
                    player.speedx = 0
                    
        #Depois de processar os eventos
        #Atualiza a acao de cada sprite
        all_sprites.update()
        
        
        hits = pygame.sprite.groupcollide(all_mobs, all_bullets, True, True)
        for hit in hits:
            destroy_sound.play()
            m = Mob()
            all_sprites.add(m)
            all_mobs.add(m)
        #Colisão entre nave e meteoro
        hits = pygame.sprite.spritecollide(player, all_mobs, False, pygame.sprite.collide_circle)
        if hits:
            #Som de colisão
            boom_sound.play()
            time.sleep(1) 
            
            running = False
    
        # A cada loop, redesenha o fundo e os sprites
        screen.fill(BLACK)
        screen.blit(background, background_rect)
        all_sprites.draw(screen)
        
        # Depois de desenhar tudo, inverte o display.
        pygame.display.flip()
        
finally:
    pygame.quit()
