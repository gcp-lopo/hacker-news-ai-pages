import re

def clean_novel_file(input_file, output_file):
    """清理小说文件中的乱码字符"""
    print(f"正在清理文件: {input_file}")
    
    # 读取原文件
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 统计原始字符数
    original_length = len(content)
    print(f"原始文件大小: {original_length} 字符")
    
    # 定义需要清理的乱码模式
    patterns_to_remove = [
        r'\(\?\?\?\?\s*\?\?\)\?\s*\?\?',  # (???? ??)? ??
        r'\(\?\?\?\?\)',                  # (????)
        r'\?\?\?\?',                      # ????
        r'\(\?\?\?\)',                    # (???)
        r'\?\?\?',                        # ???
        r'\(\?\?\)',                      # (??)
        r'\?\?',                          # ??
        r'\(\?\)',                        # (?)
        r'\?{2,}',                        # 连续2个或更多问号
        r'\([^)]*\?[^)]*\)',              # 括号内包含问号的模式
    ]
    
    # 清理内容
    cleaned_content = content
    for pattern in patterns_to_remove:
        before_count = len(re.findall(pattern, cleaned_content))
        cleaned_content = re.sub(pattern, '', cleaned_content)
        after_count = len(re.findall(pattern, cleaned_content))
        if before_count > 0:
            print(f"清理模式 '{pattern}': 删除了 {before_count} 个匹配项")
    
    # 清理多余的空白字符
    cleaned_content = re.sub(r'\n\s*\n\s*\n+', '\n\n', cleaned_content)  # 多个空行变为两个
    cleaned_content = re.sub(r'^\s+', '', cleaned_content, flags=re.MULTILINE)  # 行首空白
    cleaned_content = re.sub(r'\s+$', '', cleaned_content, flags=re.MULTILINE)  # 行尾空白
    
    # 统计清理后的字符数
    cleaned_length = len(cleaned_content)
    removed_chars = original_length - cleaned_length
    
    print(f"清理后文件大小: {cleaned_length} 字符")
    print(f"总共删除了: {removed_chars} 字符")
    
    # 保存清理后的文件
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(cleaned_content)
    
    print(f"清理后的文件已保存为: {output_file}")
    return output_file

if __name__ == "__main__":
    input_file = "天眼风水师_完整版_v4.txt"
    output_file = "天眼风水师_完整版_清理版.txt"
    
    try:
        clean_novel_file(input_file, output_file)
        print("清理完成！")
    except Exception as e:
        print(f"清理过程中出现错误: {e}") 