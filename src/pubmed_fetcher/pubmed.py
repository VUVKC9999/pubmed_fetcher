import requests
import pandas as pd
import argparse
import os
import re
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class PubMedFetcher:
    def __init__(self, query: str):
        self.query = query
        self.base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
        self.details_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
        self.api_key = os.getenv("PUBMED_API_KEY", "")
    
    def fetch_paper_ids(self):
        try:
            params = {
                "db": "pubmed",
                "term": self.query,
                "retmode": "json",
                "retmax": 10,  # Fetch first 10 results
                "api_key": self.api_key
            }
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            return response.json().get("esearchresult", {}).get("idlist", [])
        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching paper IDs: {e}")
            return []
    
    def fetch_paper_details(self, paper_ids):
        if not paper_ids:
            logging.warning("No paper IDs retrieved.")
            return []
        
        try:
            params = {
                "db": "pubmed",
                "id": ",".join(paper_ids),
                "retmode": "json",
                "api_key": self.api_key
            }
            response = requests.get(self.details_url, params=params)
            response.raise_for_status()
            return response.json().get("result", {})
        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching paper details: {e}")
            return {}
    
    def identify_non_academic_authors(self, affiliations):
        non_academic_authors = []
        company_affiliations = []
        academic_keywords = ["university", "college", "institute", "school", "academy", "lab", "research center"]
        
        for author, affiliation in affiliations.items():
            if not any(keyword in affiliation.lower() for keyword in academic_keywords):
                non_academic_authors.append(author)
                company_affiliations.append(affiliation)
        
        return ", ".join(non_academic_authors), ", ".join(company_affiliations)
    
    def extract_corresponding_author_email(self, details):
        email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
        correspondence = details.get("correspondence", "")
        emails = re.findall(email_pattern, correspondence)
        return emails[0] if emails else "N/A"
    
    def process_results(self, results):
        papers = []
        for paper_id, details in results.items():
            if paper_id == "uids":  # Skip non-paper details
                continue
            
            affiliations = details.get("affiliations", {})
            non_academic_authors, company_affiliations = self.identify_non_academic_authors(affiliations)
            corresponding_email = self.extract_corresponding_author_email(details)
            
            papers.append({
                "PubmedID": paper_id,
                "Title": details.get("title", "N/A"),
                "Publication Date": details.get("pubdate", "N/A"),
                "Non-academic Author(s)": non_academic_authors,
                "Company Affiliation(s)": company_affiliations,
                "Corresponding Author Email": corresponding_email
            })
        return papers

    def save_to_csv(self, papers, filename="papers.csv"):
        try:
            df = pd.DataFrame(papers)
            df.to_csv(filename, index=False)
            logging.info(f"Results saved to {filename}")
        except Exception as e:
            logging.error(f"Error saving to CSV: {e}")


def main():
    parser = argparse.ArgumentParser(description="Fetch research papers from PubMed.")
    parser.add_argument("query", type=str, help="Search query for PubMed.")
    parser.add_argument("-f", "--file", type=str, help="Output file name.", default="papers.csv")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug mode.")
    args = parser.parse_args()
    
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
    
    fetcher = PubMedFetcher(args.query)
    paper_ids = fetcher.fetch_paper_ids()
    details = fetcher.fetch_paper_details(paper_ids)
    papers = fetcher.process_results(details)
    fetcher.save_to_csv(papers, args.file)

if __name__ == "__main__":
    main()
