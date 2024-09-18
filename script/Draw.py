# -*-coding: utf-8 -*-

from pyecharts.charts import Bar,Line
from pyecharts import options as opts
from pyecharts.globals import CurrentConfig
from script.Parse import Parse
from jinja2 import Template, Environment, FileSystemLoader


echarts_js_path = "../js/echarts.min.js"
CurrentConfig.ONLINE_HOST = '../js/'
# CurrentConfig.js_host = "../html/js/"
class Draw(object):
    def __init__(self):
        self.table_template_dir = "../template"
        self.table_template_file = "table_template.html"
        self.echarts_js_path = "../js/echarts.min.js"
        CurrentConfig.ONLINE_HOST = '../js/'
        self.parse = Parse("../nmon_file/sampleD.nmon")

    def draw_common_table(self,datas):
        keys = list(datas.keys())
        values = list(datas.values())
        datas = []
        # 因为图表的数据与表格的数据矩阵不同，需要转置成横表
        for i in range(len(values[0])):
            row_data = []
            for val in values:
                row_data.append(val[i])
            datas.append(row_data)
        # 创建一个 Jinja2 环境对象，并指定模板文件的路径
        env = Environment(loader=FileSystemLoader(self.table_template_dir))
        # 获取模板文件对象
        template = env.get_template(self.table_template_file)
        rendered_html = template.render(theads=keys, datas=datas)
        return rendered_html

    def draw_common_echarts(self, datas, title, extend_axis=False,extend_index=0):
        print(datas)
        keys = list(datas.keys())
        values = list(datas.values())
        x_data = values[0]
        line = Line(init_opts=opts.InitOpts(width="120%", height="400px"))
        line.add_xaxis(x_data)
        for index in range(1, len(values)):
            line.add_yaxis(keys[index], values[index], yaxis_index=index-1, label_opts=opts.LabelOpts(is_show=False))

        line.set_global_opts(title_opts=opts.TitleOpts(title=title))
        if extend_axis:
            line.extend_axis(yaxis=opts.AxisOpts(name=keys[index], min_=0, max_=max(values[index])+50, position="right"))
            line.set_global_opts(yaxis_opts=opts.AxisOpts(name=keys[1],min_=0, max_=100, position='left'))
        line.set_global_opts(tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type='cross'))
        echarts_html = line.render_embed()
        table_html = self.draw_common_table(datas)
        return echarts_html, table_html
        # line.render('DISKSIZE.html')

    def draw_SYS_SUMM(self, datas):
        title = "SysSUMM"
        return self.draw_common_echarts({
            'time': datas['time'],
            'CPU%': datas['CPU%'],
            'IO / sec': datas['IO / sec']
        }, title, extend_axis=True, extend_index=2)

    def draw_CPU_ALL(self):
        title = "CPU_ALL"
        datas = self.parse.get_CPU_ALL()
        return self.draw_common_echarts(datas, title)

    def draw_CPU_SUMM(self):
        title = "CPU_SUMM"
        datas = self.parse.get_CPU_SUMM()
        return self.draw_common_echarts(datas, title)

    def draw_DISKSIZE(self):
        title = "DISKSIZE"
        datas = self.parse.get_DISKBSIZE('dict')
        return self.draw_common_echarts(datas, title)

    def draw_DISKBUSY(self):
        title = "DISKBUSY"
        datas = self.parse.get_DISKBUSY()
        return self.draw_common_echarts(datas, title)

    def draw_DISKREAD(self):
        title = "DISKREAD"
        datas = self.parse.get_DISKREAD()
        return self.draw_common_echarts(datas, title)

    def draw_DISKWRITE(self):
        title = "DISKWRITE"
        datas = self.parse.get_DISKWRITE()
        return self.draw_common_echarts(datas, title)

    def draw_DISKXFER(self):
        title = "DISKX-FER"
        datas = self.parse.get_DISKXFER()
        return self.draw_common_echarts(datas, title)

    def draw_DISKSUMM(self):
        title = "DISKSUMM"
        datas = self.parse.get_DISK_SUMM()
        return self.draw_common_echarts(datas, title)

def draw_table(datas):
    keys = list(datas.keys())
    values = list(datas.values())
    datas = []
    # 因为图表的数据与表格的数据矩阵不同，需要转置成横表
    for i in range(len(values[0])):
        row_data = []
        for val in values:
            row_data.append(val[i])
        datas.append(row_data)
    # 创建一个 Jinja2 环境对象，并指定模板文件的路径
    env = Environment(loader=FileSystemLoader('../template'))
    # 获取模板文件对象
    template = env.get_template('table_template.html')
    rendered_html = template.render(theads=keys, datas=datas)
    return rendered_html
    # with open(f"../output/{file_name}", 'w', encoding="utf-8") as f:
    #     f.write(rendered_html)


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
    line = Line(init_opts=opts.InitOpts(width="120%", height="400px"))
    line.add_xaxis(x_data)
    for index in range(1, len(values)):
        line.add_yaxis(keys[index], values[index],  label_opts=opts.LabelOpts(is_show=False))

    line.set_global_opts(title_opts=opts.TitleOpts(title='DISKSIZE'))
    # line.extend_axis(yaxis=opts.AxisOpts(name='Y2', min_=0, max_=2500, position="right"))
    line.set_global_opts(tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type='cross'))
    echart_html = line.render_embed()
    table_html = draw_table(datas)
    return echart_html,table_html
    # line.render('DISKSIZE.html')

if __name__ == '__main__':
    nmon_file = "../tmp/186.1.47.93.nmon"
    p = Parse(nmon_file)
    sys_sum = p.get_SYS_SUMM()
    draw_SYS_SUMM(sys_sum)
    # disk_size = p.get_DISKBSIZE('list')
    # draw_DISKSIZE(disk_size)