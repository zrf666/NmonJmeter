import os
import config as cf

nmon_file = os.listdir(cf.nmon_file_dir)
print(nmon_file)
print(cf.echarts_js_path)
exit()
for file in nmon_file:
    dir = file.split('.')[0]
    if not os.path.exists(dir):
        os.makedirs(os.path.join(cf.output_dir, dir), exist_ok=True)