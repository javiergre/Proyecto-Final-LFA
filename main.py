import pygame
import sys
from menu_principal import MainMenu


class ChomskyClassifierApp:
    def __init__(self):
        pygame.init()

        # Configuración de la pantalla
        self.screen_width = 1024
        self.screen_height = 768
        self.screen = pygame.display.set_mode(
            (self.screen_width, self.screen_height)
        )
        pygame.display.set_caption("Chomsky Classifier AI")

        # Crear recursos simples
        self.assets = {
            "background": self.create_background(),
            "colors": {
                "blue": (60, 100, 200),
                "white": (255, 255, 255),
                "black": (0, 0, 0),
            },
        }

        # Menú principal
        self.main_menu = MainMenu(self.screen, self.assets)

    def create_background(self):
        bg = pygame.Surface((self.screen_width, self.screen_height))

        # Cielo
        for y in range(self.screen_height):
            t = y / self.screen_height
            r = int(20 + 40 * t)
            g = int(60 + 80 * t)
            b = int(120 + 100 * t)
            pygame.draw.line(bg, (r, g, b), (0, y), (self.screen_width, y))

        # Plataforma
        ground_color = (90, 60, 40)
        pygame.draw.rect(
            bg, ground_color, (0, self.screen_height - 180, self.screen_width, 180)
        )

        block_color = (180, 120, 60)
        for i in range(8):
            x = 80 + i * 110
            y = self.screen_height - 160 - (i % 3) * 15
            pygame.draw.rect(bg, block_color, (x, y, 90, 50))
            pygame.draw.rect(bg, (220, 180, 80), (x, y, 90, 50), 3)

        return bg

    def run(self):
        """Bucle principal."""
        clock = pygame.time.Clock()
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                else:
                    self.main_menu.handle_event(event)

            self.main_menu.update()

            # Dibujar
            self.screen.blit(self.assets["background"], (0, 0))
            self.main_menu.draw()

            pygame.display.flip()
            clock.tick(60)

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    app = ChomskyClassifierApp()
    app.run()
