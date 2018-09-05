from slack_history import *
import argparse
import copy

def split_sents(message, split_symbol):
	# insert a split symbol into message for splitting sentences
	chars = ['.', '?', '!', ')', '(']
	m = message
	for c in chars:
		if c in message:
			split_m = message.strip().split(c)
			if len(split_m) > 1:
				if sum([1 if len(part)<4 else 0 for part in split_m]) < 3:
					prefix = c+split_symbol
					m = prefix.join(split_m)
	if "\n" in m:
		m = m.replace("\n", split_symbol)
	return m

def formatData(messages):
	formattedMessages=[]
	for m in messages:
		if m["type"] == "message":
			formattedMessages.append(m["text"])
	
	return formattedMessages

CODES = {'<PAD>': 0, '<EOS>': 1, '<UNK>': 2, '<GO>': 3 }

def create_lookup_tables(text):
  # make a list of unique words
  vocab = set(text.split())
  # (1)
  # starts with the special tokens
  vocab_to_int = copy.copy(CODES)
  # the index (v_i) will starts from 4 (the 2nd arg in enumerate() specifies the starting index)
  # since vocab_to_int already contains special tokens
  for v_i, v in enumerate(vocab, len(CODES)):
      vocab_to_int[v] = v_i
  # (2)
  int_to_vocab = {v_i: v for v, v_i in vocab_to_int.items()}
  return vocab_to_int, int_to_vocab


def process_decoder_input(target_data, target_vocab_to_int, batch_size):
	# get '<GO>' id
	go_id = target_vocab_to_int['<GO>']
	
	after_slice = tf.strided_slice(target_data, [0, 0], [batch_size, -1], [1, 1])
	after_concat = tf.concat( [tf.fill([batch_size, 1], go_id), after_slice], 1)
	
	return after_concat

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='download slack history')
	parser.add_argument('--token', help="an api token for a slack user")
	args = parser.parse_args()
	messages = getChannelsMessage(args.token)
	for m in messages:
		formatted_messages = formatData(m)
		for message in formatted_messages:
			vocab_to_int, int_to_vocab = create_lookup_tables(message)
			print(vocab_to_int)
			print(int_to_vocab)
	

