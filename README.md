<p align="center">
  <img src="https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white" />
  <img src="https://img.shields.io/badge/DRF-FF1709?style=for-the-badge&logo=django&logoColor=white" />
  <img src="https://img.shields.io/badge/Celery-37814A?style=for-the-badge&logo=celery&logoColor=white" />
  <img src="https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white" />
  <img src="https://img.shields.io/badge/Ollama-000000?style=for-the-badge&logo=ollama&logoColor=white" />
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" />
</p>

<h1 align="center">🎬 VidBrief AI</h1>

<p align="center">
  <strong>Turn any YouTube video into a concise, AI-powered summary — in seconds.</strong>
</p>

<p align="center">
  <em>A production-ready REST API built with Django, Celery, Redis & Ollama that fetches YouTube transcripts and generates intelligent summaries using local LLMs.</em>
</p>

<p align="center">
  <a href="#-features">Features</a> •
  <a href="#-architecture">Architecture</a> •
  <a href="#-api-reference">API Reference</a> •
  <a href="#-getting-started">Getting Started</a> •
  <a href="#-project-structure">Project Structure</a> •
  <a href="#-tech-stack">Tech Stack</a>
</p>

---

## ✨ Features

| Feature | Description |
|---|---|
| 🤖 **AI Summarization** | Leverages Ollama (Qwen 2.5 7B) running locally for fast, private AI summaries |
| 📜 **Transcript Extraction** | Automatically pulls full transcripts from any public YouTube video |
| ⚡ **Async Processing** | Background task queue via Celery + Redis — no request blocking |
| 🔐 **OTP Authentication** | Secure 3-step registration flow: OTP → Verify → Set Password |
| 🎫 **JWT Tokens** | Stateless authentication with access & refresh tokens via SimpleJWT |
| 📄 **Paginated Results** | Clean, paginated API responses for summary history |
| 🧠 **Redis Caching** | In-memory caching for OTP sessions and fast data retrieval |
| 🌐 **CORS Enabled** | Ready for frontend integration out of the box |

---

## 🏗 Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        CLIENT (Frontend)                        │
└───────────────────────────────┬─────────────────────────────────┘
                                │  HTTP / REST
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                     DJANGO REST FRAMEWORK                       │
│                                                                 │
│   ┌──────────────┐    ┌───────────────┐    ┌────────────────┐   │
│   │    Auth App   │    │   Core App    │    │    AI Module   │   │
│   │              │    │               │    │                │   │
│   │ • OTP Create │    │ • Create      │    │ • Prompt Build │   │
│   │ • OTP Verify │    │ • List All    │    │ • LLM Call     │   │
│   │ • Set Pass   │    │ • Detail View │    │ • Response Gen │   │
│   │ • JWT Token  │    │               │    │                │   │
│   └──────┬───────┘    └──────┬────────┘    └───────▲────────┘   │
│          │                   │                     │            │
└──────────┼───────────────────┼─────────────────────┼────────────┘
           │                   │                     │
           ▼                   ▼                     │
┌──────────────────┐  ┌────────────────┐   ┌────────┴─────────┐
│   Redis Cache    │  │  Celery Worker │──▶│   Ollama (LLM)   │
│                  │  │                │   │                  │
│ • OTP Storage    │  │ • Fetch YT     │   │  qwen2.5:7b      │
│ • Session Data   │  │   Transcript   │   │                  │
│ • Task Broker    │  │ • Generate     │   │  Local & Private  │
│                  │  │   AI Summary   │   │                  │
└──────────────────┘  └───────┬────────┘   └──────────────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │    SQLite DB     │
                    │                  │
                    │  • Users         │
                    │  • Summaries     │
                    │  • Transcripts   │
                    └──────────────────┘
```

---

## 📡 API Reference

### 🔐 Authentication — `/auth/`

<details>
<summary><code>POST</code> <code>/auth/otp-creation/</code> — <strong>Start Registration</strong></summary>

##### Request Body

```json
{
  "username": "adarsh",
  "email": "adarsh@example.com"
}
```

##### Response `201`

```json
{
  "message": "OTP generated successfully",
  "ref_id": "482913"
}
```

</details>

<details>
<summary><code>POST</code> <code>/auth/otp-verify/{ref_id}/</code> — <strong>Verify OTP</strong></summary>

##### Request Body

```json
{
  "otp": "482913"
}
```

##### Response `200`

```json
{
  "message": "otp verified successfully you may now set the password"
}
```

</details>

<details>
<summary><code>POST</code> <code>/auth/password-setup/{ref_id}/</code> — <strong>Set Password & Create Account</strong></summary>

##### Request Body

```json
{
  "password": "your_secure_password"
}
```

##### Response `201`

```json
{
  "message": "User Registered Successfully"
}
```

</details>

<details>
<summary><code>POST</code> <code>/auth/api/token/</code> — <strong>Login (Get JWT)</strong></summary>

##### Request Body

```json
{
  "username": "adarsh",
  "password": "your_secure_password"
}
```

##### Response `200`

```json
{
  "refresh": "eyJhbGciOi...",
  "access": "eyJhbGciOi..."
}
```

</details>

<details>
<summary><code>POST</code> <code>/auth/apt/token/refresh/</code> — <strong>Refresh Access Token</strong></summary>

##### Request Body

```json
{
  "refresh": "eyJhbGciOi..."
}
```

##### Response `200`

```json
{
  "access": "eyJhbGciOi..."
}
```

</details>

---

### 🎬 Core — `/core/` &nbsp; 🔒 *Requires JWT*

> Include the header: `Authorization: Bearer <access_token>`

<details>
<summary><code>POST</code> <code>/core/create/</code> — <strong>Submit a YouTube Video for Summarization</strong></summary>

##### Request Body

```json
{
  "link": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
}
```

##### Response `200`

```json
{
  "message": "Generation started..might take a moment",
  "db_id": 7
}
```

> 💡 The transcript fetching and AI summarization happen **asynchronously** via Celery. Poll the detail endpoint to check when it's ready.

</details>

<details>
<summary><code>GET</code> <code>/core/all/</code> — <strong>List All Your Summaries (Paginated)</strong></summary>

##### Query Params

| Param | Type | Default | Description |
|---|---|---|---|
| `page` | int | 1 | Page number |
| `page_size` | int | 10 | Results per page (max 100) |

##### Response `200`

```json
{
  "count": 12,
  "next": "http://localhost:8000/core/all/?page=2",
  "previous": null,
  "results": [
    {
      "user": 1,
      "link": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
      "time": "2026-09-26T15:04:12Z"
    }
  ]
}
```

</details>

<details>
<summary><code>GET</code> <code>/core/all/{id}/</code> — <strong>Get Summary Detail</strong></summary>

##### Response `200`

```json
{
  "id": 7,
  "user": {
    "username": "adarsh",
    "email": "adarsh@example.com"
  },
  "link": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
  "transcript": "We're no strangers to love...",
  "summary": "The video discusses the importance of commitment...",
  "time": "2026-09-26T15:04:12Z"
}
```

</details>

---

## 🚀 Getting Started

### Prerequisites

| Tool | Version | Purpose |
|---|---|---|
| Python | 3.10+ | Runtime |
| Redis | 7.0+ | Cache & task broker |
| Ollama | Latest | Local LLM inference |

### 1️⃣ Clone & Setup

```bash
git clone https://github.com/adarsh-pathak-2006/Build-my-own-VPN.git
cd Build-my-own-VPN/config
```

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Configure Environment

```bash
cp .env.example .env
```

Edit `.env` with your actual values:

```env
SECRET_KEY="your-super-secret-django-key"
OLLAMA_HOST="http://localhost:11434"
OTP_SERVICE_REFID="your-otp-refid"
OTP_SERVICE_IP="http://your-otp-service-ip"
```

### 5️⃣ Pull the Ollama Model

```bash
ollama pull qwen2.5:7b
```

### 6️⃣ Run Migrations

```bash
python manage.py migrate
```

### 7️⃣ Start All Services

Open **3 terminal tabs**:

```bash
# Terminal 1 — Redis (make sure Redis is running)
redis-server

# Terminal 2 — Celery Worker
celery -A config worker --loglevel=info -Q celery,otp

# Terminal 3 — Django Dev Server
python manage.py runserver
```

🎉 **You're live at** `http://localhost:8000`

---

## 📁 Project Structure

```
config/
├── ai/                          # AI Module
│   ├── build_prompt.py          # Prompt engineering & template
│   ├── build_response.py        # Ollama client & LLM interaction
│   └── final_response.py        # Orchestrates prompt → response pipeline
│
├── authentication/              # Auth App
│   ├── serializer.py            # User, OTP & password serializers
│   ├── tasks.py                 # Celery task: send OTP via external service
│   ├── urls.py                  # Auth route definitions
│   └── views.py                 # OTP creation, verification & password setup
│
├── config/                      # Project Configuration
│   ├── cache_keys.py            # Centralized Redis key generators
│   ├── celery.py                # Celery app initialization
│   ├── pagination.py            # DRF pagination settings
│   ├── settings.py              # Django settings (env-powered)
│   └── urls.py                  # Root URL configuration
│
├── core/                        # Core App
│   ├── models.py                # Summary model (link, transcript, summary)
│   ├── serializer.py            # Summary serializers (list & detail)
│   ├── tasks.py                 # Celery task: fetch transcript + AI summary
│   ├── urls.py                  # Core route definitions
│   └── views.py                 # Summary CRUD API views
│
├── .env                         # 🔒 Local secrets (git-ignored)
├── .env.example                 # 📋 Template for .env
├── .gitignore
├── manage.py
└── requirements.txt
```

---

## 🧰 Tech Stack

<table>
  <tr>
    <td align="center"><strong>Category</strong></td>
    <td align="center"><strong>Technology</strong></td>
    <td align="center"><strong>Why</strong></td>
  </tr>
  <tr>
    <td>🌐 Framework</td>
    <td>Django + DRF</td>
    <td>Battle-tested Python web framework with powerful REST toolkit</td>
  </tr>
  <tr>
    <td>⚡ Task Queue</td>
    <td>Celery</td>
    <td>Async background processing for transcript fetching & AI generation</td>
  </tr>
  <tr>
    <td>🗄️ Broker & Cache</td>
    <td>Redis</td>
    <td>Lightning-fast in-memory store for task brokering, OTP & session caching</td>
  </tr>
  <tr>
    <td>🤖 AI / LLM</td>
    <td>Ollama (Qwen 2.5)</td>
    <td>Run LLMs locally — no API costs, full data privacy</td>
  </tr>
  <tr>
    <td>🔐 Auth</td>
    <td>SimpleJWT</td>
    <td>Stateless JWT-based authentication with refresh token rotation</td>
  </tr>
  <tr>
    <td>📜 Transcripts</td>
    <td>youtube-transcript-api</td>
    <td>Lightweight library to pull video transcripts without YouTube API key</td>
  </tr>
  <tr>
    <td>🗃️ Database</td>
    <td>SQLite</td>
    <td>Zero-config database perfect for development (swap to PostgreSQL for prod)</td>
  </tr>
</table>

---

## 🔄 How It Works

```
User submits YouTube URL
        │
        ▼
   ┌─────────┐     ┌──────────────┐     ┌──────────────┐     ┌─────────────┐
   │  POST    │────▶│  Save to DB  │────▶│  Celery Task │────▶│  Fetch YT   │
   │ /create/ │     │  (pending)   │     │  (async)     │     │  Transcript │
   └─────────┘     └──────────────┘     └──────────────┘     └──────┬──────┘
                                                                    │
                                                                    ▼
   ┌─────────┐     ┌──────────────┐     ┌──────────────┐     ┌─────────────┐
   │  GET    │◀────│  Return      │◀────│  Save to DB  │◀────│  Ollama AI  │
   │ /all/id │     │  Summary     │     │  (complete)  │     │  Summarize  │
   └─────────┘     └──────────────┘     └──────────────┘     └─────────────┘
```

---

## 📜 License

This project is open source and available under the [MIT License](LICENSE).

---

<p align="center">
  Built with ❤️ by <a href="https://github.com/adarsh-pathak-2006">Adarsh Pathak</a>
</p>
