# -*-coding: utf-8 -*-

from pyecharts.charts import Bar,Line
from pyecharts import options as opts
from pyecharts.globals import CurrentConfig
from nmonAnalyze.Parse import Parse

echarts_js_path = "../html/js/echarts.min.js"
CurrentConfig.ONLINE_HOST = '../html/js/'
# CurrentConfig.js_host = "../html/js/"

def draw_SYS_SUMM(datas):
    x_data = [list(item.values())[0] for item in datas]
    y_data1 = [list(item.values())[1] for item in datas]
    y_data2 = [list(item.values())[2] for item in datas]
    line = Line(init_opts=opts.InitOpts(width="1600px", height="400px"))
    line.add_xaxis(x_data)
    line.add_yaxis("Y1", y_data1,yaxis_index=0, label_opts=opts.LabelOpts(is_show=False))
    line.add_yaxis("Y2", y_data2, yaxis_index=1, label_opts=opts.LabelOpts(is_show=False))
    line.set_global_opts(title_opts=opts.TitleOpts(title='SYS_SUMM'))
    line.extend_axis(yaxis=opts.AxisOpts(name='Y2',min_=0,max_=2500, position="right"))
    line.set_global_opts(yaxis_opts=opts.AxisOpts(name='Y1',min_=0,max_=100, position="left"),tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type='cross'))
    line.render('SYS_SUMM.html')


def draw_DISKSIZE(datas):
    print(datas)
    keys = list(datas.keys())
    values = list(datas.values())
    x_data = values[0]
    line = Line(init_opts=opts.InitOpts(width="1600px", height="400px"))
    line.add_xaxis(x_data)
    for index in range(1, len(values)):
        line.add_yaxis(keys[index], values[index],  label_opts=opts.LabelOpts(is_show=False))

    line.set_global_opts(title_opts=opts.TitleOpts(title='DISKSIZE'))
    # line.extend_axis(yaxis=opts.AxisOpts(name='Y2', min_=0, max_=2500, position="right"))
    line.set_global_opts(tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type='cross'))
    line.render('DISKSIZE.html')

if __name__ == '__main__':
    nmon_file = "../tmp/186.1.47.93.nmon"
    p = Parse(nmon_file)
    # sys_sum = p.get_SYS_SUMM()
    # draw_SYS_SUMM(sys_sum)
    disk_size = p.get_DISKBSIZE('list')
    draw_DISKSIZE(disk_size)