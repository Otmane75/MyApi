import hashlib
import PyPDF2

def calculate_sha512_pdf_hash(file_path):
    # Ouvrir le document PDF en mode binaire
    with open(file_path, "rb") as pdf_file:
        # Créer un objet de hachage SHA-512
        sha512_hash = hashlib.sha512()

        # Initialiser un objet PDF pour lire le contenu du fichier
        pdf_reader = PyPDF2.PdfFileReader(pdf_file)

        # Calculer le hachage du contenu du document PDF
        for page_num in range(pdf_reader.numPages):
            page = pdf_reader.getPage(page_num)
            sha512_hash.update(page.extractText().encode('utf-8'))

        # Renvoyer le hachage sous forme hexadécimale
        return sha512_hash.hexdigest()

# Exemple d'utilisation
document_path = "chemin/vers/votre/document.pdf"
pdf_hash = calculate_sha512_pdf_hash(document_path)
print("Le hash SHA-512 du document PDF est :", pdf_hash)
