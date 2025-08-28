import json
import re

# Comprehensive keywords to filter by
keywords = [
    "ai infrastructure", "cloud", "vmware", "infrastructure as a service", 
    "digital transformation", "scaling", "migration", "gpu", "llm", "oracle", 
    "chatbot", "ai", "machine learning", "artificial intelligence", 
    "cloud computing", "data center", "virtualization", "devops", 
    "microservices", "database", "analytics", "big data"
]

# Organizations/Entities being monitored
monitored_entities = [
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
    
    # Government Ministries (partial list - will match any ministry)
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

# Read the extracted tender data
with open("tenders.json", "r") as f:
    tenders = json.load(f)

filtered_tenders = []

# Filter tenders based on keywords in the title or entity names
for tender in tenders:
    title = tender["Tender Title"].lower()
    entity = tender["Entity"].lower()
    
    # Check if any keyword is in the title
    keyword_match = any(keyword.lower() in title for keyword in keywords)
    
    # Check if entity is in the monitored entities list
    entity_match = any(monitored_entity.lower() in entity for monitored_entity in monitored_entities)
    
    if keyword_match or entity_match:
        # Add match reason for better understanding
        match_reasons = []
        if keyword_match:
            matching_keywords = [kw for kw in keywords if kw.lower() in title]
            match_reasons.append(f"Keywords: {', '.join(matching_keywords)}")
        if entity_match:
            matching_entities = [ent for ent in monitored_entities if ent.lower() in entity]
            match_reasons.append(f"Entity: {', '.join(matching_entities)}")
        
        tender["Match_Reason"] = "; ".join(match_reasons)
        filtered_tenders.append(tender)

# Organize filtered tenders by entity
organized_tenders = {}
for tender in filtered_tenders:
    entity = tender["Entity"]
    if entity not in organized_tenders:
        organized_tenders[entity] = []
    organized_tenders[entity].append(tender)

# Save the organized tenders to a new JSON file
with open("comprehensive_filtered_tenders.json", "w") as f:
    json.dump(organized_tenders, f, indent=4)

# Print summary statistics
print(f"Total tenders found: {len(tenders)}")
print(f"Filtered tenders: {len(filtered_tenders)}")
print(f"Unique entities with matching tenders: {len(organized_tenders)}")
print("\nEntities with matching tenders:")
for entity, entity_tenders in organized_tenders.items():
    print(f"- {entity}: {len(entity_tenders)} tender(s)")

