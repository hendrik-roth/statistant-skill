from reportlab.graphics import renderPDF
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas


class ReportGenerator:
    def __init__(self, output_path):
        self.output_path = output_path

    def create_reg_report(self, drawing, summary: str):
        """
        function for creating a report for regressions

        Parameters
        ----------
        drawing
            drawing of regression plots
        summary
            summary of regression
        """
        c = canvas.Canvas(self.output_path)
        c.setFont("Helvetica", 10)

        # Regression plots at first half page
        renderPDF.draw(drawing, c, 10, 350)

        # summary on bottom of reg plots
        text_object = c.beginText(2 * cm, 350)
        for line in summary.splitlines(False):
            text_object.textLine(line.rstrip())
        c.drawText(text_object)

        c.showPage()
        c.save()
