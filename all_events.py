import pickle


med_events = [
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
    'Beekeeping',
    'Wedding_shower',
    'Non-motorized_vehicle_repair',
    'Fixing_musical_instrument',
    'Horse_riding_competition',
    'Felling_a_tree',
    'Parking_a_vehicle',
    'Playing_fetch',
    'Tailgating',         
    'Tuning_musical_instrument'
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


_LABEL_MAP_PATH_600 = 'concept_library/kinetics.txt'
kinetics_classes = [x.strip() for x in open(_LABEL_MAP_PATH_600)]
imageNet_classes = [pickle.load(open('concept_library/imageNet.pkl','rb'))[idx] for idx in range(1000)]
Places_classes = list(pickle.load(open('concept_library/places365.pkl','rb')))


kinetics_id2label = {i:label for i,label in enumerate(kinetics_classes)}
kinetics_label2id = {label:i for i,label in enumerate(kinetics_classes)}

places365_id2label = {i:label for i,label in enumerate(Places_classes)}
places365_label2id = {label:i for i,label in enumerate(Places_classes)}

imageNet_id2label = {i:label for i,label in enumerate(imageNet_classes)}
imageNet_label2id = {label:i for i,label in enumerate(imageNet_classes)}

# print(kinetics_id2label)
selected_labels = {}

for key in concept_select.keys():
    kinetics_id = concept_select[key][0]
    imageNet_id = concept_select[key][1]
    places365_id = concept_select[key][2]

    selected_labels[key] = {}
    selected_labels[key]['kinetics'] = [kinetics_id2label[ele] for ele in kinetics_id]
    selected_labels[key]['imageNet'] = [imageNet_id2label[ele] for ele in imageNet_id]
    selected_labels[key]['places365'] = [places365_id2label[ele] for ele in places365_id]


# for key in selected_labels.keys():
#     print('\"' + key + '\"' +" : ",[selected_labels[key]['kinetics'],selected_labels[key]['imageNet'],selected_labels[key]['places365']])

google_concepts = {
    "Birthday_party" : ['balloon', 'cake','present','celebrate','kid', 'birthday', 'happy birthdays','party','candle'],
    "Changing_a_vehicle_tire" : ['wrench', 'jack', 'flat tyre', 'tire', 'change', 'spare wheel', 'sensors can', 'lug nuts', 'wheel'],
    "Flash_mob_gathering" : ['celebrating', 'dancing', 'busking', 'sing', 'banner', 'group', 'people'],
    "Getting_a_vehicle_unstuck" : ['trac grabber', 'car', 'snow', 'snow', 'winch', 'jeep', 'truck', 'sand', 'mud', 'wheel', 'stuck', 'tire traction', 'wheel drive', 'off road','van'],
    "Grooming_an_animal" : ['dog', 'brush', 'cat', 'pet', 'nail', 'grooming', 'sheep', 'petting', 'Brushing', 'groomer', 'bath', 'puppy', 'sheep', 'pig'], 
    "Making_a_sandwich" : ['cheese', 'bread','sandwich','kitchen','sausage', 'breading', 'recipe', 'cheese sandwich','plate','hotdog'],
    "Parade" : ['march', 'float', 'marching', 'celebrate', 'parade'],
    "Parkour" : ['free running', 'jump','backflip','parkour', 'sport', 'gym', 'roof'],
    "Repairing_an_appliance" : ['kitchen', 'wrench', 'oil', 'saw','fridge','oven','washing machines','dryer','refrigerator','computer','stove'],
    "Working_on_a_sewing_project" : ['sewing machines', 'sewing', 'diy sewing', 'craft', 'garment', 'fabric', 'dressmaker', 'needle', 'craft', 'machine'],
    "Attempting_a_bike_trick" : ['bike', 'freestyle motocross', 'mountain bike', 'jumping bicycle', 'freestyle bmx', 'motorcycle', 'front flip', 'bike cross', 'mtb', 'bmx racing','unicycle'],
    "Cleaning_an_appliance" : ['washing', 'stove', 'espresso maker', 'refrigerator', 'toaster', 'oven', 'washer', 'freezer', 'soda', 'vinegar'],
    "Dog_show" : ['westminster', 'german shepherd', 'dog', 'american staffordshire terrier', 'pet', 'poodle', 'golden retriever', 'philadelphia', 'pitbull', 'australian shepherd', 'great dane', 'greyhound', 'kennel club', 'boston terrier', 'labrador', 'samoyed', 'toy', 'newfoundland', 'houston', 'bulldog', 'crufts', 'yorkshire terrier', 'champion', 'newton', 'handler', 'conformation', 'saint bernard', 'rhodesian ridgeback', 'doberman'],
    "Giving_directions_to_a_location" : ['map', 'worksheet', 'sign', 'prepositions', 'esl', 'traffic', 'exercises', 'conversations', 'directions activity', 'directions lesson plan', 'directions worksheet', 'dialogue', 'prepositional phrases', 'directions esl'],
    "Marriage_proposal" : ['marriage proposal','beach', 'kiss', 'hug', 'pinterest', 'engagement', 'restaurant', 'sunset', 'knee', 'flower', 'wedding proposal'],
    "Renovating_a_home" : ['paint', 'wall papers', 'furniture', 'cabinet','kitchen', 'house', 'budget', 'old house','sawmill'],
    "Rock_climbing" : ['wall', 'mountain', 'rope', 'thailand', 'cliff', 'rock', 'climbing wall', 'gym' ,'route'],
    "Town_hall_meeting" :  ['senator', 'conference', 'agenda', 'town', 'business', 'conference room', 'cartoon'],
    "Winning_a_race_without_a_vehicle" : ['finish line','runner', 'hurdling' , 'run', 'track', 'marathon', 'athlete', 'scorecard', 'swim', 'sports', 'swimming'],
    "Working_on_a_metal_crafts_project" : ['sheet metal fabrication', 'scrap metal', 'welding projects', 'welding art', 'arc welding', 'horseshoe', 'metal','weld'],
    "Beekeeping" : ['bee keeping','bee','honey','apiary','bee hive','bee keeper','honeycomb'],
    "Wedding_shower" : ['invitation', 'tea party', 'decoration', 'beach theme', 'marriage', 'flower', 'free printable', 'elegant', 'thank you', 'gold', 'blue', 'congratulations', 'outdoor', 'fiesta', 'rose gold', 'gift', 'bride', 'background', 'pink', 'pinterest', 'message', 'chalkboard', 'diy', 'bbq', 'mimosa bar'],
    "Non-motorized_vehicle_repair" : ['wrench', 'bicycle', 'repairing', 'repair insurance', 'fixing', 'lane', 'transport'],
    "Fixing_musical_instrument" : ['flute', 'acoustic guitar repair', 'bamboo flute', 'electric guitar', 'keyboard', 'screwdriver', 'piano', 'xylophone', 'lute' , 'trombone', 'drum', 'brass', 'horn', 'trumpet', 'violin', 'price fixing', 'luthier', 'luthier workshop', 'brass instrument', 'guitar capo', 'dizi', 'guitar', 'yellow electric', 'keyboard', 'accordion'],
    "Horse_riding_competition" : ['horse jumping','ride horse','riding horse','horse','rope','saddle', 'dressage', 'equine','scoreboard'],   
    "Felling_a_tree" : ['axe', 'chainsaw', 'cut tree', 'saw','wood', 'tree','stump', 'wedge', 'hinge', 'sawmill'],
    "Parking_a_vehicle" : ['car', 'road', 'parklot', 'parking','bus', 'boat', 'truck', 'driving', 'garage','taxi','van','jeep'],
    "Playing_fetch" : ['bulldog', 'dog', 'tennis ball', 'toy', 'dog toy', 'frisbee', 'puppy'],
    "Tailgating" : ['car', 'college', 'football', 'truck', 'concert', 'stadium', 'alabama', 'nfl', 'party', 'fsu', 'nascar', 'kenny chesney', 'the grove', 'notre dame', 'game', 'lsu', 'ole miss', 'trailer', 'baseball', 'drunk', 'auburn', 'arrowhead', 'gillette stadium', 'at&t stadium', 'south carolina', 'tennessee', 'miller park', 'food', 'metlife stadium', 'broncos', 'tail gate'],
    "Tuning_musical_instrument" : ['acoustic guitar', 'string instrument', 'violin', 'organ','tuning fork', 'banjo','piano strings', 'dulcimer','piano', '440 hz', 'hipster beard', 'transparent png', 'trendy hipster', 'guitar capo', 'piano tuning', 'guitar', 'sound tuning', 'strings sound', 'guitar bearded'],
}


event_query = {
    "Birthday_party" : ['birthday', 'birthday_party'],
    "Changing_a_vehicle_tire" : ['tire', 'vehicle'],
    "Flash_mob_gathering" : ['gathering', 'mob'],
    "Getting_a_vehicle_unstuck" : ['unstuck', 'vehicle'],
    "Grooming_an_animal" : ['animal','groom'],
    "Making_a_sandwich" : ['sandwich'],
    "Parade" : ['parade'],
    "Parkour" : ['parkour'],
    "Repairing_an_appliance" : ['appliance', 'repair'],
    "Working_on_a_sewing_project" : ['sewing', 'sewing_project'],
    "Attempting_a_bike_trick" : ['bike', 'bike_trick'],
    "Cleaning_an_appliance" : ['appliance', 'cleaning'],
    "Dog_show" : ['dog', 'dog_show'],
    "Giving_directions_to_a_location" : ['direction', 'location'],
    "Marriage_proposal" : ['marriage', 'marriage_proposal'],
    "Renovating_a_home" : ['home', 'renovating'],
    "Rock_climbing" : ['rock'],
    "Town_hall_meeting" : ['hall', 'meeting'],
    "Winning_a_race_without_a_vehicle" : ['race'],
    "Working_on_a_metal_crafts_project" : ['craft', 'metal'],
    "Beekeeping" : ['beekeeping'],
    "Wedding_shower" : ['shower'],
    "Non-motorized_vehicle_repair" : ['repair', 'vehicle'],
    "Fixing_musical_instrument" : ['instrument', 'musical_instrument'],
    "Horse_riding_competition" : ['horse'],
    "Felling_a_tree" : ['fell', 'tree'],
    "Parking_a_vehicle" : ['vehicle'],
    "Playing_fetch" : ['fetch', 'play_fetch'],
    "Tailgating" : ['tailgate'],
    "Tuning_musical_instrument" : ['instrument', 'musical_instrument']
}