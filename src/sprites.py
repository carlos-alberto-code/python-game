from typing import Tuple, Optional
import pygame as pg

class MySprite(pg.sprite.Sprite):
    def __init__(self, x: int, y: int, color: Optional[Tuple[int, int, int]] = None, image_path: Optional[str] = None, *groups: pg.sprite.AbstractGroup):
        super().__init__(*groups)
        if image_path:
            self.image = pg.image.load(image_path).convert_alpha()
            self.image = pg.transform.scale(self.image, (100, 100))
        else:
            self.image = pg.Surface((50, 50))
            if color is not None:
                self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.is_main = False
        self.velocity = pg.Vector2(2, 2)  # Velocidad del sprite

    def update(self):
        if self.is_main:
            keys = pg.key.get_pressed()
            if keys[pg.K_LEFT]:
                self.rect.x -= 5
            if keys[pg.K_RIGHT]:
                self.rect.x += 5
            if keys[pg.K_UP]:
                self.rect.y -= 5
            if keys[pg.K_DOWN]:
                self.rect.y += 5
        self.rect.x += self.velocity.x
        self.rect.y += self.velocity.y

    def draw(self, screen: pg.Surface):
        screen.blit(self.image, self.rect)


def handle_keydown(event: pg.event.Event, sprite: MySprite):
    if event.key == pg.K_LEFT:
        sprite.rect.x -= 10
    elif event.key == pg.K_RIGHT:
        sprite.rect.x += 10
    elif event.key == pg.K_UP:
        sprite.rect.y -= 10
    elif event.key == pg.K_DOWN:
        sprite.rect.y += 10

def handle_mousebuttondown(event: pg.event.Event , sprite: MySprite):
    if event.button == 1:  # Botón izquierdo del ratón
        sprite.rect.topleft = event.pos


pg.init()
clock = pg.time.Clock()
pg.display.set_caption("Sprites")

WIDTH, HEIGHT = 800, 600
screen = pg.display.set_mode((WIDTH, HEIGHT))

# Crear grupos de sprites
all_sprites = pg.sprite.Group()
enemy_sprites = pg.sprite.Group()

# Crear sprites y añadirlos a los grupos
player_sprite = MySprite(100, 100, (255, 0, 0))
player_sprite.is_main = True  # Marcar player_sprite como el sprite principal
enemy1 = MySprite(200, 200, (0, 255, 0))
enemy2 = MySprite(300, 300, (0, 0, 255))
enemy_with_image = MySprite(400, 400, image_path='imagenes/Bloquador.png')  # Sprite con imagen

all_sprites.add(player_sprite, enemy1, enemy2, enemy_with_image)
enemy_sprites.add(enemy1, enemy2, enemy_with_image)

def handle_collisions():
    collisions = pg.sprite.spritecollide(player_sprite, enemy_sprites, False)
    for collided_sprite in collisions:
        print(f"Collision with {collided_sprite}")

event_handlers = {
    pg.QUIT: lambda event: exit(),
    pg.KEYDOWN: lambda event: handle_keydown(event, player_sprite),
}

running = True
while running:
    for event in pg.event.get():
        handler = event_handlers.get(event.type)
        if handler:
            handler(event)

    screen.fill((0, 0, 0))  # Limpiar la pantalla

    # Actualizar y dibujar todos los sprites del grupo
    all_sprites.update()
    all_sprites.draw(screen)

    # Manejar colisiones
    handle_collisions()

    pg.display.flip()  # Actualizar la pantalla
    clock.tick(60)  # Controlar la tasa de fotogramas

pg.quit()
