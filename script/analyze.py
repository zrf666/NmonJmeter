import pandas as pd


class Analyzer(object):
    def __init__(self, nmon_file):
        self.nmon_file = nmon_file
        with open(nmon_file, 'r') as f:
            self.lines = f.readlines()


    def get_AAA(self):
        AAA_datas = []
        for line in self.lines:
            if line.startswith('AAA,'):
                AAA_datas.append(line.split(',')[1:])
        return AAA_datas

    def get_CPU_ALL(self):
        CPU_ALL_data = []
        count = 1
        for line in self.lines:
            if line.startswith('ZZZZ,'):
                time = line.split(',')[2]

            if line.startswith('CPU_ALL,'):
                if count == 1:
                    headers = line.strip().replace(r'\n','').split(',')[1:]
                    count = 2
                else:
                    datas = line.strip().replace(r'\n','').split(',')[1:]
                    datas[0] = time
                    dict_data = {}
                    for idx, header in enumerate(headers):
                        dict_data[header] = datas[idx]
                    CPU_ALL_data.append(dict_data)
            else: continue

        for data in CPU_ALL_data:
            print(data)
        print(len(CPU_ALL_data))
        return CPU_ALL_data



def parse_nmon_cpu_all(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    cpu_data = []
    header = None

    for line in lines:
        if line.startswith('CPU'):
            # 获取表头
            header = line.strip().split(',')
        elif line.startswith('C'):
            # 解析CPU数据
            cpu_values = line.strip().split(',')
            cpu_data.append(cpu_values)

    return header, cpu_data
def generate_cpu_excel(header, cpu_data, output_file):
    df = pd.DataFrame(cpu_data, columns=header)
    df.to_excel(output_file, sheet_name='CPU_ALL', index=False)

if __name__ == '__main__':
    # 使用示例
    nmon_file = "../nmon_file/sampleD.nmon"
    # header, cpu_data = parse_nmon_cpu_all(nmon_file)
    # generate_cpu_excel(header, cpu_data, '../output/nmon_cpu_analysis.xlsx')
    a = Analyzer(nmon_file)
    # a.get_AAA()
    a.get_CPU_ALL()