import openpyxl


def write_xlsx_to_txt(xlsx_file, txt_file):
    # 打开 Excel 文件
    wb = openpyxl.load_workbook(xlsx_file)
    # 获取第一个工作表
    sheet = wb.active

    # 打开要写入的 txt 文件
    with open(txt_file, 'w', encoding='utf-8') as txt:
        # 遍历每一行
        for row in sheet.iter_rows(values_only=True):
            # 将每一行的数据转换为字符串，列之间以制表符分隔
            line = '\t'.join(str(cell) for cell in row)
            # 写入到 txt 文件，并添加换行符
            txt.write(line + '\n')


# 指定输入和输出文件名
xlsx_file = r'C:\Users\LEGION\Desktop\scu2024\数据赋能中心\困难认定.xlsx'
txt_file = r'C:\Users\LEGION\Desktop\scu2024\数据赋能中心\困难认定.txt'

# 调用函数将 xlsx 文件写入到 txt 文件中
write_xlsx_to_txt(xlsx_file, txt_file)
