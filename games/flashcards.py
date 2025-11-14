import pygame
import random

class FlashcardGame:
    def __init__(self, screen, assets):
        self.screen = screen
        self.assets = assets
        self.cards = self.load_flashcards()
        self.current_card = 0
        self.show_answer = False
        self.score = 0
        self.setup_ui()
    
    def load_flashcards(self):
        return [
            # CONCEPTOS BÁSICOS 
            {
                "question": "¿Qué es la Jerarquía de Chomsky?",
                "answer": "Clasificación de lenguajes formales en 4 tipos (0-3) según su complejidad y poder expresivo."
            },
            {
                "question": "¿Quién propuso la Jerarquía de Chomsky?",
                "answer": "Noam Chomsky en 1956, lingüista y científico cognitivo estadounidense."
            },
            {
                "question": "¿Cuál es el propósito de la Jerarquía de Chomsky?",
                "answer": "Clasificar gramáticas según su poder generativo y las máquinas que las reconocen."
            },
            {
                "question": "¿Qué representa cada tipo en la jerarquía?",
                "answer": "Tipo 3: Regular, Tipo 2: Libre de Contexto, Tipo 1: Sensible al Contexto, Tipo 0: Recursivamente Enumerable."
            },
            {
                "question": "¿Qué es una gramática formal?",
                "answer": "Conjunto de reglas para generar cadenas en un lenguaje formal, compuesta por (V, T, P, S)."
            },
            {
                "question": "¿Qué son las variables en una gramática?",
                "answer": "Símbolos no terminales (mayúsculas) que representan categorías sintácticas."
            },
            {
                "question": "¿Qué son los terminales en una gramática?",
                "answer": "Símbolos finales (minúsculas) que aparecen en las cadenas del lenguaje."
            },
            {
                "question": "¿Qué es el símbolo inicial S?",
                "answer": "Variable especial desde donde comienzan todas las derivaciones."
            },
            {
                "question": "¿Qué es una producción gramatical?",
                "answer": "Regla de reescritura que especifica cómo transformar variables en cadenas de símbolos."
            },
            {
                "question": "¿Qué es la derivación en gramáticas?",
                "answer": "Proceso de aplicar producciones sucesivamente para generar cadenas del lenguaje."
            },

            # TIPO 3 - REGULAR
            {
                "question": "¿Qué caracteriza una gramática Tipo 3 (Regular)?",
                "answer": "Producciones de forma: A → aB, A → a, A → ε. Lado izquierdo: una sola variable."
            },
            {
                "question": "¿Qué autómata reconoce lenguajes Tipo 3?",
                "answer": "Autómatas Finitos Deterministas (AFD) y No Deterministas (AFN)."
            },
            {
                "question": "Ejemplo de gramática Regular izquierda",
                "answer": "S → Sa | Sb | a | b (Forma A → Ba)"
            },
            {
                "question": "Ejemplo de gramática Regular derecha",
                "answer": "S → aS | bS | a | b (Forma A → aB)"
            },
            {
                "question": "¿Qué lenguajes son Regulares?",
                "answer": "Lenguajes que pueden ser descritos por expresiones regulares. Ej: (a|b)*abb"
            },
            {
                "question": "Limitaciones de los lenguajes Regulares",
                "answer": "No pueden contar elementos ni manejar estructuras anidadas. Ej: {aⁿbⁿ | n≥0}"
            },
            {
                "question": "¿Qué es una expresión regular?",
                "answer": "Patrón que describe un conjunto de cadenas usando operadores como *, |, concatenación."
            },
            {
                "question": "Equivalencia AFD-AFN",
                "answer": "Todo AFN puede convertirse en un AFD equivalente, aunque con posible explosión de estados."
            },
            {
                "question": "Lema de bombeo para Regulares",
                "answer": "Herramienta para demostrar que un lenguaje NO es regular."
            },
            {
                "question": "Aplicaciones de lenguajes Regulares",
                "answer": "Búsqueda de patrones, análisis léxico, validación de formatos, editores de texto."
            },

            # TIPO 2 - LIBRE DE CONTEXTO 
            {
                "question": "¿Qué caracteriza una gramática Tipo 2?",
                "answer": "Producciones: A → α, donde A es variable y α cadena de símbolos. Lado izquierdo: una variable."
            },
            {
                "question": "¿Qué autómata reconoce LLC?",
                "answer": "Autómatas con Pila (AP) - extenden AF añadiendo una pila LIFO."
            },
            {
                "question": "Ejemplo clásico de LLC",
                "answer": "L = {aⁿbⁿ | n ≥ 1} con gramática: S → aSb | ab"
            },
            {
                "question": "¿Qué es la pila en un AP?",
                "answer": "Memoria auxiliar LIFO que permite contar y manejar estructuras anidadas."
            },
            {
                "question": "Forma Normal de Chomsky",
                "answer": "Toda GLC puede transformarse a producciones: A → BC o A → a"
            },
            {
                "question": "Árbol de derivación en GLC",
                "answer": "Estructura arbórea que muestra cómo se deriva una cadena desde S."
            },
            {
                "question": "Ambigüedad en GLC",
                "answer": "Una gramática es ambigua si una cadena tiene más de un árbol de derivación."
            },
            {
                "question": "Lenguajes libres de contexto inherentemente ambiguos",
                "answer": "Lenguajes para los cuales TODAS las gramáticas son ambiguas."
            },
            {
                "question": "Aplicaciones de LLC",
                "answer": "Análisis sintáctico, compiladores, procesamiento de lenguaje natural, XML/HTML."
            },
            {
                "question": "Lema de bombeo para LLC",
                "answer": "Herramienta para demostrar que un lenguaje NO es libre de contexto."
            },

            # TIPO 1 - SENSIBLE AL CONTEXTO 
            {
                "question": "¿Qué caracteriza una gramática Tipo 1?",
                "answer": "Producciones: α → β con |α| ≤ |β|, excepto S → ε si S no aparece en lados derechos."
            },
            {
                "question": "¿Por qué se llama 'Sensible al Contexto'?",
                "answer": "Porque las producciones pueden depender del contexto alrededor de la variable."
            },
            {
                "question": "Ejemplo de gramática Sensible al Contexto",
                "answer": "aSb → aabb, aS → ab (el contexto 'a_b' afecta la producción)"
            },
            {
                "question": "¿Qué autómata reconoce LSC?",
                "answer": "Autómatas Linealmente Acotados (LBA) - MT con cinta acotada linealmente."
            },
            {
                "question": "Restricción |α| ≤ |β|",
                "answer": "Garantiza que las derivaciones no acorten la cadena (lenguajes sensibles al contexto)."
            },
            {
                "question": "Diferencia entre GSC y GLC",
                "answer": "En GSC el lado izquierdo puede tener contexto, en GLC solo una variable."
            },
            {
                "question": "Ejemplo de lenguaje Sensible al Contexto",
                "answer": "L = {aⁿbⁿcⁿ | n ≥ 1} - requiere contar tres símbolos simultáneamente."
            },
            {
                "question": "Forma Normal de Kuroda",
                "answer": "Toda GSC puede transformarse a: A → BC, AB → CD, A → a"
            },
            {
                "question": "Aplicaciones de LSC",
                "answer": "Lenguajes de programación con dependencias contextuales, análisis semántico."
            },
            {
                "question": "Relación con problemas NP",
                "answer": "El problema de pertenencia para LSC es PSPACE-completo."
            },

            # TIPO 0 - RECURSIVAMENTE ENUMERABLE 
            {
                "question": "¿Qué caracteriza una gramática Tipo 0?",
                "answer": "No hay restricciones en las producciones: α → β con α conteniendo al menos una variable."
            },
            {
                "question": "¿Qué máquina reconoce lenguajes Tipo 0?",
                "answer": "Máquinas de Turing (MT) - modelo computacional más general."
            },
            {
                "question": "Ejemplo de gramática Tipo 0",
                "answer": "AB → BA, aB → ab, A → a (permite reordenamiento de símbolos)"
            },
            {
                "question": "¿Qué es un lenguaje Recursivamente Enumerable?",
                "answer": "Lenguaje para el cual existe una MT que lo acepta (puede no detenerse para cadenas no en L)."
            },
            {
                "question": "Diferencia entre RE y Recursivo",
                "answer": "En lenguajes recursivos, la MT siempre se detiene; en RE, puede loopear en cadenas no aceptadas."
            },
            {
                "question": "Problema de la parada",
                "answer": "Problema indecidible: no existe algoritmo para determinar si una MT se detendrá."
            },
            {
                "question": "Tesis de Church-Turing",
                "answer": "Todo algoritmo computable puede ser implementado en una Máquina de Turing."
            },
            {
                "question": "Aplicaciones de MT",
                "answer": "Modelo teórico para estudiar límites de la computación, complejidad, decidibilidad."
            },
            {
                "question": "Problemas indecidibles",
                "answer": "Problema de la parada, equivalencia de gramáticas, vacuidad de intersección para LLC."
            },
            {
                "question": "Jerarquía de Chomsky extendida",
                "answer": "Incluye subclases como: Recursivos, RE, CSL, CFL, Regular."
            }
        ]
    
    def setup_ui(self):
        self.buttons = [
            {
                "rect": pygame.Rect(150, 550, 200, 50),
                "text": "← Anterior",
                "action": "prev"
            },
            {
                "rect": pygame.Rect(400, 550, 200, 50),
                "text": "Mostrar Respuesta",
                "action": "toggle_answer"
            },
            {
                "rect": pygame.Rect(650, 550, 200, 50),
                "text": "Siguiente →",
                "action": "next"
            },
            {
                "rect": pygame.Rect(400, 620, 200, 50),
                "text": "🔀 Aleatorio",
                "action": "random"
            },
            {
                "rect": pygame.Rect(400, 690, 200, 50),
                "text": "Volver al Menú",
                "action": "menu"
            }
        ]
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for button in self.buttons:
                if button["rect"].collidepoint(event.pos):
                    result = self.execute_button_action(button["action"])
                    if result == "menu":
                        return "menu"
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.show_answer = not self.show_answer
            elif event.key == pygame.K_RIGHT:
                self.next_card()
            elif event.key == pygame.K_LEFT:
                self.prev_card()
            elif event.key == pygame.K_r:
                self.random_card()
            elif event.key == pygame.K_ESCAPE:
                return "menu"
    
    def execute_button_action(self, action):
        if action == "prev":
            self.prev_card()
        elif action == "next":
            self.next_card()
        elif action == "toggle_answer":
            self.show_answer = not self.show_answer
        elif action == "random":
            self.random_card()
        elif action == "menu":
            return "menu"
        return None
    
    def prev_card(self):
        self.current_card = (self.current_card - 1) % len(self.cards)
        self.show_answer = False
    
    def next_card(self):
        self.current_card = (self.current_card + 1) % len(self.cards)
        self.show_answer = False
    
    def random_card(self):
        self.current_card = random.randint(0, len(self.cards) - 1)
        self.show_answer = False
    
    def update(self):
        pass
    
    def draw(self):
        # Fondo
        self.screen.fill((30, 30, 60))
        
        # Título
        title_font = pygame.font.Font(None, 48)
        title = title_font.render("🎓 FLASHCARDS - Chomsky Hierarchy (80 cards)", True, (255, 255, 255))
        self.screen.blit(title, (self.screen.get_width() // 2 - title.get_width() // 2, 50))
        
        # Progreso
        progress_font = pygame.font.Font(None, 24)
        progress = progress_font.render(f"Card {self.current_card + 1}/{len(self.cards)}", True, (200, 200, 200))
        self.screen.blit(progress, (self.screen.get_width() // 2 - progress.get_width() // 2, 120))
        
        # Categoría actual
        category_font = pygame.font.Font(None, 20)
        categories = ["Conceptos Básicos", "Tipo 3 - Regular", "Tipo 2 - Libre Contexto", 
                     "Tipo 1 - Sensible Contexto", "Tipo 0 - Recursivamente Enumerable", "Autómatas"]
        category_idx = min(self.current_card // 15, 5)
        category_text = category_font.render(f"Categoría: {categories[category_idx]}", True, (150, 200, 255))
        self.screen.blit(category_text, (self.screen.get_width() // 2 - category_text.get_width() // 2, 150))
        
        # Carta (flashcard)
        card_rect = pygame.Rect(100, 200, self.screen.get_width() - 200, 300)
        pygame.draw.rect(self.screen, (255, 255, 255), card_rect, border_radius=15)
        pygame.draw.rect(self.screen, (100, 100, 100), card_rect, 3, border_radius=15)
        
        # Contenido de la carta
        card = self.cards[self.current_card]
        
        if not self.show_answer:
            # Mostrar pregunta
            question_font = pygame.font.Font(None, 28)
            question_text = self.wrap_text(card["question"], question_font, card_rect.width - 40)
            
            for i, line in enumerate(question_text):
                text_surf = question_font.render(line, True, (0, 0, 0))
                self.screen.blit(text_surf, (card_rect.centerx - text_surf.get_width() // 2, 
                                           card_rect.top + 50 + i * 35))
            
            # Indicador de click
            hint_font = pygame.font.Font(None, 20)
            hint = hint_font.render("Click 'Mostrar Respuesta' o presiona ESPACIO", True, (100, 100, 100))
            self.screen.blit(hint, (card_rect.centerx - hint.get_width() // 2, card_rect.bottom - 40))
        
        else:
            # Mostrar respuesta
            answer_font = pygame.font.Font(None, 24)
            answer_text = self.wrap_text(card["answer"], answer_font, card_rect.width - 40)
            
            for i, line in enumerate(answer_text):
                text_surf = answer_font.render(line, True, (0, 100, 0))
                self.screen.blit(text_surf, (card_rect.centerx - text_surf.get_width() // 2, 
                                           card_rect.top + 50 + i * 30))
        
        # Botones
        for button in self.buttons:
            color = (100, 150, 255) if button["rect"].collidepoint(pygame.mouse.get_pos()) else (200, 200, 200)
            pygame.draw.rect(self.screen, color, button["rect"], border_radius=8)
            pygame.draw.rect(self.screen, (50, 50, 50), button["rect"], 2, border_radius=8)
            
            button_font = pygame.font.Font(None, 20)
            text_surf = button_font.render(button["text"], True, (0, 0, 0))
            self.screen.blit(text_surf, (button["rect"].centerx - text_surf.get_width() // 2, 
                                       button["rect"].centery - text_surf.get_height() // 2))
        
        # Atajos de teclado
        shortcuts_font = pygame.font.Font(None, 18)
        shortcuts = [
            "ESPACIO: Mostrar/Ocultar respuesta",
            "FLECHAS: Navegar  |  R: Aleatorio  |  ESC: Menú"
        ]
        
        for i, shortcut in enumerate(shortcuts):
            text = shortcuts_font.render(shortcut, True, (150, 150, 150))
            self.screen.blit(text, (self.screen.get_width() // 2 - text.get_width() // 2, 750))
    
    def wrap_text(self, text, font, max_width):
        words = text.split(' ')
        lines = []
        current_line = []
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            test_surf = font.render(test_line, True, (0, 0, 0))
            
            if test_surf.get_width() <= max_width:
                current_line.append(word)
            else:
                lines.append(' '.join(current_line))
                current_line = [word]
        
        if current_line:
            lines.append(' '.join(current_line))
        
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
            
            self.update()
            self.draw()
            pygame.display.flip()
            clock.tick(60)
        
        return "menu"