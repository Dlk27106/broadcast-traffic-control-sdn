# 📡 Broadcast Traffic Control using SDN
### Computer Networks - UE24CS252B | PES University

---

## 📌 Overview

This project implements a **Software Defined Networking (SDN)** solution to detect and control excessive broadcast traffic in a virtual network. The POX SDN controller monitors incoming broadcast packets on a Mininet-emulated network and automatically installs OpenFlow flow rules to block flooding once a defined threshold is exceeded.

Broadcast storms can severely degrade network performance. This project demonstrates how SDN can proactively handle such issues through centralized control and dynamic flow rule installation.

---

## 🎯 Objectives

- Detect broadcast packets (`dl_dst = ff:ff:ff:ff:ff:ff`) in real time
- Count broadcast packets per switch
- Install a high-priority OpenFlow **drop rule** once the threshold is hit
- Evaluate network performance before and after the rule is applied
- Demonstrate SDN's ability to enforce traffic policies dynamically

---

## 🖧 Network Topology

```
    h1      h2      h3      h4
     \       |       |      /
      \      |       |     /
            [s1]
              |
           [POX Controller]
           127.0.0.1:6633
```

| Component | Details |
|-----------|---------|
| Switch | s1 (Open vSwitch) |
| Hosts | h1, h2, h3, h4 |
| Controller | POX (Remote) at 127.0.0.1:6633 |
| Topology Type | Single switch, star topology |

---

## 🛠️ Technologies Used

| Tool | Purpose |
|------|---------|
| **Mininet** | Network emulation |
| **POX Controller** | SDN controller (Python-based) |
| **OpenFlow 1.0** | Flow rule protocol |
| **Open vSwitch (OVS)** | Virtual switch |
| **Ubuntu (Linux VM)** | Host environment |

---

## ⚙️ How to Run

### Prerequisites
- Ubuntu 20.04 / 22.04
- Mininet installed (`sudo apt install mininet -y`)
- POX controller cloned (`git clone https://github.com/noxrepo/pox`)

---

### Step 1: Start the POX Controller
```bash
cd ~/pox
./pox.py broadcast_control
```

Expected output:
```
INFO:core:POX 0.7.0 (gar) is up.
INFO:openflow.of_01:[00-00-00-00-00-01 1] connected
INFO:broadcast_control:Broadcast packet count=1
INFO:broadcast_control:Broadcast packet count=2
INFO:broadcast_control:Broadcast packet count=3
INFO:broadcast_control:🚫 Blocking ALL broadcast traffic
```

---

### Step 2: Start Mininet (in a new terminal)
```bash
sudo mn --topo single,4 --controller remote
```

Expected output:
```
*** Adding hosts: h1 h2 h3 h4
*** Adding switches: s1
*** Adding links: (h1,s1) (h2,s1) (h3,s1) (h4,s1)
*** Starting controller c0
*** Starting 1 switches s1
*** Starting CLI
```

---

### Step 3: Test Connectivity
Inside the Mininet CLI:
```bash
h1 ping h2
h1 ping h3
h1 ping h4
```

---

### Step 4: Run Throughput Test
```bash
h1 iperf -s &
h2 iperf -c 10.0.0.1
```

---

### Step 5: Check Flow Rules
In a separate terminal:
```bash
sudo ovs-ofctl dump-flows s1
```

---

## 📊 Results

### Ping Test Results

| Source | Destination | Result | Avg RTT |
|--------|------------|--------|---------|
| h1 | h2 | ✅ 0% packet loss | 3.250 ms |
| h1 | h3 | ✅ 0% packet loss | 2.608 ms |
| h1 | h4 | ❌ Blocked (100% loss) | — |

> h4 is unreachable because ARP (which uses broadcast) is blocked after the threshold is hit, preventing address resolution.

---

### Throughput (iperf)

| Metric | Value |
|--------|-------|
| Transfer | 81.9 MBytes |
| Duration | 10.33 seconds |
| **Bandwidth** | **66.5 Mbits/sec** |
| TCP Window Size | 85.3 KByte |

---

### Flow Table (ovs-ofctl dump-flows s1)

**Before threshold hit:** No flow rules installed.

**After threshold hit:**
```
cookie=0x0, duration=79.243s, table=0, n_packets=9,
n_bytes=378, priority=100,
dl_dst=ff:ff:ff:ff:ff:ff actions=drop
```

| Field | Value |
|-------|-------|
| Priority | 100 |
| Match | dl_dst = ff:ff:ff:ff:ff:ff |
| Action | DROP |
| Packets matched | 9 |
| Bytes dropped | 378 |

---

## 🧠 Controller Logic (broadcast_control.py)

```
1. Register for PacketIn events
2. Parse each incoming packet
3. Check if destination MAC = ff:ff:ff:ff:ff:ff (broadcast)
4. Increment broadcast counter for that switch
5. If counter >= THRESHOLD:
      → Build OpenFlow FlowMod message
      → Match: dl_dst = ff:ff:ff:ff:ff:ff
      → Action: DROP
      → Priority: 100
      → Install rule on switch
6. Log all events to console
```

---

## 📁 Project Structure

```
broadcast-traffic-control-sdn/
│
├── broadcast_control.py     # POX controller logic
├── topology.py              # Custom Mininet topology (if any)
├── README.md                # Project documentation
│
└── screenshots/
    ├── topology_launch.png       # Mininet topology startup
    ├── controller_output.png     # POX controller logs
    ├── ping_test.png             # Ping results (h1→h2, h1→h3, h1→h4)
    ├── iperf_result.png          # Throughput test
    └── dump_flows.png            # OVS flow table
```

---

## 📋 Evaluation Coverage

| Criteria | Status |
|----------|--------|
| Problem Understanding & Setup | ✅ |
| SDN Logic & Flow Rule Implementation | ✅ |
| Functional Correctness (Demo) | ✅ |
| Performance Observation (ping + iperf) | ✅ |
| Explanation & Validation | ✅ |

---

## 📚 References

- [Mininet Official Site](https://mininet.org)
- [POX Controller Documentation](https://github.com/noxrepo/pox)
- [OpenFlow 1.0 Specification](https://opennetworking.org)
- [Open vSwitch Documentation](https://www.openvswitch.org)
- Mininet Installation Guide - UE24CS252B Lab Manual, PES University
