import pygame
import sys
import math
from classifier_ui import ClassifierUI
from games.flashcards import FlashcardGame
from games.memory_game import MemoryGame
from games.quiz_race import QuizRaceGame


class MainMenu:
    def __init__(self, screen, assets):
        self.screen = screen
        self.assets = assets
        self.buttons = []
        self.current_selection = 0
        self.camera_angle = 0
        self.setup_menu()

    def setup_menu(self):
        width = self.screen.get_width()
        height = self.screen.get_height()

        menu_options = [
            {"text": "Clasificador de gramáticas", "action": "classifier"},
            {"text": "Flashcards", "action": "flashcards"},
            {"text": "Juego de memoria", "action": "memory"},
            {"text": "Carrera de quiz", "action": "quiz_race"},
            {"text": "Salir", "action": "exit"},
        ]

        button_width = 320
        button_height = 60
        spacing = 15
        total_height = len(menu_options) * (button_height + spacing)
        start_y = height // 2 - total_height // 2 + 40

        self.buttons = []
        for i, option in enumerate(menu_options):
            rect = pygame.Rect(
                width // 2 - button_width // 2,
                start_y + i * (button_height + spacing),
                button_width,
                button_height,
            )
            self.buttons.append(
                {
                    "rect": rect,
                    "text": option["text"],
                    "action": option["action"],
                }
            )

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            for i, button in enumerate(self.buttons):
                if button["rect"].collidepoint(event.pos):
                    self.current_selection = i

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for i, button in enumerate(self.buttons):
                    if button["rect"].collidepoint(event.pos):
                        self.current_selection = i
                        self.execute_action(button["action"])
                        break

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.current_selection = (self.current_selection - 1) % len(
                    self.buttons
                )
            elif event.key == pygame.K_DOWN:
                self.current_selection = (self.current_selection + 1) % len(
                    self.buttons
                )
            elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                action = self.buttons[self.current_selection]["action"]
                self.execute_action(action)
            elif event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

    def execute_action(self, action):
        if action == "classifier":
            ui = ClassifierUI(self.screen, self.assets)
            result = ui.run()
            if result == "quit":
                pygame.quit()
                sys.exit()

        elif action == "flashcards":
            game = FlashcardGame(self.screen, self.assets)
            result = game.run()
            if result == "quit":
                pygame.quit()
                sys.exit() 

        elif action == "memory":
            game = MemoryGame(self.screen, self.assets)
            result = game.run()
            if result == "quit":
                pygame.quit()
                sys.exit()

        elif action == "quiz_race":
            game = QuizRaceGame(self.screen, self.assets)
            result = game.run()
            if result == "quit":
                pygame.quit()
                sys.exit()

        elif action == "exit":
            pygame.quit()
            sys.exit()

    def update(self):
        self.camera_angle = (self.camera_angle + 0.01) % 360

    def draw(self):
        width = self.screen.get_width()
        height = self.screen.get_height()

        # Título
        title_font = pygame.font.Font(None, 64)
        subtitle_font = pygame.font.Font(None, 32)

        title = title_font.render("Chomsky Classifier AI", True, (255, 255, 255))
        subtitle = subtitle_font.render(
            "Aventura de clasificación de gramáticas", True, (255, 255, 0)
        )

        self.screen.blit(
            title, (width // 2 - title.get_width() // 2, height // 2 - 230)
        )
        self.screen.blit(
            subtitle, (width // 2 - subtitle.get_width() // 2, height // 2 - 190)
        )

        # Botones
        for i, button in enumerate(self.buttons):
            rect = button["rect"]
            hovered = i == self.current_selection

            base_color = (60, 100, 200)
            hover_color = (90, 140, 240)
            color = hover_color if hovered else base_color

            pygame.draw.rect(self.screen, color, rect, border_radius=10)
            pygame.draw.rect(self.screen, (255, 255, 255), rect, 2, border_radius=10)

            font = pygame.font.Font(None, 30)
            text = font.render(button["text"], True, (255, 255, 255))
            self.screen.blit(
                text,
                (
                    rect.centerx - text.get_width() // 2,
                    rect.centery - text.get_height() // 2,
                ),
            )

        cx = width // 2
        cy = int(height * 0.12)  
        radius_outer = 18
        radius_inner = 8
        points = []
        for i in range(10):
            angle = (i * 36 - 90) * math.pi / 180
            r = radius_outer if i % 2 == 0 else radius_inner
            x = cx + r * math.cos(angle)
            y = cy + r * math.sin(angle)
            points.append((x, y))
        pygame.draw.polygon(self.screen, (255, 255, 0), points)

        # Instrucciones
        instruction_font = pygame.font.Font(None, 22)
        instructions = [
            "Usa el mouse o las flechas para navegar",
            "Pulsa ENTER o haz clic para seleccionar",
            "Pulsa ESC para salir",
        ]

        for i, text_line in enumerate(instructions):
            text = instruction_font.render(text_line, True, (230, 230, 230))
            self.screen.blit(
                text,
                (
                    width // 2 - text.get_width() // 2,
                    height - 110 + i * 24,
                ),
            )
