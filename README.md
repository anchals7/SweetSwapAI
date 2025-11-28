# 🍹 SweetSwap AI

> **AI-Powered Nutrition Assistant for Diabetes-Friendly Drink Substitutions**

SweetSwap AI is an intelligent web application that helps users find healthier, diabetes-friendly alternatives to their favorite drinks. By combining a curated substitution database, real-time nutrition data, and Google Gemini AI, it provides personalized recommendations that reduce sugar intake while maintaining flavor satisfaction.

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-blue.svg)](https://www.postgresql.org/)

---

## 🎯 Problem Statement

People with diabetes or those watching their sugar intake often struggle to find satisfying alternatives to their favorite high-sugar drinks. Traditional methods require extensive research, and generic "healthy" options often lack the flavor profiles users crave.

## ✨ Solution

SweetSwap AI solves this by:
- **Instant Substitutions**: Query a database of 30+ pre-validated drink alternatives
- **AI-Powered Fallback**: When a drink isn't in the database, Gemini AI generates personalized recommendations
- **Nutrition Intelligence**: Integrates with USDA FoodData Central API for accurate sugar/caffeine tracking
- **Smart Caching**: Every AI-generated suggestion is saved to the database for future instant retrieval

---

## 🚀 Key Features

### 🎨 **Intuitive Web Interface**
- Clean, modern UI built with Streamlit
- Real-time drink substitution lookup
- Visual nutrition comparison cards (before/after sugar reduction)
- One-click feedback system

### 🤖 **Intelligent AI Integration**
- Google Gemini 2.0 Flash for natural language understanding
- Context-aware prompts that consider nutrition data
- Automatic database caching of AI responses

### 📊 **Data-Driven Architecture**
- PostgreSQL database with Supabase cloud hosting
- Redis caching layer via Upstash for performance
- RESTful FastAPI backend with automatic API documentation

### 🔄 **Smart Fallback System**
1. **Database First**: Instant lookup from curated substitution database
2. **AI Second**: Gemini generates personalized suggestions for new drinks
3. **Auto-Save**: All AI responses cached for future instant access

---

## 🎥 Demo

**[📹 Watch Demo Video](#)** *(Insert your demo video link here)*

*See SweetSwap AI in action: watch how users can instantly find diabetes-friendly alternatives to popular drinks like "Mango Boba Tea" or "Starbucks Caramel Frappuccino".*

---

## 🛠️ Tech Stack

### Backend
- **FastAPI** - Modern, fast web framework for building APIs
- **SQLAlchemy** - Python ORM for database operations
- **PostgreSQL** - Relational database (hosted on Supabase)
- **Redis** - Caching layer (hosted on Upstash)
- **Google Gemini AI** - LLM for intelligent substitutions
- **USDA FoodData Central API** - Nutrition data integration

### Frontend
- **Streamlit** - Rapid UI development framework
- **Custom CSS** - Branded color palette and responsive design

### Infrastructure
- **Supabase** - PostgreSQL cloud hosting
- **Upstash** - Serverless Redis
- **Python 3.12+** - Core language

---

## 📸 Screenshots

*Add screenshots of your application here*

---

## 🏗️ Architecture

```
┌─────────────┐
│  Streamlit  │  User Interface
│   Frontend  │
└──────┬──────┘
       │ HTTP/REST
       ▼
┌─────────────┐
│   FastAPI   │  Backend API
│   Backend   │
└──────┬──────┘
       │
       ├──► PostgreSQL (Supabase) ──► Substitution Database
       │
       ├──► Redis (Upstash) ─────────► Cache Layer
       │
       ├──► Google Gemini API ────────► AI Substitution Generator
       │
       └──► USDA Nutrition API ──────► Nutrition Data
```

### Request Flow
1. User enters drink name → Frontend sends POST to `/substitute`
2. Backend checks database for existing substitution
3. If found → Return instantly from cache
4. If not found → Query Gemini AI with nutrition context
5. Save AI response to database for future use
6. Return substitution with nutrition comparison

---

## 🚀 Quick Start

### Prerequisites
- Python 3.12+
- PostgreSQL (or Supabase account)
- Redis (or Upstash account)
- Google Gemini API key
- USDA FoodData Central API key

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/SweetSwapAI.git
   cd SweetSwapAI
   ```

2. **Set up virtual environment**
   ```bash
   python -m venv .venv
   .\.venv\Scripts\activate  # Windows
   # source .venv/bin/activate  # Mac/Linux
   ```

3. **Install dependencies**
   ```bash
   pip install -r backend/requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   cp env.example .env
   # Edit .env with your API keys and database URLs
   ```

5. **Initialize database**
   ```bash
   python -m backend.app.db_init
   python -m backend.app.seed_data
   ```

6. **Start backend server**
   ```bash
   uvicorn app.main:app --reload --app-dir backend
   ```

7. **Start frontend** (in a new terminal)
   ```bash
   streamlit run frontend/app.py
   ```

8. **Access the application**
   - Frontend: http://localhost:8501
   - API Docs: http://localhost:8000/docs

For detailed setup instructions, see [DEVELOPMENT.md](DEVELOPMENT.md).

---

## 📈 Project Highlights

### What Makes This Special?
- ✅ **Production-Ready Architecture**: Cloud-hosted database, caching, and scalable API design
- ✅ **Intelligent Caching**: AI responses are automatically saved, reducing API costs and improving speed
- ✅ **Real-World Problem**: Addresses a genuine need for diabetes-friendly nutrition guidance
- ✅ **Modern Tech Stack**: Built with industry-standard tools and best practices
- ✅ **Extensible Design**: Easy to add new features (scrapers, user accounts, feedback system)

### Technical Achievements
- Implemented hybrid database + AI fallback system
- Integrated multiple external APIs (Gemini, USDA) with error handling
- Designed RESTful API with automatic OpenAPI documentation
- Built responsive UI with custom branding and color palette
- Set up cloud infrastructure (Supabase, Upstash) for scalability

---

## 🔮 Future Enhancements

- [ ] User authentication and personalized substitution history
- [ ] Feedback system to improve AI recommendations
- [ ] Automated web scraping for cafe menu updates
- [ ] Mobile app version (React Native)
- [ ] Integration with fitness trackers
- [ ] Multi-language support
- [ ] Community-contributed substitutions
- [ ] Advanced filtering (allergies, dietary restrictions)

---

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

---

## 👤 Author

**Your Name**
- GitHub: anchals7(https://github.com/anchals7)
- LinkedIn: anchal-developer(https://linkedin.com/in/anchal-developer)
- Portfolio: https://anchals7.github.io/anchalsr.github.io/

---

## 🙏 Acknowledgments

- Google Gemini AI for intelligent language model capabilities
- USDA FoodData Central for comprehensive nutrition data
- Supabase and Upstash for cloud infrastructure
- FastAPI and Streamlit communities for excellent documentation

---

**⭐ If you find this project helpful, please consider giving it a star!**

