from script.Draw import draw_DISKSIZE,draw_table
from script.Parse import Parse
from jinja2 import Template, Environment, FileSystemLoader


if __name__ == '__main__':
    nmon_file = "../nmon_file/sampleD.nmon"
    p = Parse(nmon_file)
    disk_size = p.get_DISKBSIZE("list")
    # draw_DISKSIZE(disk_size)
    # draw_table(disk_size)
    disk_busy = p.get_DISKBUSY('list')
    a = draw_DISKSIZE(disk_busy)
    b = draw_table(disk_busy, 'disk_busy.html')
    env = Environment(loader=FileSystemLoader('../template'))
    # 获取模板文件对象
    template = env.get_template('layout.html')
    rendered_html = template.render(chart=a, table=b)
    with open(f"../output/test.html", 'w', encoding="utf-8") as f:
        f.write(rendered_html)
