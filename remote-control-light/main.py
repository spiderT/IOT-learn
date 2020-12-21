
from LED import Led
from Button import Button
from Relay import Relay

import time
import uasyncio
import network
import ujson
from umqtt.simple import MQTTClient

"""
Wi-Fi Gateway : SSID and Password
"""
WIFI_AP_SSID = "你家的Wi-Fi SSID"
WIFI_AP_PSW = "你家的Wi-Fi密码"

"""
QCloud Device Info
"""
DEVICE_NAME = "你的设备名称"
PRODUCT_ID = "你的产品ID"
DEVICE_KEY = "你的设备密钥"

"""
MQTT topic
"""
MQTT_CONTROL_TOPIC = "$thing/down/property/"+PRODUCT_ID+"/"+DEVICE_NAME
MQTT_CONTROL_REPLY_TOPIC = "$thing/up/property/"+PRODUCT_ID+"/"+DEVICE_NAME

led = Led(5, 4, 0)
relay = Relay(16)
button = Button(14)

mqtt_client = None
color = 0  # enum 0=red, 1=green, 2=blue
name = ""  # light name. it is optional
brightness = 100  # 0%~100%
light_changed = False


async def wifi_connect(ssid, pwd):
    # 创建WLAN网络接口对象。network.STA_IF 站点也称为客户端，连接到上游WiFi接入点
    sta = network.WLAN(network.STA_IF)
    # 激活网络接口
    sta.active(True)
    # 使用指定的密码连接到指定的无线网络 ssid：WiFi名称 password：WiFi密码
    sta.connect(ssid, pwd)

    while not sta.isconnected():
        print("Wi-Fi Connecting...")
        time.sleep_ms(500)


def mqtt_callback(topic, msg):
    global led, relay, button
    global color, name, brightness, light_changed

    print((topic, msg))
    msg_json = ujson.loads(msg)
    if msg_json['method'] == 'control':
        params = msg_json['params']

        power_switch_tmp = params.get('power_switch')
        if power_switch_tmp is not None:
            power_switch = power_switch_tmp
            relay.set_state(power_switch)

        brightness_tmp = params.get('brightness')
        if brightness_tmp is not None:
            brightness = brightness_tmp

        color_tmp = params.get('color')
        if color_tmp is not None:
            color = color_tmp

        name_tmp = params.get('name')
        if name_tmp is not None:
            name = name_tmp

        if brightness_tmp is not None or color_tmp is not None:
            light_changed = True


async def mqtt_connect():
    global mqtt_client

    MQTT_SERVER = PRODUCT_ID + ".iotcloud.tencentdevices.com"
    MQTT_PORT = 1883
    MQTT_CLIENT_ID = PRODUCT_ID+DEVICE_NAME
    MQTT_USER_NAME = "你的用户名"
    MQTTT_PASSWORD = "你的密码"

    # 构建对象
    mqtt_client = MQTTClient(MQTT_CLIENT_ID, MQTT_SERVER,
                             MQTT_PORT, MQTT_USER_NAME, MQTTT_PASSWORD, 60)
    # 为收到的订阅消息设置回调
    mqtt_client.set_callback(mqtt_callback)
    # 连接到服务器
    mqtt_client.connect()


def mqtt_report(client, color, name, switch, brightness):

    msg = {
        "method": "report",
        "clientToken": "clientToken-2444532211",
        "params": {
            "color": color,
            "color_temp": 0,
            "name": name,
            "power_switch": switch,
            "brightness": brightness
        }
    }

    client.publish(MQTT_CONTROL_REPLY_TOPIC.encode(),
                   ujson.dumps(msg).encode())


async def light_loop():
    global led, relay, button
    global color, name, brightness, light_changed

    switch_status_last = 1
    LED_status = 1

    color = 2  # blue
    brightness = 100  # here 100% == 1
    led.rgb_light(0, 0, 255, brightness/100.0)

    time_cnt = 0
    # 订阅
    mqtt_client.subscribe(MQTT_CONTROL_TOPIC.encode())

    while True:
        # 检查服务器是否有待处理的消息。如果是，则以与wait_msg（）相同的方式处理，如果不是，则立即返回。
        mqtt_client.check_msg()

        switch_status = button.state()
        LED_status = relay.state()
        if switch_status != switch_status_last:
            if switch_status == 0 and switch_status_last == 1:
                LED_status = 0 if LED_status else 1
            relay.set_state(LED_status)
            switch_status_last = switch_status

        if light_changed:
            light_changed = False
            led.rgb_light(255 if color == 0 else 0, 255 if color ==
                          1 else 0, 255 if color == 2 else 0, brightness/100.0)

        if time_cnt >= 20:
            mqtt_report(mqtt_client, color, name, LED_status, brightness)
            time_cnt = 0
        time_cnt = time_cnt+1
        time.sleep_ms(50)

       uasyncio.sleep_ms(50)

async def main():
    global mqtt_client

    # Wi-Fi connection
    try:
        await uasyncio.wait_for(wifi_connect(WIFI_AP_SSID, WIFI_AP_PSW), 20)
    except uasyncio.TimeoutError:
        print("wifi connected timeout!")
    
    # MQTT connection
    try:
        await uasyncio.wait_for(mqtt_connect(), 20)
    except uasyncio.TimeoutError:
        print("mqtt connected timeout!")

    await uasyncio.gather(light_loop())

uasyncio.run(main())
