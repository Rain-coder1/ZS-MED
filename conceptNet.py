import requests
import json
import os
import grequests
from first_order_expand import gen_query
import pickle
import time
from textblob import TextBlob,Word
from all_events import selected_labels


def filter_unen_edges(edges):
    """
    funct: filter un-english node and save key info
    parameters:
        edges: origin edges from ConceptNet 5
    return values: 
        filtered_edges: edges that only keeps key information
    """
    filtered_edges = []
    remained_keys = ['rel','weight','surfaceText']
    node_remain_keys = ['label','sense_label','term']
    for edge in edges:
        start_node = edge['start']
        end_node = edge['end']
        if 'language' not in start_node.keys() or \
                 'language' not in end_node.keys():
            continue
        if start_node['language'] != 'en' or \
                 end_node['language'] != 'en':
            continue
        now_edge = {key:edge[key] for key in remained_keys}

        now_edge['start'] = {key:start_node[key] for key in node_remain_keys if key in start_node.keys()}
        now_edge['end'] = {key:end_node[key] for key in node_remain_keys if key in end_node.keys()}
        filtered_edges.append(now_edge)

    return filtered_edges


def get_jsons(urls):
    """
    funct: deal mutiple requests and return json file
    parameters:
        urls: a list of multiple urls
    return values: 
        json_results: a list of returned json results
    """
    json_results = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36'
    }
    req_list = []
    try:
        for url in urls:
            req_list.append(grequests.get(url,headers=headers))

        res_list = grequests.map(req_list)
        for response in res_list:
            if response.status_code == 200:
                json_results.append(response.json())
            else:
                json_results.append({})
        return json_results
    except RequestException:
        return None


def get_concept_edges(concept):
    """
    parameters:
        concept: str that indicates query concept
    return values: 
        Status: [-1: no such concept node 1: query successfully] 
        Output Json: edges that connect query concept
    """
    offset = 0
    limit = 1000
    base_url = 'http://api.conceptnet.io/c/en/{0}?offset={1}&limit={2}'.format(concept,offset,limit)
    prefix_url = 'http://api.conceptnet.io'
    output = {}
    status = 0
    print('Extracting info from {0}'.format(base_url))
    first_page = requests.get(base_url).json()
    if len(first_page['edges']) == 0:
        status = -1
        return status,output
    status = 1
    for key in first_page.keys():
        if key != 'view':
            output[key] = first_page[key]

    if 'view' not in first_page.keys():
        return status,output

    output['edges'] = []
    now_page = first_page
    while True:
        print('Now parsing page: {}'.format(now_page['view']['@id']))
        output['edges'].extend(now_page['edges']) 
        if 'nextPage' in now_page['view'].keys():
            next_page_url = now_page['view']['nextPage']
            next_page = requests.get(prefix_url + next_page_url).json()
            now_page = next_page
        else:
            break

    return status,output


def cal_relatedness(Query,Concepts):
    """
    parameters:
        Query: The two concept.
        Concepts: All the search concepts
    return values: 
        relatedness: a list that contains relatedness
    """
    prefix_url = 'http://api.conceptnet.io'
    urls = {}
    relatedness = {}
    new_url = []
    all_keys = []
    all_relatedness = pickle.load(open('conceptNet_relatedness.pkl','rb'))
    for concept in Concepts:
        concept = '_'.join(concept.split(' '))
        search_url = '/relatedness?node1=/c/en/{}&node2=/c/en/{}'.format(Query,concept)
        urls[Query+':'+concept] = prefix_url + search_url
        if Query+':'+concept in all_relatedness.keys():
            relatedness[concept] = all_relatedness[Query+':'+concept]
        else:
            new_url.append(prefix_url + search_url)
            all_keys.append(concept)
        # urls.append(prefix_url+search_url)

    if len(new_url) != 0:
        now_keys = all_keys[:60]
        seach_results = get_jsons(new_url[:60])

        for idx in range(len(seach_results)):
            seach_result = seach_results[idx]
            relatedness[now_keys[idx]] = seach_result['value']

        time.sleep(60)
        now_keys = all_keys[60:]
        seach_results = get_jsons(new_url[60:])

        for idx in range(len(seach_results)):
            seach_result = seach_results[idx]
            relatedness[now_keys[idx]] = seach_result['value']
    # seach_results = get_jsons(urls)
    
    # for idx in range(len(seach_results)):
    #     seach_result = seach_results[idx]
    #     print("#################")
    #     print(urls[idx])
    #     print("------------------")
    #     print(seach_result)
    #     print("#################")
    #     relatedness[Concepts[idx]] = seach_result['value']
    return relatedness
    # return urls


def get_related_terms(concept):
    """
    parameters:
        concept: The query concept.
    return values: 
        related_concepts: a list that contains the related concepts.
    """
    print('Searching related terms of {0}'.format(concept))
    search_url = 'http://api.conceptnet.io/related/c/en/{0}?filter=/c/en'.format(concept)
    return_json = requests.get(search_url).json()
    print('Searching Completed...')
    related_concepts = []
    for ele in return_json["related"]:
        rel_concept = {}
        rel_concept['label'] = ele['@id'].split('/')[-1].replace('_',' ')
        rel_concept['weight'] = ele['weight']
        related_concepts.append(rel_concept)
    return related_concepts


def extract_related_concepts(event_name):
    """
    parameters:
        result: related edges in conceptNet 5
    return values: 
        related_concepts: a dict that contains all kinds of relate concept
    """
    save_path = 'conceptNet_out'
    concepts = [concept.split('.')[0] for concept in os.listdir(os.path.join(save_path,event_name))]
    print('Dealing with {0}, concepts is {1}'.format(event_name,concepts))
    
    selected_relTypes = ['RelatedTo','AtLocation','HasA','UsedFor','LocatedNear',
                 'IsA','MannerOf','HasSubevent','HasFirstSubevent','HasLastSubevent']
    
    event_related_concepts = {}

    for concept in concepts:
    
        result = json.load(open(os.path.join(save_path,event_name,concept+'.json'),'r'))

        edges = result['edges']
        concept_term = '/c/en/' + concept
        related_concepts = {}
        for edge in edges:
            start_concept_term = edge['start']['term']
            end_concept_term = edge['end']['term']
            rel_concept = {}
            rel_concept['weight'] = edge['weight']
            rel_concept['label'] = edge['start']['label'] if start_concept_term != concept_term else edge['end']['label']
            rel_type = edge['rel']['label']
            related_concepts[rel_type] = related_concepts.get(rel_type,[])
            related_concepts[rel_type].append(rel_concept)
        
        filtered_concepts = {}

        for key in related_concepts.keys():
            if key in selected_relTypes:
                all_concepts = related_concepts[key]
                for ele in all_concepts:
                    filtered_concepts[ele['label'].lower()] = filtered_concepts.get(ele['label'].lower(),0) + 1

        event_related_concepts[concept] = filtered_concepts

    return event_related_concepts


def search_ConceptNet(event_name,concept):
    concept = '_'.join(concept.split(' '))
    save_path = 'conceptNet_out'
    print('The searching concept is {0}'.format(concept))

    if os.path.exists(os.path.join(save_path,event_name,concept+'.json')):
        result = json.load(open(os.path.join(save_path,event_name,concept+'.json')))

    else:
        status,result = get_concept_edges(concept)
        print('Searching Finished !!!')
        if status == -1:
            print('No such concept')
            return None
            # os._exit(status=0)
        result['edges'] = filter_unen_edges(result['edges'])
        if not os.path.exists(os.path.join(save_path,event_name)):
            os.makedirs(os.path.join(save_path,event_name))
        json.dump(result,open(os.path.join(save_path,event_name,concept+'.json'),'w'))

    return result

    
    # related_concepts = extract_related_concepts(result['edges'],concept)
    # print('\n'.join(list(related_concepts.keys())))
    # print(related_concepts['RelatedTo'])
    # print('\n'.join(related_concepts['RelatedTo']))


def search_relatedness():
    all_urls = pickle.load(open('all_urls.pkl','rb'))
    all_keys = list(all_urls.keys())
    save_dir = 'temp_results'

    for step in range(0,161):
        print(step*100,(step+1)*100)
        urls = [all_urls[ele] for ele in all_keys[step*100:(step+1)*100]]
        now_keys = all_keys[step*100:(step+1)*100]

        if os.path.exists(os.path.join(save_dir,str(step*100)+"_"+str((step+1)*100)+'.pkl')):
            continue

        # print(now_keys)
        seach_results = get_jsons(urls)
        relatedness = {}

        for idx in range(len(seach_results)):
            seach_result = seach_results[idx]
            relatedness[now_keys[idx]] = seach_result['value']

        # print(os.path.join(save_dir,str(step*100)+"_"+str((step+1)*100)+'.pkl'))
        pickle.dump(relatedness,open(os.path.join(save_dir,str(step*100)+"_"+str((step+1)*100)+'.pkl'),'wb'))
        time.sleep(30)



def aggeragate():
    all_urls = pickle.load(open('all_urls.pkl','rb'))
    all_keys = list(all_urls.keys())
    save_dir = 'temp_results'
    relatedness = {}
    for step in range(0,161):
        urls = [all_urls[ele] for ele in all_keys[step*100:(step+1)*100]]
        now_keys = all_keys[step*100:(step+1)*100]
        result = pickle.load(open(os.path.join(save_dir,str(step*100)+"_"+str((step+1)*100)+'.pkl'),'rb'))
        relatedness.update(result)

    print(len(relatedness))
    pickle.dump(relatedness,open('conceptNet_relatedness.pkl','wb'))



def get_frequency(concepts):
    key_words = []
    text = ""
    for key in concepts.keys():
        for i in range(concepts[key]):
            text += str(Word(key).singularize()) + " "
    # print(text)
    blob = TextBlob(text)
    word_counts = sorted(blob.word_counts.items(),key=lambda x:x[1],reverse=True)
    # print(word_counts)
    for ele in word_counts:
        if ele[1] > 1:
            blob = TextBlob(ele[0])
            # print(blob.tags)
            if blob.tags[0][1].startswith('N'):
                key_words.append(ele[0])
    if len(key_words) < 20:
        for ele in word_counts:
            key_words.append(ele[0])
    return key_words
 

def main():
    event_querys = gen_query()
    fw = open('output.txt','w',encoding='utf-8')
    '''
    generate conceptNet search results
    '''
    # for event_name in event_querys.keys():
    #     print('Searching for event: {}'.format(event_name))
    #     querys = event_querys[event_name]
    #     for query in querys:
    #         result = search_ConceptNet(event_name,query)


    all_urls = {}
    save_path = 'conceptNet_out'

    for event_name in event_querys.keys():
        if event_name != 'Grooming_an_animal':
            continue
        relatedness_result = {}
        print(event_name)
        if not os.path.exists(os.path.join(save_path,event_name+'_related_concepts.pkl')):
            related_concepts = extract_related_concepts(event_name)
            pickle.dump(related_concepts,open(os.path.join(save_path,event_name+'_related_concepts.pkl'),'wb'))
        else:
            related_concepts = pickle.load(open(os.path.join(save_path,event_name+'_related_concepts.pkl'),'rb'))
        # print(related_concepts.keys())
        # fw.write(str(related_concepts)+'\n')
        # print(event_name)
        # print(selected_labels[event_name])

        for key in related_concepts.keys():
            concepts = related_concepts[key]
            # fw.write(str(key)+'\n')
            # fw.write(str(concepts)+'\n')
            key_words = get_frequency(concepts)
            # fw.write(str(key_words)+'\n')
            if os.path.exists(os.path.join('relatedness',event_name+'_'+key+'.pkl')):
                relatedness = pickle.load(open(os.path.join('relatedness',event_name+'_'+key+'.pkl'),'rb'))
            else:
                relatedness = cal_relatedness(key,list(concepts.keys()))
                # all_urls.update(relatedness)
                pickle.dump(relatedness,open(os.path.join('relatedness',event_name+'_'+key+'.pkl'),'wb'))
            
            print(relatedness)
            sorrted_concepts = sorted(concepts.items(),key=lambda x:x[1],reverse=True)

            fw.write(str(relatedness)+'\n')
            
            selected_concepts = {}
            for concept in concepts:
                for word in concept.split(' '):
                    if str(Word(word).singularize()) in key_words:
                        selected_concepts[concept] = relatedness['_'.join(concept.split(' '))]

            # print(key,len(sorted_relatedness))
            sorted_relatedness = sorted(selected_concepts.items(),key=lambda x:x[1],reverse=True)
            relatedness_result[key] = sorted_relatedness
            # fw.write(str(sorted_relatedness)+'\n')
            # fw.write('\n')
            # fw.write('\n')
        pickle.dump(relatedness_result,open(os.path.join('relatedness',event_name+"_rel.pkl"),'wb'))


if __name__ == '__main__':
    # pair_edges(result)
    main()
    # get_frequency()

    # aggeragate()

    # flag = True
    # while flag:
    #     try:
    #         search_relatedness()
    #         flag = False
    #     except:
    #         flag = True

    # event_name = 'Town_hall_meeting'
    # concept = 'town hall meeting'
    # result = search_ConceptNet(event_name,concept)
    # print(result)
    # query_concept = 'parade'
    # concepts = ['parade','march','floats','column_people']
    # relatedness = cal_relatedness('parade',['march','floats','column people','gun'])
    # print(relatedness)
    # test()