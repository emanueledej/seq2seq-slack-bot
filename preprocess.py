def tokenize_lowercase(message):
    # tokenize at ,.?!
    chars = ['.', ',', ';', '?', '!']
    for c in chars:
        if c in message:
            prefix = " "+c
            m = prefix.join(message.split(c))
            message = m
    filtered_m = message.lower().replace("  ", " ").replace("(", "").replace(")", "") # delete brackets
    return filtered_m

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