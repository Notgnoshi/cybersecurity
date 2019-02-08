# Lab 1 Report

There are a few things worth mentioning about this report. First, the screenshots off the OpenSSL commands and their output have been put in an appendix in favor of an inline code block wherever possible. This is to reduce clutter, and hopefully produce a higher quality lab report. Second, I modified the `PS1` Bash variable to show the current working directory in color, but I did so incorrectly. The result is that some of the screenshots all show the same timestamp. I did not catch and fix this until roughly halfway through the lab. Finally, the take home portions of the lab have been incorporated into whichever in-class portion of the lab made sense.

## Symmetric-Key Encryption

This portion of the lab uses a 128-bit AES cipher with different block cipher chaining modes to highlight the differences between them. To make the commandline snippets less cluttered, I exported two Bash variables `AES_KEY` and `AES_IV` in a shell script.

```shell
$ cat keys.sh
#!/bin/bash

export AES_KEY="00112233445566778899aabbccddeeff"
export AES_IV="0102030405060708"
$ source keys.sh
$ echo $AES_KEY
00112233445566778899aabbccddeeff
$ echo $AES_IV
0102030405060708
```

lacking imagination, I chose the key and initial vector given in the lab write-up.

### Comparison of ECB and CBC Block Cipher Modes With Bitmap Images

First, I encrypted the given `pic_original.bmp` with AES-128 with ECB and CBC block cipher chaining modes.

```shell
$ openssl enc -aes-128-ecb -in pic_original.bmp -out pic-ecb.bmp -K $AES_KEY -iv $AES_IV
$ openssl enc -aes-128-cbc -in pic_original.bmp -out pic-cbc.bmp -K $AES_KEY -iv $AES_IV
```

Notice that I forgot the `-e` flag for the `openssl enc` command, but since it seems to have encrypted the image by default anyways, I chose not to redo this part of the lab.

Since we wish to view the encrypted data as if it were a valid bitmap image, we must copy the bitmap header from the unencrypted image to the encrypted ones. This was accomplished with the Bless hex editor.

```shell
$ file pic_original.bmp
pic_original.bmp: PC bitmap, Windows 3.x format, 460 x 134 x 24
$ # Before copying the bitmap header
$ file pic-ecb.bmp
pic-ecb.bmp: data
$ bless *.bmp &
$ # After copying the bitmap header
$ file pic-ecb-bmp
pic-ecb.bmp: PC bitmap, Windows 3.x format, 460 x 134 x 24
```

The results were surprising. The original image, shown below, contains simple shapes and colors.

![`pic_original.bmp`](figures/part1/pic_original.bmp)

I expected the encrypted images to be unrecognizable - because that is the intent of encryption. However, the image encrypted using ECB mode retained characteristics identifiable from the original image.

![`pic-ecb.bmp`](figures/part1/pic-ecb.bmp)

The ECB-encrypted image retains characteristics of the original image because each block is encrypted independently. This means that any common blocks of plaintext will have identical blocks of ciphertext, which results in visually identifiable patterns in the encrypted image. Notice that each chunk of uniform color in the original image results in a uniform chunk of ciphertext in the encrypted image. While it would be difficult to deduce information about the color of the shapes from the ciphertext, it is a simple matter to find the shape boundaries.

Note also that the boundaries between the shapes and the white background are fuzzy, but in a periodic manner. This is because the block size is not necessarily evenly divisible by the size of each pixel in the binary file. This results in the staggered effect seen above.

However, the image encrypted with CBC mode looks as expected.

![`pic-cbc.bmp`](figures/part1/pic-cbc.bmp)

The CBC-encrypted image displays no visually recognizable similarities to the original file. This is because CBC XORs the next block of plaintext to be encrypted with the previous block of ciphertext. This means that a sequence of identical blocks of plaintext will *not* have a sequence of identical blocks of ciphertext, because each ciphertext block depends on different information.

### Comparison of ECB, CBC, CFB, and OFB Block Cipher Modes With Corrupted Ciphertext

The given `plain1.txt` file was encrypted using the AES-128 cipher in the ECB, CBC, CFB, and OFB block cipher modes. After encrypting the file, the 30th byte of the ciphertext was intentionally corrupted before decrypting each ciphertext.

```shell
$ openssl enc -aes-128-ecb -in plain1.txt -out cipher1-ecb.txt -K $AES_KEY -iv $AES_IV
$ openssl enc -aes-128-cbc -in plain1.txt -out cipher1-cbc.txt -K $AES_KEY -iv $AES_IV
```

It was at this point I realized that I was missing the `-e` flag to encrypt the given files. Leaving the `-e` flag off does not appear to affect the `openssl enc` command.

```shell
$ openssl enc -aes-128-cfb -in plain1.txt -out cipher1-cfb -K $AES_KEY -iv $AES_IV
$ openssl enc -aes-128-ofb -in plain1.txt -out cipher1-ofb -K $AES_KEY -iv $AES_IV
```

Note that I forgot the `.txt` extension, which, while not required, makes globbing easier.

```shell
$ mv cipher1-cfb cipher1-cfb.txt
$ mv cipher1-ofb cipher1-ofb.txt
```

Then the 30th byte (at offset `0x1e` in the hex editor) was replaced with `0x42` in all four ciphertexts.

```shell
$ bless cipher1-*.txt &
```

After corrupting the ciphertext, all four were decrypted.

```shell
$ openssl enc -aes-128-ecb -d -in cipher1-ecb.txt -out plain1-ecb.txt -K $AES_KEY -iv $AES_IV
$ openssl enc -aes-128-cbc -d -in cipher1-cbc.txt -out plain1-cbc.txt -K $AES_KEY -iv $AES_IV
$ openssl enc -aes-128-cfb -d -in cipher1-cfb.txt -out plain1-cfb.txt -K $AES_KEY -iv $AES_IV
$ openssl enc -aes-128-ofb -d -in cipher1-ofb.txt -out plain1-ofb.txt -K $AES_KEY -iv $AES_IV
```

Then a hexdump of each of the decrypted plaintexts were `diff`ed against the original plaintext.

```shell
$ colordiff -y <(xxd plain1-ecb.txt) <(xxd plain1.txt)
$ colordiff -y <(xxd plain1-cbc.txt) <(xxd plain1.txt)
$ colordiff -y <(xxd plain1-cfb.txt) <(xxd plain1.txt)
$ colordiff -y <(xxd plain1-ofb.txt) <(xxd plain1.txt)
```

The output of the `colordiff` commands above is shown below

![The ECB and CBC mode corrupted plaintexts compared to the original](figures/part1/1.2-decrypted-ecb-cbc-diff.png)

![The CFB and OFB mode corrupted plaintexts compared to the original](figures/part1/1.2-decrypted-cfb-ofb-diff.png)

Unfortunately, I have not found a commandline `diff` program that shows a word diff, so all `colordiff` shows is which lines of the hexdumps differ, and not what byte(s).

The two differing lines of the hexdump for the ECB mode results are shown below to illustrate that none of the bytes are the same.

```text
00000010: 632a a2b8 0a12 5398 a3f5 ce33 6e20 c80b  c*....S....3n ..
00000010: 7374 2061 2062 6967 2077 6f72 6420 7468  st a big word th
```

This means that one *byte* of corrupted plaintext resulted in an unrecoverable corruption of an entire 16 byte *block* of the decrypted plaintext. This makes sense. The AES cipher is a block cipher that abides by the principles of confusion and diffusion. So a single differing bit (much more an entire byte) in the input will result in *many* differing bits in the output. Because this first example is using the ECB block cipher mode, the corruption is limited to a single block, because each block is encrypted independently of the others.

The difference in the hexdumps for the CBC results are more interesting.

```text
00000010: 212f e3e9 c66c 409a e131 02cf c018 3232  !/...l@..1....22
00000010: 7374 2061 2062 6967 2077 6f72 6420 7468  st a big word th
```

and

```text
00000020: 726f 776e 2061 726f 756e 6420 620c 2073  rown around b. s
00000020: 726f 776e 2061 726f 756e 6420 6279 2073  rown around by s
```

Notice that, again, the entire 16 byte block containing the 30th byte was corrupted in the decrypted plaintext. But also notice that a single byte in the next 16 byte block was corrupted as well. This is far more interesting, and is a consequence of the CBC cipher mode XORing the plaintext with the preceding block of ciphertext. This means that a corrupted block of input will end up corrupting two blocks of output. Also notice that the location of the corrupted byte in the third 16 byte block of the decrypted plaintext is precisely the location of the corrupted byte in the corrupted plaintext!

The results for the CFB mode are quite similar, except a single byte corruption in an input block results in a single byte corruption in the corresponding output block, and corruption of the *entire* subsequent block. This is because the CFB XORs the plaintext with the preceding ciphertext. So since the ciphertext preceding the corruption was intact, there was only one resulting byte of corruption in the corresponding output block. But since a single byte change in the plaintext results in many bytes of change in the ciphertext, XORing the corrupted ciphertext with the next block of plaintext corrupts the entire block.

Notice that the OFB cipher mode is most resistant to corruption, as there was only a single differing byte in the decrypted plaintext. In the OFB cipher mode, each key is dependent on the preceding one, and the ciphertext is obtained simply by XORing the plaintext with the next key in the stream, so as long as the initial vector is correctly known, the entire corrupted plaintext is reconstructible.

## Hash Functions

### Computing Hashes of a File

I computed the MD5 and SHA-256 hashes of the `plain1.txt` and `plain2.txt` files.

```shell
$ openssl dgst -md5 -out plain1-md5.txt plain1.txt
$ openssl dgst -sha256 -out plain1-sha256.txt plain1.txt
$ openssl dgst -md5 -out plain2-md5.txt plain2.txt
$ openssl dgst -sha256 -out plain2-sha256.txt plain2.txt
$ cat plain1-md5.txt
MD5(plain1.txt)= 25f1218e13006dc220fb9dd239c465f8
$ cat plain2-md5.txt
MD5(plain2.txt)= ad17a23d19b55b93f65dfaf064478d50
$ cat plain1-sha256.txt
SHA256(plain1.txt)= 4b553ab690f3d84e7d3e206507ebe7a8658a0169a19adddcafd01b033d90b449
$ cat plain2-sha256.txt
SHA256(plain2.txt)= 06acc34746028e55783cfbdb9dabf4c5435756d3b2c5250fc714e3f2508e8015
```

There are a few things to notice about the generated hashes. Note that the `plain1.txt` and `plain2.txt` files are of different length, but their hashes are the same size, regardless of the algorithm used. This is a key feature of hash code algorithms; the generated hashes are all the same size. The length of the hash code depends only on the algorithm used to generate it. Also, note that the hashes of the same file with two different algorithms vary wildly. This has the implication that if you provide a hash for verification purposes, you must also somehow indicate the hash code algorithm used to generate it, so that another person can verify the given hash.

To my satisfaction, the above hashes are identical to those given by the usual `md5sum` and `sha256sum` commandline programs.

```shell
$ md5sum plain1.txt
25f1218e13006dc220fb9dd239c465f8  plain1.txt
$ md5sum plain2.txt
ad17a23d19b55b93f65dfaf064478d50  plain2.txt
$ sha256sum plain1.txt
4b553ab690f3d84e7d3e206507ebe7a8658a0169a19adddcafd01b033d90b449  plain1.txt
$ sha256sum plain2.txt
06acc34746028e55783cfbdb9dabf4c5435756d3b2c5250fc714e3f2508e8015  plain2.txt
```

### Hashes of a File With One Differing Bit

I then corrupted the 30th byte (`0x74`) of the `plain1.txt` file by replacing it with `0x7c` and generated its hash again. `0x74` and `0x7c` differ only in the fourth bit.

```shell
$ cp plain1.txt corrupted1.txt
$ # Replace the 30th byte with 0x42
$ bless corrupted1.txt &
$ openssl dgst -md5 -out corrupted1-md5.txt corrupted1.txt
$ openssl dgst -sha256 -out corrupted1-sha256.txt corrupted1.txt
$ cat corrupted1-md5.txt
MD5(corrupted1.txt)= c395815029f4d9d3aa1c36fc742046ae
$ cat corrupted1-sha256.txt
SHA256(corrupted1.txt)= 87ed3c2c3668ee4af0005a7d8225bbd42b04da9dea6b8304e3714449bd90c40b
$ colordiff <(cut -f2 -d' ' corrupted1-md5.txt) <(cut -f2 -d' ' plain1-md5.txt)
$ colordiff <(cut -f2 -d' ' corrupted1-sha256.txt) <(cut -f2 -d' ' plain1-sha256.txt)
```

The difference in the hashes of the corrupted and original hashes are shown below for both the MD5 and SHA-256 hash code algorithms.

![The difference in the MD5 hashes](figures/part2/4.2-diff-md5.png)

![The difference in the SHA-256 hashes](figures/part2/4.2-diff-sha256.png)

Notice that in the MD5 hashes, there are *no* bytes in common. This is another feature essential to hash code algorithms; that a small difference in inputs gives a large difference in outputs. This prevents a form of attack where a document can be produced with the same hash as some other document. By following the diffusion and confusion principles, it becomes *much* harder to reverse engineer replacement documents.

Interestingly, the SHA-256 hashes *do* have a byte and a half in common near the end of the hash code. However, there are no more common bytes, so I think this might have just been a fluke.

### Signed Hashes

I computed the signed MD5 hash using the `-hmac` option for the `openssl dgst` command. I experimented with several key lengths, and found that the length was not limited.

![The signed MD5 command output](figures/part2/2.2-hmac-md5.png)

When I signed the SHA-256 hash code, I even thought to try the empty string as a key.

![The signed SHA-256 command output](figures/part2/2.2-hmac-sha256.png)

With both hashes, I did not find a key length limit, and saw that the signed hash with each key differed greatly, even against the unsigned hash code. According to Wikipedia, if the key is too large, the HMAC algorithm reduces the size of the key by hashing it, and then right pads with zeros up to the block size. If the key is too small to begin with, the HMAC algorithm right pads it with zeros until it is of the same size as the block size.

## Public-Key Encryption

I generated a public and private key pair with OpenSSL as follows.

```shell
$ openssl genrsa -out private.pem 1024
..........................++++++
....++++++
e is 65537 (0x10001)
$ cat private.pem
-----BEGIN RSA PRIVATE KEY-----
MIICXAIBAAKBgQCmREQEDo1p0Ft2myb0RBpuQcOgiy/FAUwtch3ugLI4uk69grES
4Ir7Pszy31+4mXjG5gMyXDQW3kBxFKALLCXdYEUkwEjlua5N2TwY1/W08bJ+7X08
UtheKd22spDFrthdOccj48HMlFFA5N2ORo1qZFSfV64L05eI2VRySmnIDQIDAQAB
AoGAdyo4QVwYuH0QAKrkuW9SLjHOPvNjEmSCr5O5piXxFj1Zj/Pqa6gplDcHdw7n
sQu2B3/1TJPO9ZDnSOTKbBeBLsgv+ofuniVtAzHZAFEIya2beReBoypC01VA3hpW
xwLtdU3BOGgOVb/3mvLf+L4ix50h3iMzfYIWUKRZCmq335UCQQDTFcT0ksYdVp5C
VxcbYECYL+AYOneamoHlDnLRLBFIcBymRj5xqh7JE3aRmeOcRZbp/fJOc6rpEkzc
gfyETc8XAkEAyaUmA3Xdk4HGMSqBqE2bQDWv/YRq4/lPdS3GTq+yd4HfS3+ZJxVM
V9v7ZV7HJEehmTB6ymDyET6wVCsUxH/4ewJAVQOwhnxStGA9bySaVtlGSsUFcVyi
7S6LYFCYZ6xi7ZTRxRoHbkoBCiT/nRaouDjC1k0D+RrW2/YV5L2pkTOxUwJANHZ2
VHInCwi5ovMXNs2yNduCBWidUuD7jlYxgSlvOm6cxQzWsPd2nGlMmAw3rbXBUpTt
bZgZgukXgV6QEavl3wJBAIEVj4O2Od4OUe3Mt57crShQE1i0zxzicKnfYT2pJjxf
nDjJ+EfonvDMSuwMDC3GRieKWz9Hslh/r++IkOKeffQ=
-----END RSA PRIVATE KEY-----
$ openssl rsa -in private.pem -pubout -out public.pem
writing RSA key
$ cat public.pem
-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCmREQEDo1p0Ft2myb0RBpuQcOg
iy/FAUwtch3ugLI4uk69grES4Ir7Pszy31+4mXjG5gMyXDQW3kBxFKALLCXdYEUk
wEjlua5N2TwY1/W08bJ+7X08UtheKd22spDFrthdOccj48HMlFFA5N2ORo1qZFSf
V64L05eI2VRySmnIDQIDAQAB
-----END PUBLIC KEY-----
```

Then I signed the `plain1.txt` file

```shell
$ openssl dgst -sha256 -sign private.pem -out plain1=signed-sha256.txt plain1.txt
$ cat plain1-signed-sha256.
iK;D\eXR¶g:Þqw8ºÈÿ±µ9»ë Bô,âßÏÿABØ"ZôœN\]¶úUÛ9¬ÉHÞò:1¿^:iR_H=kã8]äñtŽ3åS)"Ø%ú57ŠêK¿^}úHm"-«Ó!Ý¢zÏS
```

And verified that the `plain1.txt` file is, in fact, the file that I signed.

```shell
$ openssl dgst -sha256 -verify public.pem -signature plain1-signed-sha256.txt plain1.txt
gned-sha256.txt plain1.txt
Verified OK
```

![The verification](figures/part3/3.2-verification.png)

## Appendix A - Screenshots

### Symmetric-Key Encryption

![The AES key and initial vector](figures/part1/1.1-keys.png)

#### Comparison of ECB and CBC Block Cipher Modes with Bitmap Images

![Encryption of the image with AES-128-ECB](figures/part1/1.1-encrypt-bmp-ecb.png)

![Encryption of the image with AES-128-CBC](figures/part1/1.1-encrypt-bmp-cbc.png)

![The BMP header for `pic_original.bmp`](figures/part1/1.1-original-bmp-header.png)

![The copied header for `pic-ecb.bmp`](figures/part1/1.1-ecb-bmp-header.png)

![The copied header for `pic-cbc.bmp`](figures/part1/1.1-cbc-bmp-header.png)

#### Comparison of ECB, CBC, CFB, and OFB Block Cipher Modes with Corrupted Ciphertext

![Encryption of the `plain1.txt` file with ECB cipher mode](figures/part1/1.2-encrypt-ecb.png)

![Encryption of the `plain1.txt` file with CBC cipher mode](figures/part1/1.2-encrypt-cbc.png)

![Encryption of the `plain1.txt` file with CFB cipher mode](figures/part1/1.2-encrypt-cfb.png)

I forgot to take a screenshot of the encryption of the `cipher1-ofb.txt` file.

![Adding the `.txt` extension ot the CFB and OFB files](figures/part1/1.2-rename-txt.png)

![The corrupted byte in the ECB plaintext file](figures/part1/1.2-ecb-corrupted.png)

![The corrupted byte in the CBC plaintext file](figures/part1/1.2-cbc-corrupted.png)

![The corrupted byte in the CFB plaintext file](figures/part1/1.2-corrupted-cfb.png)

![The corrupted byte in the OFB plaintext file](figures/part1/1.2-corrupted-ofb.png)

![Decrypting the ECB ciphertext](figures/part1/1.2-decrypt-ecb.png)

![Decrypting the CBC ciphertext](figures/part1/1.2-decrypt-cbc.png)

![Decrypting the CFB and OFB ciphertext](figures/part1/1.2-decryption-cfb-ofb.png)

### Hash Functions

#### Computing Hashes of a File

![Computing the MD5 hash of `plain1.txt`](figures/part2/2.1-plain1-md5.png)

![Computing the MD5 hash of `plain2.txt`](figures/part2/2.1-plain2-md5.png)

![Computing the SHA-256 hash of `plain1.txt`](figures/part2/2.1-plain1-sha256.png)

![Computing the SHA-256 hash of `plain2.txt`](figures/part2/2.1-plain2-sha256.png)

![Comparing the different hash codes](figures/part2/2.1-hash-comparison.png)

![Comparing the hashes against the linux hash commands](figures/part2/2.1-linux-utils.png)

#### Hashes of a File With One Differing Bit

![The corrupted bit in the hex editor](figures/part2/4.2-corrupted.png)

![Computing the hashes of the corrupted file](figures/part2/4.2-hash-commands.png)

### Public-Key Encryption

![The private key generation](figures/part3/3.1-private.png)

![The public key generation](figures/part3/3.1-public.png)

![The signed hash](figures/part3/3.2-signed-hash.png)

![The verification of the `plain1.txt` file](figures/part3/3.2-verification.png)
