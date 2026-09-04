# Airwell TFH — Home Assistant Core integration (speculative, currently non-functional)

> [!WARNING]
> **This integration does not work against current Home Assistant core.** It depends on
> `homeassistant.components.modbus_connection`, which was
> [added to `core`'s `dev` branch on 2026-07-05](https://github.com/home-assistant/core/commit/0e1c190eec4c81914b6a3696794f32b8d3d15778)
> (#175407) and then
> [removed again on 2026-07-16](https://github.com/home-assistant/core/commit/a55511f3fb008e6669326a14f16ad7555e85b5ce)
> (#176618), 11 days later. It is not present in `dev`/`main` today, and does not appear in any
> `manifest.json` or `requirements_all.txt` in the current tree.
>
> The [`trovis557x-integration`](https://github.com/home-assistant/core/tree/trovis557x-integration/homeassistant/components/trovis557x)
> branch this folder mirrors is an orphaned artifact of that same, since-reverted experiment (it
> sits thousands of commits behind `dev`), not a live, mergeable PR.
>
> **If you want something you can actually install and test today, use
> [`../custom_components/airwell_tfh`](../custom_components/airwell_tfh) (this repo's HACS
> integration) instead** — it vendors the device library and owns its Modbus connection
> directly, with no dependency on `modbus_connection`.
>
> This folder is kept as a forward-looking design: if Home Assistant revisits shared Modbus
> connections in the future, most of this code should still be a reasonable starting point. Until
> then, treat it as a reference sketch, not something to copy into a real PR.

This folder is a drop-in `homeassistant/components/airwell_tfh` integration, structured to be
copied into a [`home-assistant/core`](https://github.com/home-assistant/core) checkout and opened
as a pull request — mirroring the pattern used by the (now-reverted, see warning above)
[`trovis557x`](https://github.com/home-assistant/core/tree/trovis557x-integration/homeassistant/components/trovis557x)
integration.

It reads and controls an Airwell TFHA/TFHW/TFHX/TFHZ heat pump water heater via the
[`airwell-tfh-modbus`](../library) device library, on top of Home Assistant's
`modbus_connection` shared-connection integration (see
[developers.home-assistant.io/docs/modbus/introduction](https://developers.home-assistant.io/docs/modbus/introduction)) —
**which does not currently exist in Home Assistant core; see the warning above.**

## Why this depends on `modbus_connection`

This integration does not open its own Modbus socket. It borrows a `ModbusUnit` from a
`modbus_connection` config entry (selected by the user in the config flow) via
`homeassistant.components.modbus_connection.async_get_unit`, so multiple integrations pointed at
the same physical Modbus link share one connection instead of competing for it.

At the time this was written, `modbus_connection` had already been merged into `home-assistant/core`'s
`dev` branch once (2026-07-05, #175407) and reverted eleven days later (2026-07-16, #176618). It is
not present in current `dev`/`main`. This folder therefore assumes a checkout where
`modbus_connection` (and its `ModbusUnit` / `async_get_unit` / `ConnectionNotReady` API) has been
reintroduced — which is not the case today.

## How to use this folder

0. **Prerequisite**: this only imports successfully in a checkout that has a working
   `homeassistant.components.modbus_connection` (`async_get_unit`, `ConnectionNotReady`, a
   `ConfigEntrySelector(integration="modbus_connection")`-compatible config entry type). As of
   this writing that means checking out core at or before commit `0e1c190e` (2026-07-05) and
   before its revert at `a55511f3` (2026-07-16), or re-vendoring that removed component yourself.
   Without it, steps 1-6 below will not result in a working integration.
1. Clone `home-assistant/core` and create a feature branch.
2. Copy `homeassistant/components/airwell_tfh/` into the checkout's
   `homeassistant/components/` directory.
3. Copy `tests/components/airwell_tfh/` into the checkout's `tests/components/` directory.
4. Add `airwell-tfh-modbus` to the checkout's `requirements_all.txt` /
   `requirements_test_all.txt` (`python3 -m script.gen_requirements_all`) once the library is
   published to PyPI.
5. `manifest.json` already lists `@mjvanderveen` as codeowner — add yourself to core's
   top-level `CODEOWNERS` file too.
6. Run `pytest tests/components/airwell_tfh` and `python3 -m script.hassfest` from the checkout
   root, then open the PR.

## What it exposes

* **Sensors** (diagnostic): water tank / defrost / ambient / exhaust / return-gas temperature,
  controller status, both alarm-code registers, EEV opening.
* **Binary sensors**: compressor / electric heater / four-way valve / fan relay state, and the
  three hardware alarm contacts (high pressure, low pressure, condensation).
* **Numbers** (config): every writable holding-register setpoint (target temperature, hysteresis,
  ambient cut-off, backup-heater tuning, sterilization interval, sensor correction, compressor
  start delay, defrost tuning).
* **Switches** (config): sterilization enable, Eco-mode backup-heater enable, heat pump enable.
  * **Select**: the Auto / Eco / Electric heater / Sterilization operating mode.

## Quality scale

See [`quality_scale.yaml`](homeassistant/components/airwell_tfh/quality_scale.yaml). Bronze tier
is fully met; several Silver/Gold/Platinum items are marked `todo` because they depend on
maintainer-facing steps (docs pages, `CODEOWNERS`, `strict-typing` config) that only make sense
once this lives inside an actual `home-assistant/core` checkout.

## License

Intended for inclusion in `home-assistant/core`, licensed Apache-2.0 like the rest of that
project. No separate `LICENSE` file is included here for that reason.
