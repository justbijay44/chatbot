
from flask import Flask,jsonify, render_template, request

import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import random  

app = Flask(__name__)

nlp = spacy.load("en_core_web_sm")

# To load data from the data.txt file
def load_data(file_path):
    questions, answers = [], []

    try:
        with open(file_path, 'r') as file:
            for line in file:
                if '|' in line:  
                    ques, ans = line.split('|', 1) 
                    questions.append(ques.strip())
                    answers.append(ans.strip())
    
    except FileNotFoundError:
        print(f"The given file {file_path} wasn't found")

    return questions, answers

# Preprocess the questions by lemmatizing
def preprocess_data(questions):
    return [' '.join(lemmatize(q)) for q in questions]

# Find the best match for the user query based on cosine similarity
def find_match(user_query, questions, vectorizer, tfidf_matrix):

    user_query_vector = vectorizer.transform([' '.join(lemmatize(user_query))])  

    similarity = cosine_similarity(user_query_vector, tfidf_matrix)  
    best_match_index = similarity.argmax()

    threshold = 0.6

    #To check the confidence of the response by the model
    if similarity[0][best_match_index] < threshold:
        return -1  # No good match
    return best_match_index

# Tokenize and lemmatize the text (removes stopwords and punctuation)
def lemmatize(text):
    doc = nlp(text)
    return [token.lemma_ for token in doc if not token.is_stop and not token.is_punct]

file_path = 'data.txt' 
questions, answers = load_data(file_path)  

preprocessed_questions = preprocess_data(questions)

vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(preprocessed_questions)

fallback_responses = [
            "Seems like the developer team didnt added that on me?",
            "I couldn't find a match. Try a different question!",
            "Hmm... I don't know. I will be sure to update this the next time"
        ]

#Flask

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_response', methods = ['POST'])
def get_response():

    user_query = request.json.get("user_input", "").strip()

    if not user_query:
        return jsonify({"response": "Please enter a question!"})
        
    best_match_index = find_match(user_query, questions, vectorizer, tfidf_matrix)

    response = random.choice(fallback_responses) if best_match_index == -1 else answers[best_match_index]

    # print(f"jerryBOT: {answers[best_match_index]}")
    return jsonify({"response": response})

#To add questions and answers
@app.route('/add_qa', methods=['POST'])
def add_qa():

    qa_pairs = request.json.get("qa_pairs", [])

    if not qa_pairs:
        return jsonify({"status": "failed", "message": "Please provide question and answer pair."})
    
    try:
        with open(file_path, 'a') as file:

            for pair in qa_pairs:
                new_question = pair.get('question', '').strip()
                new_answer = pair.get('answer', '').strip()
                if new_question and new_answer:
                    file.write(f"{new_question} | {new_answer} \n")
                    
                    questions.append(new_question)
                    answers.append(new_answer)

    except Exception as e:
        return jsonify({"status" : "failed", "message": f"Error writing onto the file : {str(e)}"})
    

    global preprocessed_questions, tfidf_matrix
    preprocessed_questions = preprocess_data(questions)
    tfidf_matrix = vectorizer.fit_transform(preprocessed_questions)

    return jsonify({"status" : "success", "message" : "Successfully added new question and answer"})

if __name__ == "__main__":
    app.run(debug=True)