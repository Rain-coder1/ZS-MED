# from textblob import Word
# from textblob import TextBlob

# from nltk.tag import StanfordPOSTagger

# eng_tagger = StanfordPOSTagger(model_filename=r'C:\Users\jy0205\Desktop\stanford-postagger-full-2018-10-16\models\english-left3words-distsim.tagger',
# 	path_to_jar=r'C:\Users\jy0205\Desktop\stanford-postagger-full-2018-10-16\stanford-postagger.jar')

# print(eng_tagger.tag('What is the airspeed of an unladen swallow ?'.split()))

# blob = TextBlob('What is the airspeed of an unladen swallow ?')
# print(blob.tags)
import numpy as np
from tqdm import tqdm
import pickle


a = pickle.load(open('google_articles/Birthday_party/google_concepts.pkl','rb'))
print(a)

i=0
word_vecs = {}
pury_word_vec = []
with open('E:\GoogleNews-vectors-negative300.bin', "rb") as f:
	header = f.readline()
	print('header',header)
	vocab_size, layer1_size = map(int, header.split())
	print('vocabsize:',vocab_size,'layer1_size:',layer1_size)
	binary_len = np.dtype('float32').itemsize * layer1_size
	print('binary_len', binary_len)
	for line in range(vocab_size):
		word = []
		while True:
			ch = f.read(1)
			#print(ch)
			if ch == b' ':
				word = ''.join(word)
				# print('single word:',word)
				break
			if ch != '\n':
				word.append(ch.decode('cp437'))##修改的主要是这里的解码方式
				#print(word)
		#print word
		word_vecs[word] = np.fromstring(f.read(binary_len), dtype='float32')
		if word == 'Marriage_Proposal':
			print(word)