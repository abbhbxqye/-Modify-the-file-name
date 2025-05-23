# ===== 配置区域 =====
# 配置说明：
#   remove_digits: 是否去除文件名中的数字（True/False）
#   case: 文件名大小写处理方式，可选："lower"（全部小写）、"upper"（全部大写）、"none"（不变）
#   remove_parentheses: 是否去除括号（True/False）
#   remove_fullwidth: 是否去除全角符号（True/False），与 remove_parentheses 配合时只去除全角括号
#   remove_ampersand: 是否去除&符号（True/False）
#   remove_hash: 是否去除#符号（True/False）
#   remove_at: 是否去除@符号（True/False）
#   remove_underscore: 是否去除下划线_（True/False）
#   remove_space: 是否去除空格（True/False）
#   remove_symbols: 需要去除的自定义符号字符串（如"￥*"，留空则不处理）
#   remove_chinese: 是否去除所有中文字符（True/False）
#   recursive: 是否递归处理子文件夹（True/False，默认False）
#   target_dir: 需要处理的目标文件夹路径（可选，不填则为脚本所在目录）
CONFIG = {
    "remove_digits": True,           # 是否去除数字
    "case": "upper",               # 文件名大小写处理方式
    "remove_parentheses": True,      # 是否去除括号
    "remove_fullwidth": True,        # 是否去除全角符号（与括号配合时只去除全角括号）
    "remove_ampersand": True,        # 是否去除&符号
    "remove_hash": True,             # 是否去除#符号
    "remove_at": True,               # 是否去除@符号
    "remove_underscore": True,       # 是否去除下划线_
    "remove_space": True,            # 是否去除空格
    "remove_symbols": "￥*-",         # 需要去除的自定义符号
    "remove_chinese": False,         # 是否去除所有中文字符
    "recursive": False,              # 是否递归处理子文件夹
    "target_dir": r"G:\hmcl\.minecraft\versions\1.20.1-Forge_47.4.1\.addurdisc\assets\addurdisc\sounds"  # 目标文件夹路径（可选）
}
# ====================

import os
import re

def process_filename(filename, config):
    name, ext = os.path.splitext(filename)
    # 去除括号
    if config.get('remove_parentheses', False):
        if config.get('remove_fullwidth', False):
            # 去除英文括号和全角括号
            name = re.sub(r'[()\[\]\{\}（）【】｛｝《》〈〉「」『』]', '', name)
        else:
            # 只去除英文括号
            name = re.sub(r'[()\[\]\{\}]', '', name)
    elif config.get('remove_fullwidth', False):
        # 只去除全角符号（不包括括号）
        # 全角符号Unicode范围：FF00-FFEF，排除全角括号
        name = re.sub(r'[\uFF01-\uFF5E]', '', name)
        # 也可根据需要扩展其它全角符号
    # 去除&符号
    if config.get('remove_ampersand', False):
        name = name.replace('&', '')
    # 去除#符号
    if config.get('remove_hash', False):
        name = name.replace('#', '')
    # 去除@符号
    if config.get('remove_at', False):
        name = name.replace('@', '')
    # 去除下划线
    if config.get('remove_underscore', False):
        name = name.replace('_', '')
    # 去除空格
    if config.get('remove_space', False):
        name = name.replace(' ', '')
    # 去除自定义符号
    symbols = config.get('remove_symbols', '')
    if symbols:
        for ch in symbols:
            name = name.replace(ch, '')
    # 去除数字
    if config.get('remove_digits', False):
        name = re.sub(r'\d+', '', name)
    # 去除中文字符
    if config.get('remove_chinese', False):
        name = re.sub(r'[\u4e00-\u9fff]', '', name)
    # 大小写处理
    case_rule = config.get('case', 'none')
    if case_rule == 'lower':
        name = name.lower()
    elif case_rule == 'upper':
        name = name.upper()
    return name + ext

def rename_files_in_dir(target_dir, config):
    for fname in os.listdir(target_dir):
        fpath = os.path.join(target_dir, fname)
        if os.path.isfile(fpath):
            new_fname = process_filename(fname, config)
            new_fpath = os.path.join(target_dir, new_fname)
            if new_fname != fname:
                # 避免重名覆盖
                counter = 1
                base_name, ext = os.path.splitext(new_fname)
                while os.path.exists(new_fpath):
                    new_fname = f"{base_name}_{counter}{ext}"
                    new_fpath = os.path.join(target_dir, new_fname)
                    counter += 1
                os.rename(fpath, new_fpath)
                print(f"重命名: {fname} -> {new_fname}")
        elif os.path.isdir(fpath) and config.get('recursive', False):
            rename_files_in_dir(fpath, config)

def main():
    target_dir = CONFIG.get('target_dir', os.path.dirname(__file__))
    rename_files_in_dir(target_dir, CONFIG)

if __name__ == '__main__':
    main()
