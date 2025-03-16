import unittest
from pubmed_fetcher.pubmed import PubMedFetcher
from unittest.mock import patch

class TestPubMedFetcher(unittest.TestCase):
    def setUp(self):
        self.fetcher = PubMedFetcher("cancer treatment")

    @patch("pubmed_fetcher.pubmed.requests.get")
    def test_fetch_paper_ids(self, mock_get):
        mock_get.return_value.json.return_value = {"esearchresult": {"idlist": ["12345", "67890"]}}
        mock_get.return_value.raise_for_status = lambda: None
        
        paper_ids = self.fetcher.fetch_paper_ids()
        self.assertEqual(paper_ids, ["12345", "67890"])

    @patch("pubmed_fetcher.pubmed.requests.get")
    def test_fetch_paper_details(self, mock_get):
        mock_get.return_value.json.return_value = {"result": {"12345": {"title": "Cancer Research", "pubdate": "2024-01-01"}}}
        mock_get.return_value.raise_for_status = lambda: None
        
        details = self.fetcher.fetch_paper_details(["12345"])
        self.assertIn("12345", details)
        self.assertEqual(details["12345"]["title"], "Cancer Research")

    def test_identify_non_academic_authors(self):
        affiliations = {
            "Dr. Smith": "XYZ Pharmaceuticals",
            "Dr. Johnson": "Harvard University",
            "Dr. Lee": "ABC Biotech"
        }
        non_academic_authors, company_affiliations = self.fetcher.identify_non_academic_authors(affiliations)
        self.assertEqual(non_academic_authors, "Dr. Smith, Dr. Lee")
        self.assertEqual(company_affiliations, "XYZ Pharmaceuticals, ABC Biotech")

    def test_extract_corresponding_author_email(self):
        details = {"correspondence": "Contact: john.doe@biotech.com for further info."}
        email = self.fetcher.extract_corresponding_author_email(details)
        self.assertEqual(email, "john.doe@biotech.com")

if __name__ == "__main__":
    unittest.main()
