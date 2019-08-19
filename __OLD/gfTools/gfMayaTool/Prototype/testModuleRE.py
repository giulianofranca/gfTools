import re

testToSearch = '''
abcdefghijklmnopqrstuvwxyz
ABCDEFGHIJKLMNOPQRSTUVWXYZ
1234567890

Ha Haha

MetaCharacters (Need to be escaped):
. ^ $ * + ? { } [ ] \ | ( )

coreyms.com

321-555-4321
123.555.1234

Mr. Schafer
Mr Smith
Ms Davis
Mrs. Robinson
Mr. T
'''

emails = '''
CoreyMSchafer@gmail.com
corey.schafer@university.edu
corey-321-schafer@my-work.net
'''

urls = '''
https://www.google.com
http://coreyms.com
https://youtube.com
https://www.nasa.gov
'''


def importMayaShelf():
    # shelves = '%s/prefs/shelves' % cmds.about(pd=True)
    pattern = re.compile(r'\d{3}[-.]\d{3}[-.]\d{4}') # Phone number = 321-555-1234 | [^-.] = Not - or .
    names = re.compile(r'(Mr|Ms|Mrs)\.?\s[A-Z]\w*')
    pattern2 = re.compile(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+')
    pattern3 = re.compile(r'https?://(www\.)?(\w+)(\.\w+)')
    # subbedUrls = pattern3.sub(r'\2\3', urls)
    # print(subbedUrls)
    matches = pattern3.findall(urls)
    for match in matches:
        print(match)
    # with open('data.txt', 'r') as f:
    #     contents = f.read()
    #     matches = pattern.finditer(contents)
    #     for match in matches:
    #         print(match)

importMayaShelf()
