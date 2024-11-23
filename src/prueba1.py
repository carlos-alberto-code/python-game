import pygame as pg
import math

class Player(pg.sprite.Sprite):
    def __init__(self, image_path: str) -> None:
        super().__init__()
        self.image = pg.image.load(image_path).convert_alpha()
        self.image = pg.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect()
        self.rect.center = (400, 300)  # Centro de la pantalla
        self._angle = 0
        self._radius = 100
        self._center = pg.Vector2(400, 300)
        self._is_main = False

    def update(self) -> None:
        self._angle += 2  # Incrementa el ángulo para mover en círculo
        if self._angle >= 360:
            self._angle = 0

        self.rect.x = int(self._center.x + self._radius * math.cos(math.radians(self._angle)))
        self.rect.y = int(self._center.y + self._radius * math.sin(math.radians(self._angle)))

    def draw(self, surface: pg.Surface) -> None:
        surface.blit(self.image, self.rect.topleft)

pg.init()
screen = pg.display.set_mode((800, 600))
pg.display.set_caption('Prueba 1')
clock = pg.time.Clock()
player = Player('imagenes/Mago.png')
player_group = pg.sprite.Group()
player_group.add(player)
running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.MOUSEBUTTONDOWN:
            player._is_main = True
        elif event.type == pg.MOUSEBUTTONUP:
            player._is_main = False

    player_group.update()
    screen.fill((0, 0, 0))
    player_group.draw(screen)
    pg.display.flip()
    clock.tick(60)

pg.quit()
