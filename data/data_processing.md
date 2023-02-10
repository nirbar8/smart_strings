# Data Processing 📊

This describes the data processing steps that were taken to prepare the data for analysis. 
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

The extraction of strings is done by **[floss](https://github.com/mandiant/flare-floss)**. Make sure you **have it installed** and in your path.
In order to process the data from raw data in `data/unprocessed/` to the extracted strings in `data/processed/`, run the script `floss_runner.py` in the `data/` folder.

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