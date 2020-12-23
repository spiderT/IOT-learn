
import time
from threading import Thread
from interruptingcow import timeout

from bluepy.btle import DefaultDelegate, Peripheral, Scanner, UUID, capitaliseName, BTLEInternalError
from bluepy.btle import BTLEDisconnectError, BTLEManagementError, BTLEGattError


class LightScanner():
    SCAN_TIMEOUT = 5

    def __init__(self, name):
        self._name = name

    def status_update(self):
        results = self._get_data()

        # messages = [
        #     MqttMessage(
        #         topic=self.format_topic("property/light"),
        #         payload=results.lightlevel,
        #     )
        # ]

        return results

    def _get_data(self):

        scan_processor = ScanProcessor(self._name)
        scanner = Scanner().withDelegate(scan_processor)
        scanner.scan(self.SCAN_TIMEOUT, passive=True)

        with timeout(
            self.SCAN_TIMEOUT,
            exception=Exception(
                "Retrieving data from {} device {} timed out after {} seconds".format(
                    repr(self), self._name, self.SCAN_TIMEOUT
                )
            ),
        ):
            while not scan_processor.ready:
                time.sleep(1)
            return scan_processor.results

        return scan_processor.results


class ScanProcessor:

    ADV_TYPE_SERVICE_DATA = 0x16

    def __init__(self, name):
        self._ready = False
        self._name = name
        self._results = MiBeaconData()

    def handleDiscovery(self, dev, isNewDev, _):
        is_nodemcu = False
        if isNewDev:
            for (adtype, desc, value) in dev.getScanData():
                # Service Data UUID == 0xFE95 according to MiBeacon
                if adtype == self.ADV_TYPE_SERVICE_DATA and value.startswith("95fe"):
                    print("FOUND service Data:", adtype, desc, value)
                    # Object ID == 0x1007 according to MiBeacon
                    if len(value) == 38 and value[26:30] == '0710':
                        light_den = int((value[-2:] + value[-4:-2]), 16)
                        mac = value[14:26]

                        self._results.lightlevel = light_den
                        self._results.mac = mac

                        self.ready = True

    @property
    def mac(self):
        return self._mac

    @property
    def ready(self):
        return self._ready

    @ready.setter
    def ready(self, var):
        self._ready = var

    @property
    def results(self):
        return self._results


class MiBeaconData:
    def __init__(self):
        self._lightlevel = None
        self._mac = None

    @property
    def lightlevel(self):
        return self._lightlevel

    @lightlevel.setter
    def lightlevel(self, var):
        self._lightlevel = var

    @property
    def mac(self):
        return self._mac

    @mac.setter
    def mac(self, var):
        self._mac = var
