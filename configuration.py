from constants import (
    CONFIGURATION_FILE,
    CONFIGURATION_RUN_BLINK_TIME_COLON,
    CONFIGURATION_RUN_CLOCK_TYPE,
    CONFIGURATION_RUN_AUTOLIGHT,
    CONFIGURATION_RUN_SHOW_TEMP,
    CONFIGURATION_MQTT_BROKER,
    CONFIGURATION_MQTT_CONFIG,
    CONFIGURATION_MQTT_ENABLED,
    CONFIGURATION_MQTT_PREFIX,
    CONFIGURATION_MQTT_USERNAME,
    CONFIGURATION_MQTT_PASSWORD,
    CONFIGURATION_RUN_CONFIG,
    CONFIGURATION_RUN_TEMP,
    CONFIGURATION_WIFI_CONFIG,
    CONFIGURATION_WIFI_ENABLED,
    CONFIGURATION_WIFI_HOSTNAME,
    CONFIGURATION_WIFI_SSID,
    CONFIGURATION_WIFI_PASSPHRASE,
    CONFIGURATION_NTP_CONFIG,
    CONFIGURATION_NTP_ENABLED,
    CONFIGURATION_NTP_SERVER,
    CONFIGURATION_NTP_INTERVAL,
)
from util import singleton
from helpers import read_json_file, write_json_file


@singleton
class Configuration:
    class WifiConfiguration:
        def __init__(self, enabled: bool, hostname: str, ssid: str, passphrase: str) -> None:
            self.enabled = enabled
            self.hostname = hostname
            self.ssid = ssid
            self.passphrase = passphrase

    class MQTTConfiguration:
        def __init__(self, enabled: bool, broker: str, prefix: str, username: str, password: str) -> None:
            self.enabled = enabled
            self.broker = broker
            self.prefix = prefix
            self.base_topic = prefix + "/"
            self.username = username
            self.password = password

    class NTPConfiguration:
        def __init__(self, enabled: bool, server: str, interval: int) -> None:
            self.enabled = enabled
            self.server = server
            self.interval = interval

    def __init__(self) -> None:
        self.config = {}
        self.blink_time_colon = False
        self.temp = "c"
        self.clock_type = "24"
        self.show_temp = True
        self.autolight = False
        self.read_config_file()

    def read_config_file(self):
        self.config = read_json_file(CONFIGURATION_FILE)
        self.update_config_variables()

    def update_config_variables(self):
        # runConfig
        self.blink_time_colon = self.config[CONFIGURATION_RUN_CONFIG][CONFIGURATION_RUN_BLINK_TIME_COLON]
        self.temp = self.config[CONFIGURATION_RUN_CONFIG][CONFIGURATION_RUN_TEMP]
        self.clock_type = self.config[CONFIGURATION_RUN_CONFIG][CONFIGURATION_RUN_CLOCK_TYPE]
        self.show_temp = self.config[CONFIGURATION_RUN_CONFIG][CONFIGURATION_RUN_SHOW_TEMP]
        self.autolight = self.config[CONFIGURATION_RUN_CONFIG][CONFIGURATION_RUN_AUTOLIGHT]

        # wifiConfig
        self.wifi_config = self.WifiConfiguration(
            enabled=self.config[CONFIGURATION_WIFI_CONFIG][CONFIGURATION_WIFI_ENABLED],
            hostname=self.config[CONFIGURATION_WIFI_CONFIG][CONFIGURATION_WIFI_HOSTNAME],
            ssid=self.config[CONFIGURATION_WIFI_CONFIG][CONFIGURATION_WIFI_SSID],
            passphrase=self.config[CONFIGURATION_WIFI_CONFIG][CONFIGURATION_WIFI_PASSPHRASE],
        )

        # mqttConfig
        self.mqtt_config = self.MQTTConfiguration(
            enabled=self.config[CONFIGURATION_MQTT_CONFIG][CONFIGURATION_MQTT_ENABLED],
            broker=self.config[CONFIGURATION_MQTT_CONFIG][CONFIGURATION_MQTT_BROKER],
            prefix=self.config[CONFIGURATION_MQTT_CONFIG][CONFIGURATION_MQTT_PREFIX],
            username=self.config[CONFIGURATION_MQTT_CONFIG][CONFIGURATION_MQTT_USERNAME],
            password=self.config[CONFIGURATION_MQTT_CONFIG][CONFIGURATION_MQTT_PASSWORD],
        )

        # ntpConfig
        ntp_conf = self.config.get(CONFIGURATION_NTP_CONFIG, {})
        self.ntp_config = self.NTPConfiguration(
            enabled=ntp_conf.get(CONFIGURATION_NTP_ENABLED, True),
            server=ntp_conf.get(CONFIGURATION_NTP_SERVER, "pool.ntp.org"),
            interval=ntp_conf.get(CONFIGURATION_NTP_INTERVAL, 21600),
        )

    def write_config_file(self):
        write_json_file(CONFIGURATION_FILE, self.config)
        self.update_config_variables()

    # toggles/updates
    def switch_blink_time_colon_value(self):
        key = CONFIGURATION_RUN_BLINK_TIME_COLON
        self.config[CONFIGURATION_RUN_CONFIG][key] = not self.config[CONFIGURATION_RUN_CONFIG][key]
        self.write_config_file()

    def switch_temp_value(self):
        key = CONFIGURATION_RUN_TEMP
        self.config[CONFIGURATION_RUN_CONFIG][key] = "f" if self.config[CONFIGURATION_RUN_CONFIG][key] == "c" else "c"
        self.write_config_file()

    def update_clock_type_value(self, value):
        self.config[CONFIGURATION_RUN_CONFIG][CONFIGURATION_RUN_CLOCK_TYPE] = value
        self.write_config_file()

    def update_autolight_value(self, value):
        self.config[CONFIGURATION_RUN_CONFIG][CONFIGURATION_RUN_AUTOLIGHT] = value
        self.write_config_file()
