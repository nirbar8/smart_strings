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
        for k, v in ds._scores.items():
            print(f'\t{k}: {v}')


test_score()
