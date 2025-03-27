# -*- coding: utf-8 -*-
# date: 2024-12-13
import qrcode
import os


def gen_qrcode(url='https://example.com'):
    """
    生成二维码
    :param url:
    :return:PIL图片对象
    """
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=1,
        border=1,
    )
    qr.add_data(url)
    qr.make(fit=True)
    qr_image = qr.make_image(fill_color="black", back_color="white")
    return qr_image


def trans_to_ascii(qr_image):
    """
    二维码图像转为ascii
    :param qr_image:
    :return:
    """
    ascii_qr = qr_image.convert('1')  # Convert to black and white
    width, height = ascii_qr.size
    qr_data = ascii_qr.getdata()

    ascii_text = ''
    for y in range(height):
        for x in range(width):
            if qr_data[y * width + x]:
                ascii_text += '||'
            else:
                ascii_text += '  '
        ascii_text += '\n'
    return ascii_text


def save_ascii_text(text):
    with open('ascii_qr.txt', 'w') as f:
        f.write(text)


if __name__ == '__main__':
    imageobj = gen_qrcode(r'http://10.1.224.117/')
    asc_txt = trans_to_ascii(imageobj)
    # save_ascii_text(asc_txt)
    print(asc_txt)
    os.system('pause')
