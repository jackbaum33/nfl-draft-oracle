const fs = require('fs');
const path = require('path');

module.exports = (req, res) => {
    // Enable CORS
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET, OPTIONS');
    
    if (req.method === 'OPTIONS') {
        return res.status(200).end();
    }

    // Try to find the database
    const possiblePaths = [
        path.join(process.cwd(), 'nfl_draft.db'),
        path.join(process.cwd(), 'database', 'nfl_draft.db'),
        path.join(process.cwd(), '..', 'nfl-draft-scrape', 'nfl_draft.db')
    ];

    let dbPath = null;
    for (const p of possiblePaths) {
        if (fs.existsSync(p)) {
            dbPath = p;
            break;
        }
    }

    if (!dbPath) {
        return res.status(404).json({ 
            error: 'Database file not found',
            searchedPaths: possiblePaths,
            cwd: process.cwd()
        });
    }

    // Read and send the database file
    const dbFile = fs.readFileSync(dbPath);
    res.setHeader('Content-Type', 'application/x-sqlite3');
    res.setHeader('Content-Disposition', 'attachment; filename="nfl_draft.db"');
    res.status(200).send(dbFile);
};
