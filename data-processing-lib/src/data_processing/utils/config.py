import os
from typing import Any, Union


class DPFConfig:
    @staticmethod
    def _get_config(env_var_list: list[str]) -> Union[str, None]:
        for var in env_var_list:
            value = os.environ.get(var, None)
            if value is not None:
                return value
        return None

    S3_ACCESS_KEY = _get_config(["DPF_S3_ACCESS_KEY", "AWS_ACCESS_KEY_ID", "COS_ACCESS_KEY"])
    """ Set from DPF_S3_ACCESS_KEY, AWS_ACCESS_KEY_ID or COS_ACCESS_KEY env vars """
    S3_SECRET_KEY = _get_config(["DPF_S3_SECRET_KEY", "AWS_SECRET_ACCESS_KEY", "COS_SECRET_KEY"])
    """ Set from DPF_S3_SECRET_KEY, AWS_SECRET_ACCESS_KEY or COS_SECRET_KEY env vars """
    LAKEHOUSE_TOKEN = _get_config(["DPF_LAKEHOUSE_TOKEN", "LAKEHOUSE_TOKEN"])
    """ Set from DPF_LAKEHOUSE_TOKEN or LAKEHOUSE_TOKEN env vars """

    DEFAULT_LOG_LEVEL = os.environ.get("DPF_LOG_LEVEL", "INFO")


def add_if_missing(config: dict[str, Any], key: str, dflt: Any):
    """
    Add the given default key value if there no value for the key in the dictionary.
    :param config:
    :param key:
    :param dflt:
    :return:
    """
    if config is None:
        return
    value = config.get(key)
    if value is None:
        config[key] = dflt