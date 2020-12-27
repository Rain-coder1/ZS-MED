from spider import search_wikihow
import json
import nltk

from nltk.stem import PorterStemmer
from nltk.corpus import stopwords

from nltk.stem import WordNetLemmatizer
from textblob import TextBlob
from textblob.np_extractors import ConllExtractor

from pattern.en import parsetree, Chunk
from nltk.tree import Tree
from textblob import Word
from cal_similarity import get_word_vector
import os
import pickle


verbs = ["VB","VBD","VBG","VBN","VBP","VBZ"]
nouns = ["NN","NNS","NNP","NNPS"]


def filter_word(word):
	for ch in word:
		if ch < 'z' and ch > 'a':
			return True
	return False


def split_to_words(sentence):
	word_tokens = []
	tags = sentence.tags
	# print(tags)
	for tag in tags:
		if tag[1] in verbs or tag[1] in nouns:
			word = tag[0]
			new_word = word.lemmatize()
			new_word = Word(new_word)
			new_word = new_word.lemmatize('v')
			new_word = new_word.lower()
			word_tokens.append(new_word)
	return word_tokens


word_list = ['ring','knee','hand','kiss','hug','kneel','finger','wed']


def textblod_method(name):
	fr = open(name+'.json','r')
	result = json.load(fr)

	statistics = {}
	stop_words = set(stopwords.words('english'))

	word_times = {}

	for name in result.keys():

		statistics[name] = {}

		print(name + ": ")

		word_tokens = []
		description = result[name]['description']
   
		extractor = ConllExtractor()
		blob = TextBlob(description,np_extractor=extractor)

		sentences = blob.sentences
		for sentence in sentences:
			word_tokens.extend(split_to_words(sentence))

		# print(description)
		# print(blob.noun_phrases)

		for key,val in result[name]['content'].items():
			for step_content in val:
				text = step_content.strip()
				blob = TextBlob(text,np_extractor=extractor)
				# print(blob.noun_phrases)
				sentences = blob.sentences
				for sentence in sentences:
					word_tokens.extend(split_to_words(sentence))

		freq = nltk.FreqDist(word_tokens)

		for key in freq.keys():
			num = word_times.get(key,0)
			word_times[key] = num + 1

	# for word in word_list:
	# 	print(word + ' ' + str(word_times[word]))

	selected_word = []

	for key,value in word_times.items():
		if value >= 4:
			selected_word.append(key)
			# cnt += 1
			# print(key+':'+str(value))
	print(selected_word)
	# get_word_vector(selected_word)


def judge_chunk(subtree,filter_words):
	for leave in subtree.leaves():
		word = Word (leave[0])
		new_word = word.lemmatize()
		new_word = Word(new_word)
		new_word = new_word.lemmatize('v')
		new_word = new_word.lower()
		if new_word in filter_words:
			return True

	return False


def parse(sentence,filter_words):
	# noun_phrase = r"""
	#     NP: {<DT|CD>?<JJ.*>*<NN.*>}
	#     VP: {<VB.*><RP|PRP.*>?<IN|TO>?<NP>?}
	# """
	noun_phrase = r"""
	    NP: {<DT|CD>?<NN|JJ>*<NN.*>}
	    VP: {<VB.*><IN|TO>?<NP>?}
	"""
	verb_phrase = r"""
	    VP: {<DT><NN|JJ>*<NN.*>}
	"""

	words = nltk.word_tokenize(sentence)
	sentence_tag = nltk.pos_tag(words)
	# print(sentence_tag)
	contents = []

	cp = nltk.RegexpParser(noun_phrase)
	tree = cp.parse(sentence_tag)
	for subtree in tree.subtrees():
		# if subtree.label() == 'NP' or subtree.label() == 'VP':
		if subtree.label() == 'VP':
			if judge_chunk(subtree,filter_words):
				content = ''
				for item in subtree.leaves():
					content += item[0] + ' '
				content = content.strip()
				contents.append(content)
				# fw.write(content+'\n')

		# if subtree.label() == 'VP':
		# 	print(subtree.leaves())
	return contents


def nltk_method(name):
	fr = open(name+'.json','r')
	result = json.load(fr)

	statistics = {}
	stop_words = set(stopwords.words('english'))

	for name in result.keys():

		statistics[name] = {}
		print(name + ": ")
		word_tokens = []

		description = result[name]['description']
		descriptions = nltk.sent_tokenize(description)

		# print(descriptions)
		for sentence in descriptions:
			# tree = parsetree(sentence)
			# for sentence_tree in tree:
			# 	print(sentence_tree.chunks)
			# parse(sentence)
			word_tokens.extend(nltk.word_tokenize(sentence))

		for key,val in result[name]['content'].items():
			for step_content in val:
				text = step_content.strip()
				sentences = nltk.sent_tokenize(text)
				for sentence in sentences:
					word_tokens.extend(nltk.word_tokenize(sentence))


		lemmatizer = WordNetLemmatizer()
		word_tokens = [lemmatizer.lemmatize(w) for w in word_tokens]

		filtered_sentence = [w for w in word_tokens if w not in stop_words]
		tokens = nltk.pos_tag(filtered_sentence)

		# print(tokens)

		freq = nltk.FreqDist(filtered_sentence)
		# for key,val in freq.items():
		# 	print(str(key) + ':' + str(val))

		standard_freq = freq.most_common(100)
		print(standard_freq)


def if_select(sentence,filter_words):
	for word in sentence.words:
		new_word = word.lemmatize()
		new_word = Word(new_word)
		new_word = new_word.lemmatize('v')
		new_word = new_word.lower()

		if new_word in filter_words:
			return True

	return False


def get_high_order_info(event_name,filter_words):
	data_dir = 'wikihow_articles'
	file_path = os.path.join(data_dir,event_name+'.json')
	fr = open(file_path,'r')
	result = json.load(fr)

	# fw = open(event_name+'_output.txt','w',encoding="utf-8")
	noun_phrases = []
	high_order_info = []

	for name in result.keys():

		# print(name + ": ")
		selected_sentences = []
		description = result[name]['description']
   
		blob = TextBlob(description)
		sentences = blob.sentences
		
		for sentence in sentences:
			if if_select(sentence,filter_words):
				selected_sentences.append(sentence)


		for key,val in result[name]['content'].items():
			for step_content in val:
				text = step_content.strip()
				blob = TextBlob(text)
				# print(blob.noun_phrases)
				sentences = blob.sentences
				for sentence in sentences:
					if if_select(sentence,filter_words):
						selected_sentences.append(sentence)


		for sentence in selected_sentences:
			contents = parse(str(sentence),filter_words)
			high_order_info.extend(contents)

	return high_order_info


if __name__ == '__main__':
	# nltk_method('Propose_Marriage')
	# textblod_method('Propose_Marriage')
	# filter_words = ['ring','knee','kiss','hug','kneel','finger','box','engagement']  # marriage
	# filter_words = ['tire','car','bike','bicycle','wheel','jack','hubcap','nut','hub','wrench','rim','replace']  # Changing_a_vehicle_tire
	# filter_words = ['sandwich','flour','dough','kitchen','yeast','bread','plate','cheese','meat','vegetable','roast','cut','onion']  # Making_a_sandwich
	# filter_words = ['sew','fabric','cloth','machine','needle','stitch','cut','thread']  # sew
	# filter_words = ['bike','bicycle','helmet','motorcycle','motorbike','wheelie','ride','jump']  # Attempting_a_bike_trick
	# filter_words = ['oven','sink','toaster','refrigerator','microwave','wash','clean','kitchen','towel','soap','wipe']  # Cleaning_an_appliance
	# filter_words = ['rock'，'rope']  # Rock_climbing
	# filter_words = ['ball','fetch','frisbee']  # Felling_a_tree
	# filter_words = ['birthday','cake','balloon','candle','gift','present','dessert']

	# nltk_method('Birthday_party')
	# textblod_method('Non-motorized_vehicle_repair')

	output_dir = 'highorder_info'

	event_name = 'Playing_fetch'
	filter_words = ['ball','fetch','frisbee']

	high_order_info = get_high_order_info(event_name,filter_words)
	# print(high_order_info)
	# print(len(high_order_info))
	print(high_order_info)
	# pickle.dump(high_order_info,open(os.path.join(output_dir,event_name+'.pkl'),'wb'))