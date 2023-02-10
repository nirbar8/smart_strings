# SmartStrings

## Description 📝

This tool has 2 main functionalities:
- Extract strings from binary files using [floss](https://github.com/mandiant/flare-floss). It will sort the strings using an algorithm that weights different features of the strings. 
- Predict whether a binary file is malicious or benign, based on the extracted strings.

## Installation 🛠️

- install python 3
-- install [regex](https://pypi.org/project/regex/)
-- install [sklearn](https://scikit-learn.org/stable/install.html)
- install [floss 2.2.0 2.2.0](https://github.com/mandiant/flare-floss)

If you want to reproduce the results of the analysis, follow the instructions in the [data processing](data/readme.md) file.


## Usage ▶️

### Extracting strings from binary file
Run the script `./strings_main.py`. See `./strings_main.py -h` for more information. Here's a snapshot of the help message:

```
 options:
  -h, --help            show this help message and exit
  -ib BINARY_FILE, --input-binary BINARY_FILE
                        the binary file to analyze
  -if FLOSS_OUTPUT, --input-floss-output FLOSS_OUTPUT
                        the floss output file to analyze
  -v, --verbose         print verbose output
  --no-color            print non-colored output
  --show-scores         print scores for each string
```

You can change the configuration in the `config.py` file. Make sure to read the algorithm description in the [algorithm](#algorithm) section.

### predicting malware / benign

TODO

## Strings scoring algorithm 🧮

The algorithm is based on the extracted strings from the binary file using floss. \
Floss program extract the following information for each string:
- type of extraction (static, decoded, stack, decoded)
- encoding
- offset

The algorithm uses only the type of extraction and extract much more information from the string itself.  \
This is done in the `DataString` class.

The algorithm will score the string in the following aspects:
- len_score - The longer the string, the higher the score. Minimal length (4 characters) will get a score of 0, and longer strings will get score closer to 1. 
- randomness_score - The more random the string, the **lower** the score. The score is calculated by measuring both the number of non-alpha characters and the number of changes in the string (e.g. from alphanumeric to non-alphanumeric).
- category_score - The string is categorized into one of the following categories: IP, URL, URI, number, DLL, DLL_function, Text, random. The category is determined by regex patterns. The score is defined in the `config.py` file. The more important the category, the higher the score.
- type_of_extraction_score - The type of extraction is defined by floss. The score is defined in the `config.py` file. The more suspicous the type of extraction, the higher the score.
- suspicous_text_score (optional, recommended) - The score is defined using a list of predefined vocabulary of suspicious words. If the string contains a word from the vocabulary, it gets non-zero score. The score is defined by the position (index) of the suspicious word in the vocabulary (first = more suspicous = higher score). 

### Remake vocabulary for suspicious score
To create your own vocabulary, I recommend using the script `./data/words_malware.py`. This script shows how to make list of words related to the word "malware". You can use any other method you like. 


## Reproducing data processing steps 🔧

See the [data processing](data/readme.md) file.

## Thanks 🙏

[Flare-Floss](https://github.com/mandiant/flare-floss) - for the great tool to extract strings from binary files.

## Contact 📧

If you have any questions, feel free to contact me at: `banir at post dot bgu dot ac dot il` (replace the `at` and `dot` with `@` and `.`, respectively, bots are not invited...)