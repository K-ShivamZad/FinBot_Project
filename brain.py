import re
from difflib import get_close_matches

CATEGORY_KNOWLEDGE_BASE = {
    "Food": ['pizza', 'burger', 'lunch', 'dinner', 'coffee', 'food', 'zomato', 'swiggy', 'grocery', 'dine', 'cafe'],
    "Travel": ['uber', 'ola', 'taxi', 'fuel', 'petrol', 'bus', 'flight', 'train', 'metro', 'auto', 'toll'],
    "Entertainment": ['movie', 'netflix', 'game', 'party', 'club', 'concert', 'spotify', 'subscription'],
    "Bills": ['rent', 'bill', 'wifi', 'recharge', 'electricity', 'emi', 'house', 'allowance', 'water', 'maintenance'],
    "Shopping": ['amazon', 'flipkart', 'myntra', 'shoes', 'clothes', 'electronics', 'mall', 'store'],
    "Health": ['doctor', 'medicine', 'hospital', 'pharmacy', 'clinic', 'gym']
}

def process_text(text):
    text_lower = text.lower()
    response = {"valid": False, "item": "Unknown", "amount": 0.0, "category": "Misc"}

    # Extract Amount
    amount_match = re.search(r'\d+(?:,\d{3})*(?:\.\d+)?', text_lower)
    if amount_match:
        clean_amount = amount_match.group().replace(',', '')
        response["amount"] = float(clean_amount)
        response["valid"] = True
    else:
        return response 

    # Extract individual words from input to test against the knowledge base
    input_words = re.findall(r'\b\w+\b', text_lower)
    found_category = False

    # Dynamic Categorization with Fuzzy Matching (80% similarity threshold)
    for category, keywords in CATEGORY_KNOWLEDGE_BASE.items():
        for word in input_words:
            # get_close_matches finds the closest dictionary word to what the user typed
            matches = get_close_matches(word, keywords, n=1, cutoff=0.8)
            if matches:
                response["category"] = category
                response["item"] = matches[0].title() 
                found_category = True
                break
        if found_category:
            break
    
    # Fallback for completely custom entries
    if not found_category:
        response["category"] = "Misc"
        cleaned_text = re.sub(r'\d+(?:,\d{3})*(?:\.\d+)?', '', text_lower).strip()
        stop_words = r'\b(i|paid|spent|bought|gave|for|on|rupees|rs|bucks|a|an|the)\b'
        cleaned_text = re.sub(stop_words, '', cleaned_text).strip()
        cleaned_text = re.sub(r'\s+', ' ', cleaned_text)
        response["item"] = cleaned_text.title() if cleaned_text else "General Expense"

    return response