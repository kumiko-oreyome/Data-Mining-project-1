from util import  preprocessing_ibm_generated_file,record_time
import argparse
from algo import brute_apriori,print_rules
from fpg import fp_growth_main



def preprocessing_func(args):
    preprocessing_ibm_generated_file(args.srcpath, args.tarpath)


def test(args):
    tran_path = args.srcpath
    outpath = args.tarpath
    #tran_path = args.srcpath+'.tl'
    #preprocessing_ibm_generated_file(args.srcpath, tran_path)
    if args.method == 'brute':
        assocciation_rule_mining(brute_apriori,tran_path,outpath,args.min_sup,args.min_conf)
    elif args.method == 'fpg':
        assocciation_rule_mining(fp_growth_main,tran_path,outpath,args.min_sup,args.min_conf)
    else:
        print('method name error!!')


def assocciation_rule_mining(func,srcpath,outpath,min_sup,min_conf):
    trans,freqs,rules = func(srcpath,min_sup,min_conf)
    print('Generate %d freq itemset %d rules'%(len(freqs),len(rules)))
    print_rules(rules,trans,outpath)












#preprocessing_ibm_generated_file('./datas/data131','./datas/data131.l')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    subparsers =  parser.add_subparsers(help='commands',dest='command')

    #preprocessing
    pre_parser = subparsers.add_parser(name='preprocessing')
    pre_parser.add_argument('srcpath')
    pre_parser.add_argument('tarpath')
    pre_parser.set_defaults(func=preprocessing_func)

    # test
    test_parser = subparsers.add_parser(name='test')
    test_parser.add_argument('method',help='brute or fpg')
    test_parser.add_argument('srcpath')
    test_parser.add_argument('tarpath')
    test_parser.add_argument('min_sup',type=float)
    test_parser.add_argument('min_conf',type=float)
    test_parser.set_defaults(func=test)
    args = parser.parse_args()
    args.func(args)

    