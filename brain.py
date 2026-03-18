import re

def process_text(text):
    """
    Input: "I spent 500 on Pizza"
    Output: {'valid': True, 'item': 'Food Item', 'amount': 500.0, 'category': 'Food'}
    """
    text = text.lower()
    response = {"valid": False, "item": "Unknown", "amount": 0.0, "category": "Misc"}

    # 1. EXTRACT AMOUNT (Finds the first number in the text using Regex)
    amount_match = re.search(r'\d+', text)
    if amount_match:
        response["amount"] = float(amount_match.group())
        response["valid"] = True
    else:
        # If no number is typed, fail the processing
        return response 

    # 2. RULE-BASED CATEGORIZATION
    if any(word in text for word in ['pizza', 'burger', 'lunch', 'dinner', 'coffee', 'food', 'zomato', 'swiggy']):
        response["category"] = "Food"
        response["item"] = "Food & Dining"
    elif any(word in text for word in ['uber', 'ola', 'taxi', 'fuel', 'petrol', 'bus', 'flight', 'train']):
        response["category"] = "Travel"
        response["item"] = "Transit/Fuel"
    elif any(word in text for word in ['movie', 'netflix', 'game', 'party', 'club']):
        response["category"] = "Entertainment"
        response["item"] = "Entertainment"
    elif any(word in text for word in ['rent', 'bill', 'wifi', 'recharge', 'electricity', 'emi']):
        response["category"] = "Bills"
        response["item"] = "Utility/Bill"
    elif any(word in text for word in ['amazon', 'flipkart', 'myntra', 'shoes', 'clothes']):
        response["category"] = "Shopping"
        response["item"] = "Retail Purchase"
    else:
        response["category"] = "Misc"
        response["item"] = "General Expense"
        
    return response