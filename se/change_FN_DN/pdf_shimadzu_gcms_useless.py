"""
无法读取岛津的pdf报告，保留此文档做pypdf2库的使用演示
"""
import PyPDF2
import os
import re

with open(r"C:\Users\Administrator\Desktop\样品2.pdf",'rb') as f:
    reader=PyPDF2.PdfFileReader(f)
    for i in range(reader.numPages):
        print(reader.getPage(i).extractText())