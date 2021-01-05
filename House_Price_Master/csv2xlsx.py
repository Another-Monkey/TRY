import csv
import xlwt
name = 'bj_houseprice.csv'
def csv_to_xlsx():
    with open(name, 'r', encoding='gbk') as f:
        read = csv.reader(f)
        workbook = xlwt.Workbook()
        sheet = workbook.add_sheet('data')  # 创建一个sheet表格
        l = 0
        for line in read:
            if line[0] == '名称' or line[1] == '价格待定' :
                continue
            if int(line[1]) < 3000:
                continue
            print(line)
            r = 0
            for i in line:

                print(i)

                sheet.write(l, r, i)  # 一个一个将单元格数据写入
                r = r + 1
            l = l + 1
        format_name = "{}".format(name)
        list1 = format_name.split(".")
        newname = "{}".format(list1[0])+".xlsx"
        print(newname)
        workbook.save(newname)  # 保存Excel



if __name__ == '__main__':
    csv_to_xlsx()
