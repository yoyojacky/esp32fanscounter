from machine import Pin, SoftI2C
import network
import urequests
import time
from ssd1306 import SSD1306_I2C
import framebuf


i2c = SoftI2C(scl=Pin(22), sda=Pin(21), freq=400000)
# oled 0.96 inch
WIDTH = 128
HEIGHT = 64
oled = SSD1306_I2C(WIDTH, HEIGHT, i2c)
oled.fill(0)
oled.show()

bilibili_logo = bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00?\xf0\x00\x01\xfe\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\xff\xfe\x00\x0f\xff\xc0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x03\xff\xff\x00\x1f\xff\xe0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x07\xff\xff\x80\x1f\xff\xf0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x07\xff\xff\x80?\xff\xf0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x07\xff\xff\x80?\xff\xf0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x03\xff\xff\x00?\xff\xf0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\xff\xfe\x00\x1f\xff\xe0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0f\xff\xff\xff\xff\xff\xfe\x00\x00\x00\x00\x00\x00\x00\x00\x00\x7f\xff\xff\xff\xff\xff\xff\xc0\x00\x00\x00\x00\x00\x00\x00\x01\xff\xff\xff\xff\xff\xff\xff\xf0\x00\x00\x00\x00\x00\x00\x00\x03\xff\xff\xff\xff\xff\xff\xff\xf8\x00\x00\x00\x00\x00\x00\x00\x07\xff\xff\xff\xff\xff\xff\xff\xfc\x00\x00\x00\x00\x00\x00\x00\x0f\xf0\x00\x00\x00\x00\x00\x01\xfe\x00\x00\x00\x00\x00\x00\x00\x0f\xc0\x00\x00\x00\x00\x00\x00\x7f\x00\x00\x00\x00\x00\x00\x00\x1f\x80\x00\x00\x00\x00\x00\x00?\x00\x00\x00\x00\x00\x00\x00\x1f\x00\x00\x00\x00\x00\x00\x00\x1f\x00\x00\x00\x00\x00\x00\x00\x1f\x00\x00\x00\x00\x0e\x00\x00\x1f\x00\x00\x00\x00\x00\x00\x00\x1f\x00\x00\xf0\x00\x0f\xc0\x00\x1f\x00\x00\x00\x00\x00\x00\x00\x1f\x00\x03\xf0\x00\x0f\xe0\x00\x1f\x00\x00\x00\x00\x00\x00\x00\x1f\x00\x07\xf0\x00\x07\xf0\x00\x1f\x00\x00\x00\x00\x00\x00\x00\x1f\x00\x0f\xc0\x00\x00\xf8\x00\x1f\x00\x00\x00\x00\x00\x00\x00\x1f\x00\x1f\x00\x00\x00|\x00\x1f\x00\x00\x00\x00\x00\x00\x00\x1f\x00<\x00\x00\x00>\x00\x1f\x00\x00\x00\x00\x00\x00\x00\x1f\x00x\x00\x00\x00\x1f\x00\x1f\x00\x00\x00\x00\x00\x00\x00\x1f\x00\xf8>\x03\xf8\x0f\xe0\x1f\x00\x00\x00\x00\x00\x00\x00\x1f\x00\xf0\x7f\x03\xf8\x07\xe0\x1f\x00\x00\x00\x00\x00\x00\x00\x1f\x01\xe0\x7f\x03\xf8\x01\xe0\x1f\x00\x00\x00\x00\x00\x00\x00\x1f\x01\xc0\x7f\x01\xf8\x00@\x1f\x00\x00\x00\x00\x00\x00\x00\x1f\x03\xc0\x7f\x01\xfc\x00\x00\x1f\x00\x00\x00\x00\x00\x00\x00\x1f\x01\x80|\x01\xfc\x00\x00\x1f\x00\x00\x00\x00\x00\x00\x00\x1f\x00\x00|\x03\xfc\x00\x00\x1f\x00\x00\x00\x00\x00\x00\x00\x1f\x00\x00|\x03\xfc\x00\x00\x1f\x00\x00\x00\x00\x00\x00\x00\x1f\x00\x00~\x03\xf8\x00\x00\x1f\x00\x00\x00\x00\x00\x00\x00\x1f\x00\x00~\x01\xf8\x0c\x00\x1f\x00\x00\x00\x00\x00\x00\x00\x1f\x00\x00>\x00\xf8\x1e\x00\x1f\x00\x00\x00\x00\x00\x00\x00\x1f\x00\x00\x1c\x00\x00\x1f\x00\x1f\x00\x00\x00\x00\x00\x00\x00\x1f\x00\x00\x00\x00\x00\x0f\x80\x1f\x00\x00\x00\x00\x00\x00\x00\x1f\x00\x00\x00\x00\x00\x1f\xc0\x1f\x00\x00\x00\x00\x00\x00\x00\x1f\x00\x00\x00\x00\x01\xff\xe0\x1f\x00\x00\x00\x00\x00\x00\x00\x1f\x00\x00\x00\x00\x07\xfd\xf0\x1f\x00\x00\x00\x00\x00\x00\x00\x1f\x00\x02\x00\x00?\xf8\xf0\x1f\x00\x00\x00\x00\x00\x00\x00\x1f\x00\x07\xc0\x01\xff\x00p\x1f\x00\x00\x00\x00\x00\x00\x00\x1f\x00\x07\xff\xff\xfe\x000\x1f\x00\x00\x00\x00\x00\x00\x00\x1f\x00\x07\xff\xff\xf0\x00\x00\x1f\x00\x00\x00\x00\x00\x00\x00\x1f\x00\x00\x7f\xff\x00\x00\x00\x1f\x00\x00\x00\x00\x00\x00\x00\x1f\x80\x00\x00\x00\x00\x00\x00?\x00\x00\x00\x00\x00\x00\x00\x0f\xe0\x00\x00\x00\x00\x00\x00\xff\x00\x00\x00\x00\x00\x00\x00\x0f\xfe\x00\x00\x00\x00\x00\x0f\xfe\x00\x00\x00\x00\x00\x00\x00\x07\xff\xff\xff\xff\xff\xff\xff\xfc\x00\x00\x00\x00\x00\x00\x00\x03\xff\xff\xff\xff\xff\xff\xff\xf8\x00\x00\x00\x00\x00\x00\x00\x00\xff\xff\xff\xff\xff\xff\xff\xf0\x00\x00\x00\x00\x00\x00\x00\x00?\xff\xff\xff\xff\xff\xff\x80\x00\x00\x00\x00\x00\x00\x00\x00\x01\xff\xff\xff\xff\xff\xf0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
logo_buff = framebuf.FrameBuffer(bilibili_logo, 128, 64, framebuf.MONO_HLSB)

bilibili2_logo = bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00p\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0e\x00\x00\x00\x00\xf8\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x1f\x00\x00\x00\x01\xf8\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x1f\xc0\x00\x00\x03\xf8\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x1f\xe0\x00\x00\x07\xf0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0f\xf0\x00\x00\x0f\xe0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x07\xf8\x00\x00?\xc0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\xfe\x00\x00\x7f\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\x00\x00\xff\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x7f\x80\x01\xfc\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00?\x80\x03\xf8\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0f\xff\xff\xff\xff\xff\xfe\x00\x00\x00\x00\x00\x00\x00\x00\x00\x7f\xff\xff\xff\xff\xff\xff\xc0\x00\x00\x00\x00\x00\x00\x00\x01\xff\xff\xff\xff\xff\xff\xff\xf0\x00\x00\x00\x00\x00\x00\x00\x03\xff\xff\xff\xff\xff\xff\xff\xf8\x00\x00\x00\x00\x00\x00\x00\x07\xff\xff\xff\xff\xff\xff\xff\xfc\x00\x00\x00\x00\x00\x00\x00\x0f\xf0\x00\x00\x00\x00\x00\x01\xfe\x00\x00\x00\x00\x00\x00\x00\x0f\xc0\x00\x00\x00\x00\x00\x00\x7f\x00\x00\x00\x00\x00\x00\x00\x1f\x80\x00\x00\x00\x00\x00\x00?\x00\x00\x00\x00\x00\x00\x00\x1f\x00\x00\x00\x00\x01\xc0\x00\x1f\x00\x00\x00\x00\x00\x00\x00\x1f\x00\x00\x0e\x00\x03\xe0\x00\x1f\x00\x00\x00\x00\x00\x00\x00\x1f\x00\x00?\x00\x03\xf0\x00\x1f\x00\x00\x00\x00\x00\x00\x00\x1f\x00\x00\x7f\x00\x03\xf8\x00\x1f\x00\x00\x00\x00\x00\x00\x00\x1f\x00\x01\xff\x00\x01\xfc\x00\x1f\x00\x00\x00\x00\x00\x00\x00\x1f\x00\x03\xfe\x00\x00\xfe\x00\x1f\x00\x00\x00\x00\x00\x00\x00\x1f\x00\x0f\xf8\x00\x00\x7f\x80\x1f\x00\x00\x00\x00\x00\x00\x00\x1f\x00?\xf0\x00\x00?\xc0\x1f\x00\x00\x00\x00\x00\x00\x00\x1f\x00\x7f\xc0\x00\x00\x1f\xe0\x1f\x00\x00\x00\x00\x00\x00\x00\x1f\x01\xff\x80\x00\x00\x0f\xf0\x1f\x00\x00\x00\x00\x00\x00\x00\x1f\x03\xfe\x00\x00\x00\x07\xf8\x1f\x00\x00\x00\x00\x00\x00\x00\x1f\x03\xf8\x00\x00\x00\x01\xfc\x1f\x00\x00\x00\x00\x00\x00\x00\x1f\x03\xf0\x00\x00\x00\x00\xfe\x1f\x00\x00\x00\x00\x00\x00\x00\x1f\x01\xc0\x00\x00\x00\x00~\x1f\x00\x00\x00\x00\x00\x00\x00\x1f\x00\x00\x00\x00\x00\x00>\x1f\x00\x00\x00\x00\x00\x00\x00\x1f\x00\x00\x00\x00\x00\x00\x1c\x1f\x00\x00\x00\x00\x00\x00\x00\x1f\x00\x00\x00\x00\x00\x00\x00\x1f\x00\x00\x00\x00\x00\x00\x00\x1f\x00\x00\x03\x00\x06\x00\x00\x1f\x00\x00\x00\x00\x00\x00\x00\x1f\x00\x00\x03\x03\x06\x00\x00\x1f\x00\x00\x00\x00\x00\x00\x00\x1f\x00\x00\x03\x07\x86\x00\x00\x1f\x00\x00\x00\x00\x00\x00\x00\x1f\x00\x00\x03\x07\x86\x00\x00\x1f\x00\x00\x00\x00\x00\x00\x00\x1f\x00\x00\x01\xcf\xc6\x00\x00\x1f\x00\x00\x00\x00\x00\x00\x00\x1f\x00\x00\x01\xfc\xfe\x00\x00\x1f\x00\x00\x00\x00\x00\x00\x00\x1f\x00\x00\x00\xf0|\x00\x00\x1f\x00\x00\x00\x00\x00\x00\x00\x1f\x00\x00\x00\x00\x00\x00\x00\x1f\x00\x00\x00\x00\x00\x00\x00\x1f\x00\x00\x00\x00\x00\x00\x00\x1f\x00\x00\x00\x00\x00\x00\x00\x1f\x00\x00\x00\x00\x00\x00\x00\x1f\x00\x00\x00\x00\x00\x00\x00\x1f\x00\x00\x00\x00\x00\x00\x00\x1f\x00\x00\x00\x00\x00\x00\x00\x1f\x00\x00\x00\x00\x00\x00\x00\x1f\x00\x00\x00\x00\x00\x00\x00\x1f\x00\x00\x00\x00\x00\x00\x00\x1f\x00\x00\x00\x00\x00\x00\x00\x1f\x80\x00\x00\x00\x00\x00\x00?\x00\x00\x00\x00\x00\x00\x00\x0f\xe0\x00\x00\x00\x00\x00\x00\xff\x00\x00\x00\x00\x00\x00\x00\x0f\xfe\x00\x00\x00\x00\x00\x0f\xfe\x00\x00\x00\x00\x00\x00\x00\x07\xff\xff\xff\xff\xff\xff\xff\xfc\x00\x00\x00\x00\x00\x00\x00\x03\xff\xff\xff\xff\xff\xff\xff\xf8\x00\x00\x00\x00\x00\x00\x00\x00\xff\xff\xff\xff\xff\xff\xff\xf0\x00\x00\x00\x00\x00\x00\x00\x00?\xff\xff\xff\xff\xff\xff\x80\x00\x00\x00\x00\x00\x00\x00\x00\x01\xff\xff\xff\xff\xff\xf0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
logo_buff2 = framebuf.FrameBuffer(bilibili2_logo, 128,64, framebuf.MONO_HLSB)


# vmid 换成你自己id
vmid = '你的vmid' 
url = 'https://api.bilibili.com/x/relation/stat?vmid='+ vmid +'&jsonp=jsonp'
ssid = '替换成你的wifi的ssid'
password = '你的密码'


wlan = network.WLAN(network.STA_IF)

def connect_wifi(ssid, password):
    if not wlan.active():
        wlan.active(1)
    
    if not wlan.isconnected():
        wlan.active(1)
        wlan.connect(ssid, password)
        wlan.ifconfig()


def draw_logo():
    #oled.text("My Bilibili fans:", 0, 0)
    oled.blit(logo_buff, 0, 0)
    oled.text(follower, 85, 30)
    oled.show()
    time.sleep(1)
    oled.blit(logo_buff2, 0, 0)
    oled.text(follower, 85, 30)
    oled.show()
    time.sleep(1)



while True:
    connect_wifi(ssid, password)
    # print(wlan.ifconfig())
    if wlan.isconnected():
        html = urequests.get(url)
        parsed = html.json()
        print('B站关注人数：{}'.format(parsed['data']['follower']))
        follower = str(parsed['data']['follower'])
        draw_logo()
        time.sleep(3)
        
