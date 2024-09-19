from script.Draw import  Draw
from script.Parse import Parse
from jinja2 import Template, Environment, FileSystemLoader


if __name__ == '__main__':
    # nmon_file = "../nmon_file/sampleD.nmon"
    # p = Parse(nmon_file)
    # disk_size = p.get_DISKBSIZE("list")
    # draw_DISKSIZE(disk_size)
    # draw_table(disk_size)
    # disk_busy = p.get_DISKBUSY('list')
    # disk_summ = p.get_DISK_SUMM()
    # sys_summ = p.get_SYS_SUMM()
    # a,b = draw_DISKSIZE(disk_busy)
    # b = draw_table(disk_busy, 'disk_busy.html')

    d = Draw()
    # a, b = d.draw_DISKSUMM(sys_summ)
    # a, b = d.draw_SYS_SUMM()
    # a, b = d.draw_CPU_SUMM()
    # a, b = d.draw_CPU_ALL()
    ip_dict = d.draw_all()
    data = {'sqmpleD' : ip_dict}
    env = Environment(loader=FileSystemLoader('../template'))
    # 获取模板文件对象
    # template = env.get_template('layout2.html')
    # rendered_html = template.render(datas=data)
    # with open(f"../output/test.html", 'w', encoding="utf-8") as f:
    #     f.write(rendered_html)

    a, b = d.draw_DISKSIZE()
    template = env.get_template('layout.html')
    rendered_html = template.render(chart=a, table=b)
    with open(f"../output/test2.html", 'w', encoding="utf-8") as f:
        f.write(rendered_html)

    a, b = d.draw_BBBP()
    template = env.get_template('layout.html')
    rendered_html = template.render(chart=a, table=b)
    with open(f"../output/AAAA.html", 'w', encoding="utf-8") as f:
        f.write(rendered_html)