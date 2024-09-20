from script.Draw import  Draw
from script.Parse import Parse
from jinja2 import Template, Environment, FileSystemLoader
import config as conf
import os
def draw_main():
    nmon_file_names = os.listdir(conf.nmon_file_dir)
    print(nmon_file_names)
    names = []
    for file in nmon_file_names:
        if file.endswith(".nmon"):
            names.append(file)
    print(names)
    chart_datas = {}
    for name in names:
        file_path = os.path.join(conf.nmon_file_dir, name)
        prefix_name = name.replace('.nmon', '')
        prefix_name = prefix_name.replace('.', '-')
        prefix_name = prefix_name.replace('_', '-')
        d = Draw(prefix_name, file_path)
        chart_datas[prefix_name] = d.draw_all_in_any_file()
    env = Environment(loader=FileSystemLoader('../template'))
    # 获取模板文件对象
    template = env.get_template('layout_any.html')
    rendered_html = template.render(datas=chart_datas)
    with open(f"{conf.output_dir}/index.html", 'w', encoding="utf-8") as f:
        f.write(rendered_html)


if __name__ == '__main__':
    draw_main()
