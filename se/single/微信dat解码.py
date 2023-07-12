"""
还原dat文件为jpg
微信图片加密方式为图片所有字节码和一个随机字节码（代码中的xor）做异或处理。
由于jpg第一二个字节码固定为0xFF 0xD8，所以选一个dat文件的第一个字节和0xFF做异或处理 ，就能得到xor，再用xor和dat的所有字节做异或计算，能得到jpg原来的字节码。
png同理，第一二个字节码更换为0x89 0x50
"""
import os
from concurrent.futures import ProcessPoolExecutor
from itertools import islice
from collections import Counter
from glob import glob, iglob


# def yielddat(walkpath):
#     for root, _, files in os.walk(walkpath):
#         for file in files:
#             if '.dat' not in file:
#                 continue
#             yield os.path.join(root, file)


def findxor(walkpath):
    """
    找到异或码，如jpg为FF d8开头,png为89 50
    :param walkpath:
    :return:
    """
    for dat in iglob(walkpath + r'\**\*.dat', recursive=True):
        with open(dat, 'rb') as f:
            codes = list(islice(f.read(), 2))
            if (xorcode := codes[0] ^ 0xff) == codes[1] ^ 0xd8:
                return xorcode
            elif (xorcode := codes[0] ^ 0x89) == codes[1] ^ 0x50:
                return xorcode
            # xorcodes.append(xorcode)
            # break
        # print(xorcodes)
        # return Counter(xorcodes).most_common(1)[0][0]


def changecode(file, xorcode):
    """
    dat异或处理
    :param file: dat文件
    :param xorcode: dat和文件类型的异或码
    :return:还原的字节码
    """
    newcodes = []
    with open(file, 'rb') as f:
        for code in f.read():
            newcode = code ^ xorcode
            newcodes.append(newcode)
    return bytes(newcodes)


def writejpg(dat, xor):
    with open(dat + '.jpg', 'wb') as f:
        f.write(changecode(dat, xor))
    os.remove(dat)


if __name__ == '__main__':
    walkpath = r"D:\用户目录\我的文档\WeChat Files\wxid_fg6ovahkatz321\FileStorage\Image"
    xor = findxor(walkpath)
    with ProcessPoolExecutor() as pool:
        for dat in glob(walkpath + r'\**\*.dat', recursive=True):
            pool.submit(writejpg, dat, xor)
