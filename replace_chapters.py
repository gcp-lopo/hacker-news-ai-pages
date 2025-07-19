import re

def replace_chapter_titles():
    """替换txt文件中的'二次元小说网'为具体的章节标题"""
    
    # 章节标题列表（根据爬虫脚本中的信息）
    chapter_titles = [
        "第1章 风水比医学更科学（道）",
        "第2章 最惨高考",
        "第3章 南上,应验",
        "第4章 预测与化解的原理（道）",
        "第5章 婚姻占卜术（术）",
        "第6章 掐指神通术（术）",
        "第7章 封建迷信进课本",
        "第8章 不要给别人算命（道）",
        "第9章 齐桓公怎么死的",
        "第10章 法不轻施,道不轻传",
        "第11章 开天眼",
        "第12章 风水轮流转",
        "第13章 坡的第一个面相（术）",
        "第14章 幻灭,节食省钱",
        "第15章 压死骆驼的最后一根稻草（术）",
        "第16章 赤口,应验",
        "第17章 语言隔阂阻挡不了的应验",
        "第18章 搬家",
        "第19章 美女如云（术）",
        "第20章 找不到组织的国际友人",
        "第21章 失之东隅,收之桑榆",
        "第22章 拉肚子（术）",
        "第23章 采日光功（术）",
        "第24章 采阴补阳",
        "第25章 第一次调风水之境煞（术）",
        "第26章 英语？华语？",
        "第27章 清水煮面",
        "第28章 不可思议的剑指站桩功（道）",
        "第29章 绝处逢生的发财之路",
        "第30章 红灯区的跟踪者",
        "第31章 万事俱备",
        "第32章 不刮东风",
        "第33章 剑指出气",
        "第34章 不再为钱所困",
        "第35章 被家暴（术）",
        "第36章 女神被包养",
        "第37章 小包子被骗",
        "第38章 性病",
        "第39章 创业危险,打工安全？（术）",
        "第40章 手艺人",
        "第41章 一个圈里支棱三根小棍儿",
        "第42章 天不助力",
        "第43章 没有我的教不会的学生",
        "第44章 正宗的坡早餐（术）",
        "第45章 不能出门的怪病",
        "第46章 人人都是神经病（术）",
        "第47章 洗心养神功（术）",
        "第48章 注意力就是生命力（道）",
        "第49章 很正确的废话",
        "第50章 咱俩不是同一个物种",
        "第51章 桃花乱乱开"
    ]
    
    # 读取原文件
    with open('天眼风水师.txt', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 统计"二次元小说网"的出现次数
    occurrences = content.count('二次元小说网')
    print(f"找到 {occurrences} 个'二次元小说网'需要替换")
    
    # 如果章节标题数量不够，补充一些
    if len(chapter_titles) < occurrences:
        for i in range(len(chapter_titles) + 1, occurrences + 1):
            chapter_titles.append(f"第{i}章 未知章节")
    
    # 替换所有的"二次元小说网"
    chapter_index = 0
    lines = content.split('\n')
    new_lines = []
    
    for line in lines:
        if '二次元小说网' in line:
            if chapter_index < len(chapter_titles):
                new_line = line.replace('二次元小说网', chapter_titles[chapter_index])
                new_lines.append(new_line)
                chapter_index += 1
                print(f"替换第 {chapter_index} 个: {chapter_titles[chapter_index-1]}")
            else:
                # 如果章节标题不够，保持原样
                new_lines.append(line)
        else:
            new_lines.append(line)
    
    # 写回文件
    new_content = '\n'.join(new_lines)
    with open('天眼风水师.txt', 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"\n替换完成！共替换了 {chapter_index} 个章节标题")
    print("文件已更新: 天眼风水师.txt")

if __name__ == "__main__":
    replace_chapter_titles() 