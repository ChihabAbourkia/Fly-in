s1 = "z"
s2 = "aa"


ascii1 = 0
for c in s1:
    ascii1 += ord(c)
ascii2 = 0
for c in s1:
    ascii2 += ord(c)

print(f"{ascii1 = }\n{ascii2 = }")
