def hex2bin(text):
    result = []
    for char in text:
        hex_value = int(char, 16)
        bin_value = bin(hex_value).replace("0b", "")
        bin_eight_bits = bin_value.zfill(4)
        result.append(bin_eight_bits)
    return "".join(result)

def bin2hex(bin_value):
    result = []
    for i in range(0, len(bin_value), 4):
        int_value = int(bin_value[i:i+4], 2)
        hex_value = hex(int_value)
        result.append(hex_value.replace("0x", ""))
    return "".join(result)

def xor (A, B):
    result = []
    for Ai, Bi in zip(A, B):
        result.append(str(int(Ai) ^ int(Bi)))
    return "".join(result)

def shift(word, shift):
    temp = word[shift:] + word[:shift]
    return temp

def add(a, b):
    temp = int(a, 2) + int(b, 2)
    temp = temp % 2**16
    temp = format(temp, "016b")
    return temp

def add_inv(a):
    temp = (0x10000 - int(a,2)) % 2**16
    temp = format(temp, "016b")
    return temp

def mult(a, b):
    temp = int(a, 2) * int(b, 2)
    if(temp != 0):
        temp = (temp % 0x10001) % 2**16
    elif(int(a,2) != 0 or int(b,2) != 0):
         temp =  (1 - int(a,2) - int(b,2)) % 2**16   
    temp = format(temp, "016b")
    return temp

def mult_inv(b, m=(0x10001)):
    m0 = m
    a = int(b,2)
    y = 0
    x = 1
    if (m == 1):
        return 0
    while (a > 1):
        q = a // m
        t = m
        m = a % m
        a = t
        t = y
        y = x - q * y
        x = t
    if (x < 0):
        x = x + m0
    return format(x, "016b")

def inverter_chave(keys):
    reverse_keys = [0]*52

    reverse_keys[48] = mult_inv(keys[0])
    reverse_keys[49] = add_inv(keys[1])
    reverse_keys[50] = add_inv(keys[2])
    reverse_keys[51] = mult_inv(keys[3])

    for r in reversed(range(1, 8)):
        reverse_keys[r*6 + 4] = keys[53 - r*6 - 7]                     
        reverse_keys[r*6 + 5] = keys[53 - r*6 - 6]                     
        reverse_keys[r*6 + 0] = mult_inv(keys[53 - r*6 - 5])   
        reverse_keys[r*6 + 2] = add_inv(keys[53 - r*6 - 4])     
        reverse_keys[r*6 + 1] = add_inv(keys[53 - r*6 - 3])     
        reverse_keys[r*6 + 3] = mult_inv(keys[53 - r*6 - 2])   

    reverse_keys[4] = keys[46]
    reverse_keys[5] = keys[47]
    reverse_keys[0] = mult_inv(keys[48])
    reverse_keys[1] = add_inv(keys[49])
    reverse_keys[2] = add_inv(keys[50])
    reverse_keys[3] = mult_inv(keys[51])

    return reverse_keys

def generate_key (key): 
    Key = [key[i:i+2] for i in range(0, len(key), 2)]
    Key_bin = []
    
    for bloco in Key:
        chave_bin = ""
        temp = ""
        for i in bloco: 
            temp = temp + str(hex(ord(i)))[2:].zfill(2)
        for i in temp: 
            chave_bin = chave_bin + str(format(int(i, 16), '04b'))
        Key_bin.append(chave_bin)

    string_bin = ''.join(Key_bin)
    temp_bloco = string_bin
    for i in range(6):
        temp_bloco = shift(temp_bloco, 25)
        for j in range(len(temp_bloco)//16):
            Key_bin.append(temp_bloco[j*16:(j+1)*16])

    Key_bin = Key_bin[:52] 
    return Key_bin


def encrypt_IDEA(plain_text, key):
    keys= generate_key(key)
    plain_text_bin = hex2bin(plain_text)
    iteration_list= [[plain_text_bin[i:i+16]] for i in range(0, len(plain_text_bin), 16)]

    for iteration in range(8):
        step1 = mult(iteration_list[0][iteration], keys[iteration*6])        
        step2 = add(iteration_list[1][iteration], keys[(iteration*6) + 1])   
        step3 = add(iteration_list[2][iteration], keys[(iteration*6) + 2])   
        step4 = mult(iteration_list[3][iteration], keys[(iteration*6) + 3])  
        step5 = mult(xor(step1, step3), keys[(iteration*6) + 4])   
        step6 = add(xor(step2, step4), step5)
        step7 = mult(step6, keys[(iteration*6) + 5])                   
        step8 = add(step7, step5)

        iteration_list[0].append(xor(step1, step7)) 
        iteration_list[1].append(xor(step3, step7))   
        iteration_list[2].append(xor(step2, step8))   
        iteration_list[3].append(xor(step4, step8))

    x1 = (mult(iteration_list[0][-1], keys[48]))
    x2 = (add(iteration_list[2][-1], keys[49]))
    x3 = (add(iteration_list[1][-1], keys[50]))
    x4 = (mult(iteration_list[3][-1], keys[51]))

    cifra = x1+ x2+ x3+ x4

    output_bin = bin2hex(cifra)
    
    return output_bin

def decrypt_IDEA(plain_text, key):
    keys_temp = generate_key(key)
    keys= inverter_chave(keys_temp)
    plain_text_bin = hex2bin(plain_text)
    iteration_list= [[plain_text_bin[i:i+16]] for i in range(0, len(plain_text_bin), 16)]

    for iteration in range(8):
        step1 = mult(iteration_list[0][iteration], keys[iteration*6])        
        step2 = add(iteration_list[1][iteration], keys[(iteration*6) + 1])   
        step3 = add(iteration_list[2][iteration], keys[(iteration*6) + 2])   
        step4 = mult(iteration_list[3][iteration], keys[(iteration*6) + 3])  
        step5 = mult(xor(step1, step3), keys[(iteration*6) + 4])   
        step6 = add(xor(step2, step4), step5)
        step7 = mult(step6, keys[(iteration*6) + 5])                   
        step8 = add(step7, step5)
        
        iteration_list[0].append(xor(step1, step7)) 
        iteration_list[1].append(xor(step3, step7))  
        iteration_list[2].append(xor(step2, step8))   
        iteration_list[3].append(xor(step4, step8))

    x1 = (mult(iteration_list[0][-1], keys[48]))
    x2 = (add(iteration_list[2][-1], keys[49]))
    x3 = (add(iteration_list[1][-1], keys[50]))
    x4 = (mult(iteration_list[3][-1], keys[51]))

    cifra = x1+ x2+ x3+ x4  
    output_bin = hex(int(cifra, 2)).upper()[2:].zfill(16)
    return output_bin
    



def encrypt(plain_text, chave):
    texto_cifrado = encrypt_IDEA(plain_text, chave)
    print("Texto claro: " + plain_text)
    print("Chave usada: " + chave)
    print("Criptografado: " + texto_cifrado)
    return texto_cifrado


def decrypt(cifra, chave):
    texto_decifrado = decrypt_IDEA(cifra, chave)
    print("Texto Decriptografado: " + texto_decifrado)
    return texto_decifrado



def apply(text, key, mode):
    key = key[0]
    key = hex2bin(key)
    generate_key(key)

    if mode == "encrypt":
        result =  encrypt(text)
    
    elif mode == "decrypt":
        result =  decrypt(text)
    
    else:
        raise Exception("Erro no mode!")

    return result
