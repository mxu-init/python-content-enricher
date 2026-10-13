from pathlib import Path

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