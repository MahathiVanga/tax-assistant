# Indian Tax Assistant

A Flask-based web application for calculating and comparing Indian tax regimes, featuring an AI-powered chatbot for tax assistance.

## Overview

The Indian Tax Assistant helps users calculate and compare tax liabilities under India's old and new tax regimes. It combines a manual tax calculator with an AI chatbot for interactive tax queries and recommendations.

## Features

- **Manual Tax Calculator**: Compare taxes under both regimes
- **AI-Powered Chatbot**: Get instant tax-related answers
- **Tax Recommendations**: Receive AI-driven tax-saving strategies
- **Responsive UI**: Works on desktop and mobile
- **Dark Theme**: Modern black and grey design

## Project Structure

```
.
├── ai/
│   ├── ai_chatbot.py
│   └── ai_recommendations.py
├── static/
│   └── style.css
├── templates/
│   ├── index.html
│   └── result.html
├── app.py
├── README.md
├── .env
├── .gitignore
├── requirements.txt
└── tax_calculator.py

```

## Setup

1. Clone the repository:
```bash
git clone https://github.com/MahathiVanga/tax-assistant.git
cd Indian-Tax-Assistant
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment:
- Create `.env` file in root directory
- Add required API keys:
```bash
GROQ_API_KEY=your_api_key
```

5. Run the application:
```bash
python app.py
```

## Usage

- Access the web interface at `http://127.0.0.1:5000`
- Use the chatbot for tax queries
- Input income details in the calculator form
- View detailed tax comparisons and recommendations

## Dependencies

- Flask
- Groq
- Python-dotenv



