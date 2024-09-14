
# -*-coding: utf-8 -*-


class Parse(object):
    def __init__(self, nmon_file):
        self.file = nmon_file
        with open(nmon_file, 'r') as f:
            self.lines = f.readlines()


    def get_data(self, XXX):
        DATA = []
        row_index = 1
        for line in self.lines:
            if line.startswith('ZZZZ,'):
                time = line.split(',')[2]
            if line.startswith(XXX):
                if row_index == 1:
                    headers = line.replace('\n', '').split(',')[1:]
                    row_index = 2
                else:
                    datas = line.replace('\n', '').split(',')[1:]
                    datas[0] = time
                    dict_data = {}
                    for idx, header in enumerate(headers):
                        dict_data[header] = datas[idx]
                    DATA.append(dict_data)
        # for data in DATA:
        #     print(data)
        # print(len(DATA))
        return DATA

    def get_data_list(self, XXX):
        row_index = 1
        DICT_DATA = {}
        for line in self.lines:
            if line.startswith('ZZZZ,'):
                time = line.split(',')[2]
            if line.startswith(XXX):
                if row_index == 1:
                    headers = line.replace('\n', '').split(',')[1:]
                    row_index = 2
                    # 初始化字典键值
                    for header in headers:
                        if header not in DICT_DATA:DICT_DATA[header] = []
                else:
                    datas = line.replace('\n', '').split(',')[1:]
                    datas[0] = time

                    for idx, header in enumerate(headers):
                        DICT_DATA[header].append(datas[idx])
        return DICT_DATA


    def get_ZZZZ(self):
        ZZZZ = []
        for line in self.lines:
            if line.startswith('ZZZZ,'):
                time = line.split(',')[2]
                ZZZZ.append(time)
        return ZZZZ

    def get_SYS_SUMM(self):
        sys_summ = []
        cpu_all = self.get_CPU_ALL()
        disk_sum = self.get_DISK_SUMM()
        zzzz = self.get_ZZZZ()
        for idx, time in enumerate(zzzz):
            sys_summ.append({
                'time' : time,
                'cpu%' : cpu_all[idx]['CPU%'],
                'io/sec' : disk_sum[idx]['IO / sec']
            })
        print(sys_summ)
        return sys_summ

    def get_AAA(self):
        AAA = []
        with open(self.file, 'r') as f:
            for line in f:
                if line.startswith('AAA'):
                    _, A1, A2,_ = line.split(',')
                    AAA.append(f"{A1}: {A2}")
                if not line.startswith('AAA'):
                    break
        print(AAA)
        return AAA


    def get_BBBP(self):
        BBBP_DATA = []
        for line in self.lines:
            if line.startswith('BBBP,'):
                BBBP_DATA.append(line.replace('\n', '').split(',')[2:])
            if line.startswith('ZZZZ,'):
                break
        for data in BBBP_DATA:
            print(data)
        return BBBP_DATA

    def get_cpus(self):
        for line in self.lines:
            if line.startswith('AAA,cpus,'):
                cpus = int(line.replace('\n', '').split(',')[-1])
                break
        cpu_xxx = []
        for num in range(1, cpus+1):
            cpu_xxx.append(f"CPU{num:03d}")
        print(cpu_xxx)
        return cpu_xxx

    def get_CPU_ALL(self):
        CPU_ALL_DATA = []
        count = 1
        for line in self.lines:
            if line.startswith('ZZZZ,'):
                time = line.split(',')[2]
            if line.startswith('CPU_ALL,'):
                if count == 1:
                    headers = line.replace('\n', '').split(',')[1:]
                    count = 2
                else:
                    datas = line.replace('\n', '').split(',')[1:]
                    datas[0] = time
                    dict_data = {}
                    for idx, header in enumerate(headers):
                        dict_data[header] = datas[idx]
                        dict_data['CPU%'] = round(sum(float(num) for num in datas[1:3]), 1)
                    CPU_ALL_DATA.append(dict_data)
            else: continue
        for data in CPU_ALL_DATA:
            print(data)
        print(len(CPU_ALL_DATA))
        return CPU_ALL_DATA

    def get_CPU_SUMM(self):
        headers = ['CPU_SUMM','User%','Sys%','Wait%','Idle%']
        cpu_xxx = self.get_cpus()
        cpu_xxx_data = []
        for cpu in cpu_xxx:
            datas = self.get_data(cpu)
            user_sum = 0
            sys_sum = 0
            wait_sum = 0
            idle_sum = 0
            for data in datas:
                user_sum += float(data[headers[1]])
                sys_sum += float(data[headers[2]])
                wait_sum += float(data[headers[3]])
                idle_sum += float(data[headers[4]])
            cpu_xxx_data.append({
                headers[0] : cpu,
                headers[1] : round(user_sum/len(datas), 1),
                headers[2] : round(sys_sum/len(datas), 1),
                headers[3] : round(wait_sum/len(datas), 1),
                headers[4] : round(idle_sum/len(datas), 1),
            })
        return cpu_xxx_data


    def get_CPU_XXX(self):
        for line in self.lines:
            if line.startswith('AAA,cpus,'):
                cpus = int(line.replace('\n', '').split(',')[-1])
                break
        cpu_xxx = []
        for num in range(1, cpus+1):
            cpu_xxx.append(f"CPU{num:03d}")
        print(cpu_xxx)
        for cpu in cpu_xxx:
            self.get_data(cpu)


    def get_DISK_SUMM(self):
        DISK_SUMM_DATA = []
        row_index = 1
        dict_data = {}
        for line in self.lines:
            # if line.startswith('ZZZZ,'):
            #     time = line.split(',')[2]
            if row_index == 1:
                if line.startswith('DISKREAD,'):
                    diskread_headers = line.replace('\n', '').split(',')[1:]
                    headers = [diskread_headers[0].replace('Read', 'Total'),
                               'Disk Read KB / s',
                               'Disk Write KB / s',
                               'IO / sec'
                               ]
                if line.startswith('BBBP,'):
                    row_index = 2
            else:
                if line.startswith('ZZZZ,'):
                    time = line.split(',')[2]
                    dict_data[headers[0]] = time
                if line.startswith('DISKREAD,'):
                    disk_read = line.replace('\n', '').split(',')[2:]
                    read_sum = round(sum(float(num) for num in disk_read), 1)
                    dict_data[headers[1]] = read_sum
                if line.startswith('DISKWRITE,'):
                    disk_write = line.replace('\n', '').split(',')[2:]
                    write_sum = round(sum(float(num) for num in disk_write), 1)
                    dict_data[headers[2]] = write_sum
                if line.startswith('DISKXFER,'):
                    disk_xfer = line.replace('\n', '').split(',')[2:]
                    xfer_sum = round(sum(float(num) for num in disk_xfer), 1)
                    dict_data[headers[3]] = xfer_sum
                    DISK_SUMM_DATA.append(dict_data)
                    dict_data = {}
        for data in DISK_SUMM_DATA:
            print(data)
        print(len(DISK_SUMM_DATA))
        return DISK_SUMM_DATA


    def get_DISKBSIZE(self, type='dict'):
        row_start = 'DISKBSIZE,'
        if type == 'dict':
            DISKBSIZE_DATA = self.get_data(row_start)
        else:
            DISKBSIZE_DATA = self.get_data_list(row_start)
        return DISKBSIZE_DATA

    def get_DISKBUSY(self, type='dict'):
        row_start = 'DISKBUSY,'
        if type == 'dict':
            DISKBUSY_DATA = self.get_data(row_start)
        else:
            DISKBUSY_DATA = self.get_data_list(row_start)
        return DISKBUSY_DATA


    def get_DISKREAD(self):
        row_start = 'DISKREAD,'
        DISKREAD_DATA = self.get_data(row_start)
        return DISKREAD_DATA


    def get_DISKWRITE(self):
        row_start = 'DISKWRITE,'
        DISKWRITE_DATA = self.get_data(row_start)
        return DISKWRITE_DATA


    def get_DISKXFER(self):
        row_start = 'DISKXFER,'
        DISKXFER_DATA = self.get_data(row_start)
        return DISKXFER_DATA


    def get_JFSFILE(self):
        row_start = 'JFSFILE,'
        JFSFILE_DATA = self.get_data(row_start)
        return JFSFILE_DATA


    def get_MEM(self):
        row_start = 'MEM,'
        MEM_DATA = self.get_data(row_start)
        return MEM_DATA


    def get_NET(self):
        row_start = 'NET,'
        NET_DATA = self.get_data(row_start)
        return NET_DATA


    def get_NETPACKET(self):
        row_start = 'NETPACKET,'
        NETPACKET_DATA = self.get_data(row_start)
        return NETPACKET_DATA


    def get_PROC(self):
        row_start = 'PROC,'
        PROC_DATA = self.get_data(row_start)
        return PROC_DATA


    def get_VM(self):
        row_start = 'VM,'
        VM_DATA = self.get_data(row_start)
        return VM_DATA


if __name__ == '__main__':
    nmon_file = "../tmp/186.1.47.93.nmon"
    p = Parse(nmon_file)
    p.get_AAA()