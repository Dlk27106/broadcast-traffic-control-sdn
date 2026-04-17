from pox.core import core
import pox.openflow.libopenflow_01 as of

log = core.getLogger()

broadcast_total = 0
THRESHOLD = 3
IDLE_TIMEOUT = 30
HARD_TIMEOUT = 60

def _handle_PacketIn(event):
    global broadcast_total
    packet = event.parsed
    src = str(packet.src)
    dst = str(packet.dst)

    if dst == "ff:ff:ff:ff:ff:ff":
        broadcast_total += 1
        log.info(f"Broadcast packet count={broadcast_total}")

        if broadcast_total >= THRESHOLD:
            log.info("🚫 Blocking ALL broadcast traffic")

            msg = of.ofp_flow_mod()
            msg.match.dl_dst = packet.dst
            msg.priority = 100
            msg.idle_timeout = IDLE_TIMEOUT
            msg.hard_timeout = HARD_TIMEOUT

            event.connection.send(msg)
            return

    msg = of.ofp_packet_out()
    msg.data = event.ofp
    msg.actions.append(of.ofp_action_output(port=of.OFPP_FLOOD))
    event.connection.send(msg)

def launch():
    core.openflow.addListenerByName("PacketIn", _handle_PacketIn)
