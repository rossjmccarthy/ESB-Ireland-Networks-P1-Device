# The ESB Networks P1 telegram

ESB Networks has not published a technical specification for the P1 port that
this project could find. Its public page covers eligibility, enablement and
safety only.

Everything below comes from one third-party report: an analysis by James Pelow
of telegrams from a single-phase Sagemcom XS211, published in November 2026 by
Smart Gateways at
<https://haprofs.com/esb-networks-smart-meter-p1-port-home-assistant/>. Smart
Gateways sells P1 readers, so treat it as a vendor source. This project has not
yet confirmed any of it on a meter. If you capture a telegram from your own
meter, please open an issue (redact it first, see below).

## Format

- DSMR 5-style plain-text telegram, sent about once per second.
- Header starts `/ESB5\`.
- Ends with a CRC16 checksum.
- Not encrypted.
- Electricity only. There are no gas or water channels.

## Registers reported (single-phase)

| OBIS code | Meaning | ESPHome `dsmr` key |
| --- | --- | --- |
| `0-0:1.0.0` | Meter clock | `timestamp` |
| `1-0:1.8.0` | Total energy imported (truncated, see below) | `energy_delivered_lux` |
| `1-0:1.8.1` | Energy imported, tariff 1 | `energy_delivered_tariff1` |
| `1-0:1.8.2` | Energy imported, tariff 2 | `energy_delivered_tariff2` |
| `1-0:1.8.3` | Energy imported, tariff 3 | `energy_delivered_tariff3` |
| `1-0:2.8.0` | Total energy exported (truncated, see below) | `energy_returned_lux` |
| `1-0:3.8.0` | Reactive energy imported | `total_imported_energy` |
| `1-0:4.8.0` | Reactive energy exported | `total_exported_energy` |
| `1-0:1.7.0` | Instantaneous power imported (kW) | `power_delivered` |
| `1-0:2.7.0` | Instantaneous power exported (kW) | `power_returned` |
| `1-0:3.7.0` | Instantaneous reactive power imported | `reactive_power_delivered` |
| `1-0:4.7.0` | Instantaneous reactive power exported | `reactive_power_returned` |
| `1-0:31.7.0` | Current, L1 (A) | `current_l1` |
| `0-0:96.7.21` | Number of power failures | `electricity_failures` |
| `1-0:32.32.0` | Voltage sags, L1 | `electricity_sags_l1` |
| `1-0:32.36.0` | Voltage swells, L1 | `electricity_swells_l1` |
| `0-0:96.3.10` | Supply switch position | `electricity_switch_position` |

## Differences from Dutch and Belgian meters

- **Three import tariff registers** (`1.8.1`, `1.8.2`, `1.8.3`), where Dutch
  meters have two. The source describes them as day, night and peak. Confirm
  the order against the codes on your own meter's display before relying on it.
- **Truncated totals.** `1.8.0` and `2.8.0` are reported to carry only the last
  four digits before the decimal point, for example `1897.040` where the meter
  display shows `31897.040`. This has been reported to ESB Networks as a bug.
  - Import: the config rebuilds the total as the sum of the three tariff
    registers, which are sent in full.
  - Export: no export tariff registers are sent, so the total cannot be
    rebuilt. Home Assistant's Energy dashboard only uses the change between
    readings, so a truncated value still gives correct daily figures. When
    the value wraps past 9999.999, Home Assistant treats the drop as a meter
    reset and carries on counting.
- **No export tariff registers.**

## Unknowns

- Three-phase meters.
- Any ESB Networks meter model other than the Sagemcom XS211.
- Whether the telegram contains a meter serial number or other identifier
  beyond the header line.

## Sharing a telegram safely

A raw telegram can identify your meter, and a series of them shows when your
home is occupied. Before posting one in an issue:

- replace any serial number or equipment identifier with `X` characters,
- never include your MPRN,
- post a single telegram, not a log.
