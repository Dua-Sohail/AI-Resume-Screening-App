import PyPDF2
import docx2txt

def extract_text(file):
    if file.name.endswith(".pdf"):
        pdf = PyPDF2.PdfReader(file)
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
        return text

    elif file.name.endswith(".docx"):
        return docx2txt.process(file)

    else:
        return file.read().decode("utf-8")


def clean_text(text):
    text=text.lower()

    text= re.sub(r'[^a-zA-z\s]', '',text)

    text= ' '.join(text.split())

    stop_words= set(stopwords.words('english'))
    words= text.split()
    words =[ word for word in words if word not in stop_words]
    text = ' '.join(words)
    
    return text