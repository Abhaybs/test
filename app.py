# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import pandas as pd
# from sklearn.metrics.pairwise import cosine_similarity
# from sklearn.feature_extraction.text import CountVectorizer

# app = Flask(__name__)
# CORS(app)  # Allow requests from front-end

# # Load dataset
# file_path = 'C:\\Users\\Dell\\Desktop\\resume-matcher\\flask-server\\jobswithID.csv'
# data = pd.read_csv(file_path)

# # Recommendation function
# def recommend_jobs(data, user_skills, top_n=5):
#     job_skills = data['Key Skills'].fillna('').str.lower()
#     all_skills = job_skills.tolist() + [user_skills.lower()]
#     vectorizer = CountVectorizer().fit_transform(all_skills)
#     vectors = vectorizer.toarray()
#     cosine_sim = cosine_similarity(vectors)
#     user_similarity_scores = cosine_sim[-1][:-1]
#     top_indices = user_similarity_scores.argsort()[-top_n:][::-1]
#     top_jobs = data.iloc[top_indices][['ID', 'Job Title', 'Location']].to_dict(orient="records")
#     return top_jobs

# # API endpoint for job recommendations
# @app.route('/recommend', methods=['POST'])
# def recommend():
#     user_skills = request.json.get('skills', '')
#     if not user_skills:
#         return jsonify({'error': 'Skills are required'}), 400
#     top_jobs = recommend_jobs(data, user_skills)
#     return jsonify(top_jobs)

# if __name__ == '__main__':
#     app.run(debug=True, host="0.0.0.0", port=5001)

from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

app = Flask(__name__)
CORS(app)  # Allow requests from front-end

# Load dataset
file_path = 'C:\\Users\\Dell\\Desktop\\resume-matcher\\flask-server\\jobswithID.csv'
data = pd.read_csv(file_path)

# Recommendation function
def recommend_jobs(data, user_skills, top_n=5):
    job_skills = data['Key Skills'].fillna('').str.lower()
    all_skills = job_skills.tolist() + [user_skills.lower()]
    vectorizer = CountVectorizer().fit_transform(all_skills)
    vectors = vectorizer.toarray()
    cosine_sim = cosine_similarity(vectors)
    user_similarity_scores = cosine_sim[-1][:-1]
    top_indices = user_similarity_scores.argsort()[-top_n:][::-1]
    top_jobs = data.iloc[top_indices][['ID', 'Job Title', 'Location']].to_dict(orient="records")
    return top_jobs

# API endpoint for job recommendations
@app.route('/recommend', methods=['POST'])
def recommend():
    user_skills = request.json.get('skills', '')
    if not user_skills:
        return jsonify({'error': 'Skills are required'}), 400
    top_jobs = recommend_jobs(data, user_skills)
    return jsonify(top_jobs)

# Debugging route (optional, remove in production)
@app.route('/test', methods=['GET'])
def test_recommendation():
    test_skills = "python, flask"
    recommendations = recommend_jobs(data, test_skills)
    return jsonify(recommendations)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5001)
