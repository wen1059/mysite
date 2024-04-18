# -*- coding: utf-8 -*-
# date: 2023-12-27
import decimal
from decimal import Decimal
import re


def epa_rounding(
        num: int | float | Decimal,
        digit: int = 3,
        mdl: int = 10,
) -> float | int | str:
    """
    四舍六入五成双保留指定有效位数，同时满足不超过检出限位数。
    放大到10^i次方倍，如保留3位有效数字就把数字放大到xxx.xxx
    修约到整数，再除以放大倍数
    :param num: 要修约的数字
    :param digit: 有效位数
    :param mdl: 检出限小数位数
    :return:
    """

    # 方法1确定zoom值
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

    # 方法2确定zoom值
    if int(num) > 0:
        zoom = digit - len(str(int(num)))  # 整数位和有效位数一样时缩放为0，每增加一位，zoom-1
    else:
        behind_0 = rst if (rst := re.search('\.(0*)', str(num)).group(1)) else ''  # 小数点后面的0
        zoom = digit + len(behind_0)  # 小数点后每增加一个0，zoom+1
    zoom = min(zoom, mdl)  # 根据检出限修正，达到这个效果：测定结果小于xxx时，结果保留小数和检出限一致。
    num_zoomed = num * (10 ** zoom)  # 放大10**zoom次方后的数字
    num_zoomed_rounded = float(Decimal(f'{num_zoomed}').quantize(Decimal('0'), decimal.ROUND_HALF_EVEN))  # 放大倍数后的数字四舍六入修约到整数
    num: float = num_zoomed_rounded / (10 ** zoom)  # 缩小倍数到原来。
    return str(int(num)) if num == int(num) else f'{num: .{zoom}f}'  # 整数的话取整去除x.0，小数的话补全后面的0。


print(epa_rounding(0.0012, 3, 3))
