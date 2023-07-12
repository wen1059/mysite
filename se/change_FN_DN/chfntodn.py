import os, stat, shutil
from bs4 import BeautifulSoup


def searchsamplename(xmlfile):
    '''
    查找样品名称
    :param xmlfile: sample_info.xml文件的绝对路径
    :return: SampleName名称
    '''
    os.chmod(xmlfile, stat.S_IWRITE)
    file = open(xmlfile, 'r+', encoding='UTF-8')
    soup = BeautifulSoup(file, features='lxml')
    elems = soup.find_all(text='Sample Name')
    tag = elems[0].parent.parent
    samplenamename = tag.select('Value')
    result = samplenamename[0].get_text()
    file.close()
    return result


def exchangename(xmlfile, samplename, dataname):
    '''
    :param xmlfile: sample_info.xml文件的绝对路径
    :param samplename:
    :param dataname: 保存的.D数据名，不含‘.D’
    :return:
    '''
    file = open(xmlfile, 'r+', encoding='UTF-8')
    text = file.read()
    text = text.replace(samplename, dataname)
    file.close()
    bakfile = xmlfile + '.bak'
    shutil.copy(xmlfile, bakfile)  # 备份，重命名为*.bak
    file = open(xmlfile, 'w+', encoding='UTF-8')
    file.write(text)
    file.close()


path = r'C:\ttmp'
for root, dirs, files in os.walk(path):
    for dir in dirs:
        if '.D' in dir:
            dataname = dir[:-2]
            xmlfile = os.path.join(root, dir, r'AcqData\sample_info.xml')
            if os.path.exists(xmlfile):
                try:
                    samplename = searchsamplename(xmlfile)
                    exchangename(xmlfile, samplename, dataname)
                    os.renames(os.path.join(root, dir), os.path.join(root, samplename + '.D'))
                    print('{}.D ————> {}.D'.format(dataname, samplename))
                except:
                    print('sample_info.xml文件可能已损坏')
            else:
                print('{}不是标准masshunter格式，请转换数据格式后重试'.format(os.path.join(root, dir)))
