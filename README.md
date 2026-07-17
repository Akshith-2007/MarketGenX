# MarketGenX
# 🚀 MarketGenX

> An AI-powered marketing assistant that helps businesses and entrepreneurs generate high-quality marketing content, analyze competitors, score leads, and create promotional assets using Large Language Models.

---

## 📖 Overview

MarketGenX is a Flask-based web application that leverages Generative AI to simplify marketing workflows. It enables users to generate marketing campaigns, sales pitches, competitor analyses, lead scores, FAQs, and AI-powered poster concepts through an intuitive interface.

This project demonstrates the integration of Large Language Models (LLMs) into a full-stack web application to automate repetitive marketing tasks and improve productivity.

---

## ✨ Features

- 📢 AI Marketing Campaign Generator
- 💼 AI Sales Pitch Generator
- 🎯 AI Lead Scoring
- 🔍 Competitor Analysis
- ❓ AI FAQ Generator
- 🤖 Marketing Assistant Chatbot
- 🎨 AI Poster Generator (Hugging Face)
- 📱 Responsive User Interface

---

## 🛠️ Tech Stack

### Frontend
- HTML5
- CSS3
- JavaScript
- Bootstrap
- Jinja2 Templates

### Backend
- Python
- Flask

### AI & APIs
- Groq API (Llama 3.3 70B Versatile)
- Hugging Face Inference API

### Libraries
- requests
- python-dotenv
- Pillow
- OpenCV

### Tools
- Git
- GitHub

---

## 📂 Project Structure

```
MarketGenX/
│
├── static/
│   ├── css/
│   ├── js/
│   └── images/
│
├── templates/
│   ├── index.html
│   ├── campaign.html
│   ├── competitor.html
│   ├── lead_scorer.html
│   ├── chatbot.html
│   └── ...
│
├── app.py
├── requirements.txt
├── .env
└── README.md
```

---

## ⚙️ Getting Started

### Clone the Repository

```bash
git clone https://github.com/Akshith-2007/MarketGenX.git
```

### Navigate to the Project

```bash
cd MarketGenX
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Environment Variables

Create a `.env` file in the project root.

```env
GROQ_API_KEY=your_groq_api_key
HF_API_KEY=your_huggingface_api_key
```

### Run the Application

```bash
python app.py
```

Open your browser and visit:

```
http://127.0.0.1:5000
```

---

## 🏗️ System Architecture

```
                User
                  │
                  ▼
        Flask Web Application
                  │
      ┌───────────┴───────────┐
      ▼                       ▼
 Groq API              Hugging Face API
(Text Generation)      (Image Generation)
      │                       │
      └───────────┬───────────┘
                  ▼
          AI Generated Output
```

---

## 💡 Why MarketGenX?

Marketing tasks such as campaign planning, content creation, competitor research, and promotional design often require significant time and creativity.

MarketGenX uses Generative AI to automate these tasks, allowing users to quickly generate professional-quality marketing content and creative assets.

---

## 📚 Learning Outcomes

While developing this project, I gained hands-on experience with:

- Flask web development
- REST API integration
- Prompt engineering
- LLM integration using Groq
- Hugging Face Inference API
- Environment variable management
- Full-stack application development
- AI-assisted content generation

---

## 🚀 Future Enhancements

- User authentication
- Save generated marketing reports
- Export results as PDF
- Social media post generation
- Marketing analytics dashboard
- Multi-language support
- Cloud deployment

---

## 📸 Screenshots

Add screenshots of:

- Home Page
- Campaign Generator
- Competitor Analysis
- Lead Scorer
- AI Chatbot
- Poster Generator

---

## 👨‍💻 Author

**Akshith M**

GitHub: https://github.com/Akshith-2007

---

## ⭐ Support

If you found this project useful, consider giving it a ⭐ on GitHub.
