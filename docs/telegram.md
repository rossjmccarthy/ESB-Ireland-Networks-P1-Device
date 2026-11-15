# The ESB Networks P1 telegram

ESB Networks has not published a technical specification for the P1 port that
this project could find. Its public page covers eligibility, enablement and
safety only.

The register list first came from one third-party report: an analysis by
James Pelow of telegrams from a single-phase Sagemcom XS211, published in
November 2026 by Smart Gateways at
<https://haprofs.com/esb-networks-smart-meter-p1-port-home-assistant/>. Smart
Gateways sells P1 readers, so treat it as a vendor source.

On 14 November 2026 this project confirmed it on its own meter, a
single-phase Sagemcom Siconia: the header, the serial settings, every register
in the table below, and the truncated totals. The front label of that meter
reads Sagemcom Siconia, 230 V, 0.25–5 (100) A, IP54, with P1 and wM-Bus; it
gives the meter family rather than a model code, so it may be the same meter
as the XS211 in the vendor report. If you capture a telegram from your own
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
  meters have two. On this project's meter, hourly readings over
  14 and 15 November 2026 showed:

  | Register | Rate | Counts during (Irish time) |
  | --- | --- | --- |
  | `1.8.1` | Night | 23:00 to 08:00 |
  | `1.8.2` | Day | 08:00 to 17:00 and 19:00 to 23:00 |
  | `1.8.3` | Peak | 17:00 to 19:00 |

  These match the standard smart-meter time bands. They were checked on one
  meter in winter time only, so check your own: watch which register moves at
  a few different times of day.
- **Truncated totals.** `1.8.0` and `2.8.0` carry only the last four digits
  before the decimal point, for example `1897.040` where the meter display
  shows `31897.040`. Confirmed on this project's meter, where the three tariff
  registers add up to a five-digit total and `1.8.0` shows only its last four
  digits. This has been reported to ESB Networks as a bug.
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
- Which other ESB Networks meter models send the same telegram. Confirmed so
  far: a single-phase Sagemcom Siconia (this project) and a single-phase
  Sagemcom XS211 (the vendor report).
- Whether the tariff registers follow the same time bands on every meter and
  plan, and whether the bands shift with summer time.

## Identifiers in the telegram

The header line (`/ESB5\...`, shown in Home Assistant as "Meter
Identification") carries an identifier after the `ESB5\` prefix. Treat it as
private, like your MPRN.

## How often values reach Home Assistant

The meter sends a telegram about once a second. Home Assistant stores a new
database row every time a value changes, so passing every reading on would add
hundreds of thousands of rows a day. The configuration therefore filters each
sensor before sending it:

| Sensors | Sent |
| --- | --- |
| Active power (1.7.0, 2.7.0) | Averaged over 5 s, sent when it moves by 10 W or more, repeated every 60 s |
| Reactive power (3.7.0, 4.7.0) | Averaged over 5 s, sent when it moves by 20 var or more, repeated every 60 s |
| Current (31.7.0) | Averaged over 5 s, sent when it moves by 0.1 A or more, repeated every 60 s |
| Energy registers (1.8.x, 2.8.0) and the rebuilt import total | At most once a minute |
| Reactive energy, power failures, sags and swells | At most once every 5 minutes |
| Meter clock (1.0.0) | Every second, so disabled in Home Assistant by default |

The energy registers are cumulative, so sending them less often loses nothing:
daily and hourly energy figures stay exact. If you need faster power readings,
change the `filters` lines in `esphome/esb-p1-reader.yaml`.

## Sharing a telegram safely

A raw telegram can identify your meter, and a series of them shows when your
home is occupied. Before posting one in an issue:

- replace any serial number or equipment identifier with `X` characters,
- never include your MPRN,
- post a single telegram, not a log.
