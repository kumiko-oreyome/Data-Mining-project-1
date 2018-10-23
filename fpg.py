import itertools
import util
from util import record_time
from collections import deque,OrderedDict
from algo import print_rules,generate_association_rules
class TreeNode():
    def __init__(self,parent,item,cnt):
        self.parent = parent
        self.item = item
        self.cnt = cnt
        self.childs = []
        self.next = None
    # return : next node to add item
    def add_item(self,item,cnt):
        if item==self.item:
            self.cnt+=cnt
            return self
        ret_node = self.find_child(item)
        if ret_node is None:
            ret_node = TreeNode(self,item,cnt)
            self.add_child(ret_node)
        else:
            ret_node.cnt+=cnt
        return ret_node 

    def add_child(self,node):
        self.childs.append(node)

    def find_child(self,item):
        for node in self.childs:
            if node.item == item:
                return node
        return None

    def append_next_by_next(self,node):
        if self.next is None:
            self.next = node
        else:
            self.next.append_next_by_next(node)

    def __str__(self):
        return f'<{self.item}:{self.cnt}>'
    def __repr__(self):
        return self.__str__()
    

class FpTree():
    def __init__(self):
        self.root =  TreeNode(None,None,0)
        self.header_table = {}
    def add_itemset(self,sorted_itemset):
        prev = self.root
        for item in sorted_itemset:
            if item==prev.item:
                prev.cnt+=1
                continue
            node = prev.find_child(item)
            if node is None:
                new_node = TreeNode(prev,item,1)
                prev.add_child(new_node)
                prev = new_node
                if new_node.item not in self.header_table:
                    self.header_table[new_node.item] = new_node
                else:
                     self.header_table[new_node.item].append_next_by_next(new_node)
            else:
                node.cnt+=1
                prev = node

    def get_item_nodes(self,item):
        l = []
        cur = self.header_table[item]
        while cur is not None:
            l.append(cur)
            cur = cur.next
        return l


    def print(self,space_num=2):
        #depth = 0
        queue = deque([[self.root]])
        while len(queue) > 0:
            node_groups = list(queue)
            queue.clear()
            for node_group in node_groups:
                print(" ".join([str(node) for node in node_group])+'|',end='')
                queue.extend( [node.childs  for node in node_group])
            print('')


class FpPath():
    def __init__(self,leaf):
        self.leaf = leaf
        self.min_cnt = self.leaf.cnt
        self._get_pattern_base()
        

    def _get_pattern_base(self):
        self.pattern_base = []
        cur = self.leaf
        while cur.item is not None:
            assert self.min_cnt <= cur.cnt 
            if cur is not self.leaf:
                self.pattern_base.append(cur.item)
            cur = cur.parent
        self.pattern_base = (list(reversed(self.pattern_base)),self.min_cnt)



def build_freq_table(trans,min_sup_cnt):
    freq_table = {}
    for tran in trans:
        for item in tran:
            if item not in freq_table:
                freq_table[item] = 0
            freq_table[item]+=1
    for item in list(freq_table.keys()):
        if freq_table[item]<min_sup_cnt:
            del freq_table[item]

    freq_table = OrderedDict(sorted(freq_table.items(),key=lambda t:t[1],reverse=True))
    return freq_table


def reorder_transactions(trans,freq_table):
    sorted_trans = []
    for tran in trans:
        tran = list(filter(lambda x:x in freq_table,tran))
        tran = sorted(tran,key=lambda x:freq_table[x],reverse=True)
        sorted_trans.append(tran)
    return sorted_trans


def power_set(l):
    return itertools.chain.from_iterable([itertools.combinations(l, r) for r in range(0,len(l)+1)])


def fp_tree_mining(fp_tree,freq_table,min_sup_cnt):
    patterns = {}
    for item in reversed(freq_table):
        item_nodes = fp_tree.get_item_nodes(item)
        pattern_bases = [FpPath(node).pattern_base for node in item_nodes]
        # find
        for pattern_base,min_cnt in pattern_bases:
            for pattern in power_set(pattern_base):
                freq = min_cnt
                pattern =  pattern+(item,)
                pattern_key = frozenset(pattern)
                if pattern_key not in patterns:
                    patterns[pattern_key] = 0
                patterns[pattern_key] +=freq
    freq_items = []        
    for pattern in patterns:
        freq = patterns[pattern]
        if  freq >= min_sup_cnt:
            freq_items.append(pattern)
    return freq_items 




def build_fp_tree(sorted_trans):
    tree = FpTree()
    for tran in sorted_trans:
        tree.add_itemset(tran)
    return tree
        
def generate_freqitems_by_fpg(trans,min_sup_cnt):
    freq_table = build_freq_table(trans,min_sup_cnt)
    sorted_trans = reorder_transactions(trans,freq_table)
    tree = build_fp_tree(sorted_trans)
    return fp_tree_mining(tree,freq_table,min_sup_cnt)

@record_time
def fp_growth_main(path,min_sup,min_conf):
    trans = util.read_trans_lines(path)
    min_sup_cnt = len(trans)*min_sup
    freq_items = generate_freqitems_by_fpg(trans, min_sup_cnt)
    rules = generate_association_rules(trans,freq_items,min_conf)
    return trans,freq_items,rules
    

#trans,freq_items,rules = fp_growth_main('./datas/tesco.tl',0.17,0.68)
#print_rules(rules,trans)
#generate_freqitems_by_fpg([set(['A','B','C']),set(['A','B']),set('A')],2)