
from ble_lightsensor import BLELightSensor
from lightsensor import LightSensor
import time
import bluetooth


def main():
    ble = bluetooth.BLE()
    ble.active(True)
    ble_light = BLELightSensor(ble)

    light = LightSensor(36)
    light_density = light.value()
    i = 0

    while True:
        # Write every second, notify every 10 seconds.
        i = (i + 1) % 10
        ble_light.set_light(light_density, notify=i == 0)
        print("Light Lux:", light_density)

        light_density = light.value()
        time.sleep_ms(1000)


if __name__ == "__main__":
    main()
