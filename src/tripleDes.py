from . import des

def apply(text, key, mode):
    key1 = [key[0]]
    key2 = [key[1]]

    if mode == "encrypt":
        r1 = des.apply(text, key1, "encrypt")
        r2 = des.apply(r1, key2, "decrypt")
        result = des.apply(r2, key1, "encrypt")

    elif mode == "decrypt":
        r1 = des.apply(text, key1, "decrypt")
        r2 = des.apply(r1, key2, "encrypt")
        result = des.apply(r2, key1, "decrypt")

    return result

# text = "123456ABCD132536"
# key = "AABB09182736CCDD"

# ct = "c0b7a8d05f3a829c"

# print(apply(text, key, "apply"))
# print(apply(ct, key, "decrypt"))


# text = "123456abcd132536"
# key = "AABB09182736CCDD"
# key2 = "Aa5509182798CBAD"

# des1 = des(text, key, "encrypt")
# des2 = des(des1, key2, "decrypt")
# des3 = des(des2, key, "encrypt")

# print(des3)

# des1 = des(des3, key, "decrypt")
# des2 = des(des1, key2, "encrypt")
# des3 = des(des2, key, "decrypt")

# print(des3)





