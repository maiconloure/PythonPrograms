def replace(index, key, start, end):
    n = end - start + 1
    k = (index + key) % (end + 1) + ((index + key) // (end + 1)) * start

    if index + key < start:
        k = k + n

    return chr(k)


def encrypt(message, key):
    # 65-90 97-122
    nA, nZ, na, nz = ord('A'), ord('Z'), ord('a'), ord('z')
    encrypted = ''

    for character in message:
        index = ord(character)
        new_word = character

        if nA <= index <= nZ:
            new_word = replace(index, key, nA, nZ)

        elif index in range(na, nz + 1):
            new_word = replace(index, key, na, nz)

        encrypted = encrypted + new_word

    return encrypted


def decrypt(message, key):
    return encrypt(message, -key)


def encryptdoc(source, destination, key):
    file = open(source, 'r')
    content = file.read()
    file.close()

    encrypted = encrypt(content, key)

    file = open(destination, "w")
    file.write(encrypted)
    file.close()


def decryptdoc(source, destination, key):
    return encryptdoc(source, destination, -key)


key = 7

encryptdoc("message.txt", "message_encrypted.txt", key)
print("Message encrypted successfully!")

decryptdoc("message_encrypted.txt", "message_decrypted.txt", key)
print("Message decrypted successfully!")
