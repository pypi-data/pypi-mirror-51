"""adutils - helper functions for AppDaemon apps

  @benleb / https://github.com/benleb/adutils
"""

import pprint
from typing import Any, Callable, Dict, Iterable, Optional


def show_info(
    # log: Any,  # log: Callable[[str, bool], None] or something...
    log: Callable[[Any], None],
    app_name: str,
    config: Dict[str, Any],
    sensors: Iterable[str],
    icon: Optional[str] = None,
    legacy_appdaemon: bool = False,
) -> None:
    # output initialized values
    log("")

    if legacy_appdaemon:
        log(app_name)
    else:
        app_name = f"{icon if icon else ''} \033[1m{app_name}\033[0m"
        log(app_name, ascii_encode=bool(icon))

    # output app configuration
    for key, value in config.items():

        if key == "delay":
            value = f"{int(value / 60)}:{int(value % 60):02d} minutes ~ {value} seconds"

        if isinstance(value, list):
            log(f"  {key}:")

            for list_value in value:

                if isinstance(list_value, dict):
                    name = list_value.pop("name", "")
                    log(
                        f"    - \033[1m{name}\033[0m: {pprint.pformat(list_value, compact=True)}"
                    )
                else:
                    log(f"    - \033[1m{list_value}\033[0m")

                continue
        else:
            log(f"  {key}: \033[1m{value}\033[0m")

    if sensors:
        log(f"  state listener:")
        _ = [log(f"    - \033[1m{sensor}\033[0m") for sensor in sorted(sensors)]

    log("")
