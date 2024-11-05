#要將這些字串模式（包含重複的字母數量條件）映射到特定的手術名稱，可以使用正則表達式（regex）來捕捉 H 和 G 的出現次數。以下是 Python 代碼示例，用於根據這些模式匹配輸入字串並將其映射到對應的手術名稱：

### Regex Method

import re

def classify_surgery_rex(code):
    # 定義模式
    patterns = {
        'Surgery_1': r'^AHGBDE$',                         # 完全匹配 AHGBDE
        'Surgery_2': r'^AHBGE$',                          # 完全匹配 AHBGE
        'Surgery_3': r'^AH{2,4}G{1,2}BDE$',               # H 出現 2 到 4 次, G 出現 1 到 2 次
        'Surgery_4': r'^AH{4,6}G{2,4}BDE$'                # H 出現 4 到 6 次, G 出現 2 到 4 次
    }

    # 逐個模式進行匹配
    for surgery, pattern in patterns.items():
        if re.match(pattern, code):
            return surgery

    return "Unknown Surgery"

def classify_surgery_cnt(code):
    # 檢查基本的固定結構（舉例：如必須以'A'開頭，'BDE'結尾）
    if not code.startswith('A') or not code.endswith('BDE'):
        return "Unknown Surgery"

    # 計算 H 和 G 的出現次數
    h_count = code.count('H')
    g_count = code.count('G')

    # 分類條件判斷
    if code == 'AHGBDE':
        return 'Surgery_1'
    elif code == 'AHBGE':
        return 'Surgery_2'
    elif 2 <= h_count <= 4 and 1 <= g_count <= 2 and code.startswith('AH') and code.endswith('BDE'):
        return 'Surgery_3'
    elif 4 <= h_count <= 6 and 2 <= g_count <= 4 and code.startswith('AH') and code.endswith('BDE'):
        return 'Surgery_4'
    else:
        return "Unknown Surgery"

# 測試
test_codes = ['AHGBDE', 'AHBGE', 'AHHHHBGGBDE', 'AHHHHHHGGGGBDE', 'AHHHBGGBDE']
for code in test_codes:
    print(f"{code}: {classify_surgery_rex(code)}")
    print(f"{code}: {classify_surgery_cnt(code)}")
