# Agricola - Multi Play

# 개요

[Agricola - 4Player in 1PC](https://www.notion.so/Agricola-4Player-in-1PC-e083cdc5cb554d39a879bba34362148e?pvs=21) 에서는 1PC에서 4명의 플레이가 가능했다. 이 프로세스에서는 다양한 한계를 가지게 되었다. 

1. 플레이어의 직업, 보조, 주요 카드를 상대에게 공개하지 않기 위하여 휴대전화 사진 촬영 등 방법을 활용해야 한다. 
2. 모든 플레이어의 정보를 화면에 동일하게 노출해야하기 때문에 개인 전술을 준비하는데 어려움이 있다. 
3. 화면 전환, 화면 규제 등 프로세스가 복잡하여 오류 발생 가능성을 높인다.
4. 한개의 하드웨어를 공유하기에 많은 불편함이 있음

이러한 문제점을 해결하기 위하여 통신을 기반으로 한 플레이를 진행하고자 한다.

통신 방식은 총 세가지로 Socket, Server-relay, Server-Client를 기반으로 개발을 하고자 한다. 

Socket, Server-relay 두 방식 모두 1 Server Process와 4 Client Process가 존재하는데 4명의 플레이어 중 1명의 플레이어가 Host권을 가지게 된다. 모든 플레이어는 Client Process를 통해 게임을 진행하고 Host Player의 Server Process에서 데이터를 처리하게 된다.  

다만 Server-Client 에서는 Server Hardware에서 데이터를 처리하게 된다.

세 통신 방식의 차이는 다음과 같다.

## Socket

Socket 통신은 같은 네트워크에 있는 PC간의 로컬 네트워크 통신을 기반으로 한다. 
4명의 플레이어 중 게임방을 개설한 player가 Host Player가 되고, Host Player는 Server Client도 실행한다. Nomal Player들은 Server Client의 IP와 Port에 접근하여 이벤트를 전달하하고, Sever Client에서 데이터를 처리하게 된다. 

> Nomal Client → Server Client(Player) → Normal Client
> 

Plyaer의 HardWare에서 데이터를 처리하기에 게임 진행 속도가 Player Hardware에 의존한다는 단점이 있다. 

## Server

Server 기반 통신은 다른 네트워크에 있는 PC간 통신도 가능하게 해준다. 

서로 다른 네트워크에 연결되어있는 경우 Host Player의 공인 ip를 통해 Server Client에 접근해야한다. 하지만 대부분의 환경에서는 공인 ip를 직접 연결하지 않고 공유기의  DHCP 서버를 이용한다. 이런 경우 Server Client의 IP, Port에 접근하기 위해서는 공유기단에서 Port-Fowarding을 해줘야 한다. 하지만 이는 네트워크 지식이 충분하지 않은 사용자들에게는 매우 어려운 일이다. 또한 공유기의 방화벽을 수정하는 일은 보안상으로도 취약할 수 있기때문에 매우 조심스러운 일이다. 

따라서 Player들의 하드웨어를 제외한 Server-Hardware가 개입하게 된다. 
이때 Server는 두가지의 역할로 구분할 수 있다. 

### relay

기본적으로 [Socket](https://www.notion.so/Socket-6a0f1739e41f42f7bab87dedeb1139ae?pvs=21) 의 구조를 그대로 사용하게 된다. 다만 relay Server에서 Server Client와 Nomal Client간의 통신을 중계해준다는 차이점이 있다.

> Nomal Client → relay Server → Server Client → relay Server→ Normal Client
> 

Normal Client 와 Server Client간의 데이터 이동을 그대로 할 수 있기 때문에 [Socket](https://www.notion.so/Socket-6a0f1739e41f42f7bab87dedeb1139ae?pvs=21) 의 모든 프로세스를 그대로 사용할 수 있다. 또한 relay Server에서의 프로세싱은 단순 정보 이동으로 높은 수준의 Hardware 성능을 요구하지 않는다. 따라서 relay Server의 구축 비용 또한 크지 않을 것으로 생각된다. 
Linux 기반의 Raspberry Pi 만으로도 충분할 것으로 생각된다.

### Client

기본적으로 [Socket](https://www.notion.so/Socket-6a0f1739e41f42f7bab87dedeb1139ae?pvs=21) 와 [relay](https://www.notion.so/relay-6db299c9244e47efbece718bd03ba1c7?pvs=21) 의 결합으로 생각할 수 있다. 
플레이어 외 Server Hardware에 Server Client를 구성하는 방법이다. 모든 데이터 처리를 Server Hardware에서 진행한다.

> Nomal Client → Server Client(Server) → Normal Client
> 

이 방식은 의도하지 않은 사용자의 Cheeting을 방지할 수 있으며 Player Hardware의 의존성 문제를 해결하며 모든 플레이어의 하드웨어 최소 요구사항을 낮출 수 있다. 
다만 많은 게임이 진행되면 Srever Hardware에 높은 성능을 요구하게 될 것이다.

## In Same Network - Socket

Nomal Client → Server Client(Player) → Normal Client

---

## In Diffrent Network - Server(relay)

Nomal Client → relay Server → Server Client → relay Server→ Normal Client

---

## In Diffrent Network - Server(Client)

Nomal Client → Server Client(Server) → Normal Client

---

# 세부사항

https://github.com/kimmoney/Agricola_multi