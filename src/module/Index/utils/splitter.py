import nltk
nltk.download('punkt')
from nltk.tokenize import sent_tokenize
import re

def doc_split(text: str)-> tuple[list[str], list[str], dict[str:str]]:
	paragraphs = re.split('\n{2,}', text)
	graph = {}
	ret_p = []
	ret_s = []
	for para in paragraphs:
		sentences = sent_tokenize(para)
		if not sentences:
			continue
		ret_p.append(para)
		for s in sentences:
			graph[s] = para
			ret_s.append(s)
	return ret_s, ret_p, graph

#TODO support accuracy improvement based on the relation between nearest neighbors in sentences and paragraphs
