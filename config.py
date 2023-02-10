type_of_extraction_scores = {
    'static_string': 0,
    'decoded_string': 0.5,
    'stack_string': 0.9,
    'tight_string': 1,
}

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

scores_weights = {
    # not limited to 0-1, used for weighted average
    'randomness_score': 0.5,
    'len_score': 1,
    'category_score': 1,
    'suspicous_text_score': 1.5,
    'type_of_extraction_score': 3,
}
