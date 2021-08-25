import os
from io import BytesIO
from secrets import token_hex

import matplotlib.pyplot as plt
import statsmodels.api as sm
from reportlab.graphics import renderPDF
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
from svglib.svglib import svg2rlg


class ReportGenerator:
    """
    This class represents all operations for handling a file.

    Attributes
    ----------
    filename : str
        name of the file
    output_path : str
        path of the generated report file as String
    """

    def __init__(self, func, filename):
        directory = f"statistant/results/{func}_{filename}_{token_hex(5)}.pdf"
        parent_dir = os.path.expanduser("~")
        self.output_path = os.path.join(parent_dir, directory)

    def create_reg_report(self, model, x_col):
        """
        function for creating a report for regressions

        Parameters
        ----------
        x_col
        model
            model of regression plots
        """
        # plot regression
        fig = plt.figure(figsize=(6, 5))
        sm.graphics.plot_regress_exog(model, x_col, fig=fig)
        fig.tight_layout(pad=1.0)

        # save plot for report
        img_data = BytesIO()
        fig.savefig(img_data, format='svg')
        plt.clf()
        img_data.seek(0)  # rewind the data
        drawing = svg2rlg(img_data)  # convert svg to drawing

        c = canvas.Canvas(self.output_path)
        c.setFont("Helvetica", 10)

        # Regression plots at first half page
        renderPDF.draw(drawing, c, 10, 350)

        # summary on bottom of reg plots
        summary = model.summary().as_text()
        text_object = c.beginText(2 * cm, 350)
        for line in summary.splitlines(False):
            text_object.textLine(line.rstrip())
        c.drawText(text_object)

        c.showPage()
        c.save()
