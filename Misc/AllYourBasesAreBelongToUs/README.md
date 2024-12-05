# All Your Bases Are Belong To Us

## Analysis

This problem gives us an [encoded message](./message.txt) along with the hint:

````
Base 32? Sure.
Base 64? Yeah I know that one.
Base 2^16? ?????????
````

## Solution

The first step is to find that 2ˆ16 is 65536 and, given the hint, the decoding will likely involve `Base65536`. Using an [online decoder for `Base65536`](https://www.better-converter.com/Encoders-Decoders/Base65536-Decode) does not give us a useful result right away, so more steps are required.

Putting the message through [CyberChef](https://gchq.github.io/CyberChef/) using the `Magic` recipe shows us that the message is `Base64` encoded. Repeating the process for the newly decoded message suggests that the message is `Base58` encoded. Once again, it suggests that the message is `Base32` encoded. And one more time, that the message is `Base85` encoded, which finally gives us:

```
𔕷𠅦𖥣桢顲桨鑦敤𓅥𓉮鵟𔐴鐳ꌴ鑬鵴鐳𐘴𔕳𓀳鑳𔔴敧栴鬲ᕽ
```

Although it doesn't look like much, all these characters are valid UTF-8 characters and, therefore, can be decoded in `Base65536`. Passing these values to the decoder gives us:

```
wwf{cyb3rch3f_d0esnt_h4v3_4ll_th3_4nsw3rs_4wg0432f}
```