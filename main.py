import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('punkt_tab')

from nltk.corpus import stopwords,wordnet
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from utility import text_preprocessing,ngrams_generate,match_ngrams,rabin_karp,match_ngrams_semantic

with open('sample1.txt','r') as f1,open('sample2.txt','r') as f2:
    text1=f1.read()
    text2=f2.read()
tokens1=text_preprocessing(text1)
tokens2=text_preprocessing(text2)
print("Tokens from File 1:",tokens1)
print("Tokens from File 2:",tokens2)

ngrams1=ngrams_generate(tokens1,n=5)
ngrams2=ngrams_generate(tokens2,n=5)
matches_normal=match_ngrams(ngrams1,ngrams2)
matches_semantic=match_ngrams_semantic(ngrams1,ngrams2,threshold=0.75)

print(f"Total Rabin Karp Matches: {len(matches_normal)}")
print("Matching Items:")
for item in matches_normal:
    print(f"- {item}")

print(f"Total Semantic Matches: {len(matches_semantic)}")
print("Matching Items:")
for ng1,ng2,score in matches_semantic:
    print(f"- {ng1} = {ng2} (score={score})")

normal_weight=1
sematic_weight=0.6
final_score=(((normal_weight*(len(matches_normal)))+(sematic_weight*(len(matches_semantic))))/(len(ngrams1)))*100
if final_score>=75:
    print(f"Plagiarism score:{final_score}")
    print(f"High Risk")
    risk="High"
elif final_score>=40:
    print(f"Plagiarism score:{final_score}")
    print(f"Moderate Risk")
    risk="Moderate"
else:
    print(f"Plagiarism score:{final_score}")
    print(f"Low Risk")
    risk="Low"

with open("report.txt","w") as f:
    f.write("Plagiarism Report\n")
    f.write(f"Plagiarism Score: {final_score}\n")
    f.write(f"Risk Level: {risk}\n")
    f.write("\nRabin-Karp Exact Matches:\n")
    for item in matches_normal:
        f.write(f"- {item}\n")
    f.write("\nSemantic Matches:\n")
    for ng1,ng2,score in matches_semantic:
        f.write(f"- {ng1} = {ng2} (score={score})\n")

