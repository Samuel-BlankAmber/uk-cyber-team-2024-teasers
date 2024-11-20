**Reconstruct - 50 Points**

Summary: Reconstruct USBPcap audio data

We're given a pcap file containing USBPcap data. As the title suggests, we must *reconstruct* the original audio data.

To do this, we first need to grab all the isochronous USB data. I do this using `scapy` in my solve script, but I'm sure there's faster alternatives using `tshark` etc.

[This is a useful document for learning about USB audio data.](https://www.silabs.com/documents/public/application-notes/AN295.pdf)

Then we can use Python's `wave` module to construct a `wav` file from data.

If you listen to it you can vaguely make out a TTS voice, but also a ton of static.

Throwing it into Audacity, we can see that the left channel is purely static, while the right channel is the TTS.

You can split the stereo track then delete the left channel to isolate the right channel.

This is the flag, although it's a little hard to tell what exactly the format is or what exactly the TTS is saying.

Some ideas:
```
do wiresharks dream of digital sounds?
do wiresharks dream of digital cells?
do wire sharks dream of digital sounds?
do wire sharks dream of digital cells?
```

And of course, all of the above except no question mark, or perhaps underscores instead of spaces, or leetspeak. The puzzle gets a bit guessy at this point, but here's the thought process I had to ensure 100% hit rate:

`digital sounds` *makes more sense* than `digital cells`. You can mess around with the audio properties a bit and `sounds` may become a little more apparent.

I didn't deduce the exact TTS voice used (although some did), but a TTS voice would interpret numbers literally, so that rules out leetspeak.

The underscores are a bit more ambiguous since all of the other teaser flags contained underscores, but I decided to approach it from the angle of *what did the author type into the TTS?* Realistically if it contained underscores or other *inaudible data* (like question marks) then the puzzle would be even more guessy. Therefore, I made the assumption to take everything at face value and not add in any extra data I cannot hear.

Now we have one of two options:
```
do wiresharks dream of digital sounds
do wire sharks dream of digital sounds
```

Spaces are *kind of* audible data. In this case, it's quite ambiguous. I compared TTS samples of "wiresharks" and "wire sharks" and stared at the waveforms for a long time. Honestly, it didn't help that much.

I tried doing OSINT to see if this was a joke stolen from somewhere, but I couldn't find it. However, Wireshark, the tool, is singular. The joke is also referring to *sharks* as an animal, independent from the tool.

The correct flag is `do wire sharks dream of digital sounds`

It's guessy but it can be (somewhat) logically deduced.
