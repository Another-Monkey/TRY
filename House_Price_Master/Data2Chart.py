import symbol

# import cities as cities
# import pyecharts
# import xlrd
# from pyecharts.charts import Bar
# from pyecharts.charts import Geo
# from pyecharts.charts import Line
# data = xlrd.open_workbook("bj_houseprice.xlsx") #读取表格
# table = data.sheets()[0] #读取表格的sheet
# print(table.nrows) #输出行数
# print(table.ncols) #输出列数
# #获取第一行数据
# rowldata = table.row_values(0)
# print(type(rowldata))
# print(rowldata) #['列1','列2']
# print(rowldata[0])
# averageprice = [43358, 11826, 30157, 10403, 15738, 23650, 11081, 11916, 19493, 24167, 31430]
#
# xdata = []
# ydata = []
# for i in range(0,table.nrows):
#     print(table.row_values(i))
#     xdata.append(table.row_values(i)[0])
#     ydata.append(table.row_values(i)[1])
#
# print(xdata)
# print(ydata)
# #对xdata和ydata列表进行处理
# sum = 0
# for i in range(len(ydata)):
# #    print(type(ydata[i]))
#     sum = sum + int(ydata[i])
# average = sum/len(ydata)
# print(average)
#
# #数据可视化,柱状图
# bar = Bar()
# bar.add_xaxis(xdata)
# bar.add_yaxis("Price,average",ydata)
# bar.add_xaxis(sum)
# bar.render()



from pyecharts.faker import Faker
from pyecharts import options as opts
from pyecharts.charts import Geo
from pyecharts.globals import ChartType
import os

provinces = ["北京", "成都", "杭州", "重庆", "合肥", "天津", "长沙","沈阳","青岛","宁波","东莞"]
averageprice = [43358, 11826, 30157, 10403, 15738, 23650, 11081, 11916, 19493, 24167, 31430]
def geo_heatmap(address, value) -> Geo:
    aa = [list(z) for z in zip(address, value)]
    c = (
        Geo()
        .add_schema(maptype="china")
        .add(
            "省热点图",    #图题
            aa,
            type_=ChartType.EFFECT_SCATTER,   #地图类型
        )
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))  #设置是否显示标签
        .set_global_opts(
                visualmap_opts=opts.VisualMapOpts(max_ = 50000),    #设置legend显示的最大值
                title_opts=opts.TitleOpts(title="Geo-HeatMap"),   #左上角标题
        )
    )
    return c
if __name__ == '__main__':
    province_heat = geo_heatmap(provinces, averageprice)
    province_heat.render("test_heatmap.html")
    os.system("test_heatmap.html") ####直接调用系统打开文件