**Decrypt - 50 Points**

Summary: Cracking Chow's White-Box AES scheme

*In my opinion, the hardest of the teaser challenges.*

This is, much to my dismay, a reverse engineer puzzle, not a cryptography puzzle - although knowledge of AES certainly helps.

We're given a binary called `crypttool`, and some kind of ciphertext stored in `challenge.enc`.

From decompiling and running the binary, we can tell it's an implementation of AES CBC mode.

The first 16 bytes are the IV, and all further 16 byte blocks make up the plaintext.

I used Binary Ninja, but also a bit of Ghidra, and also a bit of Ida (this puzzle took a while).

From analysing the source code and comparing it to a [standard implementation of AES](https://github.com/kokke/tiny-AES-c/blob/master/aes.c), it does not look the same. This points to one of two options:

1. Insecurely implemented AES
2. White-Box AES

Linear and/or differential cryptanalysis combined with reverse engineering felt too cruel, so I assumed it was whitebox AES. Whitebox refers to when you have full access to its implementation. White-Box AES is intentionally designed to obfuscate the key, so that even with the source code you can't easily encrypt or decrypt whatever you want.

One of the most common White-Box AES schemes is [Chow et al's ](https://home.cs.colorado.edu/~jrblack/class/csci7000/s03/project/oorschot-whitebox.pdf). This has a common key-extraction attack called [BGE](https://link.springer.com/chapter/10.1007/978-3-540-30564-4_16). The maths is complicated, but fortunately you don't need to implement it from scratch.

We can confirm that our AES scheme is indeed Chow's by comparing it to an [existing implementation](https://github.com/balena/aes-whitebox).

This repo mentions that the scheme makes use of various lookup tables. Some of these lookup tables are constructed based on the key, while others are just constants. The first step is to extract these tables.

I won't go into too much detail here, but the gist is to look at the decompiled code, in particular the constants it references. They are massive. It's important to figure out which constant refers to which lookup table (the table has a handy chart which contains their sizes). Figuring out which size of AES is being used is left as an exercise to the reader 😁

Hint: be careful not to mix up big and little endian

From there, I cloned the repo mentioned above, and replaced the tables they generate with the tables I extracted. This was to compare the ciphertexts produced to confirm the tables were extracted correctly.

I then reimplemented it in Python so I could use the [bluegalaxyenergy](https://pypi.org/project/bluegalaxyenergy/) Pip module which implements the BGE attack.

This allows us to extract the key. From there, decryption is straightforward.

The Python files are a bit too long to include them in the writeup, but it's in this repo!

`aes_whitebox_tables.py` includes all the lookup tables.
`solve.py` implements the BGE attack and decrypts `challenge.enc`.

`Flag: Br34k1ng_Th3_W1t3B0x_M4tr1x`
