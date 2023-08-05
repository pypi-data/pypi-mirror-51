#!/usr/bin/python3.7
# -*- coding: utf-8 -*-
# @Time    : 2019/7/20 13:42
# @Email  : jtyoui@qq.com
# @Software: PyCharm
from jtyoui.error import LibraryNotInstallError
from jtyoui.tools import pips
import os
import glob

try:
    import fitz  # 安装 pip install PyMuPDF
except ModuleNotFoundError:
    try:
        fitz = pips('fitz', 'PyMuPDF')  # 自动安装
    except ModuleNotFoundError:
        raise LibraryNotInstallError("安装 pip install PyMuPDF")


def _get_dir_name(file_dir):
    base_name = os.path.basename(file_dir)  # 获得地址的文件名
    dir_name = os.path.dirname(file_dir)  # 获得地址的父链接
    return dir_name, base_name


def image_pdf(file_dir, pdf_address=None):
    """
    照片转pdf
    :param file_dir: 照片的地址文件夹
    :param pdf_address: 保存pdf的文件地址，默认是当前地址
    :return: 成功返回True
    """
    dir_name, base_name = _get_dir_name(file_dir)
    doc = fitz.Document()
    for img in sorted(glob.glob(file_dir + '\\*'), key=os.path.getmtime):  # 排序获得对象
        img_doc = fitz.Document(img)  # 获得图片对象
        pdf_bytes = img_doc.convertToPDF()  # 获得图片流对象
        img_pdf = fitz.Document("pdf", pdf_bytes)  # 将图片流创建单个的PDF文件
        doc.insertPDF(img_pdf)  # 将单个文件插入到文档
        img_doc.close()
        img_pdf.close()
    if not pdf_address:
        doc.save(dir_name + os.sep + base_name + ".pdf")  # 保存文档
    else:
        doc.save(pdf_address + ".pdf")  # 保存文档
    doc.close()
    return True


def pdf_image(pdf_address, image_dir=None):
    """
    PDF转照片
    :param pdf_address: PDF文件地址
    :param image_dir: 照片的文件夹地址
    :return: 成功返回True
    """
    dir_name, base_name = _get_dir_name(pdf_address)
    pdf = fitz.Document(pdf_address)
    for pg in range(0, pdf.pageCount):
        page = pdf[pg]  # 获得每一页的对象
        trans = fitz.Matrix(1.0, 1.0).preRotate(0)
        pm = page.getPixmap(matrix=trans, alpha=False)  # 获得每一页的流对象
        if not image_dir:
            pm.writePNG(str(pdf_address[:-4]) + os.sep + str(base_name[:-4]) + '_{:0>4d}.jpg'.format(pg + 1))  # 保存图片
        else:
            pm.writePNG(image_dir + os.sep + str(base_name[:-4]) + '_{:0>4d}.jpg'.format(pg + 1))  # 保存图片
    pdf.close()
    return True


if __name__ == '__main__':
    image_pdf(r'D:\temp')  # 将照片转pdf
    pdf_image(r'D:\temp.pdf')  # 将PDF转照片
