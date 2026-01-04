// server.js - Simple Express server to proxy OpenAI API calls
require('dotenv').config();
const express = require('express');
const cors = require('cors');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.static('public')); // Serve static files

// API endpoint to proxy OpenAI requests
app.post('/api/openai', async (req, res) => {
    const apiKey = process.env.OPENAI_API_KEY;
    
    if (!apiKey) {
        return res.status(500).json({ 
            error: 'OPENAI_API_KEY not found in environment variables' 
        });
    }

    try {
        const response = await fetch('https://api.openai.com/v1/chat/completions', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${apiKey}`
            },
            body: JSON.stringify(req.body)
        });

        const data = await response.json();
        
        if (!response.ok) {
            return res.status(response.status).json(data);
        }

        res.json(data);
    } catch (error) {
        console.error('OpenAI API Error:', error);
        res.status(500).json({ 
            error: 'Failed to communicate with OpenAI API',
            details: error.message 
        });
    }
});

// Serve the database file
app.get('/database/nfl_draft.db', (req, res) => {
    const dbPath = path.join(__dirname, '..', 'nfl-draft-scrape', 'nfl_draft.db');
    res.sendFile(dbPath, (err) => {
        if (err) {
            console.error('Error sending database file:', err);
            res.status(404).json({ error: 'Database file not found' });
        }
    });
});

// Serve the main HTML file
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

app.listen(PORT, () => {
    console.log(`🏈 NFL Draft Oracle server running on http://localhost:${PORT}`);
    console.log(`📁 Place your HTML file in the 'public' folder as 'index.html'`);
    console.log(`📊 Database will auto-load from: ../nfl_draft_scrape/nfl_draft.db`);
});