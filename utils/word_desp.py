import json,re
from pathlib import Path

_PATH = Path(__file__).resolve().parent.parent / "data" / "word.json"
# _CHARLIST_PATH = Path(__file__).resolve().parent.parent / "data" / "charlist.json"

def _load():
    if not _PATH.exists():
        print("⚠️ 警告: data/word.json 不存在")
        return {}

    with open(_PATH, encoding="utf-8") as f:
        data = json.load(f)

    m = {}
    for item in data:
        word = item.get("word")
        if word:
            # 提取你想要的信息
            m[word] = {
                "explanation": item.get("explanation", ""),  # 详细释义
                "more": item.get("more", ""),  # 简介
                "strokes": item.get("strokes", ""),  # 笔画
                "radicals": item.get("radicals", ""),  # 结构
                "pinyin": item.get("pinyin", ""),  # 拼音
            }
    return m
WORD_DES = _load()

# def _load_charlist():
#     if not _CHARLIST_PATH.exists():
#         print("⚠️ 警告: data/charlist.json 不存在")
#         return []
#     with open(_CHARLIST_PATH, encoding="utf-8") as f:
#         return json.load(f)
# CHAR_LIST = _load_charlist()

def get_word_des(char):
    """获取汉字详细简介信息"""
    return WORD_DES.get(char, {})


def get_clean_description(word_data):
    """极简简介提取器：直击本义，去除词典冗余排版"""
    raw = word_data.get("explanation", "")
    if not raw:
        return "暂无简介。"

    # 1. 核心提取：如果有“本义”，直接抓取“本义”后面的内容
    match = re.search(r'本义[：:]?\s*([^。；\n]+)', raw)
    if match:
        core_text = match.group(1).strip()
        # 🌟 在 strip 中加入括号 ( ) 和全角括号 （ ）
        core_text = core_text.strip('。，,；;()（） ')
        return f"本义：{core_text}。"

    # 2. 如果没有“本义”，按行切分找第一句像人话的释义
    lines = raw.split("\n")
    for line in lines:
        line = line.strip()

        # 跳过空行、字本身、太短的行
        if not line or line == word_data.get("word") or len(line) < 2:
            continue

        # 跳过古文、拼音、词典序号
        if '--' in line or '《' in line or re.search(r'[a-zA-Z]{2,}', line) or re.search(r'[①②③④⑤]', line):
            continue

        # 清理掉所有成对的括号及其里面的内容
        line = re.sub(r'[\(（].*?[\)）]', '', line).strip()
        line = line.replace('(', '').replace(')', '').replace('（', '').replace('）', '')

        # 去掉尾巴上的词典标签，如 ；同本义、；亦作...
        line = re.split(r'[；;]', line)[0].strip()
        line = line.replace('同本义', '').strip()

        # 如果清理完还有字，就取这一句作为简介
        if len(line) >= 2:
            if not line.endswith('。'):
                line += '。'
            return line

    return "暂无简介。"

