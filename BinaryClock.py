# BinaryClock: a simple binary clock by Joerg Harzmann (eh-systemhaus)
# BinaryClock_OLED: Converted to Pico-OLED-1.3 by Joerg Harzmann (eh-systemhaus)
# customized for educational project:
# basic display output, binary/decimal system, x/y geometrics

from machine import Pin, SPI
from machine import RTC
from PicoGameBoy import *
import framebuf
import time

# Color scheme
BLACK = PicoGameBoy.color(0, 0, 0)
WHITE = PicoGameBoy.color(255, 255, 255)
GRID_BACKGROUND_COLOR = PicoGameBoy.color(255, 211, 132)
BACKGROUND_COLOR = PicoGameBoy.color(99, 154, 132)
BACKGROUND_COLOR2 = PicoGameBoy.color(57, 89, 41)
TEXT_COLOR = BLACK
TEXT_BACKGROUND_COLOR = WHITE


def binary_clock_main():
    """ Main Program"""

    ' LED'
    led = Pin(25, Pin.OUT)

    ' Pico GameBoy'
    pgb = PicoGameBoy()

    ' Clear display'
    pgb.fill(BLACK)

    ' 1. to 4. Row - 6x Left to Right 10x10px tile  '
    '   Space 10 between 2 cols,                    '
    '   Space 15 between Group of 2 cols            '
    y_pos = 52
    b2d = 1
    for y_row in range(4):
        x_pos = 8
        for x_col in range(6):
            pgb.rect(x_pos, y_pos, 8, 8, WHITE)
            pgb.show()
            if x_col % 2:
                x_pos = x_pos + 20
            else:
                x_pos = x_pos + 15
        pgb.text(str(b2d), x_pos, y_pos, WHITE)
        pgb.show()
        y_pos = y_pos - 8 - 2
        b2d = b2d * 2

    ' Rectangle/Border line whole display'
    pgb.rect(0, 0, 128, 64, WHITE)
    pgb.line(36, 0, 36, 64, WHITE)
    pgb.line(72, 0, 72, 64, WHITE)
    pgb.line(106, 0, 106, 64, WHITE)
    pgb.show()

    ' Decimal Time placeholder'
    pgb.text("H H", 8, 8, WHITE)
    pgb.text("M M", 42, 8, WHITE)
    pgb.text("S S", 78, 8, WHITE)
    pgb.show()

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
        pgb.fill_rect(8, 8, 24, 8, BLACK)
        pgb.text(H_f[:1] + " " + H_f[-1:], 8, 8, WHITE)
        ' Minutes decimal'
        M_f = "{:02d}".format(M)
        pgb.fill_rect(42, 8, 24, 8, BLACK)
        pgb.text(M_f[:1] + " " + M_f[-1:], 42, 8, WHITE)
        ' Seconds decimal'
        S_f = "{:02d}".format(S)
        pgb.fill_rect(78, 8, 24, 8, BLACK)
        pgb.text(S_f[:1] + " " + S_f[-1:], 78, 8, WHITE)

        ' Hours binary'
        bcd_at(pgb, H, 1)
        ' Minutes binary'
        bcd_at(pgb, M, 3)
        ' Seconds binary'
        bcd_at(pgb, S, 5)

        ' Refresh Display OLED'
        pgb.show()

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
    b_f8 = b_f[0:1]  # Left char - Bit 8
    b_f4 = b_f[1:2]  # One char Pos. 2 - Bit 4
    b_f2 = b_f[2:3]  # One char Pos. 3 - Bit 2
    b_f1 = b_f[-1:]  # Right char - Bit 1

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
        disp.fill_rect(x_pos, 52, 8, 8, BLACK)
    else:
        disp.fill_rect(x_pos, 52, 8, 8, WHITE)
    if b_f2 == "0":
        disp.fill_rect(x_pos, 42, 8, 8, BLACK)
    else:
        disp.fill_rect(x_pos, 42, 8, 8, WHITE)
    if b_f4 == "0":
        disp.fill_rect(x_pos, 32, 8, 8, BLACK)
    else:
        disp.fill_rect(x_pos, 32, 8, 8, WHITE)
    if b_f8 == "0":
        disp.fill_rect(x_pos, 22, 8, 8, BLACK)
    else:
        disp.fill_rect(x_pos, 22, 8, 8, WHITE)

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
    binary_at(disp, d2, x + 1)


if __name__ == '__main__':
    binary_clock_main()
