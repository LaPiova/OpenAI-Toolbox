import tiktoken

def get_num_tokens(text:str, encoding=tiktoken.encoding_for_model("gpt-3.5-turbo-0301")):
	return len(encoding.encode(text))
