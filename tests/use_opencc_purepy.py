from opencc_purepy import OpenCC

text = "“春眠不觉晓，处处闻啼鸟。”"
opencc = OpenCC("s2t")
converted = opencc.convert(text, punctuation=True)
print("Input text: {}".format(text))
print("Input text code: {}".format(opencc.zho_check(text)))
print("Output text: {}".format(converted))
print("Output text code: {}".format(opencc.zho_check(converted)))
