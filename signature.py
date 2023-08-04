import hashlib

def sha512_for_pdf(pdf_path):
    hash = hashlib.sha512()
    with open(pdf_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash.update(chunk)
    return hash.hexdigest()

pdf_path = 'document.pdf'
pdf_hash = sha512_for_pdf(pdf_path)
print(pdf_hash)
