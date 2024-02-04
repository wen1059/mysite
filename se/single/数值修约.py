# -*- coding: utf-8 -*-
# date: 2023-12-27
import decimal
from decimal import Decimal
import re


def epa_rounding(num: int | float | Decimal, digit: int = 3) -> float | int:
    """
    四舍六入五成双保留指定有效位数。
    放大到10^i次方倍，如保留3位有效数字就把数字放大到xxx.
    修约到整数，再除以放大倍数
    :param num: 要修约的数字
    :param digit: 有效位数
    :return:
    """
    # zoom = 0  # 放大倍数：10**zoom次方
    # if num < 10 ** (digit - 1):  # 需要放大的情况
    #     for i in range(1, 100):
    #         if num * (10 ** i) >= 10 ** (digit - 1):
    #             zoom = i
    #             break
    # elif num >= 10 ** digit:  # 需要缩小的情况
    #     for i in range(1, 100):
    #         if num * (10 ** -i) <= 10 ** digit:
    #             zoom = -i
    #             break

    if int(num) > 0:
        zoom = digit - len(str(int(num)))
    else:
        behind_0 = rst if (rst := re.search('\.(0*)', str(num)).group(1)) else ''  # 小数点后面的数字
        zoom = digit + len(behind_0)
    num_zoomed = num * (10 ** zoom)  # 放大后的数字
    num_zoomed_rounded = float(Decimal(f'{num_zoomed}').quantize(Decimal('0'), decimal.ROUND_HALF_EVEN))  # 放大后修约后的数字
    num = num_zoomed_rounded / (10 ** zoom)
    return int(num) if num >= 10 ** (digit - 1) else f"{num: .{zoom}f}"


print(epa_rounding(0.00033, 3))
