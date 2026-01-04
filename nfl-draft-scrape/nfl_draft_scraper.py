#!/usr/bin/env python3
"""
NFL Draft Data Scraper from Pro Football Reference
Scrapes all NFL draft data from 1936 to present and stores in multiple formats
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import sqlite3
import time
import json
from pathlib import Path
from datetime import datetime
import logging


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class NFLDraftScraper:
    def __init__(self, start_year=1936, end_year=None):
        """
        Initialize the scraper
        
        Args:
            start_year: First year to scrape (default: 1936, first NFL draft)
            end_year: Last year to scrape (default: current year)
        """
        self.start_year = start_year
        self.end_year = end_year or datetime.now().year
        self.base_url = "https://www.pro-football-reference.com/years/{}/draft.htm"
        self.all_data = []
        
        # Create output directory
        self.output_dir = Path("nfl_draft_data")
        self.output_dir.mkdir(exist_ok=True)
        
        # User agent to identify ourselves
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Educational Research Bot)'
        }
    
    def scrape_year(self, year):
        """Scrape draft data for a single year"""
        url = self.base_url.format(year)
        logger.info(f"Scraping {year} draft data from {url}")
        
        try:
            response = requests.get(url, headers=self.headers, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find the draft table
            draft_table = soup.find('table', {'id': 'drafts'})
            
            if not draft_table:
                logger.warning(f"No draft table found for {year}")
                return []
            
            # Extract headers
            headers = []
            header_row = draft_table.find('thead').find_all('tr')[-1]  # Get last header row
            for th in header_row.find_all('th'):
                header_text = th.get('data-stat', th.text.strip())
                if header_text and header_text != 'ranker':
                    headers.append(header_text)
            
            # Extract data rows
            year_data = []
            tbody = draft_table.find('tbody')
            
            for row in tbody.find_all('tr'):
                # Skip header rows within tbody
                if row.find('th', {'scope': 'col'}):
                    continue
                
                row_data = {'year': year}
                
                for td in row.find_all(['th', 'td']):
                    stat = td.get('data-stat')
                    if stat and stat != 'ranker':
                        # Extract text, handling links
                        text = td.text.strip()
                        row_data[stat] = text
                        
                        # Also get player ID if it's a player link
                        if stat == 'player':
                            link = td.find('a')
                            if link and 'href' in link.attrs:
                                player_id = link['href'].split('/')[-1].replace('.htm', '')
                                row_data['player_id'] = player_id
                
                if row_data:
                    year_data.append(row_data)
            
            logger.info(f"Successfully scraped {len(year_data)} picks from {year}")
            return year_data
            
        except requests.RequestException as e:
            logger.error(f"Error scraping {year}: {e}")
            return []
        except Exception as e:
            logger.error(f"Unexpected error scraping {year}: {e}")
            return []
    
    def scrape_all_years(self, delay=3):
        """
        Scrape all years from start_year to end_year
        
        Args:
            delay: Seconds to wait between requests (be respectful!)
        """
        logger.info(f"Starting scrape from {self.start_year} to {self.end_year}")
        
        for year in range(self.start_year, self.end_year + 1):
            year_data = self.scrape_year(year)
            self.all_data.extend(year_data)
            
            # Be respectful - wait between requests
            if year < self.end_year:
                logger.info(f"Waiting {delay} seconds before next request...")
                time.sleep(delay)
        
        logger.info(f"Scraping complete! Total picks collected: {len(self.all_data)}")
    
    def save_to_csv(self, filename="nfl_draft_all_years.csv"):
        """Save data to CSV file"""
        if not self.all_data:
            logger.warning("No data to save")
            return
        
        filepath = self.output_dir / filename
        df = pd.DataFrame(self.all_data)
        df.to_csv(filepath, index=False)
        logger.info(f"Data saved to CSV: {filepath}")
        return filepath
    
    def save_to_sqlite(self, db_name="nfl_draft.db"):
        """Save data to SQLite database"""
        if not self.all_data:
            logger.warning("No data to save")
            return
        
        filepath = self.output_dir / db_name
        df = pd.DataFrame(self.all_data)
        
        # Create SQLite connection
        conn = sqlite3.connect(filepath)
        
        # Save to database
        df.to_sql('draft_picks', conn, if_exists='replace', index=False)
        
        # Create some useful indexes
        cursor = conn.cursor()
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_year ON draft_picks(year)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_player ON draft_picks(player)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_team ON draft_picks(team)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_college ON draft_picks(college_name)')
        
        conn.commit()
        conn.close()
        
        logger.info(f"Data saved to SQLite database: {filepath}")
        return filepath
    
    def save_to_json(self, filename="nfl_draft_all_years.json"):
        """Save data to JSON file"""
        if not self.all_data:
            logger.warning("No data to save")
            return
        
        filepath = self.output_dir / filename
        with open(filepath, 'w') as f:
            json.dump(self.all_data, f, indent=2)
        
        logger.info(f"Data saved to JSON: {filepath}")
        return filepath
    
    def save_yearly_csvs(self):
        """Save separate CSV file for each year"""
        if not self.all_data:
            logger.warning("No data to save")
            return
        
        df = pd.DataFrame(self.all_data)
        yearly_dir = self.output_dir / "by_year"
        yearly_dir.mkdir(exist_ok=True)
        
        for year in df['year'].unique():
            year_df = df[df['year'] == year]
            filepath = yearly_dir / f"draft_{year}.csv"
            year_df.to_csv(filepath, index=False)
        
        logger.info(f"Individual year CSVs saved to: {yearly_dir}")
    
    def get_summary_stats(self):
        """Print summary statistics of the scraped data"""
        if not self.all_data:
            logger.warning("No data available")
            return
        
        df = pd.DataFrame(self.all_data)
        
        print("\n" + "="*60)
        print("NFL DRAFT DATA SUMMARY")
        print("="*60)
        print(f"Total draft picks: {len(df):,}")
        print(f"Years covered: {df['year'].min()} - {df['year'].max()}")
        print(f"Total years: {df['year'].nunique()}")
        
        if 'team' in df.columns:
            print(f"Unique teams: {df['team'].nunique()}")
        
        if 'college_name' in df.columns:
            print(f"Unique colleges: {df['college_name'].nunique()}")
            print("\nTop 10 Colleges by Draft Picks:")
            print(df['college_name'].value_counts().head(10))
        
        if 'pos' in df.columns:
            print("\nPicks by Position:")
            print(df['pos'].value_counts())
        
        print("\nPicks per Year:")
        print(df.groupby('year').size().describe())
        print("="*60 + "\n")


def main():
    """Main function to run the scraper"""
    print("NFL Draft Data Scraper")
    print("="*60)
    print("This will scrape draft data from Pro Football Reference")
    print("Please be patient - this may take several minutes")
    print("="*60 + "\n")
    
    # Create scraper instance
    # You can modify the year range here
    scraper = NFLDraftScraper(start_year=1936, end_year=2024)
    
    # Scrape all years (with 3 second delay between requests)
    scraper.scrape_all_years(delay=3)
    
    # Save in multiple formats
    scraper.save_to_csv()
    scraper.save_to_sqlite()
    scraper.save_to_json()
    scraper.save_yearly_csvs()
    
    # Print summary
    scraper.get_summary_stats()
    
    print("\n" + "="*60)
    print("SCRAPING COMPLETE!")
    print("="*60)
    print(f"\nAll files saved to: {scraper.output_dir.absolute()}")
    print("\nYou can now:")
    print("1. Query the SQLite database: nfl_draft_data/nfl_draft.db")
    print("2. Analyze the CSV: nfl_draft_data/nfl_draft_all_years.csv")
    print("3. Use individual year files in: nfl_draft_data/by_year/")
    print("\nExample SQLite query:")
    print("  sqlite3 nfl_draft_data/nfl_draft.db")
    print('  SELECT * FROM draft_picks WHERE team="CHI" AND year=2024;')
    print("="*60)


if __name__ == "__main__":
    main()