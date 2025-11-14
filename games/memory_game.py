import pygame
import random


class MemoryGame:
    def __init__(self, screen, assets):
        self.screen = screen
        self.assets = assets
        self.cards = self.create_card_pairs()
        self.setup_game()

    def create_card_pairs(self):
        card_pairs = [
            # TIPOS DE GRAMÁTICAS (10 pares)
            {"type": "Tipo 3", "description": "Gramática Regular", "color": (0, 255, 0)},
            {"type": "Tipo 2", "description": "Libre de Contexto", "color": (255, 255, 0)},
            {"type": "Tipo 1", "description": "Sensible al Contexto", "color": (255, 165, 0)},
            {"type": "Tipo 0", "description": "Recursivamente Enumerable", "color": (255, 0, 0)},
            {"type": "Gramática Regular", "description": "A → aB | a", "color": (100, 255, 100)},
            {"type": "Gramática LC", "description": "A → α", "color": (255, 255, 100)},
            {"type": "Gramática SC", "description": "α → β, |α|≤|β|", "color": (255, 200, 100)},
            {"type": "Gramática RE", "description": "α → β sin restricciones", "color": (255, 100, 100)},
            {"type": "Producción Regular", "description": "A → aB o A → a", "color": (150, 255, 150)},
            {"type": "Producción LC", "description": "A → BC, A → a", "color": (255, 255, 150)},

            # AUTÓMATAS Y MÁQUINAS (10 pares)
            {"type": "AFD", "description": "Autómata Finito Determinista", "color": (100, 200, 255)},
            {"type": "AFN", "description": "Autómata Finito No Determinista", "color": (150, 200, 255)},
            {"type": "AP", "description": "Autómata con Pila", "color": (200, 100, 255)},
            {"type": "APD", "description": "Autómata con Pila Determinista", "color": (200, 150, 255)},
            {"type": "MT", "description": "Máquina de Turing", "color": (255, 100, 200)},
            {"type": "LBA", "description": "Autómata Linealmente Acotado", "color": (255, 150, 200)},
            {"type": "Máquina Universal", "description": "MT que simula otras MT", "color": (255, 100, 150)},
            {"type": "Expresión Regular", "description": "Patrón para lenguajes regulares", "color": (100, 255, 200)},
            {"type": "Árbol de Derivación", "description": "Estructura para GLC", "color": (200, 255, 100)},
            {"type": "Pila LIFO", "description": "Estructura de AP", "color": (255, 200, 100)},

            # CONCEPTOS TEÓRICOS (10 pares)
            {"type": "Noam Chomsky", "description": "Creador de la jerarquía", "color": (150, 150, 255)},
            {"type": "Tesis Church-Turing", "description": "Definición de computabilidad", "color": (150, 200, 255)},
            {"type": "Problema de la parada", "description": "Ejemplo clásico de problema indecidible", "color": (200, 150, 255)},
            {"type": "Lema de bombeo", "description": "Para Regular y LC", "color": (255, 150, 200)},
            {"type": "Forma normal de Chomsky", "description": "Normalización de GLC", "color": (255, 200, 150)},
            {"type": "Ambigüedad", "description": "Múltiples árboles de derivación", "color": (200, 255, 150)},
            {"type": "Derivación", "description": "Aplicación de producciones", "color": (150, 255, 200)},
            {"type": "Símbolo inicial S", "description": "Comienza las derivaciones", "color": (255, 150, 150)},
            {"type": "Variables", "description": "Símbolos no terminales", "color": (150, 255, 150)},
            {"type": "Terminales", "description": "Símbolos finales", "color": (255, 255, 150)},

            # LENGUAJES EJEMPLO (10 pares)
            {"type": "L = a*b*", "description": "Lenguaje Regular", "color": (100, 255, 100)},
            {"type": "L = a^n b^n", "description": "Lenguaje Libre de Contexto", "color": (255, 255, 100)},
            {"type": "L = a^n b^n c^n", "description": "Lenguaje Sensible al Contexto", "color": (255, 200, 100)},
            {"type": "L = ww", "description": "No Libre de Contexto", "color": (255, 150, 100)},
            {"type": "L = ww^R", "description": "Libre de Contexto", "color": (255, 255, 150)},
            {"type": "HTML/XML", "description": "Lenguaje LC típico", "color": (200, 255, 200)},
            {"type": "Expresiones regulares", "description": "Definen lenguajes regulares", "color": (200, 200, 255)},
            {"type": "Lenguaje Pascal", "description": "Ejemplo de lenguaje SC", "color": (255, 200, 255)},
            {"type": "Problema de palabra", "description": "Problema para MT", "color": (200, 255, 255)},
            {"type": "Lenguaje no RE", "description": "Más allá de las MT", "color": (255, 200, 200)},
        ]

        cards = card_pairs * 2
        random.shuffle(cards)
        return cards

    def setup_game(self):
        self.selected_cards = []
        self.matched_pairs = []
        self.moves = 0
        self.game_won = False
        self.cards_per_row = 8

        self.card_rects = []
        card_width = 100
        card_height = 120
        margin = 10
        start_x = (self.screen.get_width() - (self.cards_per_row * card_width + (self.cards_per_row - 1) * margin)) // 2
        start_y = 120

        rows = (len(self.cards) + self.cards_per_row - 1) // self.cards_per_row

        for i in range(rows):
            for j in range(min(self.cards_per_row, len(self.cards) - i * self.cards_per_row)):
                x = start_x + j * (card_width + margin)
                y = start_y + i * (card_height + margin)
                self.card_rects.append(pygame.Rect(x, y, card_width, card_height))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and not self.game_won:
            for i, rect in enumerate(self.card_rects):
                if i < len(self.cards) and rect.collidepoint(event.pos) and i not in self.matched_pairs and i not in self.selected_cards:
                    if len(self.selected_cards) < 2:
                        self.selected_cards.append(i)
                        self.moves += 1

                        if len(self.selected_cards) == 2:
                            idx1, idx2 = self.selected_cards
                            if self.cards[idx1]["type"] == self.cards[idx2]["type"]:
                                self.matched_pairs.extend([idx1, idx2])
                                self.selected_cards = []

                                if len(self.matched_pairs) == len(self.cards):
                                    self.game_won = True
                            else:
                                pygame.time.set_timer(pygame.USEREVENT, 1000)

        elif event.type == pygame.USEREVENT:
            self.selected_cards = []
            pygame.time.set_timer(pygame.USEREVENT, 0)

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return "menu"
            elif event.key == pygame.K_r and self.game_won:
                self.setup_game()

    def draw(self):
        self.screen.fill((40, 40, 80))

        # Título
        title_font = pygame.font.Font(None, 48)
        title = title_font.render("Juego de memoria - 40 pares", True, (255, 255, 255))
        self.screen.blit(title, (self.screen.get_width() // 2 - title.get_width() // 2, 30))

        # Info
        info_font = pygame.font.Font(None, 24)
        moves_text = info_font.render(f"Movimientos: {self.moves}", True, (200, 200, 200))
        pairs_text = info_font.render(f"Pares: {len(self.matched_pairs)//2}/40", True, (200, 200, 200))
        progress = len(self.matched_pairs) / len(self.cards) * 100
        progress_text = info_font.render(f"Progreso: {progress:.1f}%", True, (200, 200, 200))

        self.screen.blit(moves_text, (50, 80))
        self.screen.blit(pairs_text, (self.screen.get_width() // 2 - 50, 80))
        self.screen.blit(progress_text, (self.screen.get_width() - 220, 80))

        # Cartas
        for i, rect in enumerate(self.card_rects):
            if i >= len(self.cards):
                continue

            if i in self.matched_pairs or i in self.selected_cards:
                card = self.cards[i]
                pygame.draw.rect(self.screen, card["color"], rect, border_radius=8)
                pygame.draw.rect(self.screen, (50, 50, 50), rect, 2, border_radius=8)

                # Tipo
                type_font = pygame.font.Font(None, 16)
                type_text = type_font.render(card["type"], True, (0, 0, 0))
                self.screen.blit(type_text, (rect.centerx - type_text.get_width() // 2, rect.top + 8))

                # Descripción
                desc_font = pygame.font.Font(None, 12)
                desc_lines = self.wrap_text(card["description"], desc_font, rect.width - 10)

                # Limitar número de líneas para que el texto no se salga
                max_lines = int((rect.height - 40) / 14)
                desc_lines = desc_lines[:max_lines]

                for j, line in enumerate(desc_lines):
                    desc_text = desc_font.render(line, True, (0, 0, 0))
                    self.screen.blit(
                        desc_text,
                        (
                            rect.centerx - desc_text.get_width() // 2,
                            rect.top + 30 + j * 14,
                        ),
                    )
            else:
                pygame.draw.rect(self.screen, (100, 100, 200), rect, border_radius=8)
                pygame.draw.rect(self.screen, (50, 50, 100), rect, 2, border_radius=8)

                inner = rect.inflate(-15, -15)
                pygame.draw.rect(self.screen, (80, 80, 160), inner, border_radius=5)

                question_font = pygame.font.Font(None, 24)
                question = question_font.render("?", True, (200, 200, 255))
                self.screen.blit(
                    question,
                    (
                        rect.centerx - question.get_width() // 2,
                        rect.centery - question.get_height() // 2,
                    ),
                )

        # Mensaje de victoria
        if self.game_won:
            overlay = pygame.Surface(
                (self.screen.get_width(), self.screen.get_height()), pygame.SRCALPHA
            )
            overlay.fill((0, 0, 0, 150))
            self.screen.blit(overlay, (0, 0))

            win_font = pygame.font.Font(None, 64)
            win_text = win_font.render("¡GANASTE!", True, (255, 255, 0))
            self.screen.blit(
                win_text,
                (
                    self.screen.get_width() // 2 - win_text.get_width() // 2,
                    250,
                ),
            )

            stats_font = pygame.font.Font(None, 36)
            stats_text = stats_font.render(f"Movimientos: {self.moves}", True, (255, 255, 255))
            efficiency = (40 / max(1, self.moves)) * 100
            efficiency_text = stats_font.render(f"Eficiencia: {efficiency:.1f}%", True, (255, 255, 255))

            self.screen.blit(
                stats_text,
                (
                    self.screen.get_width() // 2 - stats_text.get_width() // 2,
                    340,
                ),
            )
            self.screen.blit(
                efficiency_text,
                (
                    self.screen.get_width() // 2 - efficiency_text.get_width() // 2,
                    390,
                ),
            )

            restart_font = pygame.font.Font(None, 24)
            restart_text = restart_font.render(
                "Presiona R para reiniciar o ESC para volver al menú", True, (230, 230, 230)
            )
            self.screen.blit(
                restart_text,
                (
                    self.screen.get_width() // 2 - restart_text.get_width() // 2,
                    460,
                ),
            )

    def wrap_text(self, text, font, max_width):
        words = text.split(" ")
        lines = []
        current_line = []

        for word in words:
            test_line = " ".join(current_line + [word])
            surf = font.render(test_line, True, (0, 0, 0))
            if surf.get_width() <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(" ".join(current_line))
                current_line = [word]

        if current_line:
            lines.append(" ".join(current_line))

        return lines

    def run(self):
        clock = pygame.time.Clock()
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"

                result = self.handle_event(event)
                if result == "menu":
                    running = False

            self.draw()
            pygame.display.flip()
            clock.tick(60)

        return "menu"
