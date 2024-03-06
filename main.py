from PyPDF2 import PdfReader, PdfWriter
import os
import nltk
nltk.download('punkt')
nltk.download('stopwords')
# install wkhtmltopdf ubuntu
import pdfkit
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Criar diretório para os PDFs sem stopwords
outputDirectory = "./pdf_no_stop_words"
os.makedirs(outputDirectory, exist_ok=True)

# Ler stopwords da biblioteca NLTK
stop_words = set(stopwords.words('english'))

texts = {}
for i in range(10):
    texts['arq'+str(i)] = []
    
for project in range(10):
    reader = PdfReader(f"./pdf/PDF.js viewer"+str(project)+".pdf")
    writer = PdfWriter()
    
    numberOfPages = len(reader.pages)
    
    
    texts['arq'+str(project)].append('')
    for pageNumber in range(numberOfPages):
        page = reader.pages[pageNumber]
        
        pageText = page.extract_text()
        # tokenize_words = word_tokenize(pageText)
        tokenize_words = word_tokenize(pageText)
        
        texts['arq'+str(project)][project] = tokenize_words
        
        # texts['arq'+str(project)].append(tokenize_words)
        
        pageTextWithoutStopWords = ' '.join([word for word in tokenize_words if word.lower() not in stop_words])
        
    # Salvar o novo PDF sem stopwords
    output_file = os.path.join(outputDirectory, f"PDF_no_stop_words_viewer{str(project)}.pdf")
    pdfkit.from_string(texts['arq'+str(project)][project], output_file)
    
print("PDFs sem stopwords foram salvos na pasta 'pdf_no_stop_words'.")
