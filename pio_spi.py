import rp2
from machine import Pin

@rp2.asm_pio(
    out_shiftdir=0,
    autopull=True,
    pull_thresh=8,
    autopush=True,
    push_thresh=8,
    sideset_init=rp2.PIO.OUT_LOW,
    out_init=rp2.PIO.OUT_LOW
    )

def _spi_send_only():
    out(pins, 1)      .side(0x0)
    nop()             .side(0x1) [1]


class SpiSendOnly:
    """Uses only two pins (clock and data).""
    def __init__(self, sm_id, mosi,  sck, freq=4000000):
        self._sm = rp2.StateMachine(sm_id,
                                    _spi_send_only,
                                    freq=4*freq,
                                    sideset_base=Pin(sck),
                                    out_base=Pin(mosi),
                                    in_base=Pin(sck)
                                    )
        self._sm.active(1)

    def write(self, wdata):
        for b in wdata:
            self._sm.put(b << 24)

