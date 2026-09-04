# Airwell TFH Heat Pump Water Heater — Home Assistant custom integration (HACS)

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)
[![Validate](https://github.com/mjvanderveen/airwell_tfh_modbus/actions/workflows/validate.yml/badge.svg)](https://github.com/mjvanderveen/airwell_tfh_modbus/actions/workflows/validate.yml)

Monitor and control an **Airwell TFHA / TFHW / TFHX / TFHZ** heat pump domestic hot water heater
over Modbus, straight from Home Assistant — installable via [HACS](https://hacs.xyz) by adding
this repository's URL directly, while the equivalent Home Assistant Core integration (see
[`core-integration-draft/`](core-integration-draft/)) and its `modbus_connection` dependency work
their way through review.

This integration bundles its own vendored copy of the device library (see
[`library/`](library/) for the canonical, standalone source, and
`custom_components/airwell_tfh/airwell_tfh_modbus/` for the vendored copy actually used at
runtime) and manages its own Modbus TCP / RTU-over-TCP connection, so it has no dependency on an
unpublished PyPI package or on Home Assistant's (not yet released) `modbus_connection`
integration.

> Once `modbus_connection` and the core `airwell_tfh` integration ship in Home Assistant, remove
> this custom component and use the core one instead — see
> [`core-integration-draft/`](core-integration-draft/).

## Features

- **Sensors**: water tank / defrost / ambient / exhaust / return-gas temperature, controller
  status, both alarm-code registers, EEV opening.
- **Binary sensors**: compressor / electric heater / four-way valve / fan relay state, plus the
  high-pressure, low-pressure and condensation hardware alarm contacts.
- **Numbers**: every writable setpoint — target temperature, hysteresis, ambient cut-off,
  backup-heater tuning, sterilization interval, sensor correction, compressor start delay, and
  defrost tuning.
- **Switches**: sterilization enable, Eco-mode backup-heater enable, heat pump enable.
- **Select**: the Auto / Eco / Electric heater / Sterilization operating mode.

## Installation

### Via HACS (custom repository)

1. In HACS, go to **Integrations → ⋮ → Custom repositories**.
2. Add this repository's URL with category **Integration**.
3. Search for "Airwell TFH" in HACS and install it.
4. Restart Home Assistant.
5. Go to **Settings → Devices & Services → Add Integration**, search for "Airwell TFH", and enter
   your Modbus gateway's host, port and unit id.

### Manual

Copy `custom_components/airwell_tfh` into your Home Assistant `config/custom_components/`
directory and restart Home Assistant.

## Connecting to the controller

This integration talks Modbus TCP. If your controller only exposes a serial (RS-485) port, put a
serial-to-Ethernet gateway in RTU mode in front of it (as used during development: a gateway
presenting RTU framing over a TCP socket — Home Assistant's classic `modbus: rtuovertcp` — on
port 5021), and enter that gateway's host/port here.

## Repository layout

This repo holds three related but separate things:

```
custom_components/airwell_tfh/   <- the HACS integration itself (repo root, as HACS requires)
library/                         <- standalone airwell-tfh-modbus device library (own pyproject.toml)
core-integration-draft/          <- speculative home-assistant/core PR draft (see its README warning)
```

`custom_components/airwell_tfh/airwell_tfh_modbus/` is a **vendored copy** of `library/`, kept in
sync by hand — see [`CONTRIBUTING.md`](CONTRIBUTING.md) before changing register definitions.

## Relationship to the other Airwell TFH pieces

1. [`library/`](library/) — the standalone, Home-Assistant-agnostic device library (vendored here
   under `custom_components/airwell_tfh/airwell_tfh_modbus/`).
2. [`core-integration-draft/`](core-integration-draft/) — the equivalent integration structured
   for contribution to `home-assistant/core`. **Currently non-functional against current core**
   — see the warning at the top of its README.
3. **`custom_components/airwell_tfh/`** (repo root) — the same functionality, packaged so the
   community can install and test it today via HACS, without waiting for `modbus_connection` or a
   core PR to merge.

## Development

This repository follows the layout of
[`ludeeus/integration_blueprint`](https://github.com/ludeeus/integration_blueprint). Open it in
VS Code with the dev container (or run `scripts/setup` locally), then:

```bash
scripts/lint     # ruff format + check
scripts/develop  # run a throwaway Home Assistant instance with this component loaded
```

## Reporting register-map issues

The register meanings come from a real, working installation's Home Assistant Modbus
configuration for a TFHA 300L — not an official vendor register table. If your TFHW/TFHX/TFHZ
unit disagrees, please open an issue with a raw register capture (see the
`async_read_raw()` helper on the underlying device object).

## License

MIT. See [LICENSE](LICENSE).
