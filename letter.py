import nltk
from collections import Counter
from itertools import product

# 确保布朗语料库已下载
nltk.download('brown')

# 加载布朗语料库
from nltk.corpus import brown

# 获取所有文本
texts = brown.words()

# 将所有文本转换为小写并合并为一个字符串
all_text = ' '.join(word.lower() for word in texts)

# 统计单个字母的频率
letter_counts = Counter(all_text.replace(' ', ''))  # 移除空格后统计

# 输出单个字母频率排序
print("单个字母频率排序:")
for letter, count in letter_counts.most_common():
    if letter.isalpha():  # 确保是字母
        print(f"{letter}: {count}")

# 统计两字母组合的频率
bigram_counts = Counter()
for i in range(len(all_text) - 1):
    if all_text[i].isalpha() and all_text[i+1].isalpha():  # 确保是字母组合
        bigram = all_text[i] + all_text[i+1]
        bigram_counts[bigram] += 1

# 输出两字母组合频率排序
print("\n两字母组合频率排序:")
for bigram, count in bigram_counts.most_common():
    print(f"{bigram}: {count}")
#
# 将这些字符按顺序存入数组singleworld中
singleworld = [
    'e', 't', 'a', 'o', 'i', 'n', 's', 'r', 'h', 'l', 'd', 'c', 'u', 'm', 
    'f', 'p', 'g', 'w', 'y', 'b', 'v', 'k', 'x', 'j', 'q', 'z'
]
# 将这些字符按顺序存入数组doubleworld中
doubleworld = [
    'th', 'he', 'in', 'er', 'an', 're', 'on', 'at', 'en', 'nd', 
    'ed', 'or', 'es', 'ti', 'te', 'it', 'is', 'st', 'to', 
    'ar', 'of', 'ng', 'ha', 'al', 'ou', 'nt', 'as', 'hi',
    'se', 'le', 've', 'me', 'co', 'ne', 'de', 'ea',
    # ... (继续添加其他组合)
]