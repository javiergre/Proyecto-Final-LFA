from fpdf import FPDF
from datetime import datetime
import os


class ReportGenerator:
    def __init__(self):
        self.output_dir = "reports"
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def _safe(self, text: str) -> str:
        if text is None:
            return ""
        if not isinstance(text, str):
            text = str(text)
        return text.encode("latin-1", "ignore").decode("latin-1")

    def generate_pdf(self, classification_result, grammar_text=None):
        pdf = FPDF()
        pdf.add_page()

        # Encabezado
        pdf.set_font("Arial", "B", 16)
        pdf.cell(
            0,
            10,
            self._safe("Chomsky Classifier AI - Reporte de análisis"),
            0,
            1,
            "C",
        )
        pdf.ln(5)

        # Fecha
        pdf.set_font("Arial", "I", 10)
        pdf.cell(
            0,
            10,
            self._safe(
                f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            ),
            0,
            1,
        )
        pdf.ln(5)

        # Gramática analizada
        if grammar_text:
            pdf.set_font("Arial", "B", 12)
            pdf.cell(0, 10, self._safe("Entrada analizada"), 0, 1)
            pdf.set_font("Arial", "", 10)

            grammar_lines = grammar_text.split("\n")
            for line in grammar_lines[:10]:
                clean = line.strip()
                if clean and not clean.startswith("#"):
                    pdf.cell(0, 6, self._safe(clean), 0, 1)
            pdf.ln(5)

        # Resultado de clasificación
        pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 10, self._safe("Resultado de la clasificación:"), 0, 1)

        pdf.set_font("Arial", "B", 12)
        pdf.cell(
            0,
            8,
            self._safe(f"Tipo: {classification_result.get('type', 'N/A')}"),
            0,
            1,
        )

        pdf.set_font("Arial", "", 10)
        pdf.multi_cell(
            0,
            5,
            self._safe(
                f"Descripción: {classification_result.get('description', '')}"
            ),
        )
        pdf.ln(5)

        # Detalle del análisis 
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 10, self._safe("Proceso de análisis:"), 0, 1)
        pdf.set_font("Arial", "", 9)

        y_pos = pdf.get_y()
        steps = classification_result.get("steps", [])

        for step in steps:
            step = self._safe(step)
            if y_pos > 260:
                pdf.add_page()
                y_pos = 20
                pdf.set_y(y_pos)

            pdf.multi_cell(0, 4, step)
            y_pos = pdf.get_y()

        # Pie de página
        pdf.set_y(-15)
        pdf.set_font("Arial", "I", 8)
        pdf.cell(
            0,
            10,
            self._safe(
                "Generado por Chomsky Classifier AI - Proyecto final de Teoría de la Computación"
            ),
            0,
            0,
            "C",
        )

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"chomsky_report_{timestamp}.pdf"
        filepath = os.path.join(self.output_dir, filename)
        pdf.output(filepath)

        return filename
