import numpy as np
import faiss
from typing import Any, Callable
import openai
from utils.tokenizer import get_num_tokens

def get_embedding(text:str):
	response = openai.Embedding.create(
	    input=text,
	    model="text-embedding-ada-002"
	)
	embeddings = response['data'][0]['embedding']
	return embeddings

class Index:
	def __init__(self, dim:int, get_embedding: Callable[[str], Any]=get_embedding):
		self.index: faiss.Index = faiss.IndexFlatIP(dim)
		self.texts: List[str] = []
		self.text_set: set[str] = set()
		self.get_embedding: Callable[[str], Any] = get_embedding

	def add(self, text: str):
		if (text in self.text_set):
			return
		embedding = self.get_embedding(text)
		self.index.add(np.array(embedding).reshape(1, -1).astype(np.float32))
		self.texts.append(text)
		self.text_set.add(text)

	def search(self, text:str, k:int=1, token_limit=0):
		embedding = self.get_embedding(text)
		if (k > len(self.texts)):
			k = len(self.texts)
		_, indices = self.index.search(np.array(embedding).reshape(1, -1).astype(np.float32), k)
		if not token_limit:
			return [self.texts[i] for i in indices[0]]
		else:
			token_count = 0
			ret = []
			for i in indices[0]:
				token_count += get_num_tokens(self.texts[i])
				if token_count < token_limit:
					ret.append(self.texts[i])
				else:
					break
			return ret
