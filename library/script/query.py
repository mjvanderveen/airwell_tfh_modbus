"""Query a real Airwell TFH controller over Modbus and print every reading.

Usage::

    python script/query.py --host 192.0.2.10 --port 5021 --unit 1

The device in this repository's origin was reached with a serial-to-Ethernet
gateway presenting RTU framing over a TCP socket (Home Assistant's
``rtuovertcp``), which is why the example below asks tmodbus for RTU framing
over a plain TCP connection. Pass ``--serial`` to use a local serial port
instead.
"""

from __future__ import annotations

import argparse
import asyncio

from modbus_connection import ModbusSerialParams, ModbusTcpParams
from modbus_connection.tmodbus import ModbusConnection

from airwell_tfh_modbus import AirwellTFH


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", help="Modbus TCP/RTU-over-TCP gateway host")
    parser.add_argument("--port", type=int, default=502, help="TCP port (default: 502)")
    parser.add_argument("--serial", help="Local serial device, e.g. /dev/ttyUSB0")
    parser.add_argument("--baudrate", type=int, default=9600)
    parser.add_argument("--unit", type=int, default=1, help="Modbus unit/slave id")
    return parser.parse_args()


async def main() -> None:
    """Connect, read everything once, and print the decoded values."""
    args = _parse_args()

    if args.serial:
        params = ModbusSerialParams(port=args.serial, baudrate=args.baudrate)
    else:
        if not args.host:
            msg = "Pass --host (RTU-over-TCP/TCP gateway) or --serial (local port)."
            raise SystemExit(msg)
        params = ModbusTcpParams(host=args.host, port=args.port, framer="rtu")

    connection = ModbusConnection(params)
    try:
        unit = connection.for_unit(args.unit)
        device = AirwellTFH(unit)
        await device.async_update()

        print(f"Model: {device.info.model} (code {device.info.model_code})")
        print(f"Firmware code: {device.info.software_version}")
        print()
        print("Sensors:")
        for name in (
            "water_tank_temperature",
            "defrost_temperature",
            "ambient_temperature",
            "exhaust_temperature",
            "return_gas_temperature",
        ):
            print(f"  {name}: {getattr(device.sensors, name)}")
        print("Relays:")
        for name in ("compressor", "electric_heater", "four_way_valve", "fan"):
            print(f"  {name}: {getattr(device.relays, name)}")
        print("Alarms:")
        for name in ("high_pressure", "low_pressure", "condensation"):
            print(f"  {name}: {getattr(device.alarms, name)}")
        print("Controller:")
        for name in (
            "controller_status",
            "alarm_register_1",
            "alarm_register_2",
            "operation_mode",
            "eev_opening",
        ):
            print(f"  {name}: {getattr(device.controller, name)}")
    finally:
        await connection.close()


if __name__ == "__main__":
    asyncio.run(main())
