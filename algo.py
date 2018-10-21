from util import  read_trans_lines
import itertools






class Rule():
    def __init__(self,lhs,rhs):
        self.lhs = lhs
        self.rhs = rhs
    def itemset_str(self,itemset):
        return ",".join(sorted(list(itemset)))

    def get_rhs(self):
        return self.rhs


    def __str__(self):
        return '%s->%s'%(self.itemset_str(self.lhs),self.itemset_str(self.rhs))

    def __eq__(self,other):
        return other.lhs == self.lhs and other.rhs == self.rhs






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
    all_freq = []
    all_item = get_all_item(trans)
    # generate 1 item freq
    for item in all_item:
        item = set([item])
        freq =  count_freq(trans,item)
        if freq>min_sup_cnt:
            freq_itemsets.append(item)
    all_freq.extend(freq_itemsets)
    for _ in range(1,len(all_item)):
        candidates = join_candidates(freq_itemsets)
        candidates = prune_candidates(candidates,freq_itemsets)
        freqs = []
        for itemset in candidates:
            if count_freq(trans,itemset) > min_sup_cnt:
                freqs.append(itemset)
        freq_itemsets = freqs
        all_freq.extend(freq_itemsets)
    rules = generate_association_rules(trans,all_freq,min_conf)
    return trans,all_freq,rules




def generate_association_rules(trans,freq_itemset,min_conf):
    # rule : tuple (frozenset,frozenset)
    def generate_child_rules(rule):
        lhs,rhs = rule
        assert len(lhs)>1
        subsets_1 = list(map(frozenset,itertools.combinations(lhs,len(lhs)-1)))
        child_rules = []
        for subset in subsets_1:
            new_lhs,new_rhs = subset,rhs|lhs-subset
            child_rules.append((new_lhs,new_rhs))
        return child_rules
    
    def qualify_rule(rule):
        conf = confidence(rule[0],rule[1],trans)
        if conf>=min_conf:
            return True
        return False

    asso_rules = []
    for itemset in freq_itemset:
        if len(itemset)<=1:
            continue
        root_rule = (frozenset(itemset),frozenset([])) 
        # enumerate rhs number to apply prune
        new_rules_li = [root_rule]
        child_rules = generate_child_rules(root_rule)
        for i in range(1,len(itemset)):
            new_rules_li =  list(filter(qualify_rule,child_rules))
            asso_rules.extend(new_rules_li)
            if i == len(itemset)-1:
                break
            child_rules = itertools.chain(*map(generate_child_rules,new_rules_li))
            child_rules = list(set(child_rules))

    ret_rules = []
    for rule in asso_rules:
        ret_rules.append(Rule(rule[0],rule[1]))
    return ret_rules
        



def get_all_item(trans):
    all_item = set()
    for tran in trans:
        all_item = all_item | tran
    return all_item

def count_freq(trans,itemset):
    cnt = 0
    for tran in trans:
        if itemset.issubset(tran):
            cnt+=1
    return cnt


def confidence(s1,s2,trans):
    c1,c2 =  count_freq(trans,s1),count_freq(trans,s1|s2)
    if c1  == 0 :
        return 0
    return c2/c1


trans,freqs,rules = brute_apriori('./datas/tesco.tl',0.17,0.68)
for rule in rules:
    s = str(rule)
    print(f'{s} : {confidence(rule.lhs,rule.rhs,trans)}')
#print(rules)