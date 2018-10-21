from util import  read_trans_lines
import itertools

def brute_apriori(path,min_sup,min_conf):
    def join_candidates(freq_itemsets):
        candidates = []
        n = len(freq_itemsets)
        for i in range(n):
            for j in range(i+1,n):
                set1 = freq_itemsets[i]
                set2 = freq_itemsets[j]
                join = set1 & set2
                assert len(set1) == len(set2)
                k = len(set1)
                if len(join) == k-1:
                    candidate = set1|set2
                    if candidate not in candidates:
                        candidates.append(candidate)
        return candidates
    def prune_candidates(candidates,freq_itemsets):
        pruned = []
        for itemset in candidates:
            subsets_1 = list(map(frozenset,itertools.combinations(itemset,len(itemset)-1)))
            flag = True
            for subset in subsets_1:
                if subset not in freq_itemsets:
                    flag = False
                    break
            if flag :
                pruned.append(itemset)
        return pruned     

    trans = read_trans_lines(path)
    min_sup_cnt = len(trans)*min_sup
    # generate freq itemset
    freq_itemsets = []
    ret = []
    all_item = get_all_item(trans)
    # generate 1 item freq
    for item in all_item:
        item = set([item])
        freq =  count_freq(trans,item)
        if freq>min_sup_cnt:
            freq_itemsets.append(item)
    ret.extend(freq_itemsets)
    for _ in range(1,len(all_item)):
        candidates = join_candidates(freq_itemsets)
        candidates = prune_candidates(candidates,freq_itemsets)
        freqs = []
        for itemset in candidates:
            if count_freq(trans,itemset) > min_sup_cnt:
                freqs.append(itemset)
        freq_itemsets = freqs
        ret.extend(freq_itemsets)

    return ret







    # generate rules




def get_all_item(trans):
    all_item = set()
    for tran in trans:
        all_item = all_item | tran
    return all_item

def get_confidence():
    pass

def count_freq(trans,itemset):
    cnt = 0
    for tran in trans:
        if itemset.issubset(tran):
            cnt+=1
    return cnt

#print(brute_apriori('./datas/test.tl',0.2,0.5))