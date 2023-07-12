import qrcode

ewm = qrcode.QRCode(
    version=4,
    error_correction=qrcode.ERROR_CORRECT_M,
    box_size=10,
    border=4
)
ewm.add_data('https://www.baidu.com/')
img = ewm.make_image()
img.show()
