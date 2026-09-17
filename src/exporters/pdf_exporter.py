from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

class PdfExporter:
    def export(self,data,output_file):
        doc=SimpleDocTemplate(output_file)
        styles=getSampleStyleSheet()
        content=[Paragraph(str(data),styles["BodyText"])]
        doc.build(content)
        return output_file
