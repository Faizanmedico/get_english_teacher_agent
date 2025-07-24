# tool.py
import re
import requests

def search_products(keyword: str) -> str:
    """
    Searches for products based on a keyword using an external API.

    Args:
        keyword (str): The keyword to search for.

    Returns:
        str: A formatted string of matching products, or an error message.
    """
    try:
        url = "https://hackathon-apis.vercel.app/api/products"
        response = requests.get(url)
        response.raise_for_status()
        products = response.json()

        words = re.findall(r"\b\w+\b", keyword.lower())
        stopwords = {"the", "with", "under", "above", "for", "of", "and", "or", "a", "an", "in", "to", "below", "between", "is", "best"}
        keywords = [w for w in words if w not in stopwords]

        filtered = []
        for p in products:
            title = p.get("title", "").lower()
            price = p.get("price", None)
            if not title or price is None:
                continue
            if any(kw in title for kw in keywords):
                filtered.append(f"- {p['title']} | Rs {price}")

        if filtered:
            return "\n".join(filtered[:5])
        else:
            return ""

    except Exception as e:
        return f"❌ API Error: {str(e)}"

# --- New English Teacher Tools ---

def correct_grammar(text: str) -> str:
    """
    Corrects grammatical errors in the provided English text.

    Args:
        text (str): The English text to correct.

    Returns:
        str: The grammatically corrected text.
    """
    # In a real application, you might use a more sophisticated NLP library
    # or even call another LLM specifically for grammar correction here.
    # For demonstration, a simple placeholder:
    corrected_text = text.replace("is happy", "are happy").replace("good done", "well done")
    return f"Grammar corrected: '{corrected_text}'"

def explain_concept(concept: str) -> str:
    """
    Explains a given English grammar or linguistic concept.

    Args:
        concept (str): The English concept to explain (e.g., "present perfect", "modal verbs").

    Returns:
        str: A simple explanation of the concept.
    """
    explanations = {
        "present perfect": "The present perfect tense connects the past with the present. It's used for actions that started in the past and continue to the present, or for actions completed in the past but relevant now. Example: 'I have lived here for five years.'",
        "modal verbs": "Modal verbs are auxiliary verbs that express necessity or possibility. They include can, could, may, might, must, shall, should, will, and would. Example: 'You should study harder.'",
        "adverb": "An adverb modifies a verb, an adjective, or another adverb. It answers questions like how, when, where, or to what extent. Example: 'She sings beautifully.'"
    }
    return explanations.get(concept.lower(), f"Sorry, I don't have a specific explanation for '{concept}'.")