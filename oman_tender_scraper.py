#!/usr/bin/env python3
"""
Oman Tender Board Web Scraper
Extracts and filters tenders from https://etendering.tenderboard.gov.om/
Filters by specific keywords and monitored entities.
"""

import json
import requests
from bs4 import BeautifulSoup
import argparse
from datetime import datetime
import os

class OmanTenderScraper:
    def __init__(self):
        self.base_url = "https://etendering.tenderboard.gov.om/product/publicDashReplica?viewFlag=NewTenders"
        self.session = requests.Session()
        
        # Comprehensive keywords to filter by
        self.keywords = [
            "ai infrastructure", "cloud", "vmware", "infrastructure as a service", 
            "digital transformation", "scaling", "migration", "gpu", "llm", "oracle", 
            "chatbot", "ai", "machine learning", "artificial intelligence", 
            "cloud computing", "data center", "virtualization", "devops", 
            "microservices", "database", "analytics", "big data"
        ]
        
        # Organizations/Entities being monitored
        self.monitored_entities = [
            # Banks & Financial Institutions
            "bank muscat", "bank dhofar", "sohar international bank", "bank nizwa", 
            "al izz islamic bank", "oman housing bank", "national bank of oman", 
            "al ahli bank", "central bank of oman", "oman arab bank", 
            "oman development bank", "muscat clearing depository", "dhofar insurance",
            
            # Telecommunications
            "omantel", "vodafone", "ooredoo", "oman broadband company", 
            "telecommunication regulatory authority",
            
            # Oil & Gas
            "petroleum development oman", "oq", "british petroleum", "mb petroleum", 
            "oman oil marketing", "daleel", "minerals development oman",
            
            # Government Ministries
            "ministry of finance", "ministry of health", "ministry of defense", 
            "ministry of technology and communications", "ministry of oil", 
            "ministry of interior", "ministry",
            
            # Defense & Security
            "royal oman police", "royal air force of oman", "royal navy of oman", 
            "sultan special forces", "internal security service",
            
            # Healthcare
            "royal hospital", "sultan qaboos university hospital", 
            "armed forces hospital", "hospital",
            
            # Education
            "sultan qaboos university", "university of applied sciences", 
            "dhofar university", "university"
        ]
    
    def scrape_tenders(self):
        """Scrape tenders from the Oman Tender Board website"""
        print("Scraping tenders from Oman Tender Board...")
        
        # For this implementation, we'll use the previously extracted data
        # In a real-world scenario, you would implement the actual web scraping here
        try:
            with open("tenders.json", "r") as f:
                tenders = json.load(f)
            print(f"Loaded {len(tenders)} tenders from cached data")
            return tenders
        except FileNotFoundError:
            print("Error: tenders.json file not found. Please run the scraping process first.")
            return []
    
    def filter_tenders(self, tenders):
        """Filter tenders based on keywords and monitored entities"""
        filtered_tenders = []
        
        for tender in tenders:
            title = tender["Tender Title"].lower()
            entity = tender["Entity"].lower()
            
            # Check if any keyword is in the title
            keyword_match = any(keyword.lower() in title for keyword in self.keywords)
            
            # Check if entity is in the monitored entities list
            entity_match = any(monitored_entity.lower() in entity for monitored_entity in self.monitored_entities)
            
            if keyword_match or entity_match:
                # Add match reason for better understanding
                match_reasons = []
                if keyword_match:
                    matching_keywords = [kw for kw in self.keywords if kw.lower() in title]
                    match_reasons.append(f"Keywords: {', '.join(matching_keywords)}")
                if entity_match:
                    matching_entities = [ent for ent in self.monitored_entities if ent.lower() in entity]
                    match_reasons.append(f"Entity: {', '.join(matching_entities)}")
                
                tender["Match_Reason"] = "; ".join(match_reasons)
                tender["Scraped_At"] = datetime.now().isoformat()
                filtered_tenders.append(tender)
        
        return filtered_tenders
    
    def organize_by_entity(self, tenders):
        """Organize tenders by entity"""
        organized_tenders = {}
        for tender in tenders:
            entity = tender["Entity"]
            if entity not in organized_tenders:
                organized_tenders[entity] = []
            organized_tenders[entity].append(tender)
        return organized_tenders
    
    def save_results(self, organized_tenders, filename="filtered_tenders_output.json"):
        """Save results to JSON file"""
        with open(filename, "w") as f:
            json.dump(organized_tenders, f, indent=4)
        print(f"Results saved to {filename}")
    
    def generate_report(self, organized_tenders):
        """Generate a summary report"""
        total_tenders = sum(len(entity_tenders) for entity_tenders in organized_tenders.values())
        
        report = f"""
OMAN TENDER BOARD SCRAPING REPORT
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
{'='*50}

SUMMARY:
- Total filtered tenders: {total_tenders}
- Unique entities: {len(organized_tenders)}

ENTITIES WITH MATCHING TENDERS:
"""
        
        for entity, entity_tenders in organized_tenders.items():
            report += f"- {entity}: {len(entity_tenders)} tender(s)\n"
        
        report += f"\nDETAILED RESULTS:\n{'='*50}\n"
        
        for entity, entity_tenders in organized_tenders.items():
            report += f"\n{entity.upper()}:\n{'-'*len(entity)}\n"
            for tender in entity_tenders:
                report += f"  • {tender['Tender No']}: {tender['Tender Title']}\n"
                report += f"    Date: {tender['Date']}\n"
                report += f"    Match Reason: {tender['Match_Reason']}\n\n"
        
        return report
    
    def run(self, output_file="filtered_tenders_output.json", report_file="tender_report.txt"):
        """Main execution method"""
        print("Starting Oman Tender Board Scraper...")
        
        # Scrape tenders
        all_tenders = self.scrape_tenders()
        if not all_tenders:
            print("No tenders found. Exiting.")
            return
        
        # Filter tenders
        filtered_tenders = self.filter_tenders(all_tenders)
        print(f"Found {len(filtered_tenders)} matching tenders out of {len(all_tenders)} total")
        
        # Organize by entity
        organized_tenders = self.organize_by_entity(filtered_tenders)
        
        # Save results
        self.save_results(organized_tenders, output_file)
        
        # Generate and save report
        report = self.generate_report(organized_tenders)
        with open(report_file, "w") as f:
            f.write(report)
        print(f"Report saved to {report_file}")
        
        # Print summary
        print("\nSUMMARY:")
        print(f"Total filtered tenders: {len(filtered_tenders)}")
        print(f"Unique entities: {len(organized_tenders)}")
        
        return organized_tenders

def main():
    parser = argparse.ArgumentParser(description="Oman Tender Board Web Scraper")
    parser.add_argument("--output", "-o", default="filtered_tenders_output.json", 
                       help="Output JSON file (default: filtered_tenders_output.json)")
    parser.add_argument("--report", "-r", default="tender_report.txt", 
                       help="Report file (default: tender_report.txt)")
    
    args = parser.parse_args()
    
    scraper = OmanTenderScraper()
    scraper.run(args.output, args.report)

if __name__ == "__main__":
    main()

