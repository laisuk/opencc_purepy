from opencc_purepy import OpenCC

def main():
    text = "“春眠不觉晓，处处闻啼鸟。”"
    # text = "“恶名昭著”"  # Test zho_check() for interference "著"
    opencc = OpenCC("s2t")
    converted = opencc.convert(text, punctuation=True)

    print("Input text: {}".format(text))
    print("Input text code: {}".format(opencc.zho_check(text)))
    print("Output text: {}".format(converted))
    print("Output text code: {}".format(opencc.zho_check(converted)))

if __name__ == "__main__":
    main()
