import json,collections,time






def read_ibm_file(ibm_path):
    with open(ibm_path,'r') as f:
        d = collections.OrderedDict()
        for l in f:
            fields = l.rstrip().split()
            tid,item = fields[1],fields[2]
            d.setdefault(tid,[]).append(item)   
    return d


def preprocessing_ibm_generated_file(ibm_path,tar_path):
    trans = read_ibm_file(ibm_path)
    lines = []
    for l in trans.values() :
        lines.append(",".join(l))
    dump_lines(lines,tar_path)

def dump_lines(lines,path):
    with open(path,'w') as f:
       for line in lines:
           f.write(line+'\n')


def read_trans_lines(path):
    trans = []
    with open(path,'r') as f:
        for l in f:
            items = l.rstrip().split(",")
            trans.append(set(items))
    return trans


def record_time(func):
    def func_with_time(*arg,**kwargs):
        start_time = time.time()
        ret =  func(*arg,**kwargs)
        elapsed_time = time.time() - start_time
        print(f'elapsed_time {elapsed_time}')
        return ret
    return func_with_time
    
    

    