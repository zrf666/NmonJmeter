# -*-coding: utf-8 -*-

from pyecharts.charts import Bar,Line
from pyecharts import options as opts
from pyecharts.globals import CurrentConfig
from script.Parse import Parse
from jinja2 import Template, Environment, FileSystemLoader
import numpy as np
import os
import shutil
import config as conf

# echarts_js_path = "../js/echarts.min.js"
# CurrentConfig.ONLINE_HOST = '../js/'
# CurrentConfig.js_host = "../html/js/"
class Draw(object):
    def __init__(self, name, file_path):
        self.table_template_dir = "../template"
        self.table_template_file = "table_template.html"
        # self.echarts_js_path = "../js/echarts.min.js"
        CurrentConfig.ONLINE_HOST = conf.echarts_js_path
        self.parse = Parse(file_path)
        self.save_dir = os.path.join(conf.output_dir, name)
        if os.path.exists(self.save_dir):
            shutil.rmtree(self.save_dir)
            os.makedirs(self.save_dir, exist_ok=True)
        else:
            os.makedirs(self.save_dir, exist_ok=True)

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

    def draw_common_line(self, datas, title, extend_axis=False,extend_index=0):
        print(datas)
        keys = list(datas.keys())
        values = list(datas.values())
        x_data = values[0]
        line = Line(init_opts=opts.InitOpts(width="100%", height="400px"))
        line.add_xaxis(x_data)
        for index in range(1, len(values)):
            line.add_yaxis(keys[index], values[index], label_opts=opts.LabelOpts(is_show=False))

        line.set_global_opts(title_opts=opts.TitleOpts(title=title))
        line.set_global_opts(tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type='cross'))
        echarts_html = line.render_embed()
        table_html = self.draw_common_table(datas)
        return echarts_html, table_html
        # line.render('DISKSIZE.html')

    def draw_common_stack_bar(self, datas, title, count=None):
        keys = list(datas.keys())
        values = list(datas.values())
        x_data = values[0]
        bar = Bar(init_opts=opts.InitOpts(width="100%", height="400px"))
        bar.add_xaxis(x_data)
        count = len(values) if count is None else count+1
        for index in range(1, count):
            bar.add_yaxis(keys[index], values[index], stack='stack')
        bar.set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        bar.set_global_opts(title_opts=opts.TitleOpts(title=title))
        echarts_html = bar.render_embed()
        table_html = self.draw_common_table(datas)
        return echarts_html, table_html

    def draw_SYS_SUMM(self):
        title = "SysSUMM"
        sys_sum_datas = self.parse.get_SYS_SUMM()
        datas = {
            'time': sys_sum_datas['time'],
            'CPU%': sys_sum_datas['CPU%'],
            'IO / sec': sys_sum_datas['IO / sec']
        }
        keys = list(datas.keys())
        values = list(datas.values())
        x_data = values[0]
        line = Line(init_opts=opts.InitOpts(width="100%", height="400px"))
        line.add_xaxis(x_data)
        for index in range(1, len(values)):
            line.add_yaxis(keys[index], values[index], yaxis_index=index - 1, label_opts=opts.LabelOpts(is_show=False))

        line.set_global_opts(title_opts=opts.TitleOpts(title=title))

        line.extend_axis(
            yaxis=opts.AxisOpts(name=keys[index], min_=0, max_=max(values[index]) + 50, position="right"))
        line.set_global_opts(yaxis_opts=opts.AxisOpts(name=keys[1], min_=0, max_=100, position='left'))
        line.set_global_opts(tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type='cross'))
        echarts_html = line.render_embed()
        table_html = self.draw_common_table(datas)
        return echarts_html, table_html

    def draw_AAAA(self):
        title = "AAAA"
        datas = self.parse.get_AAA()
        echarts_html = ""
        for data in datas:
            echarts_html += f"<div>{data}</div>\n"
        table_html = ""
        return echarts_html, table_html

    def draw_BBBP(self):
        title = "BBBP"
        datas = self.parse.get_BBBP()
        echarts_html = ""
        for data in datas:
            echarts_html += f"<div>{data}</div>\n"
        table_html = ""
        return echarts_html, table_html

    def draw_CPU_ALL(self):
        title = "CPU_ALL"
        datas = self.parse.get_CPU_ALL()
        # return self.draw_common_line(datas, title)
        return self.draw_common_stack_bar(datas, title, 4)

    def draw_CPU_SUMM(self):
        title = "CPU_SUMM"
        datas = self.parse.get_CPU_SUMM()
        # return self.draw_common_line(datas, title)
        return self.draw_common_stack_bar(datas, title, 3)

    def draw_CPU_XXX(self,cpu_xxx, cpu_xxx_data):
        title = f"{cpu_xxx}"
        return self.draw_common_stack_bar(cpu_xxx_data, title)

    def draw_DISKSIZE(self):
        title = "DISKSIZE"
        datas = self.parse.get_DISKBSIZE('dict')
        return self.draw_common_line(datas, title)

    def draw_DISKBUSY(self):
        title = "DISKBUSY"
        datas = self.parse.get_DISKBUSY()
        return self.draw_common_line(datas, title)

    def draw_DISKREAD(self):
        title = "DISKREAD"
        datas = self.parse.get_DISKREAD()
        return self.draw_common_line(datas, title)

    def draw_DISKWRITE(self):
        title = "DISKWRITE"
        datas = self.parse.get_DISKWRITE()
        return self.draw_common_line(datas, title)

    def draw_DISKXFER(self):
        title = "DISKX-FER"
        datas = self.parse.get_DISKXFER()
        return self.draw_common_line(datas, title)

    def draw_DISKSUMM(self):
        title = "DISKSUMM"
        datas = self.parse.get_DISK_SUMM()
        return self.draw_common_line(datas, title)


    def draw_JFSFILE(self):
        title = "JFSFILE"
        datas = self.parse.get_JFSFILE()
        keys = list(datas.keys())
        values = list(datas.values())
        # x_data = values[0]
        bar = Bar(init_opts=opts.InitOpts(width="100%", height="400px"))
        bar.add_xaxis(keys[1:3])
        y_avg_data = []
        for index in range(1, 3):
            y_avg_data.append(np.mean([float(val) for val in values[index]]))
        bar.add_yaxis('Avg', y_avg_data)
        bar.set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        bar.set_global_opts(title_opts=opts.TitleOpts(title=title))
        echarts_html = bar.render_embed()
        table_html = self.draw_common_table(datas)
        return echarts_html, table_html
        # return self.draw_common_stack_bar(datas, title, count=2)

    def draw_MEM(self):
        title = "MEMFree"
        datas = self.parse.get_MEM()
        keys = list(datas.keys())
        values = list(datas.values())
        x_data = values[0]
        line = Line(init_opts=opts.InitOpts(width="100%", height="400px"))
        line.add_xaxis(x_data)
        line.add_yaxis(keys[5], values[5], label_opts=opts.LabelOpts(is_show=False))

        line.set_global_opts(title_opts=opts.TitleOpts(title=title))
        line.set_global_opts(tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type='cross'))
        echarts_html = line.render_embed()
        table_html = self.draw_common_table(datas)
        return echarts_html, table_html

    def draw_NET(self):
        datas = self.parse.get_NET()
        title = "NET"
        return self.draw_common_line(datas, title)

    def draw_NETPACKET(self):
        datas = self.parse.get_NETPACKET()
        title = "NETPACKET"
        return self.draw_common_line(datas, title)

    def draw_PROC(self):
        datas = self.parse.get_PROC()
        title = "PROC"
        return self.draw_common_line(datas, title)

    def draw_VM(self):
        datas = self.parse.get_VM()
        title = "VM"
        return self.draw_common_line(datas, title)

    def draw_all_in_one_file(self):
        chart_dict = {
            'AAAA': self.draw_AAAA(),
            'BBBP': self.draw_BBBP(),
            'SYS_SUMM': self.draw_SYS_SUMM(),
            'CPU_ALL': self.draw_CPU_ALL(),
            'CPU_SUMM': self.draw_CPU_SUMM(),
        }
        for cpu_xxx in self.parse.get_cpus():
            cpu_xxx_data = self.parse.get_CPU_XXX(cpu_xxx)
            chart_dict[cpu_xxx] = self.draw_CPU_XXX(cpu_xxx, cpu_xxx_data)

        chart_dict['DISKSIZE'] = self.draw_DISKSIZE()
        chart_dict['DISKBUSY'] = self.draw_DISKBUSY()
        chart_dict['DISKREAD'] = self.draw_DISKREAD()
        chart_dict['DISKWRITE'] = self.draw_DISKWRITE()
        chart_dict['DISKXFER'] = self.draw_DISKXFER()
        chart_dict['DISKSUMM'] = self.draw_DISKSUMM()
        chart_dict['JFSFILE'] = self.draw_JFSFILE()
        chart_dict['MEM'] = self.draw_MEM()
        chart_dict['NET'] = self.draw_NET()
        chart_dict['NETPACKET'] = self.draw_NETPACKET()
        chart_dict['PROC'] = self.draw_PROC()
        # caht_dict['VM'] = self.draw_VM()
        return chart_dict

    def draw_all_in_any_file(self):
        chart_dict = self.draw_all_in_one_file()
        env = Environment(loader=FileSystemLoader('../template'))
        # 获取模板文件对象
        template = env.get_template('xxx_template.html')
        for key, val in chart_dict.items():
            rendered_html = template.render(chart=val[0], table=val[1])
            with open(os.path.join(self.save_dir, f'{key}.html'), 'w', encoding="utf-8") as f:
                f.write(rendered_html)
        return chart_dict.keys()



if __name__ == '__main__':
    nmon_file = "../tmp/186.1.47.93.nmon"
    p = Parse(nmon_file)