import PyPDF2

def extract_signature(pdf_file):
    pdf = PyPDF2.PdfFileReader(pdf_file)
    if pdf.getSignature():
        signature = pdf.getSignature()
        return signature
    else:
        return None
from PyPDF2 import PdfFileWriter, PdfFileReader

def add_signature(inputpdf, outputpdf):
    # Load your input PDF
    pdfReader = PdfFileReader(inputpdf)
    pdfWriter = PdfFileWriter()
    
    # Add a signature page 
    pdfWriter.addPage(pdfReader.getPage(0))
    
    # Get the signature and cert
    signature = input("Signature: ")
    cert = input("Cert: ") # Base64 encoded string
    
    # Add the signature field
    pdfWriter.addAnnotation(
        name         = "Signature1",
        type         = "/Widget",
        lowerLeft    =   (50, 50), 
        lowerRight   =  (200 , 120 ),
        contents     =  signature,
        seal         = True,
        embeddedfile =  cert,        
        sigtype      =  "/DocMDP" 
    )
    
    # Write to output PDF
    with open(outputpdf, "wb") as out:
        pdfWriter.write(out)

-------------------------------------------------------------------
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
