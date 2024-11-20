from scapy.all import rdpcap, Raw
from scapy.layers.usb import USBpcap
import wave

packets = rdpcap("challenge.pcap")

all_iso_data = []
for j, packet in enumerate(packets, start=1):
    if Raw in packet:
        if packet[USBpcap].transfer == 0 and packet[USBpcap].info == 0:
            num_data = packet[USBpcap].dataLength // 192
            iso_data = [packet[Raw].load[num_data*10:][i*192:i*192+192] for i in range(num_data)]
            assert all(len(data) == 192 for data in iso_data)
            all_iso_data.extend(iso_data)

iso_data = b"".join(all_iso_data)

sample_rate = 32000
n_samples = len(iso_data) // 128
n_frames = n_samples
n_channels = 2
sampwidth = 3

wav_file = wave.open("reconstruct.wav", "w")
wav_file.setparams((n_channels, sampwidth, sample_rate, n_frames, "NONE", "not compressed"))

wav_file.writeframes(iso_data)
wav_file.close()
