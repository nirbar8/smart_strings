# The strings that are not static are potentially important and can indicate on malicious behavior.
type_of_extraction_scores = {
    'static_string': 0,
    'decoded_string': 0.5,
    'stack_string': 0.9,
    'tight_string': 1,
}

# IP, URLs, URIs are not common in benign files.
# Strings extractors extract random strings very often.
category_scores = {
    'IP': 1,
    'URL': 0.9,
    'URI': 0.9,
    'number': 0.7,
    'DLL': 0.7,
    'DLL_function': 0.6,
    'Text': 0.5,
    'random': 0
}

# Overall, in the field of malware analysis, type of extraction is very important factor.
# Randomness and length are mostly important for distinguishing between random and non-random strings.
scores_weights = {
    # not limited to 0-1, used for weighted average
    'randomness_score': 0.5,
    'len_score': 1,
    'category_score': 1,
    'suspicous_text_score': 1.5,
    'type_of_extraction_score': 3,
}

# Optional - can be commented out to disable scoring by suspicious words
suspicious_words_path = 'data/processed/words_malware.pickle'
