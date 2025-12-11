"""Utility constants and functions for answer evaluation."""

import re

# Word to number mapping for numeric evaluation
WORD_TO_NUM: dict[str, int] = {
    "zero": 0, "one": 1, "two": 2, "three": 3, "four": 4,
    "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9,
    "ten": 10, "eleven": 11, "twelve": 12, "thirteen": 13,
    "fourteen": 14, "fifteen": 15, "sixteen": 16, "seventeen": 17,
    "eighteen": 18, "nineteen": 19, "twenty": 20, "thirty": 30,
    "forty": 40, "fifty": 50, "sixty": 60, "seventy": 70,
    "eighty": 80, "ninety": 90, "hundred": 100,
    "first": 1, "second": 2, "third": 3, "fourth": 4, "fifth": 5,
}

# Common synonyms and contractions for flexible matching
SYNONYMS: dict[str, str] = {
    "dont": "don't",
    "cant": "can't",
    "wont": "won't",
    "isnt": "isn't",
    "arent": "aren't",
    "doesnt": "doesn't",
    "didnt": "didn't",
    "hasnt": "hasn't",
    "havent": "haven't",
    "wouldnt": "wouldn't",
    "couldnt": "couldn't",
    "shouldnt": "shouldn't",
    "autumn": "fall",
    "fall": "autumn",
}


def normalize_text(text: str) -> str:
    """
    Normalize text by removing punctuation and extra whitespace.

    Parameters
    ----------
    text : str
        Input text to normalize.

    Returns
    -------
    str
        Normalized text with punctuation removed and whitespace collapsed.
    """
    # Remove punctuation except hyphens in words
    text = re.sub(r"[^\w\s-]", " ", text)
    # Collapse multiple spaces
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def get_words(text: str) -> set[str]:
    """
    Extract normalized words from text as a set.

    Parameters
    ----------
    text : str
        Input text to extract words from.

    Returns
    -------
    set[str]
        Set of normalized words.
    """
    normalized = normalize_text(text)
    return set(normalized.split())


def extract_numbers(text: str) -> list[str]:
    """
    Extract all numeric values from text including word numbers.

    Parameters
    ----------
    text : str
        Input text to extract numbers from.

    Returns
    -------
    list[str]
        List of number strings found in the text.
    """
    # Remove currency symbols and % signs for number extraction
    text_clean = re.sub(r"[$%]", "", text)
    numbers = re.findall(r"-?\d+\.?\d*", text_clean)

    # Also check for word numbers
    text_lower = text.lower()
    for word, num in WORD_TO_NUM.items():
        if word in text_lower:
            numbers.append(str(num))

    return numbers


def apply_synonyms(text: str) -> str:
    """
    Apply synonym substitutions to text.

    Parameters
    ----------
    text : str
        Input text to apply synonyms to.

    Returns
    -------
    str
        Text with synonyms applied.
    """
    result = text
    for orig, syn in SYNONYMS.items():
        result = result.replace(orig, syn)
    return result


def cosine_similarity(vec1: list, vec2: list) -> float:
    """
    Calculate cosine similarity between two vectors.

    Parameters
    ----------
    vec1 : list
        First vector.
    vec2 : list
        Second vector.

    Returns
    -------
    float
        Cosine similarity score between 0 and 1.
    """
    import numpy as np

    vec1 = np.array(vec1)
    vec2 = np.array(vec2)

    dot_product = np.dot(vec1, vec2)
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)

    if norm1 == 0 or norm2 == 0:
        return 0.0
    return dot_product / (norm1 * norm2)
