import board
import busio

spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
