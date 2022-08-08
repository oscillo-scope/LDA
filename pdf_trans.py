from io import StringIO
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import process_pdf
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
import re
import os
from tqdm import tqdm
def read_from_pdf(file_path):
    """
    读取pdf文件
    """
    with open(file_path,'rb') as file:
        resource_manager = PDFResourceManager()
        return_str = StringIO()
        lap_params = LAParams()
        device = TextConverter(resource_manager,return_str,laparams=lap_params)
        process_pdf(resource_manager,device,file)
        device.close()
        content = return_str.getvalue()
        return_str.close()
        return re.sub('\s+',' ',content)

if __name__ == '__main__':
    path = './Annual Report on Exchange Arrangements and Exchange Restrictions/'
    files = os.listdir(path)
    fies_ = []
    for file in files:
        if file.split('.')[0] + '.txt' not in files2:
            fies_.append(file)
    for file in tqdm(fies_):
        print('正在处理：', file)
        content = read_from_pdf(path + file)
        with open('./转化为文本/' + file.split('.')[0] + '.txt', 'w', encoding='utf-8') as f:
            for line in content:
                f.write(line)