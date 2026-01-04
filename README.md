# 🏈 NFL Draft Oracle

An AI-powered interactive web application for querying and analyzing NFL draft data using natural language.

![NFL Draft Oracle](https://img.shields.io/badge/NFL-Draft%20Oracle-FFB81C?style=for-the-badge)
![Vercel](https://img.shields.io/badge/Deployed%20on-Vercel-000000?style=for-the-badge&logo=vercel)
![GitHub Pages](https://img.shields.io/badge/Frontend-GitHub%20Pages-222222?style=for-the-badge&logo=github)

## ✨ Features

- 🤖 **Natural Language Queries** - Ask questions in plain English
- 🔍 **AI-Powered SQL Generation** - Automatically converts questions to SQL using GPT-4o
- 📊 **Smart Visualizations** - Automatic charts for statistical queries
- 💾 **Complete Draft History** - Data from 1936 to present
- 🎨 **Beautiful UI** - Football-themed design with smooth animations
- ⚡ **Fast & Free** - Serverless backend on Vercel, hosted on GitHub Pages

## 🚀 Live Demo

**Live App**: [Your GitHub Pages URL]  
**API Backend**: [Your Vercel URL]

## 📸 Screenshots

[Add screenshots here]

## 🛠️ Tech Stack

### Frontend
- HTML5, CSS3, JavaScript (Vanilla)
- Chart.js for data visualization
- SQL.js for client-side database queries

### Backend
- Node.js + Express
- OpenAI GPT-4o API
- Vercel Serverless Functions

### Data
- SQLite database
- 89 years of NFL draft history (1936-2024)
- 30+ data fields per player

## 🏗️ Architecture

```
┌─────────────────┐
│  GitHub Pages   │  Static Frontend (HTML/CSS/JS)
│   (Frontend)    │  
└────────┬────────┘
         │
         │ HTTPS
         │
┌────────▼────────┐
│     Vercel      │  Serverless Functions
│   (Backend)     │  • OpenAI API Proxy
│                 │  • Database Serving
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
┌───▼────┐ ┌─▼────────┐
│ OpenAI │ │ SQLite   │
│  API   │ │ Database │
└────────┘ └──────────┘
```

## 📦 Installation

### Prerequisites
- Node.js 18+ 
- OpenAI API Key
- Git

### Local Development

1. **Clone the repository**
```bash
git clone https://github.com/YOUR_USERNAME/nfl-draft-oracle.git
cd nfl-draft-oracle
```

2. **Install dependencies**
```bash
cd nfl-draft-oracle
npm install
```

3. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

4. **Run the server**
```bash
npm start
```

5. **Open your browser**
```
http://localhost:3000
```

## 🌐 Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for complete deployment instructions.

### Quick Deploy

**Backend (Vercel):**
```bash
cd nfl-draft-oracle
vercel --prod
```

**Frontend (GitHub Pages):**
```bash
git push origin main
# GitHub Actions will deploy automatically
```

## 📊 Example Queries

Try asking questions like:

- "Which college has produced the most draft picks?"
- "Show me all quarterbacks drafted in the first round from 2020-2024"
- "What's the average career length for players drafted in round 7?"
- "Which team has made the most draft picks?"
- "Show me Hall of Fame players with more than 5 Pro Bowls"
- "What positions get drafted most often?"

## 🗄️ Database Schema

The database includes these key fields:

| Field | Description |
|-------|-------------|
| `year` | Draft year |
| `draft_round` | Round number |
| `draft_pick` | Overall pick number |
| `team` | Team that drafted the player |
| `player` | Player name |
| `pos` | Position |
| `college_id` | College/University |
| `pro_bowls` | Number of Pro Bowl selections |
| `all_pros_first_team` | First-team All-Pro selections |
| `g` | Games played |
| And 20+ more fields... |

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Data scraped from [Pro Football Reference](https://www.pro-football-reference.com/)
- Powered by [OpenAI GPT-4o](https://openai.com/)
- Hosted on [Vercel](https://vercel.com/) and [GitHub Pages](https://pages.github.com/)
- Built with love for football stats 🏈

## 📧 Contact

Your Name - [@yourtwitter](https://twitter.com/yourtwitter)

Project Link: [https://github.com/YOUR_USERNAME/nfl-draft-oracle](https://github.com/YOUR_USERNAME/nfl-draft-oracle)

---

⭐ Star this repo if you found it helpful!