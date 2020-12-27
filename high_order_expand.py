import pickle
from all_events import *
import os
import json
import numpy as np
from tqdm import tqdm
from extract import get_high_order_info


m_val = list(range(5,101,5))

def get_high_order(m):
    # bc = BertClient()
    file_dir = '../expansion'
    high_expand = {}
    event_results = {}
    for event in med_events:
        
        path = os.path.join('final_score',event+'_score.pkl')
        raw_expansions = pickle.load(open(path,'rb'))
        filter_words = []
        for key in raw_expansions.keys():
            expansions = raw_expansions[key]
            for ele in expansions[:m]:
                if len(ele[0].split()) == 1:
                    filter_words.append(ele[0])
        
        if os.path.exists('wikihow_articles/%s.json'%event):
            results = get_high_order_info(event,filter_words)
        else:
            results = []
        event_results[event] = results

    return event_results



if __name__ == "__main__":
    for m in m_val:
        print('dealing %d'%m)
        results = get_high_order(m)
        pickle.dump(results,open('high_order_results/high_results_%d.pkl'%m,'wb'))