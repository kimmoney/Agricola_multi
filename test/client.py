import ctypes
import sys
from scapy.all import ARP, Ether, srp

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def scan_network(ip_range):
    # ARP 패킷 생성
    arp = ARP(pdst=ip_range)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether/arp

    # 패킷 전송 및 응답 수신
    result = srp(packet, timeout=2, verbose=False)[0]

    # 네트워크 내의 모든 활성 IP 주소 수집
    devices = []
    for sent, received in result:
        devices.append({'ip': received.psrc, 'mac': received.hwsrc})

    return devices

if __name__ == "__main__":
    if is_admin():
        ip_range = "192.168.1.0/24"  # 스캔할 IP 범위를 지정하세요
        devices = scan_network(ip_range)
        for device in devices:
            print(f"IP: {device['ip']}, MAC: {device['mac']}")
    else:
        # 관리자 권한 요청
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, __file__, None, 1)
