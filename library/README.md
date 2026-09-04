# `airwell-tfh-modbus` Python library

[![CI](https://github.com/mjvanderveen/airwell_tfh_modbus/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/mjvanderveen/airwell_tfh_modbus/actions/workflows/ci.yml)
[![PyPI](https://img.shields.io/pypi/v/airwell-tfh-modbus.svg)](https://pypi.org/project/airwell-tfh-modbus/)
[![Python](https://img.shields.io/pypi/pyversions/airwell-tfh-modbus.svg)](https://pypi.org/project/airwell-tfh-modbus/)
[![License](https://img.shields.io/github/license/mjvanderveen/airwell_tfh_modbus.svg)](LICENSE)

`airwell-tfh-modbus` is an asynchronous, transport-independent Python library for communicating
with Airwell TFH-series heat pump water heaters over Modbus.

## Purpose and scope

The library:

* contains the device's Modbus register map — sensors, relays, alarms, settings and controller
  status — as a typed Python data model, including scaling, units, and which registers are
  writable,
* exposes controller identity (manufacturer, model code, firmware code),
* does not create or own the Modbus transport. Applications using the library provide a
  [`modbus_connection.ModbusUnit`](https://github.com/home-assistant-libs/modbus-connection) and
  may use any backend supported by `modbus-connection` (`tmodbus`, `pymodbus`, ...).

An example script [`script/query.py`](script/query.py) shows how to build an application that
queries a real controller over Modbus/TCP, Modbus RTU-over-TCP (a serial-to-Ethernet gateway), or
a local serial port.

## Supported controllers

| Model | Storage capacity | Comments |
| :---- | :---------------: | :------- |
| Airwell TFHA 300L | 300 L | Reference unit this library was validated against |
| Airwell TFHW | — | Shares the "Modbus Table TFHW/TFHX/TFHZ" register map |
| Airwell TFHX | — | Shares the "Modbus Table TFHW/TFHX/TFHZ" register map |
| Airwell TFHZ | — | Shares the "Modbus Table TFHW/TFHX/TFHZ" register map |

Note: the TFHW/TFHX/TFHZ models have not been independently verified against real hardware by
this project. They are listed because Airwell documents them against the same register table as
the TFHA. Please open an issue (or better, a PR to [`tests/test_device.py`](tests/test_device.py)
with a captured register snapshot) if you find a difference.

## Data provided by the library

* controller identity (manufacturer, model code, firmware code),
* measured temperatures: water tank, defrost/evaporator, ambient, exhaust gas, return gas,
* actuator relay states: compressor, electric heater, four-way valve, fan,
* hardware alarm contacts: high pressure, low pressure, condensation,
* controller-wide status, two alarm-code registers, and the user-selectable operating mode
  (Auto / Eco / Electric heater / Sterilization),
* writable settings: target temperature, hysteresis, ambient cut-off, backup-heater behaviour,
  sterilization schedule, sensor correction, compressor start delay, and defrost tuning.

The exact meaning of a handful of registers (`electric_heater_mode`, `eev_opening`) is not
publicly documented; they are exposed as raw values rather than guessed enums. See the docstrings
in [`src/airwell_tfh_modbus/subsystems/`](src/airwell_tfh_modbus/subsystems/) for details.

## Installation

```bash
pip install airwell-tfh-modbus[tmodbus]
# or
pip install airwell-tfh-modbus[pymodbus]
```

## Usage

```python
import asyncio

from airwell_tfh_modbus import AirwellTFH, OperationMode
from modbus_connection import ModbusTcpParams
from modbus_connection.tmodbus import ModbusConnection


async def main() -> None:
    connection = ModbusConnection(ModbusTcpParams(host="192.0.2.10", port=5021, framer="rtu"))
    try:
        unit = connection.for_unit(1)
        device = AirwellTFH(unit)
        await device.async_update()

        print("Water tank:", device.sensors.water_tank_temperature, "°C")
        print("Mode:", device.controller.operation_mode)

        await device.controller.write("operation_mode", OperationMode.ECO)
        await device.settings.write("target_temperature", 55)
    finally:
        await connection.close()


asyncio.run(main())
```

## Testing and validation

Automated tests run against the in-memory Modbus mock shipped with `modbus-connection` (no
hardware required); see [`tests/`](tests/). The register map itself was derived from an
installer's own Home Assistant Modbus configuration for a live Airwell TFHA 300L unit.

## Development

```bash
script/setup   # install runtime + dev dependencies
script/lint    # ruff format + check
script/test    # pytest
```

## Contribution guidelines

Contributions are welcome — issues, register-map corrections for the TFHW/TFHX/TFHZ variants, and
pull requests. Please run `script/lint` and `script/test` before opening a PR.

## License

Apache-2.0. See [LICENSE](LICENSE).
