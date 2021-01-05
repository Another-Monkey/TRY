# coding : UTF-8
import requests
import csv
import random
import time
import socket
import http.client
# import urllib.request
from bs4 import BeautifulSoup
#用于转换数据格式
import csv
import xlwt
#用于绘制图表
import xlrd
from pyecharts.charts import Bar,Page
from pyecharts import options as opts
#用于绘制Geo地理图表
from pyecharts import options as opts
from pyecharts.charts import Geo
from pyecharts.globals import ChartType
import os
################### 城市缩略名与对应城市名 字典##################
City_Name_Dict = {'bj':"北京",'cd':"成都",'hz':"杭州",'cq':"重庆",'hf':"合肥",'tj':"天津",'cs':"长沙",
                  'sy':"沈阳",'qd':"青岛",'nb':"宁波",'dg':"东莞",'sz':"深圳",'wuhan':"武汉",
                  'nanjing':"南京",'sh':"上海",'suzhou':"苏州"}
def get_content(url, data=None):
    header = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
    }
    timeout = random.choice(range(80, 180))
    while True:
        try:
            rep = requests.get(url, headers=header, timeout=timeout)
            rep.encoding = 'gb2312'
            break
        except socket.timeout as e:
            print('3:', e)
            time.sleep(random.choice(range(8, 15)))

        except socket.error as e:
            print('4:', e)
            time.sleep(random.choice(range(20, 60)))

        except http.client.BadStatusLine as e:
            print('5:', e)
            time.sleep(random.choice(range(30, 80)))

        except http.client.IncompleteRead as e:
            print('6:', e)
            time.sleep(random.choice(range(5, 15)))

    return rep.text
    # return html_text


# 解析html
def get_data(html_text):
    final = []
    bs = BeautifulSoup(html_text, "html.parser")  # 创建BeautifulSoup对象
    body = bs.body  # 获取body部分
    data = body.find('div', {'id': 'newhouse_loupai_list'})  # 找到id为newhouse_loupai_list的div
    ul = data.find('ul')  # 获取ul部分
    li = ul.find_all('li')  # 获取所有的li

    list = []
    temp = ['名称','价格']
    list.append(temp)
    for day in li:  # 对每个li标签中的内容进行遍历
        try:
            temp = []
            name = day.find('div', {'class': 'nlcd_name'}).find('a').string.strip()  # 找到名称
            temp.append(name)  # 添加到temp中
            price = day.find('div', {'class': 'nhouse_price'}).find('span').get_text().strip()  # 找到价格
            temp.append(price)  # 第一个p标签中的内容加到temp中
            list.append(temp)
        except:
            print
            pass
        continue
    return list


# 生成表格
def write_data(data, name):
    file_name = name
    with open(file_name, 'a', errors='ignore', newline='') as f:
        f_csv = csv.writer(f)
        f_csv.writerows(data)

#用于转换数据格式（.csv）到（.xlsx）
def csv_to_xlsx(filename):
    with open(filename, 'r', encoding='gbk') as f:
        read = csv.reader(f)
        workbook = xlwt.Workbook()
        sheet = workbook.add_sheet('data')  # 创建一个sheet表格
        l = 0
        for line in read:
            if line[0] == '名称' or line[1] == '价格待定':
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
        format_name = "{}".format(filename)
        list1 = format_name.split(".")
        newname = "{}".format(list1[0])+".xlsx"
        print(newname)
        workbook.save(newname)  # 保存Excel

# 数据可视化
def Data2Chart(filename):
    data = xlrd.open_workbook(filename) #读取表格
    table = data.sheets()[0] #读取表格的sheet
    print(table.nrows) #输出行数
    print(table.ncols) #输出列数
    #获取第一行数据
    rowldata = table.row_values(0)
    print(type(rowldata))
    print(rowldata) #['列1','列2']
    print(rowldata[0])

    xdata = []
    ydata = []
    for i in range(0,table.nrows):
        print(table.row_values(i))
        xdata.append(table.row_values(i)[0])
        ydata.append(table.row_values(i)[1])

    print(xdata)
    print(ydata)
    #对xdata和ydata列表进行处理
    sum = 0
    for i in range(len(ydata)):
    #    print(type(ydata[i]))
        sum = sum + int(ydata[i])
    average = int(sum/len(ydata))
    print(average)
    Average_Pice.append(average)
    Selected_City.append(City_Name_Dict[city_simple])

    bar = Bar()
    bar.add_xaxis(xdata)
    bar.add_yaxis("Price",ydata)
    # bar.render(city_simple+'_render.html')
    bar.set_global_opts(title_opts=opts.TitleOpts(title=City_Name_Dict[city_simple]+"房价平均价格为："
                                                        +str(average)+"元"))
    Bar_List.append(bar)

#数据可视化进阶版 Geographic
def geo_heatmap(address, value) -> Geo:
    aa = [list(z) for z in zip(address, value)]
    c = (
        Geo()
        .add_schema(maptype="china")
        .add(
            "所选城市",    #图题
            aa,
            type_=ChartType.EFFECT_SCATTER,   #地图类型
        )
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))  #设置是否显示标签
        .set_global_opts(
                visualmap_opts=opts.VisualMapOpts(max_ = 60000),    #设置legend显示的最大值
                title_opts=opts.TitleOpts(title="城市房价分布图p"),   #左上角标题
        )
    )
    return c

# 主函数
if __name__ == '__main__':
    Average_Pice = []  #######在数据可视化函数中 每执行一次对列表元素追加一个城市的平均房价
    Selected_City = [] #######在数据可视化函数中，每执行一次，对列表中追加一个爬取房价的城市名称的缩略字母
    Bar_List = []      #######在数据可视化函数中，每执行一次函数，bar一次，将得到的bar放到此列表中
    # 获取北京的房价
    city_simple = 'bj'
    for i in range(1):
        page = str(i+1)
        print("开始获取第[" + page + "]页")
        url = 'http://'+city_simple+'.newhouse.fang.com/house/s/b9'+str(i)+'/?ctm=1.'+city_simple+'.xf_search.page.'+page
        print("url="+url)
        html = get_content(url)
        result = get_data(html)
        write_data(result, City_Name_Dict[city_simple]+'_HousePrice.csv')  #将爬取的数据写入.csv文件
    csv_to_xlsx(City_Name_Dict[city_simple]+'_HousePrice.csv') #转换文件格式
    Data2Chart(City_Name_Dict[city_simple]+'_HousePrice.xlsx')

    # 获取上海的房价
    city_simple = 'sh'
    for i in range(1):
        page = str(i + 1)
        print("开始获取第[" + page + "]页")
        url = 'http://'+city_simple+'.newhouse.fang.com/house/s/b9'+str(i)+'/?ctm=1.'+city_simple+'.xf_search.page.'+page
        print("url=" + url)
        html = get_content(url)
        result = get_data(html)
        write_data(result, City_Name_Dict[city_simple] + '_HousePrice.csv')  # 将爬取的数据写入.csv文件
    csv_to_xlsx(City_Name_Dict[city_simple] + '_HousePrice.csv')  # 转换文件格式
    Data2Chart(City_Name_Dict[city_simple] + '_HousePrice.xlsx')

    # 获取苏州的房价
    city_simple = 'suzhou'
    for i in range(1):
        page = str(i + 1)
        print("开始获取第[" + page + "]页")
        url = 'http://' + city_simple + '.newhouse.fang.com/house/s/b9' + str(
            i) + '/?ctm=1.' + city_simple + '.xf_search.page.' + page
        print("url=" + url)
        html = get_content(url)
        result = get_data(html)
        write_data(result, City_Name_Dict[city_simple] + '_HousePrice.csv')  # 将爬取的数据写入.csv文件
    csv_to_xlsx(City_Name_Dict[city_simple] + '_HousePrice.csv')  # 转换文件格式
    Data2Chart(City_Name_Dict[city_simple] + '_HousePrice.xlsx')

    # 获取成都的房价
    city_simple = 'cd'
    for i in range(1):
        page = str(i+1)
        print("开始获取第[" + page + "]页")
        url = 'http://'+city_simple+'.newhouse.fang.com/house/s/b9'+str(i)+'/?ctm=1.'+city_simple+'.xf_search.page.'+page
        print("url="+url)
        html = get_content(url)
        result = get_data(html)
        write_data(result, City_Name_Dict[city_simple]+'_Houseprice.csv')
    csv_to_xlsx(City_Name_Dict[city_simple] + '_Houseprice.csv')
    Data2Chart(City_Name_Dict[city_simple] + '_Houseprice.xlsx')

    #获取深圳的房价
    city_simple = 'sz'
    for i in range(1):
        page = str(i + 1)
        print("开始获取第[" + page + "]页")
        url = 'http://' + city_simple + '.newhouse.fang.com/house/s/b9' + str(
            i) + '/?ctm=1.' + city_simple + '.xf_search.page.' + page
        print("url=" + url)
        html = get_content(url)
        result = get_data(html)
        write_data(result, City_Name_Dict[city_simple] + '_Houseprice.csv')
    csv_to_xlsx(City_Name_Dict[city_simple] + '_Houseprice.csv')
    Data2Chart(City_Name_Dict[city_simple] + '_Houseprice.xlsx')

    # 获取武汉的房价
    city_simple = 'wuhan'
    for i in range(1):
        page = str(i + 1)
        print("开始获取第[" + page + "]页")
        url = 'http://' + city_simple + '.newhouse.fang.com/house/s/b9' + str(
            i) + '/?ctm=1.' + city_simple + '.xf_search.page.' + page
        print("url=" + url)
        html = get_content(url)
        result = get_data(html)
        write_data(result, City_Name_Dict[city_simple] + '_Houseprice.csv')
    csv_to_xlsx(City_Name_Dict[city_simple] + '_Houseprice.csv')
    Data2Chart(City_Name_Dict[city_simple] + '_Houseprice.xlsx')

    # 获取杭州的房价
    city_simple = 'hz'
    for i in range(1):
        page = str(i+1)
        print("开始获取第[" + page + "]页")
        url = 'http://'+city_simple+'.newhouse.fang.com/house/s/b9'+str(i)+'/?ctm=1.'+city_simple+'.xf_search.page.'+page
        print("url="+url)
        html = get_content(url)
        result = get_data(html)
        write_data(result, City_Name_Dict[city_simple]+'_Houseprice.csv')
    csv_to_xlsx(City_Name_Dict[city_simple] + '_Houseprice.csv')  # 转换文件格式
    Data2Chart(City_Name_Dict[city_simple] + '_Houseprice.xlsx')

    # 获取重庆的房价
    city_simple = 'cq'
    for i in range(1):
        page = str(i+1)
        print("开始获取第[" + page + "]页")
        url = 'http://'+city_simple+'.newhouse.fang.com/house/s/b9'+str(i)+'/?ctm=1.'+city_simple+'.xf_search.page.'+page
        print("url="+url)
        html = get_content(url)
        result = get_data(html)
        write_data(result, City_Name_Dict[city_simple]+'_Houseprice.csv')
    csv_to_xlsx(City_Name_Dict[city_simple] + '_Houseprice.csv')  # 转换文件格式
    Data2Chart(City_Name_Dict[city_simple] + '_Houseprice.xlsx')

    # 获取合肥的房价
    city_simple = 'hf'
    for i in range(1):
        page = str(i+1)
        print("开始获取第[" + page + "]页")
        url = 'http://'+city_simple+'.newhouse.fang.com/house/s/b9'+str(i)+'/?ctm=1.'+city_simple+'.xf_search.page.'+page
        print("url="+url)
        html = get_content(url)
        result = get_data(html)
        write_data(result, City_Name_Dict[city_simple]+'_Houseprice.csv')
    csv_to_xlsx(City_Name_Dict[city_simple] + '_Houseprice.csv')  # 转换文件格式
    Data2Chart(City_Name_Dict[city_simple] + '_Houseprice.xlsx')

    # 获取天津的房价
    city_simple = 'tj'
    for i in range(1):
        page = str(i+1)
        print("开始获取第[" + page + "]页")
        url = 'http://'+city_simple+'.newhouse.fang.com/house/s/b9'+str(i)+'/?ctm=1.'+city_simple+'.xf_search.page.'+page
        print("url="+url)
        html = get_content(url)
        result = get_data(html)
        write_data(result, City_Name_Dict[city_simple]+'_Houseprice.csv')
    csv_to_xlsx(City_Name_Dict[city_simple] + '_Houseprice.csv')  # 转换文件格式
    Data2Chart(City_Name_Dict[city_simple] + '_Houseprice.xlsx')

    # 获取长沙的房价
    city_simple = 'cs'
    for i in range(1):
        page = str(i+1)
        print("开始获取第[" + page + "]页")
        url = 'http://'+city_simple+'.newhouse.fang.com/house/s/b9'+str(i)+'/?ctm=1.'+city_simple+'.xf_search.page.'+page
        print("url="+url)
        html = get_content(url)
        result = get_data(html)
        write_data(result, City_Name_Dict[city_simple]+'_Houseprice.csv')
    csv_to_xlsx(City_Name_Dict[city_simple] + '_Houseprice.csv')  # 转换文件格式
    Data2Chart(City_Name_Dict[city_simple] + '_Houseprice.xlsx')

    # 获取沈阳的房价
    city_simple = 'sy'
    for i in range(1):
        page = str(i+1)
        print("开始获取第[" + page + "]页")
        url = 'http://'+city_simple+'.newhouse.fang.com/house/s/b9'+str(i)+'/?ctm=1.'+city_simple+'.xf_search.page.'+page
        print("url="+url)
        html = get_content(url)
        result = get_data(html)
        write_data(result, City_Name_Dict[city_simple]+'_Houseprice.csv')
    csv_to_xlsx(City_Name_Dict[city_simple] + '_Houseprice.csv')  # 转换文件格式
    Data2Chart(City_Name_Dict[city_simple] + '_Houseprice.xlsx')

    # 获取青岛的房价
    city_simple = 'qd'
    for i in range(1):
        page = str(i+1)
        print("开始获取第[" + page + "]页")
        url = 'http://'+city_simple+'.newhouse.fang.com/house/s/b9'+str(i)+'/?ctm=1.'+city_simple+'.xf_search.page.'+page
        print("url="+url)
        html = get_content(url)
        result = get_data(html)
        write_data(result, City_Name_Dict[city_simple]+'_Houseprice.csv')
    csv_to_xlsx(City_Name_Dict[city_simple] + '_Houseprice.csv')  # 转换文件格式
    Data2Chart(City_Name_Dict[city_simple] + '_Houseprice.xlsx')

    # 获取宁波的房价
    city_simple = 'nb'
    for i in range(1):
        page = str(i+1)
        print("开始获取第[" + page + "]页")
        url = 'http://'+city_simple+'.newhouse.fang.com/house/s/b9'+str(i)+'/?ctm=1.'+city_simple+'.xf_search.page.'+page
        print("url="+url)
        html = get_content(url)
        result = get_data(html)
        write_data(result, City_Name_Dict[city_simple]+'_Houseprice.csv')
    csv_to_xlsx(City_Name_Dict[city_simple] + '_Houseprice.csv')  # 转换文件格式
    Data2Chart(City_Name_Dict[city_simple] + '_Houseprice.xlsx')

    # 获取东莞的房价
    city_simple = 'dg'
    for i in range(1):
        page = str(i+1)
        print("开始获取第[" + page + "]页")
        url = 'http://'+city_simple+'.newhouse.fang.com/house/s/b9'+str(i)+'/?ctm=1.'+city_simple+'.xf_search.page.'+page
        print("url="+url)
        html = get_content(url)
        result = get_data(html)
        write_data(result, City_Name_Dict[city_simple]+'_Houseprice.csv')
    csv_to_xlsx(City_Name_Dict[city_simple] + '_Houseprice.csv')  # 转换文件格式
    Data2Chart(City_Name_Dict[city_simple] + '_Houseprice.xlsx')

    print("获取结束")
    print(Average_Pice)
    print(Selected_City)
    print(Bar_List)
    Provience_Map = geo_heatmap(Selected_City,Average_Pice)
    Provience_Map.render("城市房价分布图.html")
    page = Page(layout=Page.DraggablePageLayout)
    page.add(Bar_List[0],Bar_List[1],Bar_List[2],Bar_List[3],
             Bar_List[4],Bar_List[5],Bar_List[6],Bar_List[7],
             Bar_List[8],Bar_List[9],Bar_List[10],Bar_List[11],
             Bar_List[12],Bar_List[13],Bar_List[14])
    page.render("房价统计图.html")
    ########调用os.system直接打开相应文件#########
    os.system("房价统计图.html")
    os.system("城市房价分布图.html")