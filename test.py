a = {"happy":"😀"}
b = "I am happy Happy is me"
b = b.lower()
for word in b.lower().split():
    if word in a:
        b = b.replace(word, a[word])
print(b)