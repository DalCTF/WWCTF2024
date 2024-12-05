# Too Hidden

## Analysis

The problem provides us with a [.pcap file](./chall.pcapng) for analysis. It expects us to find a flag hidden in it.

## Solution

The flag is not directly accessible in the `.pcap`. The only thing available is a trace of `echo` requests from one host to the server. The only difference between each one of the requests is a single bit at the end of the data section. 

If we compile all of these bits from the packets in order, we get the following message:

```
FEE2FEE2FFEF22FFFF2EEE2FEFF2EFEE2FFEEFE2FFF2FFFF2F2F2F2F2E2FFEEFE2EFEE2EEE2FFE2FFEEFE2EFEF2FE2EF2FFEEFE2FFEF2FF2EF2EFF2FFEEFE2EE2F2FFEEFE2FFEEFF2FFEEFF2FFEEFF2FFEEFF2FFEEFF2FFEEFF2FFEEFF2FFEEFF2FFEEFF2FFEEFF2
```

The sequence is too well-behaved not to mean something. A little bit of trial and error leads us to the conclusion that the character `2` is a separator, and that the message is encoded in morse, where the character `F` represents dots (`.`) and the character `E` represents dashes (`_`). The decoded message is then presented:

```
WWFHOLY_SHEEEET_YOU_CAN_FIND_ME_??????????
```

By formatting this according to the flag format given in the problem description ("Flag is case insensitive, but follow the format `wwf{fl46_f0rm47}`"), we have:

```
wwf{HOLY_SHEEEET_YOU_CAN_FIND_ME_??????????}
```