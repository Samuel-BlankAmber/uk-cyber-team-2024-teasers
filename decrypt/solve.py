from bluegalaxyenergy import WhiteBoxedAES, BGE
from aes_whitebox_tables import num_rounds, xor_table, tyboxes, mbl_table, tboxes_last_round
from Crypto.Cipher import AES

def ShiftRows(state):
    assert len(state) == 16
    shifts = [
        0,  5, 10, 15,
        4,  9, 14,  3,
        8, 13,  2,  7,
        12,  1,  6, 11,
    ]

    temp = [
        state[ 0], state[ 1], state[ 2], state[ 3],
        state[ 4], state[ 5], state[ 6], state[ 7],
        state[ 8], state[ 9], state[10], state[11],
        state[12], state[13], state[14], state[15],
    ]

    for i in range(16):
        state[i] = temp[shifts[i]]

class MyWhiteBoxedAES(WhiteBoxedAES):
    def isEncrypt(self):
        return True

    def getRoundNumber(self):
        return num_rounds

    def applyRound(self, data, roundN):
        new_data = bytearray(data)
        if roundN < 9:
            ShiftRows(new_data)
            for j in range(4):
                aa = tyboxes[roundN][j*4 + 0][new_data[j*4 + 0]]
                bb = tyboxes[roundN][j*4 + 1][new_data[j*4 + 1]]
                cc = tyboxes[roundN][j*4 + 2][new_data[j*4 + 2]]
                dd = tyboxes[roundN][j*4 + 3][new_data[j*4 + 3]]

                n0 = xor_table[roundN][j*24 +    0][(aa >> 28) & 0xf][(bb >> 28) & 0xf]
                n1 = xor_table[roundN][j*24 +    1][(cc >> 28) & 0xf][(dd >> 28) & 0xf]
                n2 = xor_table[roundN][j*24 +    2][(aa >> 24) & 0xf][(bb >> 24) & 0xf]
                n3 = xor_table[roundN][j*24 +    3][(cc >> 24) & 0xf][(dd >> 24) & 0xf]
                new_data[j*4 + 0] = (xor_table[roundN][j*24 + 4][n0][n1] << 4) | xor_table[roundN][j*24 + 5][n2][n3]

                n0 = xor_table[roundN][j*24 +    6][(aa >> 20) & 0xf][(bb >> 20) & 0xf]
                n1 = xor_table[roundN][j*24 +    7][(cc >> 20) & 0xf][(dd >> 20) & 0xf]
                n2 = xor_table[roundN][j*24 +    8][(aa >> 16) & 0xf][(bb >> 16) & 0xf]
                n3 = xor_table[roundN][j*24 +    9][(cc >> 16) & 0xf][(dd >> 16) & 0xf]
                new_data[j*4 + 1] = (xor_table[roundN][j*24 + 10][n0][n1] << 4) | xor_table[roundN][j*24 + 11][n2][n3]

                n0 = xor_table[roundN][j*24 + 12][(aa >> 12) & 0xf][(bb >> 12) & 0xf]
                n1 = xor_table[roundN][j*24 + 13][(cc >> 12) & 0xf][(dd >> 12) & 0xf]
                n2 = xor_table[roundN][j*24 + 14][(aa >>    8) & 0xf][(bb >>    8) & 0xf]
                n3 = xor_table[roundN][j*24 + 15][(cc >>    8) & 0xf][(dd >>    8) & 0xf]
                new_data[j*4 + 2] = (xor_table[roundN][j*24 + 16][n0][n1] << 4) | xor_table[roundN][j*24 + 17][n2][n3]

                n0 = xor_table[roundN][j*24 + 18][(aa >>    4) & 0xf][(bb >>    4) & 0xf]
                n1 = xor_table[roundN][j*24 + 19][(cc >>    4) & 0xf][(dd >>    4) & 0xf]
                n2 = xor_table[roundN][j*24 + 20][(aa >>    0) & 0xf][(bb >>    0) & 0xf]
                n3 = xor_table[roundN][j*24 + 21][(cc >>    0) & 0xf][(dd >>    0) & 0xf]
                new_data[j*4 + 3] = (xor_table[roundN][j*24 + 22][n0][n1] << 4) | xor_table[roundN][j*24 + 23][n2][n3]

                aa = mbl_table[roundN][j*4 + 0][new_data[j*4 + 0]]
                bb = mbl_table[roundN][j*4 + 1][new_data[j*4 + 1]]
                cc = mbl_table[roundN][j*4 + 2][new_data[j*4 + 2]]
                dd = mbl_table[roundN][j*4 + 3][new_data[j*4 + 3]]

                n0 = xor_table[roundN][j*24 +    0][(aa >> 28) & 0xf][(bb >> 28) & 0xf]
                n1 = xor_table[roundN][j*24 +    1][(cc >> 28) & 0xf][(dd >> 28) & 0xf]
                n2 = xor_table[roundN][j*24 +    2][(aa >> 24) & 0xf][(bb >> 24) & 0xf]
                n3 = xor_table[roundN][j*24 +    3][(cc >> 24) & 0xf][(dd >> 24) & 0xf]
                new_data[j*4 + 0] = (xor_table[roundN][j*24 + 4][n0][n1] << 4) | xor_table[roundN][j*24 + 5][n2][n3]

                n0 = xor_table[roundN][j*24 +    6][(aa >> 20) & 0xf][(bb >> 20) & 0xf]
                n1 = xor_table[roundN][j*24 +    7][(cc >> 20) & 0xf][(dd >> 20) & 0xf]
                n2 = xor_table[roundN][j*24 +    8][(aa >> 16) & 0xf][(bb >> 16) & 0xf]
                n3 = xor_table[roundN][j*24 +    9][(cc >> 16) & 0xf][(dd >> 16) & 0xf]
                new_data[j*4 + 1] = (xor_table[roundN][j*24 + 10][n0][n1] << 4) | xor_table[roundN][j*24 + 11][n2][n3]

                n0 = xor_table[roundN][j*24 + 12][(aa >> 12) & 0xf][(bb >> 12) & 0xf]
                n1 = xor_table[roundN][j*24 + 13][(cc >> 12) & 0xf][(dd >> 12) & 0xf]
                n2 = xor_table[roundN][j*24 + 14][(aa >>    8) & 0xf][(bb >>    8) & 0xf]
                n3 = xor_table[roundN][j*24 + 15][(cc >>    8) & 0xf][(dd >>    8) & 0xf]
                new_data[j*4 + 2] = (xor_table[roundN][j*24 + 16][n0][n1] << 4) | xor_table[roundN][j*24 + 17][n2][n3]

                n0 = xor_table[roundN][j*24 + 18][(aa >>    4) & 0xf][(bb >>    4) & 0xf]
                n1 = xor_table[roundN][j*24 + 19][(cc >>    4) & 0xf][(dd >>    4) & 0xf]
                n2 = xor_table[roundN][j*24 + 20][(aa >>    0) & 0xf][(bb >>    0) & 0xf]
                n3 = xor_table[roundN][j*24 + 21][(cc >>    0) & 0xf][(dd >>    0) & 0xf]
                new_data[j*4 + 3] = (xor_table[roundN][j*24 + 22][n0][n1] << 4) | xor_table[roundN][j*24 + 23][n2][n3]
        elif roundN == 9:
            ShiftRows(new_data)
            for i in range(16):
                new_data[i] = tboxes_last_round[i][new_data[i]]
        else:
            assert False
        return new_data

mywb = MyWhiteBoxedAES()

bge = BGE(mywb)
bge.run()

key = bge.computeKey()

if key is None:
    print("Key not found :(")
    exit()

cipher = AES.new(key, AES.MODE_ECB)

with open("challenge.enc", "rb") as f:
    data = f.read()

iv = data[:16]
ct = data[16:]

cipher = AES.new(key, AES.MODE_CBC, iv)
print(cipher.decrypt(ct).decode())
