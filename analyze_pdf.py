import pdfplumber
import re

def analyze_pdf_structure(pdf_path):
    """Analyze PDF structure to understand question format"""
    
    with pdfplumber.open(pdf_path) as pdf:
        print(f"PDF heeft {len(pdf.pages)} paginas")
        
        # Lees eerste paar pagina's voor analyse
        for page_num in range(min(3, len(pdf.pages))):
            print(f"\n=== PAGINA {page_num + 1} ===")
            text = pdf.pages[page_num].extract_text()
            
            if text:
                lines = text.split('\n')
                print(f"Aantal lijnen: {len(lines)}")
                
                # Toon eerste 20 lijnen
                for i, line in enumerate(lines[:20]):
                    if line.strip():
                        print(f"{i+1:2d}: {line}")
                
                print("...")
                
                # Zoek naar vraag patronen in deze pagina
                question_patterns = [
                    r'\b(\d+)\.\s',
                    r'\bQ(\d+)',
                    r'Question\s+(\d+)',
                    r'\b(\d+)\)',
                ]
                
                for pattern in question_patterns:
                    matches = re.findall(pattern, text)
                    if matches:
                        print(f"Patroon '{pattern}' gevonden: {matches[:5]}")

if __name__ == "__main__":
    analyze_pdf_structure("/root/quiz-app/PSPO1_v1.2.1.pdf")