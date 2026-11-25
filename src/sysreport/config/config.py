import os
import tomllib

DEFAULT_CONFIG = "[options]"

CONFIG_PATH = f"{os.environ.get('HOME')}/.config/sysreport/"
FILE_PATH = f"{CONFIG_PATH}/sysreport.toml"


class SysreportConfig:
    @staticmethod
    def __create_default_config() -> None:
        os.makedirs(CONFIG_PATH)
        with open(FILE_PATH, "w", encoding="utf-8") as f:
            f.write(DEFAULT_CONFIG)

    @staticmethod
    def load() -> dict:
        if not os.path.exists(FILE_PATH):
            SysreportConfig.__create_default_config()

        with open(FILE_PATH, "rb") as f:
            config = tomllib.load(f)

        return config
