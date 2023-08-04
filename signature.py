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
-------------------------------------------------------------------------
# Extraction de l'objet signature
from pdfrw import PdfReader

def get_signature_object(pdf_path):
    pdf = PdfReader(pdf_path)
    if "/SigFlags" in pdf.trailers[0]:
        return pdf.trailers[0]["/Root"]["/AcroForm"]["/Fields"]["/Signature1"]
    else:
        return None

# Ajout d'un champ de signature
from pdfrw import PdfReader, PdfWriter, PdfDict, PdfName

def add_signature_field(pdf_path, output_path, cert_file):
    pdf = PdfReader(pdf_path)
    signature = PdfDict(
        Type = PdfName.Sig,
        Filter = PdfName.Adobe_PPKLite,
        SubFilter = PdfName.ETSI_CADES_DETACHED,
        Contents = (PdfName.DocMDP, PdfName.AuthEvent),
        Reason = "Signature",
        M = PdfName.Date,
        Location = "Paris",
        ContactInfo = "John Doe"
    )
    signature_field = PdfDict(
        FT = PdfName.Sig,
        T = signature,
        V = PdfName.Unchanged,
        P = PdfDict(Reference=[PdfDict(Type=PdfName.SigRef, TransformMethod=PdfName.DocMDP, TransformParams=PdfDict(Type=PdfName.TransformParams, V=PdfName.DocMDP))]),
        Ff = PdfDict(Ff = PdfName.FixedPrint),
    )
    pdf.Root.AcroForm.Fields.Signature1 = signature_field
    
    writer = PdfWriter()
    writer.addpages(pdf.pages)
    writer.trailer = pdf
    writer.write(output_path, certify=cert_file)
