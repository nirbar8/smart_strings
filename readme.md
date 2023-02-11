# SmartStrings

## Description 📝

This tool has 2 main functionalities:
- Extract strings from binary files using [floss](https://github.com/mandiant/flare-floss). It will sort the strings using an algorithm that weights different features of the strings. 
- Predict whether a binary file is malicious or benign, based on the extracted strings.

## Installation 🛠️

- install python 3
  - install [regex](https://pypi.org/project/regex/) 
  - install [sklearn](https://scikit-learn.org/stable/install.html)
  - install [pandas](https://pandas.pydata.org/pandas-docs/stable/getting_started/install.html)
  - install [tqdm](https://pypi.org/project/tqdm/)
  - install [numpy](https://numpy.org/install/)
  - install [matplotlib](https://matplotlib.org/stable/users/installing.html)
- install [floss 2.2.0](https://github.com/mandiant/flare-floss)

If you want to reproduce the results of the analysis, follow the instructions in the [data processing](data/readme.md) file.


## Usage ▶️

### 1) Extracting strings from binary file
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

You can change the configuration in the `config.py` file. Make sure to read the algorithm description in the [Strings scoring algorithm](extraction) section.

### 2) predicting malware / benign

Run the script `./classifier_main.py`. See `./classifier_main.py -h` for more information. Here's a snapshot of the help message:

```
options:
  -h, --help            show this help message and exit
  -ib INPUT_BINARY_PATH, --input-binary INPUT_BINARY_PATH
                        the path to the input binary
  -if INPUT_FLOSS_OUTPUT_PATH, --input-floss-output INPUT_FLOSS_OUTPUT_PATH
                        the path to the floss result file (json)
  -m MODEL_PATH, --model MODEL_PATH
                        the path to the trained model (pickle format)
                        default: 'data/model.pickle'
  -sd STRINGS_DATASET_PATH, --strings-dataset STRINGS_DATASET_PATH
                        the path to the strings dataset (json format)
                        default: 'data/strings_dataset.json'
```

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
To create your own vocabulary, I recommend using the script `data/words_malware.py`. This script shows how to make list of words related to the word "malware". You can use any other method you like. 


## Reproducing data processing steps - For classifier model 🔧

See the [data processing](data/readme.md) file.


## Results 📊

The data was separated into 3 groups:
- strings dataset - used to create the feature extractor model (275 benign and 275 malicious files)
- train dataset - used to train the classifier model (135 benign and 135 malicious files)
- test dataset - used to test the classifier model (45 benign and 45 malicious files)

The results on the test dataset are as follows:
```
The average score for the malicous test set is: 73.5637322293583
The average score for the benign test set is: 19.874307665594802

Accuracy: 83.3%
Precision: 96.9%
Recall: 68.9%
F1: 80.5%
```

**As you can see, only by using the strings of binary files, without any manual analysis, we can achieve a high accuracy in predicting whether a file is malicious or benign!**

**Note that as expected, the percision is much higher than the recall. So, this tool can be useful for incriminating a file, but not for exculpating it.**

You can easily add more data, using the [data processing](data/readme.md) tutorial, and retrain the model to get even better results. 


## Thanks 🙏

- [Flare-Floss](https://github.com/mandiant/flare-floss) - for the great tool to extract strings from binary files.
- [zip of malwares](https://mega.nz/file/WjomTSzK#2yb9W7_FhVp_DL6jscfOWdOHfDYszIZY2CyO6sLpEZs)
- [DikeDataset](https://github.com/iosifache/DikeDataset) - Labeled dataset containing benign and malicious PE and OLE files

## Contact 📧

If you have any questions, feel free to contact me at: `banir at post dot bgu dot ac dot il` (replace the `at` and `dot` with `@` and `.`, respectively, bots are not welcome...)
