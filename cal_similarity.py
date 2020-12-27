import numpy as np
import pickle
from scipy.spatial.distance import cosine
from tqdm import tqdm
from textblob import Word

med13 = [
    'Birthday_party',
    'Changing_a_vehicle_tire',
    'Flash_mob_gathering',
    'Getting_a_vehicle_unstuck',
    'Grooming_an_animal',
    'Making_a_sandwich',
    'Parade',
    'Parkour',
    'Repairing_an_appliance',
    'Working_on_a_sewing_project',
    'Attempting_a_bike_trick',
    'Cleaning_an_appliance',
    'Dog_show',
    'Giving_directions_to_a_location',
    'Marriage_proposal',
    'Renovating_a_home',
    'Rock_climbing',
    'Town_hall_meeting',
    'Winning_a_race_without_a_vehicle',
    'Working_on_a_metal_crafts_project',
]

med14 = [
    'Attempting_a_bike_trick',
    'Cleaning_an_appliance',
    'Dog_show',
    'Giving_directions_to_a_location',
    'Marriage_proposal',
    'Renovating_a_home',
    'Rock_climbing',
    'Town_hall_meeting',
    'Winning_a_race_without_a_vehicle',
    'Working_on_a_metal_crafts_project',
    'Beekeeping',
    'Wedding_shower',
    'Non-motorized_vehicle_repair',
    'Fixing_musical_instrument',
    'Horse_riding_competition',
    'Felling_a_tree',
    'Parking_a_vehicle',
    'Playing_fetch',
    'Tailgating',         
    'Tuning_musical_instrument',    
]

concept_select = {
    'Birthday_party':[[38,159,79],[470,417],[]],
    'Changing_a_vehicle_tire':[[82,83,180,81],[751,535,479],[]],
    'Flash_mob_gathering':[[569,281,599,79,132,62,291,84,234,113,130,491],[],[]],
    'Getting_a_vehicle_unstuck':[[59,552,567,393,454],[609,803,586,586,717,847,408,802,627,792,864,656,751,675,867,817,511,595,866,757],[]],
    'Grooming_an_animal':[[23,202,315,203,314,125,447,574],[435,285,332,284,194],[346]],
    'Making_a_sandwich':[[269,109,47],[923,567,934,891,930,712],[114,203]],
    'Parade':[[281],[862,439,417,652],[47,319]],
    'Parkour':[[307,17],[],[]],
    'Repairing_an_appliance':[[557,81,14,302,560],[713,897,827,740],[]],
    'Working_on_a_sewing_project':[[439,168,526],[786,769],[137]],
    'Attempting_a_bike_trick':[[240,172,31],[671,880],[]],
    'Cleaning_an_appliance':[[573,382,576],[827,550,438,760,859],[]],
    'Dog_show':[[540,314,473,58],[160,264,233,267,229,194,220,198,258,250,249,257,179,268,180,167,224,159,254],[225]],
    'Giving_directions_to_a_location':[[137,234,149,516,459],[480,487,468,475],[82,112]],
    'Marriage_proposal':[[282,220,247],[],[]],
    'Renovating_a_home':[[324,54,554],[739,743,634],[]],
    'Rock_climbing':[[422],[972,970],[]],
    'Town_hall_meeting':[[15,16],[906],[211]],
    'Winning_a_race_without_a_vehicle':[[219,223,504,505,506,507,545],[433,781,842],[24,325]],
    'Working_on_a_metal_crafts_project':[[273,588,557,30,274],[],[23]],
    'Beekeeping':[[26],[410,599,519,309],[]],
    'Wedding_shower':[[282,301,200,12],[762,793],[126]],
    'Non-motorized_vehicle_repair':[[180,13,408,557],[671,535,880,612],[]],
    'Fixing_musical_instrument':[[407,350,345,362,341,335,373,353,379,340],[402,546,477,401,881,784,810,579,420],[]],
    'Horse_riding_competition':[[414,495,413],[354,339,781,603],[17,275]],
    'Felling_a_tree':[[544,102,432,527],[634,491],[36,338]],
    'Parking_a_vehicle':[[149,140,393,552],[627,675,468,654,656,404,867,403,817,779,864,609],[257]],
    'Playing_fetch':[[540,571,77],[209,208,263,273,189,264,239,284],[209]],
    'Tailgating':[[569,62,184,425,250],[],[257]],         
    'Tuning_musical_instrument':[[345,359,519],[402,881,546,420,579,783],[238]],   
}

def get_word_vector(word_list):
	fr = open('word_vector.pkl','rb')
	all_vectors = pickle.load(fr)
	word_scores = {}

	event_name = 'Marriage_Proposal'

	for word in word_list:
		vec1 = all_vectors[event_name]
		if word in all_vectors.keys():
			vec2 = all_vectors[word]
			word_scores[word] = cos_sim(vec1,vec2)

	cnt = 0

	for k in sorted(word_scores,key=word_scores.__getitem__,reverse=True):
		print(k,word_scores[k])
		# cnt += 1
		# if cnt > 10:
		# 	break



def cos_sim(vector_a, vector_b):
    vector_a = np.mat(vector_a)
    vector_b = np.mat(vector_b)
    num = float(vector_a * vector_b.T)
    denom = np.linalg.norm(vector_a) * np.linalg.norm(vector_b)
    # print(denom)
    if denom == 0:
    	return 0
    else:
	    cos = num / denom
	    return cos

# def cal_cas_distance():

def gen_vector():
	# imageNet_classes = pickle.load(open('label_1000.pkl','rb'))
	# imageNet_name = []
	# for i in range(1000):
	# 	content = imageNet_classes[i].split(',')[0]
	# 	if '-' in content:
	# 		content = ' '.join(content.split('-'))
	# 	print(content)
	# 	imageNet_name.append(content)
	# pickle.dump(imageNet_name,open('Image_class.pkl','wb'))

    Places_classes = pickle.load(open('places_label.pkl','rb'))
    Places_name = []
    for i in range(365):
        content = Places_classes[i]
        if '/' in content:
            # content = ','.join(content.split('/'))
            content = content.split('/')[0]
        if '_' in content:
            content = ' '.join(content.split('_'))
        Places_name.append(content)
        # print(Places_classes[i],'//',content)
    # print(Places_name)
    pickle.dump(Places_name,open('Places_class.pkl','wb'))


def gen_sim_vector():
    concept_sel = {}
    concept_select = pickle.load(open('concept_R_med14.pkl','rb'))
    event_vec = pickle.load(open('med14_vec.pkl','rb'))
    for event in med14:
        expansion = []
        # fr = open('expansion/'+event+'.txt','r')
        # for line in fr.readlines():
        #     line = line.strip()
        #     if line != '':
        #         expansion.append(line)
        expansion_vec = event_vec[event]
        print(event)
        I3D = np.load('Places_vec.npy')
        I3D_sent = pickle.load(open('Places_class.pkl','rb'))
        I3D_score = []
        for i in range(365):
            vec1 = I3D[i]
            score = cos_sim(vec1, expansion_vec)
            # score = np.sum(vec1 * expansion_vec, axis=1) / (np.linalg.norm(expansion_vec, axis=1)*np.linalg.norm(vec1))
            I3D_score.append(score)
            # if I3D_sent[i] == 'blowing out candles':
            #     for idx in topk_idx:
            #         print(score[idx],expansion[idx])
            # print(I3D_sent[i],expansion[topk_idx],score[topk_idx])
        I3D_score = np.array(I3D_score)
        topk_idx = np.argsort(I3D_score)[::-1][0:5]
        for idx in topk_idx:
            print(I3D_sent[idx],I3D_score[idx],idx)
        concept_sel[event] = list(topk_idx)
        if concept_select[event][2] == []:
            concept_select[event][2] = list(topk_idx)

    pickle.dump(concept_select,open('concept_R_med14.pkl','wb'))


if __name__ == '__main__':
	# word_list = ['box','ring','kiss','kneel','get','restaurant']
 #    fr = open('word_vector.pkl','rb')
 #    all_vectors = pickle.load(fr)
	# # print(all_vectors['hello'].shape)
 #    event_vec = {}

 #    for event in med13:
 #        vec = np.zeros(300)
 #        expansion = []
 #        expansion = event.split('_')
 #        # print(expansion)
 #        for word in expansion:
 #            try:
 #                vec = vec + all_vectors[word]
 #            except:
 #                try:
 #                    vec = vec + all_vectors[Word(word).lemmatize()]
 #                except:
 #                    print(word)
 #        event_vec[event] = vec

 #    pickle.dump(event_vec,open('med13_vec.pkl','wb'))

 #    event_vec = {}

 #    for event in med14:
 #        vec = np.zeros(300)
 #        expansion = []
 #        expansion = event.split('_')
 #        for word in expansion:
 #            try:
 #                vec = vec + all_vectors[word]
 #            except:
 #                try:
 #                    vec = vec + all_vectors[Word(word).lemmatize()]
 #                except:
 #                    print(word)
 #        event_vec[event] = vec

 #    pickle.dump(event_vec,open('med14_vec.pkl','wb'))

	# imageNet_name = pickle.load(open('Places_class.pkl','rb'))
	# imageNet_vec = []

	# for sent in tqdm(imageNet_name):
	# 	words = sent.split(' ')
	# 	new_words = [word.lower() for word in words]
	# 	vec = np.zeros(300)
	# 	for word in new_words:
	# 		try:
	# 			vec = vec + all_vectors[word]
	# 		except:
	# 			try:
	# 				vec = vec + all_vectors[Word(word).lemmatize()]
	# 			except:
	# 				print(word)
	# 	imageNet_vec.append(vec)
	
	# np.save('Places_vec.npy',np.array(imageNet_vec))

	# vec = np.load('Image_vec.npy')
	# cnt = 0
	# for i in range(vec.shape[0]):
	# 	if np.sum(vec[i]) == 0:
	# 		print('555')
	# 		cnt += 1
	# 	else:
	# 		print(vec[i])
	# 		break
	# print(cnt)

	# for word in word_list:
	# 	vec1 = all_vectors['marriage']
	# 	vec2 = all_vectors[word]
	# 	print(word + ' ' + str(cos_sim(vec1,vec2)))
	# gen_vector()
	gen_sim_vector()
	# concept_select = pickle.load(open('concept_R_med13.pkl','rb'))
	# print(concept_select)
	





