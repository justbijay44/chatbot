import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

nlp = spacy.load("en_core_web_sm")

# To load data from the data.txt file
def load_data(file_path):
    
    questions, answers = [],[]

    try:
        with open(file_path, 'r') as file:
            for line in file:
                if '|' in line:
                    ques, ans = line.split('|')

                    questions.append(ques.strip())

                    answers.append(ans.strip())
    
    except FileNotFoundError:
        print(f"The given file {file_path} wasn't found")

    return questions, answers

def preprocessing_data(questions):
    return [''.join(lemmatize(q)) for q in questions]

def find_match(user_query, questions, vectorize_question, tfidf_matrix):
    user_query_vector = vectorize_question.transform([' '.join(lemmatize(user_query))])
    similarity = cosine_similarity(user_query, tfidf_matrix)
    best_match_index = similarity.argmax()
    return best_match_index
    
def tokenize(text):
    doc = nlp(text)
    return [token.text for token in doc if not token.is_stop and not token.is_punct]

def lemmatize(text):
    doc = nlp(text)
    return [token.lemma_ for token in doc if not token.is_stop and not token.is_punct]

def response_query(user_query):

    if "best college" in user_query:
        return "The best college depends on your field of interest. Do you have a specific field in mind?"
    
    elif "best field" in user_query:
        return "Some top fields right now are Computer Science, AI, and Data Science. What are your interests?"
    
    else:
        return "Sorry, I didn't quite understand that. Can you clarify your question?"


# Here the __name__ is used to check if file is being executed directly or by imported 
# And the block inside only runs if the file is executed directly else in __name__ the imported file is stored  

if __name__ == '__main__':
    file_path = 'data.txt' #to ensure the file is in same folder
    questions, answers = load_data(file_path)

    preprocessed_question = preprocessing_data(questions)

    #To convert the question into the tf idf matrix
    vectorize_question = TfidfVectorizer()
    tfidf_matrix = vectorize_question.fit_transform(preprocessed_question)

    while True:

        user_query = input("You : ").strip()
        if user_query.lower() in ['Bye', 'exit']:
            print("See you again")
            break
        
        best_match_index = find_match(user_query, questions, vectorize_question, tfidf_matrix)

        print(f"Answer :",answers[best_match_index])


        # tokens = tokenize(user_input)
        # lemma = lemmatize(user_input)

        # response = response_query(user_input)
        # print(f"Bot:{response}")


        # if text_data:
        #     print("Original ", text_data[:50])

        #     tokens = tokenize(text_data)
        #     print("Tokenized text", tokens[:5])

        #     lemma = lemmatize(text_data)
        #     print("Lemmatization text", lemma[:5])