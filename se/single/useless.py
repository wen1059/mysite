import pdfplumber


def readtables(pdffile: str):
    with pdfplumber.open(pdffile) as f:
        for page in f.pages:
            tables_page = page.extract_tables()
    yield tables_page


for tables in readtables(
        r"C:\Users\Administrator\Documents\xwechat_files\wxid_l30992hnzgxe21_5a2c\msg\file\2025-08\6636氰化物.pdf"):
    for table in tables:
        for line in table:
            print([i.replace('\n', '') for i in line])
        print()
