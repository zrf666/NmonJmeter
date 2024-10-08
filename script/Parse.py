
# -*-coding: utf-8 -*-


class Parse(object):
    def __init__(self, nmon_file):
        self.file = nmon_file
        with open(nmon_file, 'r') as f:
            self.lines = f.readlines()


    def get_data_list(self, XXX):
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

    def get_data_dict(self, XXX):
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

    def get_SYS_SUMM(self, type='dict'):
        sys_summ = []
        cpu_all = self.get_CPU_ALL('list')
        disk_sum = self.get_DISK_SUMM('list')
        zzzz = self.get_ZZZZ()
        for idx, time in enumerate(zzzz):
            sys_summ.append({
                'time' : time,
                'cpu%' : cpu_all[idx]['CPU%'],
                'io/sec' : disk_sum[idx]['IO / sec']
            })
        print(sys_summ)
        if type == 'dict':
            DICT_DATA = {}
            DICT_DATA['time'] = zzzz
            DICT_DATA.update(self.get_CPU_ALL())
            DICT_DATA.update(self.get_DISK_SUMM())
            return DICT_DATA
        return sys_summ

    def get_AAA(self):
        AAA = []
        for line in self.lines:
            if line.startswith('AAA'):
                A = line.split(',')
                AAA.append(f"{A}")
            if not line.startswith('AAA'):
                break
        return AAA


    def get_BBBP(self):
        BBBP_DATA = []
        for line in self.lines:
            if line.startswith('BBBP,'):
                BBBP_DATA.append(line.replace('\n', '').split(',')[2:])
            if line.startswith('ZZZZ,'):
                break
        return BBBP_DATA

    def get_cpus(self):
        for line in self.lines:
            if line.startswith('AAA,cpus,'):
                cpus = int(line.replace('\n', '').split(',')[-1])
                break
        cpu_xxx = []
        for num in range(1, cpus+1):
            cpu_xxx.append(f"CPU{num:02d}")
        print(cpu_xxx)
        return cpu_xxx

    def get_CPU_ALL(self, type='dict'):
        CPU_ALL_DATA = []
        DICT_DATA = {}
        count = 1
        for line in self.lines:
            if line.startswith('ZZZZ,'):
                time = line.split(',')[2]
            if line.startswith('CPU_ALL,'):
                if count == 1:
                    headers = line.replace('\n', '').split(',')[1:]
                    count = 2
                    # 初始化字典键值
                    for header in headers:
                        if header not in DICT_DATA: DICT_DATA[header] = []
                    DICT_DATA['CPU%'] = []
                else:
                    datas = line.replace('\n', '').split(',')[1:]
                    datas[0] = time
                    dict_data = {}
                    for idx, header in enumerate(headers):
                        dict_data[header] = datas[idx]
                        dict_data['CPU%'] = round(sum(float(num) for num in datas[1:3]), 1)
                        DICT_DATA[header].append(datas[idx])
                    DICT_DATA['CPU%'].append(round(sum(float(num) for num in datas[1:3]), 1))
                    CPU_ALL_DATA.append(dict_data)
            else: continue
        # for data in CPU_ALL_DATA:
        #     print(data)
        # print(len(CPU_ALL_DATA))
        if type == 'dict':
            return DICT_DATA
        else:
            return CPU_ALL_DATA

    def get_CPU_SUMM(self, type='dict'):
        DICT_DATA = {}
        headers = ['CPU_SUMM','User%','Sys%','Wait%','Idle% ']
        for header in headers:
            DICT_DATA[header] = []
        cpu_xxx = self.get_cpus()
        cpu_xxx_data = []

        for cpu in cpu_xxx:
            datas = self.get_data_list(cpu)
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
            DICT_DATA[headers[0]].append(cpu)
            DICT_DATA[headers[1]].append(round(user_sum/len(datas), 1))
            DICT_DATA[headers[2]].append(round(sys_sum/len(datas), 1))
            DICT_DATA[headers[3]].append(round(wait_sum/len(datas), 1))
            DICT_DATA[headers[4]].append(round(idle_sum/len(datas), 1))
        if type == 'dict':
            return DICT_DATA
        else:
            return cpu_xxx_data


    def get_CPU_XXX(self, cpu_xxx):
        return self.get_data_dict(cpu_xxx)


    def get_DISK_SUMM(self, type='dict'):
        DISK_SUMM_DATA = []
        DICT_DATA = {}
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
                    for header in headers:
                        if header not in DICT_DATA:DICT_DATA[header] = []
                if line.startswith('BBBP,'):
                    row_index = 2
            else:
                if line.startswith('ZZZZ,'):
                    time = line.split(',')[2]
                    dict_data[headers[0]] = time
                    DICT_DATA[headers[0]].append(time)
                if line.startswith('DISKREAD,'):
                    disk_read = line.replace('\n', '').split(',')[2:]
                    read_sum = round(sum(float(num) for num in disk_read), 1)
                    dict_data[headers[1]] = read_sum
                    DICT_DATA[headers[1]].append(read_sum)
                if line.startswith('DISKWRITE,'):
                    disk_write = line.replace('\n', '').split(',')[2:]
                    write_sum = round(sum(float(num) for num in disk_write), 1)
                    dict_data[headers[2]] = write_sum
                    DICT_DATA[headers[2]].append(write_sum)
                if line.startswith('DISKXFER,'):
                    disk_xfer = line.replace('\n', '').split(',')[2:]
                    xfer_sum = round(sum(float(num) for num in disk_xfer), 1)
                    dict_data[headers[3]] = xfer_sum
                    DICT_DATA[headers[3]].append(xfer_sum)
                    DISK_SUMM_DATA.append(dict_data)
                    dict_data = {}
        # for data in DISK_SUMM_DATA:
        #     print(data)
        # print(len(DISK_SUMM_DATA))
        if type == 'dict':
            return  DICT_DATA
        else:
            return DISK_SUMM_DATA


    def get_DISKBSIZE(self, type='dict'):
        row_start = 'DISKBSIZE,'
        if type == 'dict':
            DISKBSIZE_DATA = self.get_data_dict(row_start)
        else:
            DISKBSIZE_DATA = self.get_data_list(row_start)
        return DISKBSIZE_DATA

    def get_DISKBUSY(self, type='dict'):
        row_start = 'DISKBUSY,'
        if type == 'dict':
            DISKBUSY_DATA = self.get_data_dict(row_start)
        else:
            DISKBUSY_DATA = self.get_data_list(row_start)
        return DISKBUSY_DATA


    def get_DISKREAD(self, type='dict'):
        row_start = 'DISKREAD,'
        if type == 'dict':
            DISKREAD_DATA = self.get_data_dict(row_start)
        else:
            DISKREAD_DATA = self.get_data_list(row_start)
        return DISKREAD_DATA


    def get_DISKWRITE(self, type='dict'):
        row_start = 'DISKWRITE,'
        if type == 'dict':
            DISKWRITE_DATA = self.get_data_dict(row_start)
        else:
            DISKWRITE_DATA = self.get_data_list(row_start)
        return DISKWRITE_DATA


    def get_DISKXFER(self, type='dict'):
        row_start = 'DISKXFER,'
        if type == 'dict':
            DISKXFER_DATA = self.get_data_dict(row_start)
        else:
            DISKXFER_DATA = self.get_data_list(row_start)
        return DISKXFER_DATA


    def get_JFSFILE(self, type='dict'):
        row_start = 'JFSFILE,'
        if type == 'dict':
            JFSFILE_DATA = self.get_data_dict(row_start)
        else:
            JFSFILE_DATA = self.get_data_list(row_start)
        return JFSFILE_DATA


    def get_MEM(self, type='dict'):
        row_start = 'MEM,'
        if type == 'dict':
            MEM_DATA = self.get_data_dict(row_start)
        else:
            MEM_DATA = self.get_data_list(row_start)
        return MEM_DATA


    def get_NET(self, type='dict'):
        row_start = 'NET,'
        if type == 'dict':
            NET_DATA = self.get_data_dict(row_start)
        else:
            NET_DATA = self.get_data_list(row_start)
        return NET_DATA


    def get_NETPACKET(self, type='dict'):
        row_start = 'NETPACKET,'
        if type == 'dict':
            NETPACKET_DATA = self.get_data_dict(row_start)
        else:
            NETPACKET_DATA = self.get_data_list(row_start)
        return NETPACKET_DATA


    def get_PROC(self, type='dict'):
        row_start = 'PROC,'
        if type == 'dict':
            PROC_DATA = self.get_data_dict(row_start)
        else:
            PROC_DATA = self.get_data_list(row_start)
        return PROC_DATA


    def get_VM(self, type='dict'):
        row_start = 'VM,'
        if type == 'dict':
            VM_DATA = self.get_data_dict(row_start)
        else:
            VM_DATA = self.get_data_list(row_start)
        return VM_DATA


if __name__ == '__main__':
    nmon_file = "../tmp/186.1.47.93.nmon"
    p = Parse(nmon_file)
    p.get_AAA()