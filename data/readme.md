# Data Processing 📊

This describes the data processing steps that were taken to prepare the data for the model training.
The data processing steps are described in the order in which they were performed.
This is the first step in reproducing (from scratch) the results of the analysis.

*Note: The documentation is mainly for linux users. However, everything should work on windows as well, with some adjustments.*

## Data Acquisition 🗃️

You should download malwares and benign files from wherever you like to the folder `data/unprocessed/`.
The raw data is not included in this repository because of the size of the data.
I used the following sources:
- Malwares given by the instructor of the course of previous tasks.
- [zip of malwares](https://mega.nz/file/WjomTSzK#2yb9W7_FhVp_DL6jscfOWdOHfDYszIZY2CyO6sLpEZs)
- [DikeDataset](https://github.com/iosifache/DikeDataset) - Labeled dataset containing benign and malicious PE and OLE files


## Data filtering (optional) 🗄️

In my analysis, I used only the PE32 files, due to the long runtime of 'floss' on malwares.
You can filter the data by running the script `filter_win32.sh` in the `data/unprocessed/` folder.

If you would like to support all the file types, take into account that you will need more data and more time to process it.


## String Extraction 📜

The extraction of strings is done by **[floss 2.2.0](https://github.com/mandiant/flare-floss)**. Make sure you **have it installed** and in your path.
In order to process the data from raw data in `data/unprocessed/` to the extracted strings in `data/processed/`, run the script `floss_runner.py`.
You should split the processed data into two folders, one for benign files (`data/processed/benign_floss_output`), and one for malicious files (`data/processed/malware_floss_output`)

Run `./floss_runner.py -h` to see the options. Here's snaphot of the help message:

```
usage: floss_runner.py [-h] [-d DIRECTORY] [-o OUTPUT] [--malicious]
                       [--random] [--static]

options:
  -h, --help            show this help message and exit
  -d DIRECTORY, --directory DIRECTORY
                        directory of files to run floss on
  -o OUTPUT, --output OUTPUT
                        output directory for floss json files
  --malicious           mark files as malicious
  --random              randomize file order, helpful when dir is large,
                        and you want to parse some of the files, uniformly
  --static              run floss in only-static mode, much faster,
                        recommended only for benign files
```

The script will run floss on all the files in the directory, and save the results in the output directory.

## Data Splitting ✂️

Use the `split_data.ipynb` notebook to split the data into train, test and another set for the strings dataset.

## Data Preprocessing - creating strings dataset 〰️

Now, you should have a 2 folders (benign and malicious) of json files that are intended for the strings dataset. Each json containing the strings extracted by floss.

Run the `create_strings_dataset.py` script to create the dataset of strings. The script will create a json dataset with the following structure:

```
{
    "scanned_files": ['file1', 'file2', ...],
    "strings": {
      "string1": {
        "suspicious_score": float
        "malware_files": ['file1', 'file2', ...],
        "benign_files": ['file1', 'file2', ...],
      },
      ...
    }
}
```

That is, a dictionary with all the strings seen in given files, and the files in which they were seen.

### Data Processing - strings dataset exploration 📊

I have included a jupyter notebook `strings_dataset_exploration.ipynb` that explores the strings dataset.
You can run it to see the frequency of strings in malware and benign files, and the suspicious score of each string.
This notebook is a visualization of the strings dataset processing, and it also created **new processed strings dataset**, so you must run it in order to continue with the analysis.

The new processed strings dataset is keeping only the strings that were seen in at least `mal_threshold` malware files, and at most at `ben_threshold` benign files. You can change these values in the notebook.

The new processed strings dataset is keeping only the strings with the following scores (removing the lists of files):
- suspicious_score - extracted in the strings scoring algorithm, see in [algorithm description](../readme.md##strings-scoring-algorithm-).
- frequency_score - The ratio between the number of malicious files in which the string was seen, to the number of benign files in which the string was seen. 

This processed data can be used for further analysis, and for feature extraction, but for now, I am using only the list of strings (in a lot of malwares but not in many benign files).

## Feature Extraction - strings dataset 

Now, given old or new, input file, binary or floss_output file, we would like to extract features from it, and use it for classification.

This can be done by the functions in the script `feature_extractor.py`. For example the function `extract_features_from_output(output_path, strings_dataset_path)` will extract the features from the given floss output file, and return a list of features.

## Creating the files dataset

Using the feature extractor, we can create the dataset that we be used for classification of files. \
The script `create_dataset.py` will create a tabular csv dataset with the following structure: \
*strings_features (list of 0/1), *type_of_extraction_features (list of 0/1), is_malware (bool) \
Where the * represents unpacking.

Run this script twice, once use the floss output directories of "train", and once use the floss output directories of "test". 

**Use the filtered strings dataset, got from the notebook `strings_dataset_exploration.ipynb`. This because the training of the model should be on a reasonable (and meaningful) amount of features.**


## Train and Test the model

Using the script `regressor_trainer.py`, you can train using train dataset and save the model as a pickle file.
The script also has an option to test the model on the test dataset, and print some scores. 