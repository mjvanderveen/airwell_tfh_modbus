"""Tests for the top-level AirwellTFH device object."""

from __future__ import annotations

from airwell_tfh_modbus import AlarmCode1, ControllerStatus, OperationMode


async def test_sensors_decode_scaled_temperatures(device, mock_modbus_unit):
    """Input registers decode as signed, 0.1-scaled temperatures."""
    mock_modbus_unit.input[0] = 512  # 51.2 degC
    mock_modbus_unit.input[2] = 0xFFCE  # -50 as int16 -> -5.0 degC

    await device.async_update()

    assert device.sensors.water_tank_temperature == 51.2
    assert device.sensors.ambient_temperature == -5.0


async def test_relays_and_alarms_are_independent_bit_spaces(device, mock_modbus_unit):
    """Coils and discrete inputs are read independently, by address."""
    mock_modbus_unit.coils[0] = True
    mock_modbus_unit.discrete_inputs[6] = True

    await device.async_update()

    assert device.relays.compressor is True
    assert device.relays.fan is False
    assert device.alarms.low_pressure is True
    assert device.alarms.high_pressure is False


async def test_controller_status_and_alarms_decode_to_enums(device, mock_modbus_unit):
    """Holding registers 1101-1104 decode to the documented enums."""
    mock_modbus_unit.holding[1101] = 3
    mock_modbus_unit.holding[1102] = 1
    mock_modbus_unit.holding[1104] = 2

    await device.async_update()

    assert device.controller.controller_status is ControllerStatus.HEATING
    assert device.controller.alarm_register_1 is AlarmCode1.HIGH_PRESSURE
    assert device.controller.operation_mode is OperationMode.ELECTRIC_HEATER


async def test_writing_the_operation_mode(device, mock_modbus_unit):
    """Writing operation_mode sends the enum's raw value to register 1104."""
    await device.controller.write("operation_mode", OperationMode.STERILIZATION)

    assert mock_modbus_unit.holding[1104] == 3


async def test_writing_the_target_temperature(device, mock_modbus_unit):
    """Writing a Settings field sends its raw (unscaled) value."""
    await device.settings.write("target_temperature", 55)

    assert mock_modbus_unit.holding[10] == 55


async def test_identity_is_read_once_but_polled_components_read_every_update(
    device, mock_modbus_unit
):
    """The identity block is not re-read on a second async_update()."""
    mock_modbus_unit.holding[1000] = 300

    await device.async_update()
    assert device.info.model_code == 300

    reads_after_first = len(mock_modbus_unit.read_events)
    await device.async_update()
    reads_after_second = len(mock_modbus_unit.read_events)

    assert reads_after_second > reads_after_first

    identity_reads = [
        e
        for e in mock_modbus_unit.read_events
        if e.register_type == "holding" and e.address <= 1000 < e.address + e.count
    ]
    assert len(identity_reads) == 1
