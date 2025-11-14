import pygame
import random
import time


class QuizRaceGame:
    def __init__(self, screen, assets):
        self.screen = screen
        self.assets = assets
        self.questions = self.load_questions()
        self.setup_game()

    def load_questions(self):
        return [
            # Tipo 3 - Regulares
            {
                "question": "¿Qué tipo es la gramática S → aS | b?",
                "options": ["Tipo 0", "Tipo 1", "Tipo 2", "Tipo 3"],
                "correct": 3,
                "explanation": "Es Regular (Tipo 3): las producciones tienen la forma A → aB o A → a.",
            },
            {
                "question": "¿Qué autómata reconoce gramáticas Regulares?",
                "options": ["Máquina de Turing", "Autómata con pila", "Autómata finito", "LBA"],
                "correct": 2,
                "explanation": "Los autómatas finitos reconocen lenguajes regulares.",
            },
            {
                "question": "¿Cuál de los siguientes lenguajes es Regular?",
                "options": ["a^n b^n", "a^n b^n c^n", "a*b*", "ww (w en {a,b}*)"],
                "correct": 2,
                "explanation": "a*b* es aceptado por un autómata finito.",
            },
            {
                "question": "Una forma típica de producción Regular derecha es:",
                "options": ["A → Ba", "A → aB", "A → BC", "AB → a"],
                "correct": 1,
                "explanation": "En forma Regular derecha la variable va al final: A → aB.",
            },
            {
                "question": "¿Para qué se usa el lema de bombeo en Regulares?",
                "options": [
                    "Probar que un lenguaje es Regular",
                    "Probar que un lenguaje no es Regular",
                    "Construir autómatas",
                    "Optimizar gramáticas",
                ],
                "correct": 1,
                "explanation": "Se usa para demostrar que algunos lenguajes no pueden ser regulares.",
            },
            # Tipo 2 - Libres de contexto
            {
                "question": "¿Qué condición debe cumplir el lado izquierdo en una GLC?",
                "options": [
                    "Puede contener símbolos terminales",
                    "Puede ser cualquier cadena",
                    "Debe ser una sola variable",
                    "Debe ser ε",
                ],
                "correct": 2,
                "explanation": "En una GLC cada producción tiene un único no terminal en el lado izquierdo.",
            },
            {
                "question": "¿Qué autómata se asocia con lenguajes Libres de Contexto?",
                "options": ["Autómata finito", "Autómata con pila", "LBA", "Máquina de Turing"],
                "correct": 1,
                "explanation": "Los autómatas con pila reconocen lenguajes LC.",
            },
            {
                "question": "Ejemplo clásico de lenguaje Libre de Contexto:",
                "options": ["a^n b^n", "a^n b^n c^n", "a*b*", "ww"],
                "correct": 0,
                "explanation": "a^n b^n es reconocido por un AP con una pila.",
            },
            {
                "question": "¿Qué estructura se usa para visualizar derivaciones en GLC?",
                "options": ["Árbol de derivación", "Diagrama de estados", "Tabla de transición", "Autómata finito"],
                "correct": 0,
                "explanation": "Los árboles de derivación muestran la aplicación de producciones.",
            },
            {
                "question": "Una gramática es ambigua si:",
                "options": [
                    "Tiene más de un símbolo inicial",
                    "Genera lenguajes infinitos",
                    "Hay cadenas con varios árboles de derivación",
                    "Usa muchas variables",
                ],
                "correct": 2,
                "explanation": "Ambigüedad: una cadena tiene más de un árbol de derivación.",
            },
            # Tipo 1 - Sensibles al contexto
            {
                "question": "¿Qué restricción cumple una gramática Sensible al Contexto?",
                "options": [
                    "|α| ≥ |β|",
                    "|α| ≤ |β| (salvo S → ε bajo condiciones)",
                    "|α| = |β| siempre",
                    "Solo permite producciones A → a",
                ],
                "correct": 1,
                "explanation": "En las GSC se cumple |α| ≤ |β|.",
            },
            {
                "question": "¿Qué autómata reconoce lenguajes Sensibles al Contexto?",
                "options": ["Autómata finito", "Autómata con pila", "LBA", "Máquina de Turing"],
                "correct": 2,
                "explanation": "Los LBA reconocen lenguajes SC.",
            },
            {
                "question": "Ejemplo clásico de lenguaje Sensible al Contexto:",
                "options": ["a^n b^n", "a^n b^n c^n", "a*b*", "ww"],
                "correct": 1,
                "explanation": "a^n b^n c^n requiere contar tres símbolos a la vez.",
            },
            {
                "question": "Relación entre lenguajes LC y SC:",
                "options": [
                    "No están relacionados",
                    "Todo LC es también SC",
                    "Todo SC es también LC",
                    "Son iguales",
                ],
                "correct": 1,
                "explanation": "L(LC) es subconjunto propio de L(SC).",
            },
            # Tipo 0 - RE
            {
                "question": "¿Qué son las gramáticas de Tipo 0?",
                "options": [
                    "Gramáticas regulares",
                    "Gramáticas sin restricciones",
                    "Gramáticas LC",
                    "Gramáticas finitas",
                ],
                "correct": 1,
                "explanation": "Tipo 0: gramáticas sin restricciones; generan lenguajes RE.",
            },
            {
                "question": "Modelo asociado a lenguajes de Tipo 0:",
                "options": ["AFD", "AP", "LBA", "Máquina de Turing"],
                "correct": 3,
                "explanation": "Las MT reconocen lenguajes recursivamente enumerables.",
            },
            {
                "question": "En un lenguaje recursivamente enumerable:",
                "options": [
                    "La MT siempre se detiene",
                    "La MT puede no detenerse en cadenas fuera del lenguaje",
                    "Solo hay un número finito de cadenas",
                    "No puede aceptarse por MT",
                ],
                "correct": 1,
                "explanation": "Para cadenas fuera del lenguaje la MT puede no parar.",
            },
            {
                "question": "¿Qué afirma la Tesis de Church–Turing?",
                "options": [
                    "Que las MT son más débiles que los programas reales",
                    "Que toda función computable puede ser calculada por una MT",
                    "Que solo algunos lenguajes son RE",
                    "Que toda MT es determinista",
                ],
                "correct": 1,
                "explanation": "Es una tesis sobre el poder expresivo de las MT.",
            },
            # Otros
            {
                "question": "¿Qué tipo de lenguaje describe una expresión regular?",
                "options": ["Regular", "LC", "SC", "RE"],
                "correct": 0,
                "explanation": "Las expresiones regulares describen lenguajes regulares.",
            },
            {
                "question": "¿Cuál es la jerarquía correcta?",
                "options": [
                    "Regulares ⊆ LC ⊆ SC ⊆ RE",
                    "LC ⊆ Regulares ⊆ SC ⊆ RE",
                    "RE ⊆ SC ⊆ LC ⊆ Regulares",
                    "SC ⊆ LC ⊆ Regulares ⊆ RE",
                ],
                "correct": 0,
                "explanation": "Regulares ⊆ LC ⊆ SC ⊆ RE.",
            },
        ]

    def setup_game(self):
        self.current_question = 0
        self.score = 0
        self.time_left = 45
        self.game_over = False
        self.selected_answer = None
        self.show_feedback = False
        self.feedback_timer = 0
        self.start_time = time.time()
        self.questions_answered = 0

        random.shuffle(self.questions)

        self.option_buttons = []
        option_height = 60
        start_y = 260

        for i in range(4):
            rect = pygame.Rect(180, start_y + i * (option_height + 15), 640, option_height)
            self.option_buttons.append(rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and not self.game_over and not self.show_feedback:
            for i, rect in enumerate(self.option_buttons):
                if rect.collidepoint(event.pos):
                    self.selected_answer = i
                    self.check_answer()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return "menu"
            elif event.key == pygame.K_r and self.game_over:
                self.setup_game()
            elif not self.game_over and not self.show_feedback:
                if event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4]:
                    self.selected_answer = event.key - pygame.K_1
                    self.check_answer()

    def check_answer(self):
        question = self.questions[self.current_question]
        self.show_feedback = True
        self.feedback_timer = time.time()
        self.questions_answered += 1

        if self.selected_answer == question["correct"]:
            self.score += 10
            self.time_left += 3  # pequeño bonus

    def update(self):
        current_time = time.time()
        elapsed = current_time - self.start_time

        if not self.game_over and not self.show_feedback:
            self.time_left = max(0, 45 - elapsed)
            if self.time_left <= 0:
                self.game_over = True

        if self.show_feedback:
            if current_time - self.feedback_timer > 1.5:
                self.show_feedback = False
                self.current_question += 1
                self.selected_answer = None

                if self.current_question >= len(self.questions) or self.questions_answered >= 20:
                    self.game_over = True

    def draw(self):
        self.screen.fill((60, 40, 80))

        title_font = pygame.font.Font(None, 48)
        title = title_font.render("Carrera de quiz - Banco de preguntas", True, (255, 255, 255))
        self.screen.blit(
            title,
            (self.screen.get_width() // 2 - title.get_width() // 2, 50),
        )

        info_font = pygame.font.Font(None, 24)
        score_text = info_font.render(f"Puntuación: {self.score}", True, (255, 255, 0))
        time_color = (255, 100, 100) if self.time_left < 10 else (100, 255, 100)
        time_text = info_font.render(f"Tiempo: {int(self.time_left)} s", True, time_color)
        progress_text = info_font.render(f"Progreso: {self.questions_answered}/20", True, (220, 220, 220))

        self.screen.blit(score_text, (50, 120))
        self.screen.blit(time_text, (self.screen.get_width() // 2 - time_text.get_width() // 2, 120))
        self.screen.blit(progress_text, (self.screen.get_width() - 220, 120))

        if not self.game_over:
            question = self.questions[self.current_question]

            q_font = pygame.font.Font(None, 30)
            q_surface = q_font.render(question["question"], True, (255, 255, 255))
            self.screen.blit(
                q_surface,
                (self.screen.get_width() // 2 - q_surface.get_width() // 2, 180),
            )

            for i, rect in enumerate(self.option_buttons):
                color = (140, 170, 255) if rect.collidepoint(
                    pygame.mouse.get_pos()
                ) else (220, 220, 220)

                if self.show_feedback and i == question["correct"]:
                    color = (120, 255, 120)
                elif self.show_feedback and i == self.selected_answer and i != question["correct"]:
                    color = (255, 120, 120)

                pygame.draw.rect(self.screen, color, rect, border_radius=8)
                pygame.draw.rect(self.screen, (50, 50, 50), rect, 2, border_radius=8)

                option_text = f"{i+1}. {question['options'][i]}"
                option_font = pygame.font.Font(None, 24)
                option_surf = option_font.render(option_text, True, (0, 0, 0))
                self.screen.blit(
                    option_surf,
                    (
                        rect.centerx - option_surf.get_width() // 2,
                        rect.centery - option_surf.get_height() // 2,
                    ),
                )

            if self.show_feedback:
                fb_font = pygame.font.Font(None, 22)
                if self.selected_answer == question["correct"]:
                    fb_text = f"Correcto. +10 puntos - {question['explanation']}"
                    fb_color = (120, 255, 120)
                else:
                    correct_answer = question["options"][question["correct"]]
                    fb_text = f"Incorrecto. Correcto: {correct_answer}. {question['explanation']}"
                    fb_color = (255, 150, 150)

                fb_surface = fb_font.render(fb_text, True, fb_color)
                self.screen.blit(
                    fb_surface,
                    (
                        self.screen.get_width() // 2 - fb_surface.get_width() // 2,
                        550,
                    ),
                )

        else:
            result_font = pygame.font.Font(None, 64)
            if self.score >= 160:
                result_text = result_font.render("¡Genio!", True, (255, 215, 0))
            elif self.score >= 120:
                result_text = result_font.render("¡Excelente!", True, (255, 255, 0))
            elif self.score >= 80:
                result_text = result_font.render("¡Muy bien!", True, (255, 200, 0))
            else:
                result_text = result_font.render("Buen intento", True, (255, 150, 0))

            self.screen.blit(
                result_text,
                (
                    self.screen.get_width() // 2 - result_text.get_width() // 2,
                    260,
                ),
            )

            score_font = pygame.font.Font(None, 48)
            score_display = score_font.render(f"Puntuación final: {self.score}", True, (255, 255, 255))
            accuracy = (self.score / max(1, self.questions_answered * 10)) * 100
            accuracy_text = score_font.render(f"Precisión: {accuracy:.1f}%", True, (255, 255, 255))

            self.screen.blit(
                score_display,
                (
                    self.screen.get_width() // 2 - score_display.get_width() // 2,
                    340,
                ),
            )
            self.screen.blit(
                accuracy_text,
                (
                    self.screen.get_width() // 2 - accuracy_text.get_width() // 2,
                    390,
                ),
            )

            restart_font = pygame.font.Font(None, 24)
            restart_text = restart_font.render(
                "Presiona R para reiniciar o ESC para volver al menú", True, (220, 220, 220)
            )
            self.screen.blit(
                restart_text,
                (
                    self.screen.get_width() // 2 - restart_text.get_width() // 2,
                    460,
                ),
            )

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

            self.update()
            self.draw()
            pygame.display.flip()
            clock.tick(60)

        return "menu"
