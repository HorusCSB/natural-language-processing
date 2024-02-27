from PyPDF2 import PdfReader

# LER
# ver numero
# pegar a pagina
# extrair texto

texts = {}
for i in range(10):
    texts['arq'+str(i)] = []
    
for project in range(10):
    reader = PdfReader("./pdf/PDF.js viewer"+str(project)+".pdf")
    number_of_pages = len(reader.pages)
    for pageNumber in range(number_of_pages):
        page = reader.pages[pageNumber]
        pageText = page.extract_text()
        texts['arq'+str(project)].append(pageText)
