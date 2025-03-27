# -*- coding: utf-8 -*-
# date: 2025-3-27
# colored_logging.py
import logging
from colorama import Fore, Back, Style, init

# 初始化colorama
init(autoreset=True)


class ColoredFormatter(logging.Formatter):
    """彩色日志格式化器"""

    # 定义日志级别颜色映射
    level_colors = {
        logging.DEBUG: Fore.CYAN,
        logging.INFO: Fore.GREEN,
        logging.WARNING: Fore.YELLOW,
        logging.ERROR: Fore.RED,
        logging.CRITICAL: Fore.RED + Back.WHITE + Style.BRIGHT
    }

    def format(self, record):
        # 获取默认格式化的日志消息
        message = super().format(record)
        # 根据日志级别添加颜色
        color = self.level_colors.get(record.levelno, Fore.WHITE)
        return color + message


def setup_colored_logging():
    """设置彩色日志输出（最小侵入式）"""
    # 获取根logger
    root_logger = logging.getLogger()

    # 只处理控制台handler
    for handler in root_logger.handlers:
        if isinstance(handler, logging.StreamHandler):
            # 保留原有格式，只添加颜色
            if handler.formatter:
                fmt = handler.formatter._fmt
                datefmt = handler.formatter.datefmt
            else:
                fmt = '%(levelname)s:%(name)s:%(message)s'
                datefmt = None

            # 替换为彩色格式化器
            handler.setFormatter(ColoredFormatter(fmt, datefmt))


# 使用示例
if __name__ == '__main__':
    setup_colored_logging()
