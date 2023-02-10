# Unlike the name suggests, this file is not really the test file.
# Just a playground for testing some functions.

from DataString import DataString


def test_category():
    lst = [
        'http://www.google.com',
        'http://ocsp.thawte.com0',
        '1232',
        'Local/Users/username/Downloads/',
        '124.0.1.1',
        'Thawte Code Signing CA - G20',
        'as$As',
        'Kernel32.dll',
        'kernel32.DLL',
        'CreateFileA',
        'CreateFileW',
        'CreateFileWithAttributesA',
        'CreateFileWithAttributes',
        'Abc@123',
    ]

    for s in lst:
        print(DataString.category(s), ' : ', s)


def test_tanh():
    for i in range(4, 30):
        string = 'a' * i
        print(f'{i} : {DataString._len_score(string)}')


def test_randomness():
    lst = [
        'ABCabc123',
        'azaz!@#$',
        '1234567890',
        'a&*s@A#dsA@#d',
        'a&*s',
        'FindFirstFileA',
    ]

    for s in lst:
        print(f'"{s}" : {DataString._randomness_score(s)}')


def test_score():
    lst = [
        'http://www.google.com',
        'http://ocsp.thawte.com0',
        '1232',
        '1232546',
        'Local/Users/username/Downloads/',
        'a&*s@A#dsA@#d',
        'a&*s',
        'FindFirstFileA',
        'as$As',
        'Kernel32.dll',
        'kernel32.DLL',
    ]

    lst = [DataString(s, 'static_strings') for s in lst]
    lst.append(DataString('as$Aw', 'tight_strings'))
    lst = sorted(lst, reverse=True)
    for ds in lst:
        print(f'"{ds.string}" : {ds.score}')
        for k, v in ds.scores.items():
            print(f'\t{k}: {v}')


def test_feature_extractor():
    from feature_extractor import extract_features_from_output

    features = extract_features_from_output(
        'data/processed/malware_floss_output/malware-set_Backdoor.Win32.SkyDance.json', 'strings_above10_below3.json')
    print(features)

    features = extract_features_from_output(
        'data/processed/benign_floss_output/DikeDataset-main_files_benign_0a2027ea20fd995fd41fbe1a6e6a361dbdc09a83741f1d9e928eddf50030c6b3.exe.json', 'strings_above10_below3.json')

    print(features)


# test_category()
# test_tanh()
# test_randomness()
# test_score()
# test_feature_extractor()
