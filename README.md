# 🎯 AI Resume Matcher

An AI-powered web application that matches resumes with job descriptions using NLP and Machine Learning.

---

## 🚀 Features

* 📄 Resume parsing (PDF)
* 🧹 Text preprocessing using NLP (spaCy)
* 🤖 Matching using:

  * TF-IDF (fast)
  * BERT (accurate)
* 📊 Match score with visual gauge
* 🏆 Rating system (Excellent / Good / Average / Poor)
* 🛠 Skill gap analysis
* 💡 Smart suggestions to improve resume
* 📚 Multi-resume ranking system

---

## 🧰 Tech Stack

* Python
* Streamlit
* Scikit-learn
* spaCy
* Sentence Transformers (BERT)
* Plotly

---

## 📂 Project Structure

```
resume_matcher/
│── core/
│   ├── matcher.py
│   ├── rating.py
│   ├── skill_extractor.py
│   ├── suggester.py
│   ├── ranker.py
│
│── utils/
│   ├── extractor.py
│   ├── preprocessor.py
│
│── app.py
│── requirements.txt
│── README.md
```

---

## ⚙️ Installation

```bash
git clone https://github.com/Sraj-1/AI-Resume-Matcher.git
cd AI-Resume-Matcher

python -m venv venv
venv\Scripts\activate   # Windows

pip install -r requirements.txt
```

---

## ▶️ Run the App

```bash
streamlit run app.py
```

---

## 🧪 Example Workflow

1. Upload resume (PDF)
2. Paste job description
3. Choose model (TF-IDF / BERT)
4. Click "Analyze Match"
5. View:

   * Match Score
   * Rating
   * Skill Gap
   * Suggestions

---

## 🧠 Future Improvements

* 🔐 User authentication system
* 📊 Resume history dashboard
* 🌐 Deployment on cloud
* 🧠 Fine-tuned BERT model

---

## 👨‍💻 Author

Saurabh Raj
GitHub: https://github.com/Sraj-1
