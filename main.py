import os
from PyPDF2 import PdfReader
import re
import nltk
nltk.download("stopwords")
nltk.download("punkt")
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import CountVectorizer

# Criar diretório para os textos sem stopwords
output_directory = "./pdf_no_stop_words"
os.makedirs(output_directory, exist_ok=True)

# Ler stopwords da biblioteca NLTK
stop_words = set(stopwords.words('english'))

# Processar os arquivos PDF
all_texts_without_stop_words = []

def extract_article_info(text):
    # Exemplo simples: procurar por palavras-chave nas seções relevantes
    objective = ""
    problem = ""
    method = ""
    contribution = ""

    objective_pattern = re.compile(r"aim[s](.*?\.)", re.DOTALL | re.IGNORECASE)
    problem_pattern = re.compile(r"problem[s](.*?\.)", re.DOTALL | re.IGNORECASE)
    method_pattern = re.compile(r"method(.*?\.)", re.DOTALL | re.IGNORECASE)
    contribution_pattern = re.compile(r"contribute[s]?(.*?\.)", re.DOTALL | re.IGNORECASE)

    objective_match = objective_pattern.search(text)
    problem_match = problem_pattern.search(text)
    method_match = method_pattern.search(text)
    contribution_match = contribution_pattern.search(text)

    if objective_match:
        objective = objective_match.group(1).strip()
    if problem_match:
        problem = problem_match.group(1).strip()
    if method_match:
        method = method_match.group(1).strip()
    if contribution_match:
        contribution = contribution_match.group(1).strip()

    return objective, problem, method, contribution


for project in range(10):
    texts_without_stop_words = []
    reader = PdfReader(f"./pdf/PDF.js viewer{project}.pdf")
    number_of_pages = len(reader.pages)

    # Extrair texto e remover stopwords para cada página
    for pageNumber in range(number_of_pages):
        page = reader.pages[pageNumber]
        page_text = page.extract_text()
        tokenize_words = word_tokenize(page_text)
        page_text_without_stop_words = ' '.join([word for word in tokenize_words if word.lower() not in stop_words])
        texts_without_stop_words.append(page_text_without_stop_words)
    
    # Salvar o texto sem stopwords em um novo arquivo
    output_file = os.path.join(output_directory, f"PDF_no_stop_words_viewer{project}.txt")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write('\n'.join(texts_without_stop_words))

    # Adicionar texto sem stopwords à lista para análise de bag-of-words
    all_texts_without_stop_words.extend(texts_without_stop_words)


for project in range(10):
    objective, problem, method, contribution = extract_article_info(all_texts_without_stop_words[project])

    # Imprimir as informações
    print(f"Projeto {project + 1}:")
    print("Objetivo:", objective)
    print("Problema:", problem)
    print("Método:", method)
    print("Contribuição:", contribution)
    print()


# Utilizar modelo bag-of-words para contar frequência de termos
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(all_texts_without_stop_words)
terms = vectorizer.get_feature_names_out()

# Calcular a soma das contagens para cada termo
term_counts = X.sum(axis=0).A1

# Criar um dicionário com termos e suas contagens
term_count_dict = dict(zip(terms, term_counts))

# Classificar os termos por contagem e identificar os 10 mais citados
top_terms = sorted(term_count_dict.items(), key=lambda x: x[1], reverse=True)[:10]
print("Top 10 termos mais citados nos artigos:")
for term, count in top_terms:
    print(f"{term}: {count}")

