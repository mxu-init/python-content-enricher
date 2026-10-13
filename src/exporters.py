from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

class TxtExporter:
    
    def export(self, filename: str, original: str, enriched: str, translated: str) -> None:
        if not filename.endswith(".txt"):
            filename = f"{filename}.txt"
            
        path = Path(filename)
        
        with open(path, "w", encoding="utf-8") as file:
            file.write("=== CONTENIDO ORIGINAL ===\n")
            file.write(f"{original}\n\n")
            
            file.write("=== CONTENIDO ENRIQUECIDO (IA) ===\n")
            file.write(f"{enriched}\n\n")
            
            file.write("=== CONTENIDO TRADUCIDO ===\n")
            file.write(f"{translated}\n")


class PdfExporter:
    
    def export(self, filename: str, original: str, enriched: str, translated: str) -> None:
        if not filename.endswith(".pdf"):
            filename = f"{filename}.pdf"
            
        path = Path(filename)
        
        doc = SimpleDocTemplate(str(path), pagesize=letter)
        styles = getSampleStyleSheet()
        story = []

        story.append(Paragraph("Contenido Original", styles["Heading1"]))
        story.append(Paragraph(original, styles["Normal"]))
        story.append(Spacer(1, 12))

        story.append(Paragraph("Contenido Enriquecido (IA)", styles["Heading1"]))
        story.append(Paragraph(enriched, styles["Normal"]))
        story.append(Spacer(1, 12))

        story.append(Paragraph("Contenido Traducido", styles["Heading1"]))
        story.append(Paragraph(translated, styles["Normal"]))

        doc.build(story)