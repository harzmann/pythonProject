from machine import Pin, SPI
from machine import RTC
import framebuf
import time

DC = 8
RST = 12
MOSI = 11
SCK = 10
CS = 9

def binary_clock_main():
    """ Main Program"""
    ' Parameter'
    led = Pin(25, Pin.OUT)

    ' Demo OLED'
    OLED = OLED_1inch3()
    OLED.fill(0x0000)
    OLED.show()
    OLED.rect(0, 0, 128, 64, OLED.white)
    time.sleep(0.5)
    OLED.show()
    OLED.rect(10, 22, 20, 20, OLED.white)
    time.sleep(0.5)
    OLED.show()
    OLED.fill_rect(40, 22, 20, 20, OLED.white)
    time.sleep(0.5)
    OLED.show()
    OLED.rect(70, 22, 20, 20, OLED.white)
    time.sleep(0.5)
    OLED.show()
    OLED.fill_rect(100, 22, 20, 20, OLED.white)
    time.sleep(0.5)
    OLED.show()
    time.sleep(1)

    ' Clear display '
    OLED.fill(0x0000)

    ' 1. Row - 6x Left to Right 10x10px tile        '
    '   Space 10 between 2 cols,                    '
    '   Space 15 between Group of 2 cols            '
    # OLED.rect(0, 54, 10, 10, OLED.white)
    # OLED.show()
    # OLED.rect(15, 54, 10, 10, OLED.white)
    # OLED.show()
    # OLED.rect(35, 54, 10, 10, OLED.white)
    # OLED.show()
    # OLED.rect(50, 54, 10, 10, OLED.white)
    # OLED.show()
    # OLED.rect(70, 54, 10, 10, OLED.white)
    # OLED.show()
    # OLED.rect(85, 54, 10, 10, OLED.white)
    # OLED.text("1", 100, 54, OLED.white)

    ' 1. to 4. Row - 6x Left to Right 10x10px tile  '
    '   Space 10 between 2 cols,                    '
    '   Space 15 between Group of 2 cols            '
    # y_pos = 54
    # b2d = 1
    # for i in range(4):
    #     OLED.rect(0, y_pos, 10, 10, OLED.white)
    #     OLED.show()
    #     OLED.rect(15, y_pos, 10, 10, OLED.white)
    #     OLED.show()
    #     OLED.rect(35, y_pos, 10, 10, OLED.white)
    #     OLED.show()
    #     OLED.rect(50, y_pos, 10, 10, OLED.white)
    #     OLED.show()
    #     OLED.rect(70, y_pos, 10, 10, OLED.white)
    #     OLED.show()
    #     OLED.rect(85, y_pos, 10, 10, OLED.white)
    #     OLED.show()
    #     OLED.text(str(b2d), 100, y_pos, OLED.white)
    #     OLED.show()
    #     y_pos = y_pos - 10 - 5
    #     b2d = b2d * 2

    ' 1. to 4. Row - 6x Left to Right 10x10px tile  '
    '   Space 10 between 2 cols,                    '
    '   Space 15 between Group of 2 cols            '
    y_pos = 52
    b2d = 1
    for y_row in range(4):
        x_pos = 8
        for x_col in range(6):
            OLED.rect(x_pos, y_pos, 8, 8, OLED.white)
            OLED.show()
            if x_col % 2:
                x_pos = x_pos + 20
            else:
                x_pos = x_pos + 15
        OLED.text(str(b2d), x_pos, y_pos, OLED.white)
        OLED.show()
        y_pos = y_pos - 8 - 2
        b2d = b2d * 2

    ' Rectangle/Border line whole display'
    OLED.rect(0, 0, 128, 64, OLED.white)
    OLED.line(36, 0, 36, 64, OLED.white)
    OLED.line(72, 0, 72, 64, OLED.white)
    OLED.line(106, 0, 106, 64, OLED.white)
    OLED.show()

    ' Decimal Time placeholder'
    OLED.text("H H", 8, 8, OLED.white)
    OLED.text("M M", 42, 8, OLED.white)
    OLED.text("S S", 78, 8, OLED.white)
    OLED.show()

    ' Init RTC'
    rtc = RTC()

    ' Loop Refreshing Display'
    while True:
        ' Toggle LED Light'
        led.toggle()

        ' Get current Date and Time'
        Y, M, D, W, H, M, S, SS = rtc.datetime()
        # print(H, M, S)

        ' Hours decimal'
        H_f = "{:02d}".format(H)
        OLED.fill_rect(8, 8, 24, 8, OLED.balck)
        OLED.text(H_f[:1] + " " + H_f[-1:], 8, 8, OLED.white)
        ' Minutes decimal'
        M_f = "{:02d}".format(M)
        OLED.fill_rect(42, 8, 24, 8, OLED.balck)
        OLED.text(M_f[:1] + " " + M_f[-1:], 42, 8, OLED.white)
        ' Seconds decimal'
        S_f = "{:02d}".format(S)
        OLED.fill_rect(78, 8, 24, 8, OLED.balck)
        OLED.text(S_f[:1] + " " + S_f[-1:], 78, 8, OLED.white)

        ' Hours binary'
        bcd_at(OLED, H, 1)
        ' Minutes binary'
        bcd_at(OLED, M, 3)
        ' Seconds binary'
        bcd_at(OLED, S, 5)

        ' Refresh Display OLED'
        OLED.show()

        ' Nothing to do > Sleeping...'
        time.sleep(0.1)


def binary_at(disp, d, x):
    """ Display on OLED using tiles """
    ' Format Description'
    ' :0 means filling up with zeros'
    ' > means right alignment'
    ' 4b means convert to 4 digit binary'
    b_f = "{:0>4b}".format(d)
    # print(x, b_f)

    ' Divide string into 4 bit-string'
    b_f8 = b_f[0:1]     # Left char - Bit 8
    b_f4 = b_f[1:2]     # One char Pos. 2 - Bit 4
    b_f2 = b_f[2:3]     # One char Pos. 3 - Bit 2
    b_f1 = b_f[-1:]     # Right char - Bit 1

    ' Re-Write Tiles '
    if x == 1:
        x_pos = 8
    elif x == 2:
        x_pos = 23
    elif x == 3:
        x_pos = 43
    elif x == 4:
        x_pos = 58
    elif x == 5:
        x_pos = 78
    elif x == 6:
        x_pos = 93

    if b_f1 == "0":
        disp.fill_rect(x_pos, 52, 8, 8, disp.balck)
    else:
        disp.fill_rect(x_pos, 52, 8, 8, disp.white)
    if b_f2 == "0":
        disp.fill_rect(x_pos, 42, 8, 8, disp.balck)
    else:
        disp.fill_rect(x_pos, 42, 8, 8, disp.white)
    if b_f4 == "0":
        disp.fill_rect(x_pos, 32, 8, 8, disp.balck)
    else:
        disp.fill_rect(x_pos, 32, 8, 8, disp.white)
    if b_f8 == "0":
        disp.fill_rect(x_pos, 22, 8, 8, disp.balck)
    else:
        disp.fill_rect(x_pos, 22, 8, 8, disp.white)

    ' Code for displaying on 8x8 Matrix'
    # y = 7
    # while y > 1:
    #     bit = d & 0x01
    #     print(d, x, y, bit)
    #     if bit == 1:
    #         disp.pixel(x, y, 1)
    #     y = y - 1
    #     d = d >> 1


def bcd_at(disp, b, x):
    """ Value To Decimal digit 1 (High) & 2 (Low) """
    d1 = b // 10
    d2 = b % 10
    # print(b, d1, d2)
    binary_at(disp, d1, x)
    binary_at(disp, d2, x+1)


class OLED_1inch3(framebuf.FrameBuffer):

    def __init__(self):
        self.width = 128
        self.height = 64

        self.cs = Pin(CS, Pin.OUT)
        self.rst = Pin(RST, Pin.OUT)

        self.cs(1)
        self.spi = SPI(1)
        self.spi = SPI(1, 2000_000)
        self.spi = SPI(1, 20000_000, polarity=0, phase=0, sck=Pin(SCK), mosi=Pin(MOSI), miso=None)
        self.dc = Pin(DC, Pin.OUT)
        self.dc(1)
        self.buffer = bytearray(self.height * self.width // 8)
        super().__init__(self.buffer, self.width, self.height, framebuf.MONO_HMSB)
        self.init_display()

        self.white = 0xffff
        self.balck = 0x0000

    def write_cmd(self, cmd):
        """Write Command via SPI"""
        self.cs(1)
        self.dc(0)
        self.cs(0)
        self.spi.write(bytearray([cmd]))
        self.cs(1)

    def write_data(self, buf):
        """Write Data via SPI"""
        self.cs(1)
        self.dc(1)
        self.cs(0)
        self.spi.write(bytearray([buf]))
        self.cs(1)

    def init_display(self):
        """ Initialize display """
        self.rst(1)
        time.sleep(0.001)
        self.rst(0)
        time.sleep(0.01)
        self.rst(1)

        self.write_cmd(0xAE)  # turn off OLED display

        self.write_cmd(0x00)  # set lower column address
        self.write_cmd(0x10)  # set higher column address

        self.write_cmd(0xB0)  # set page address

        self.write_cmd(0xdc)  # et display start line
        self.write_cmd(0x00)
        self.write_cmd(0x81)  # contract control
        self.write_cmd(0x6f)  # 128
        self.write_cmd(0x21)  # Set Memory addressing mode (0x20/0x21) #

        self.write_cmd(0xa0)  # set segment remap
        self.write_cmd(0xc0)  # Com scan direction
        self.write_cmd(0xa4)  # Disable Entire Display On (0xA4/0xA5)

        self.write_cmd(0xa6)  # normal / reverse
        self.write_cmd(0xa8)  # multiplex ratio
        self.write_cmd(0x3f)  # duty = 1/64

        self.write_cmd(0xd3)  # set display offset
        self.write_cmd(0x60)

        self.write_cmd(0xd5)  # set osc division
        self.write_cmd(0x41)

        self.write_cmd(0xd9)  # set pre-charge period
        self.write_cmd(0x22)

        self.write_cmd(0xdb)  # set vcomh
        self.write_cmd(0x35)

        self.write_cmd(0xad)  # set charge pump enable
        self.write_cmd(0x8a)  # Set DC-DC enable (a=0:disable; a=1:enable)
        self.write_cmd(0XAF)

    def show(self):
        """Write Framebuffer to Display > Show"""
        self.write_cmd(0xb0)
        for page in range(64):
            self.column = 63 - page
            self.write_cmd(0x00 + (self.column & 0x0f))
            self.write_cmd(0x10 + (self.column >> 4))
            for num in range(16):
                self.write_data(self.buffer[page * 16 + num])
                print(page, num, page * 16 + num)


if __name__ == '__main__':
    binary_clock_main()

