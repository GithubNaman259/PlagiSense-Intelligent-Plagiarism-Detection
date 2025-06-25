import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

from nltk.corpus import stopwords,wordnet
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from sentence_transformers import SentenceTransformer,util

stop_words=set(stopwords.words('english'))
lemmatizer=WordNetLemmatizer()

#Text Preprocessing
def text_preprocessing(text):
    text=text.lower()
    tokens=word_tokenize(text)
    filtered_tokens=[]
    for w in tokens:
        if w.isalnum() and w not in stop_words:
            filtered_tokens.append(lemmatizer.lemmatize(w))
    return filtered_tokens

#Ngrams Generator
def ngrams_generate(tokens,n=5):
    ngrams=[]
    total_tokens=len(tokens)
    for i in range(0,total_tokens-n+1):
        ngram=tokens[i:i+n]
        ngram_joined=' '.join(ngram)
        ngrams.append(ngram_joined)
    return ngrams

#Level 1: Ngrams Match using Rabin Karp
def rabin_karp(pattern,text,d=256,q=101):
    n=len(text)
    m=len(pattern)
    if m>n:
        return False
    h=pow(d,m-1,q)
    p=0
    t=0
    for i in range(m):
        p=((d*p)+ord(pattern[i]))%q
        t=((d*t)+ord(text[i]))%q
    for s in range(n-m+1):
        if p==t:
            if text[s:s+m]==pattern:
                return True
        if s<n-m:
            t=(d*(t-ord(text[s])*h)+ord(text[s+m]))%q
            t=(t+q)%q
    return False 
       
def match_ngrams(ngrams1,ngrams2):
    matches=[]
    for p in ngrams1:
        for t in ngrams2:
            if rabin_karp(p,t):
                matches.append(p)
    return matches

#Level 2: Semantic Ngrams Match
model=SentenceTransformer("all-MiniLM-L6-v2")

def match_ngrams_semantic(ngrams1,ngrams2,threshold=0.75):
    matches=[]
    for gram1 in ngrams1:
        best_match=None
        best_score=0
        embedding1=model.encode(gram1,convert_to_tensor=True)
        for gram2 in ngrams2:
            embedding2=model.encode(gram2,convert_to_tensor=True)
            similarity=util.cos_sim(embedding1,embedding2).item()
            if similarity>=threshold and similarity>best_score:
                best_match=(gram1,gram2,round(similarity,2))
                best_score=similarity
        if best_match:
            matches.append(best_match)
    return matches