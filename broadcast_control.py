from pox.core import core
import pox.openflow.libopenflow_01 as of

log = core.getLogger()

broadcast_total = 0
THRESHOLD = 3   # 🔥 BLOCK AT 3

def _handle_PacketIn(event):
    global broadcast_total

    packet = event.parsed
    src = str(packet.src)
    dst = str(packet.dst)

    # Detect broadcast
    if dst == "ff:ff:ff:ff:ff:ff":
        broadcast_total += 1
        log.info(f"Broadcast packet count={broadcast_total}")

        # BLOCK after threshold
        if broadcast_total >= THRESHOLD:
            log.info("🚫 Blocking ALL broadcast traffic")

            # Install DROP rule in switch
            msg = of.ofp_flow_mod()
            msg.match.dl_dst = packet.dst   # match broadcast
            msg.priority = 100
            # No actions = DROP
            event.connection.send(msg)

            return

    # Normal forwarding
    msg = of.ofp_packet_out()
    msg.data = event.ofp
    msg.actions.append(of.ofp_action_output(port=of.OFPP_FLOOD))
    event.connection.send(msg)

def launch():
    core.openflow.addListenerByName("PacketIn", _handle_PacketIn)
