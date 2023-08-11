
import zlib
import base64

with open('cert.pem', 'rb') as f:
    data = f.read()

compressed = zlib.compress(data)
b64_compressed = base64.b64encode(compressed)

print(f"Certificat original : {len(data)} octets")  
print(f"Certificat compressé : {len(b64_compressed)} octets")
-------------------
import binascii

def cert_pem_to_hex(pem_file):
    with open(pem_file, 'rb') as f:
        pem_data = f.read()
    hex_data = binascii.b2a_hex(pem_data).decode('ascii')
    return hex_data

def cert_hex_to_pem(hex_data, pem_file):
    bin_data = binascii.a2b_hex(hex_data.encode('ascii'))
    with open(pem_file, 'wb') as f:
        f.write(bin_data)

# Exemple
pem_hex = cert_pem_to_hex('cert.pem') 
print(pem_hex)

cert_hex_to_pem(pem_hex, 'new_cert.pem')


------------------------
import PyPDF2

def extraire_signature_pdf(nom_fichier):
    try:
        with open(nom_fichier, 'rb') as fichier_pdf:
            lecteur_pdf = PyPDF2.PdfFileReader(fichier_pdf)
            nb_pages = lecteur_pdf.getNumPages()
            
            for num_page in range(nb_pages):
                page = lecteur_pdf.getPage(num_page)
                annotations = page['/Annots']
                
                if annotations:
                    for annotation in annotations:
                        if annotation['/Subtype'] == '/Widget' and annotation['/FT'] == '/Sig':
                            # Objet de signature trouvé
                            return annotation
                        
            # Aucun objet de signature trouvé
            return None
        
    except FileNotFoundError:
        print("Le fichier PDF spécifié est introuvable.")


import pdfrw

def ajouter_champ_signature_pdf(nom_fichier, nom_champ):
    try:
        template_pdf = pdfrw.PdfReader(nom_fichier)
        
        # Créer un nouveau champ de signature
        new_field = pdfrw.PdfDict(
            FT='/Sig',
            Ff=1,
            V='',
            P=template_pdf.pages[0]
        )
        
        # Ajouter le champ de signature aux annotations de la première page
        template_pdf.pages[0][pdfrw.PdfName.Annots].append(new_field)
        
        # Attribuer un nom au champ de signature
        template_pdf.Root.AcroForm.Fields.append(pdfrw.PdfDict(
            T=nom_champ,
            V=template_pdf.pages[0][pdfrw.PdfName.Annots][-1]
        ))
        
        # Écrire les modifications dans un nouveau fichier PDF
        nouveau_fichier = f"nouveau_{nom_fichier}"
        pdfrw.PdfWriter().write(nouveau_fichier, template_pdf)
        
        print(f"Champ de signature '{nom_champ}' ajouté avec succès au fichier '{nouveau_fichier}'.")
        
    except FileNotFoundError:
        print("Le fichier PDF spécifié est introuvable.")
-----------------------------------------------------------------------------------------------------------------------------
import PyPDF2

with open('file.pdf', 'rb') as f:
    pdf = PyPDF2.PdfFileReader(f)
    signature_obj = pdf.getPage(0).getAnnotations()[0]
    print(signature_obj.getSubject())
------------------------------------------------------------------
import PyPDF2
annotation.update({
        NameObject('/Type'): NameObject('/Annot'),
        NameObject('/Subtype'): NameObject('/Widget'),
        NameObject('/FT'): NameObject('/Sig'),
        NameObject('/Rect'): createStringObject('[100 100 200 200]'),  # Coordonnées du rectangle de l'annotation
        NameObject('/T'): createStringObject('MaSignature'),  # Nom de l'annotation
        NameObject('/V'): createStringObject(''),  # Valeur de l'annotation (vide pour une signature)
        NameObject('/AP'): createStringObject(''),  # Apparence de l'annotation (vide pour une signature)
        NameObject('/P'): pdf.getPage(0),  # Page sur laquelle ajouter l'annotation (première page ici)
    })

import PyPDF2

def extract_signature(pdf_file):
    pdf = PyPDF2.PdfFileReader(pdf_file)
    if '/VRI' in pdf.trailer:    
        vri = pdf.getVRI()
        return vri   
    else:
        return None

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
