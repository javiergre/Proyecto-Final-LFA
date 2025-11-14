import pygame
from classifier import ChomskyClassifier
from grammar_parser import GrammarParser
from visualizer import GrammarVisualizer
from report_generator import ReportGenerator


class ClassifierUI:
    def __init__(self, screen, assets):
        self.screen = screen
        self.assets = assets
        self.classifier = ChomskyClassifier()
        self.parser = GrammarParser()
        self.visualizer = GrammarVisualizer()
        self.report_generator = ReportGenerator()

        # Texto de entrada y resultado
        self.input_text = ""
        self.result = None
        self.running = True

        # Editor de texto
        self.cursor_pos = 0          # índice en el string
        self.selection_start = None  # None = sin selección
        self.cursor_visible = True
        self.cursor_timer = 0

        # Áreas de entrada y salida
        self.input_rect = pygame.Rect(60, 120, 900, 260)
        self.output_rect = pygame.Rect(60, 420, 900, 260)

        self.buttons = []
        self.active_input = True

        # Fuentes
        try:
            self.editor_font = pygame.font.Font("DejaVuSansMono.ttf", 24)
            self.result_font = pygame.font.Font("DejaVuSansMono.ttf", 20)
        except Exception:
            # Por si no se encuentra el archivo, usar la default
            self.editor_font = pygame.font.Font(None, 24)
            self.result_font = pygame.font.Font(None, 20)

        self.ui_font_small = pygame.font.Font(None, 22)
        self.ui_font_button = pygame.font.Font(None, 26)
        self.ui_font_title = pygame.font.Font(None, 40)

        self.setup_ui()

    # -------------------- CONFIGURACIÓN --------------------

    def setup_ui(self):
        self.buttons = [
            {
                "rect": pygame.Rect(60, 390, 160, 40),
                "text": "Clasificar",
                "action": "classify",
            },
            {
                "rect": pygame.Rect(240, 390, 200, 40),
                "text": "Generar diagrama",
                "action": "visualize",
            },
            {
                "rect": pygame.Rect(460, 390, 160, 40),
                "text": "Exportar PDF",
                "action": "export_pdf",
            },
            {
                "rect": pygame.Rect(640, 390, 160, 40),
                "text": "Cargar ejemplo",
                "action": "load_example",
            },
            {
                "rect": pygame.Rect(60, 700, 260, 40),
                "text": "Comparar gramáticas",
                "action": "compare",
            },
            {
                "rect": pygame.Rect(700, 700, 260, 40),
                "text": "Volver al menú",
                "action": "menu",
            },
        ]

    # -------------------- LOOP PRINCIPAL --------------------

    def run(self):
        clock = pygame.time.Clock()
        self.running = True

        while self.running:
            for event in pygame.event.get():
                result = self.handle_event(event)
                if result == "menu":
                    return "menu"
                if result == "quit":
                    return "quit"

            self.cursor_blink()
            self.draw()
            pygame.display.flip()
            clock.tick(60)

    # -------------------- EVENTOS --------------------

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            return "quit"

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.input_rect.collidepoint(event.pos):
                self.active_input = True
            else:
                self.active_input = False

            if event.button == 1:
                for button in self.buttons:
                    if button["rect"].collidepoint(event.pos):
                        self.execute_action(button["action"])

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return "menu"

            # Atajos globales
            if event.key == pygame.K_F1:
                self.classify_grammar()
                return
            elif event.key == pygame.K_F2:
                self.load_example()
                return

            if self.active_input:
                self.handle_text_input(event)

    # -------------------- MANEJO DE TEXTO (EDITOR) --------------------

    def handle_text_input(self, event):
        mods = pygame.key.get_mods()
        ctrl = mods & pygame.KMOD_CTRL

        if ctrl:
            if event.key == pygame.K_a:  # Ctrl + A
                self.selection_start = 0
                self.cursor_pos = len(self.input_text)
                return
            elif event.key == pygame.K_c:  # Ctrl + C
                self.copy_selection()
                return
            elif event.key == pygame.K_v:  # Ctrl + V
                self.paste_clipboard()
                return

        # --- Movimiento del cursor ---
        if event.key == pygame.K_LEFT:
            if self.cursor_pos > 0:
                self.cursor_pos -= 1
            self.selection_start = None

        elif event.key == pygame.K_RIGHT:
            if self.cursor_pos < len(self.input_text):
                self.cursor_pos += 1
            self.selection_start = None

        elif event.key == pygame.K_HOME:
            self.move_cursor_line_home()
            self.selection_start = None

        elif event.key == pygame.K_END:
            self.move_cursor_line_end()
            self.selection_start = None

        elif event.key == pygame.K_UP:
            self.move_cursor_vertical(-1)
            self.selection_start = None

        elif event.key == pygame.K_DOWN:
            self.move_cursor_vertical(1)
            self.selection_start = None

        # --- Borrado ---
        elif event.key == pygame.K_BACKSPACE:
            if self.has_selection():
                self.delete_selection()
            elif self.cursor_pos > 0:
                self.input_text = (
                    self.input_text[: self.cursor_pos - 1]
                    + self.input_text[self.cursor_pos :]
                )
                self.cursor_pos -= 1

        elif event.key == pygame.K_DELETE:
            if self.has_selection():
                self.delete_selection()
            elif self.cursor_pos < len(self.input_text):
                self.input_text = (
                    self.input_text[: self.cursor_pos]
                    + self.input_text[self.cursor_pos + 1 :]
                )

        # --- Saltos y tabulación ---
        elif event.key == pygame.K_RETURN:
            self.insert_text("\n")

        elif event.key == pygame.K_TAB:
            self.insert_text("    ")

        # --- Texto normal ---
        else:
            if event.unicode and not ctrl:
                self.insert_text(event.unicode)

    # Utilidades de edición
    def has_selection(self):
        return (
            self.selection_start is not None
            and self.selection_start != self.cursor_pos
        )

    def insert_text(self, text):
        if self.has_selection():
            self.delete_selection()
        self.input_text = (
            self.input_text[: self.cursor_pos]
            + text
            + self.input_text[self.cursor_pos :]
        )
        self.cursor_pos += len(text)
        self.selection_start = None

    def delete_selection(self):
        start = min(self.selection_start, self.cursor_pos)
        end = max(self.selection_start, self.cursor_pos)
        self.input_text = self.input_text[:start] + self.input_text[end:]
        self.cursor_pos = start
        self.selection_start = None

    def copy_selection(self):
        if not self.has_selection():
            return
        start = min(self.selection_start, self.cursor_pos)
        end = max(self.selection_start, self.cursor_pos)
        selected = self.input_text[start:end]
        try:
            import pyperclip

            pyperclip.copy(selected)
        except Exception:
            # Si no existe pyperclip o falla, se ignora
            pass

    def paste_clipboard(self):
        try:
            import pyperclip

            clip = pyperclip.paste()
        except Exception:
            clip = ""
        if clip:
            clip = clip.replace("\r\n", "\n").replace("\r", "\n")
            self.insert_text(clip)

    def move_cursor_line_home(self):
        before = self.input_text[: self.cursor_pos]
        last_newline = before.rfind("\n")
        if last_newline == -1:
            self.cursor_pos = 0
        else:
            self.cursor_pos = last_newline + 1

    def move_cursor_line_end(self):
        after = self.input_text[self.cursor_pos :]
        next_newline = after.find("\n")
        if next_newline == -1:
            self.cursor_pos = len(self.input_text)
        else:
            self.cursor_pos += next_newline

    def move_cursor_vertical(self, direction):
        lines = self.input_text.split("\n")

        # localizar línea y columna actuales
        total = 0
        line_index = 0
        col = 0
        for i, line in enumerate(lines):
            line_len = len(line)
            if self.cursor_pos <= total + line_len:
                line_index = i
                col = self.cursor_pos - total
                break
            total += len(line) + 1  # +1 por el '\n'

        new_line = line_index + direction
        if new_line < 0 or new_line >= len(lines):
            return

        new_line_len = len(lines[new_line])
        new_col = min(col, new_line_len)

        # calcular nueva posición absoluta
        new_pos = 0
        for i in range(new_line):
            new_pos += len(lines[i]) + 1
        new_pos += new_col
        self.cursor_pos = new_pos

    def cursor_blink(self):
        self.cursor_timer += 1
        if self.cursor_timer >= 30:
            self.cursor_visible = not self.cursor_visible
            self.cursor_timer = 0

    # -------------------- ACCIONES LÓGICAS --------------------

    def execute_action(self, action):
        if action == "classify":
            self.classify_grammar()
        elif action == "visualize":
            self.visualize_grammar()
        elif action == "export_pdf":
            self.export_pdf()
        elif action == "load_example":
            self.load_example()
        elif action == "compare":
            self.compare_grammars()
        elif action == "menu":
            self.running = False

    def classify_grammar(self):
        try:
            productions = self.parser.parse_grammar(self.input_text)

            if productions:
                self.result = self.classifier.classify(productions)
            else:
                # Si no se pudo parsear como gramática, probar como autómata
                self.result = self.classifier.classify_automaton_from_text(
                    self.input_text
                )
        except Exception as e:
            self.result = {
                "type": "Error",
                "description": "Error en el análisis",
                "explanation": f"Error: {str(e)}",
                "steps": [f"Error al procesar la entrada: {str(e)}"],
            }

    def visualize_grammar(self):
        if not self.input_text.strip():
            self.result = {
                "type": "Error",
                "description": "No hay entrada para visualizar",
                "explanation": "Ingrese una gramática o un autómata antes de generar el diagrama.",
                "steps": [],
            }
            return

        # 1) Intentar como gramática
        productions = self.parser.parse_grammar(self.input_text)
        if productions:
            try:
                path = self.visualizer.generate_diagram(productions)
                self.result = {
                    "type": "Información",
                    "description": "Diagrama de gramática generado",
                    "explanation": f"Se generó el diagrama de la gramática en: {path}",
                    "steps": [
                        "Se detectaron producciones válidas de gramática.",
                        f"Diagrama de derivaciones generado en: {path}",
                    ],
                }
            except Exception as e:
                self.result = {
                    "type": "Error",
                    "description": "Error al generar diagrama de gramática",
                    "explanation": f"Error: {str(e)}",
                    "steps": [f"Error al generar diagrama: {str(e)}"],
                }
            return

        # 2) Si no hay producciones, intentar como autómata / MT
        try:
            path = self.visualizer.generate_automaton_diagram_from_text(self.input_text)
            self.result = {
                "type": "Información",
                "description": "Diagrama de autómata / Máquina de Turing generado",
                "explanation": f"Se generó un diagrama de estados en: {path}",
                "steps": [
                    "No se reconocieron producciones de gramática.",
                    "La entrada parece describir un autómata o Máquina de Turing.",
                    f"Se generó un grafo de estados usando Graphviz en: {path}",
                ],
            }
        except Exception as e:
            self.result = {
                "type": "Error",
                "description": "Error al generar diagrama de autómata / MT",
                "explanation": f"Error: {str(e)}",
                "steps": [f"Error al generar diagrama de autómata: {str(e)}"],
            }


    def export_pdf(self):
        try:
            # Intentar parsear como gramática
            productions = self.parser.parse_grammar(self.input_text)

            if productions:
                classification_result = self.classifier.classify(productions)
            else:
                # Si no hay producciones, se trata como autómata / MT
                classification_result = self.classifier.classify_automaton_from_text(
                    self.input_text
                )

            filename = self.report_generator.generate_pdf(
                classification_result,
                grammar_text=self.input_text
            )

            # Actualiza el resultado mostrado en pantalla
            self.result = {
                "type": classification_result["type"],
                "description": f"Reporte exportado correctamente como {filename}",
                "explanation": classification_result["explanation"],
                "steps": classification_result["steps"] + [
                    f"Reporte PDF generado: {filename}"
                ],
            }

        except Exception as e:
            self.result = {
                "type": "Error",
                "description": "Error al generar PDF",
                "explanation": f"Error: {str(e)}",
                "steps": [f"Error al generar PDF: {str(e)}"],
            }


    def load_example(self):
        example = [
            "# Ejemplo: lenguaje { a^n b^n | n ≥ 1 }",
            "S -> aSB | ab",
            "B -> b",
        ]
        self.input_text = "\n".join(example)
        self.cursor_pos = len(self.input_text)
        self.selection_start = None

    def compare_grammars(self):
        """
        Convención:
        Gramática 1
        ---
        Gramática 2
        """
        try:
            parts = self.input_text.split("---")
            if len(parts) < 2:
                self.result = {
                    "type": "Comparación",
                    "description": "Entrada insuficiente",
                    "explanation": (
                        "Para comparar, escriba la primera gramática, luego una línea con '---', "
                        "y después la segunda gramática."
                    ),
                    "steps": [
                        "Formato esperado:",
                        "Gramática 1",
                        "---",
                        "Gramática 2",
                    ],
                }
                return

            g1_text = parts[0]
            g2_text = parts[1]

            productions1 = self.parser.parse_grammar(g1_text)
            productions2 = self.parser.parse_grammar(g2_text)

            self.result = self.classifier.compare_grammars(
                productions1, productions2
            )

        except Exception as e:
            self.result = {
                "type": "Error",
                "description": "Error en comparación",
                "explanation": f"Error al comparar gramáticas: {str(e)}",
                "steps": [f"Error al comparar: {str(e)}"],
            }

    # -------------------- DIBUJO --------------------

    def draw(self):
        self.screen.fill((30, 30, 60))
        width = self.screen.get_width()

        # Título
        title = self.ui_font_title.render(
            "Clasificador de gramáticas - Jerarquía de Chomsky",
            True,
            (255, 255, 255),
        )
        self.screen.blit(
            title,
            (width // 2 - title.get_width() // 2, 30),
        )

        # Instrucciones
        info_lines = [
            "Ingrese su gramática o descripción de autómata en el cuadro de abajo.",
            "Formato de producción: Variable -> símbolos ",
            "Ejemplo: S -> aSB | ab | ε",
            "Atajos: F1 = Clasificar, F2 = Cargar ejemplo, ESC = Volver al menú",
            "Edición: Ctrl+A/C/V, flechas, Enter, Tab.",
        ]
        for i, line in enumerate(info_lines):
            text = self.ui_font_small.render(line, True, (210, 210, 210))
            self.screen.blit(text, (60, 80 + i * 18))

        # Área de entrada
        pygame.draw.rect(self.screen, (230, 230, 230), self.input_rect, border_radius=6)
        pygame.draw.rect(self.screen, (80, 80, 80), self.input_rect, 2, border_radius=6)
        self.draw_editor_text()

        # Botones
        for button in self.buttons:
            rect = button["rect"]
            color = (90, 140, 240)
            pygame.draw.rect(self.screen, color, rect, border_radius=8)
            pygame.draw.rect(self.screen, (255, 255, 255), rect, 2, border_radius=8)

            text = self.ui_font_button.render(button["text"], True, (255, 255, 255))
            self.screen.blit(
                text,
                (
                    rect.centerx - text.get_width() // 2,
                    rect.centery - text.get_height() // 2,
                ),
            )

        # Área de resultado
        pygame.draw.rect(
            self.screen, (245, 245, 245), self.output_rect, border_radius=6
        )
        pygame.draw.rect(self.screen, (80, 80, 80), self.output_rect, 2, border_radius=6)

        result_title_font = pygame.font.Font(None, 28)
        result_title = result_title_font.render(
            "Resultado del análisis:", True, (0, 0, 0)
        )
        self.screen.blit(
            result_title, (self.output_rect.x + 10, self.output_rect.y + 10)
        )

        if self.result:
            text_area = self.output_rect.copy()
            text_area.x += 10
            text_area.y += 40
            text_area.width -= 20
            text_area.height -= 50

            explanation = self.result.get("explanation", "")
            self.draw_text_block(
                explanation, text_area, self.result_font, (0, 0, 0)
            )
        else:
            default_font = pygame.font.Font(None, 22)
            default_text = default_font.render(
                "Ingrese una gramática o autómata y haga clic en 'Clasificar'.",
                True,
                (120, 120, 120),
            )
            self.screen.blit(
                default_text,
                (
                    self.output_rect.centerx - default_text.get_width() // 2,
                    self.output_rect.centery - default_text.get_height() // 2,
                ),
            )

    # --- Dibujo del editor ---

    def draw_editor_text(self):
        rect = self.input_rect
        font = self.editor_font
        line_height = font.get_linesize()

        lines = self.input_text.split("\n")

        y = rect.y + 4
        index_counter = 0  # para saber dónde está cada carácter

        for line in lines:
            if y + line_height > rect.bottom:
                break

            # Dibujar texto
            text_surface = font.render(line, True, (0, 0, 0))
            self.screen.blit(text_surface, (rect.x + 4, y))

            # Si el cursor está en esta línea, se calcula su posición
            start_index = index_counter
            end_index = index_counter + len(line)
            if start_index <= self.cursor_pos <= end_index:
                if self.cursor_visible and self.active_input:
                    col = self.cursor_pos - start_index
                    caret_x = rect.x + 4 + font.size(line[:col])[0]
                    caret_y1 = y
                    caret_y2 = y + line_height - 2
                    pygame.draw.line(
                        self.screen,
                        (0, 0, 0),
                        (caret_x, caret_y1),
                        (caret_x, caret_y2),
                        2,
                    )

            index_counter += len(line) + 1  # +1 por el '\n'
            y += line_height

    def draw_text_block(self, text, rect, font, color):
        # 1) Normalizar unicode para evitar símbolos rotos
        import unicodedata

        text = unicodedata.normalize("NFKC", text)

        # 2) Reemplazar saltos raros
        text = text.replace("\r\n", "\n").replace("\r", "\n")

        # 3) Limpiar caracteres no imprimibles que generan �
        cleaned = ""
        for ch in text:
            if ch == "\n" or ch == "\t" or ch == " ":
                cleaned += ch
            elif ord(ch) >= 32:  # caracteres imprimibles
                cleaned += ch
            # Si no, se omite.

        text = cleaned

        # 4) Word wrapping básico
        words = text.split(" ")
        lines = []
        current = ""

        for word in words:
            test = (current + " " + word).strip()
            w, _ = font.size(test)
            if w <= rect.width:
                current = test
            else:
                lines.append(current)
                current = word

        if current:
            lines.append(current)

        # 5) Dibujar líneas dentro del rectángulo
        y = rect.y
        for line in lines:
            if y + font.get_linesize() > rect.bottom:
                break
            surf = font.render(line, True, color)
            self.screen.blit(surf, (rect.x, y))
            y += font.get_linesize()
