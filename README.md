# ESB Networks P1 Reader

Read near real-time electricity data from the P1 port of an ESB Networks
(Ireland) smart meter with an ESP32 board, and send it to Home Assistant over
your own network.

The firmware is [ESPHome](https://esphome.io/). This repository provides a
configuration for it, wiring notes for a generic ESP32, and what is known so
far about the Irish telegram format.

> **Status: early.** The configuration passes ESPHome's validation but this
> project has not yet confirmed it on a meter. The register list comes from a
> single third-party report on one meter model. See
> [docs/telegram.md](docs/telegram.md).

This is an independent community project. It is not affiliated with, endorsed
by or supported by ESB Networks.

> **Read the [disclaimer](DISCLAIMER.md) before you connect anything.** Use of
> the P1 port is subject to ESB Networks' conditions, a self-built device is
> not a certified product, and you fit one entirely at your own risk.

## Before you start

### Check your meter can do this

ESB Networks enabled customer access to the P1 port in November 2026. Not every
smart meter has the port.

1. Log in to your [ESB Networks online account](https://www.esbnetworks.ie/).
2. Go to **Access Additional Meter Data Services**, then **Manage my P1 Port**.
3. If you can enable the port, do so. It takes up to an hour and needs no
   technician visit. If the account says the functionality is unavailable, your
   meter has no P1 port and this project cannot help yet.

Do this before buying or building anything.

### Safety and ESB Networks' conditions

These come from ESB Networks'
[near real-time data page](https://www.esbnetworks.ie/about-us/company/data-and-digital/accessing-near-real-time-data).
Read that page in full: it is the authority, and it can change. The fuller list
is in the [disclaimer](DISCLAIMER.md). In summary:

- **Do not fit a device where there are multiple meters**, such as the shared
  meter cabinet of an apartment block. ESB Networks does not permit it and will
  remove the device without notice.
- **Look before you touch.** If you see water in the meter box, exposed wires,
  broken parts, removed seals or signs of heating or charring, stop and phone
  ESB Networks on 1800 372 999.
- **Use no tools** in or near the meter box. The P1 socket takes a plug by hand.
- **The device must be detachable.** If ESB Networks exchanges your meter they
  will unplug it and leave it in the meter box.
- **You carry the risk.** ESB Networks accepts no liability for damage arising
  from a device connected to the P1 port, and offers no support for it.

Two further points specific to a self-built device:

- ESB Networks advises buying devices that carry a CE mark. A board you wire
  and flash yourself is not a certified product. If that matters to you, buy a
  CE-marked P1 reader that runs ESPHome and use this configuration on it.
- This project only ever connects to the low-voltage customer socket. Never
  open the meter, break a seal or touch the mains wiring.

### Privacy

One reading per second shows when your home is occupied and which appliances
are running. The configuration keeps the data on your own network, over an
encrypted connection to Home Assistant. ESB Networks is not the data controller
for P1 data: what happens to it is up to you. Do not post raw telegrams, your
MPRN or your `secrets.yaml` publicly.

## What you need

- An ESB Networks smart meter with the P1 port enabled.
- An ESP32 board, or a ready-made P1 reader that runs ESPHome. The
  configuration defaults to an ESP32-C6-WROOM-1 on an ESP32-C6-DevKitC-1.
- An RJ12 (6P6C) cable.
- A resistor of 1 kΩ to 4.7 kΩ, if you are wiring a bare board.
- Home Assistant with the ESPHome integration.

Wiring is in [docs/hardware.md](docs/hardware.md).

## Flashing

1. Install ESPHome: either the ESPHome add-on in Home Assistant or the
   [command-line tool](https://esphome.io/install/).
2. Copy `esphome/secrets.yaml.example` to `esphome/secrets.yaml` and fill in
   your own values. Generate your own API key; do not reuse one from a guide.
3. Edit the `substitutions` at the top of `esphome/esb-p1-reader.yaml` so
   `board`, `variant` and `rx_pin` match your hardware.
4. With the RJ12 cable unplugged, connect the board by USB and run:

   ```bash
   esphome run esphome/esb-p1-reader.yaml
   ```

5. Unplug USB, connect the board to the meter, and add the device in Home
   Assistant when it is discovered.

Later changes can be flashed over Wi-Fi.

## Home Assistant Energy dashboard

- **Grid consumption:** `Import Total (sum of tariffs)`
- **Return to grid:** `Export Total as sent (2.8.0)`

The meter's own import total (`1.8.0`) is reported to be truncated, which is
why the configuration provides a rebuilt one. Details are in
[docs/telegram.md](docs/telegram.md).

## Troubleshooting

| Symptom | Likely cause |
| --- | --- |
| No data at all | P1 port not enabled yet, data request pin not tied to 5 V, or RJ12 not fully seated |
| CRC errors in the log | Missing or too-weak pull-up on the data line, `inverted: true` removed, or cable too long |
| Board resets or will not boot on meter power | The port cannot supply the Wi-Fi current peaks. See "Power" in [docs/hardware.md](docs/hardware.md) |
| `1.8.0` does not match the meter display | Known truncation. Use `Import Total (sum of tariffs)` |

## Contributing

Reports from other meter models and from three-phase meters are the most useful
thing you can add. Please redact telegrams before posting them. See "Sharing a
telegram safely" in [docs/telegram.md](docs/telegram.md).

## Credits

- The Irish register list and the telegram quirks were first documented by
  James Pelow and published by Smart Gateways at
  [haprofs.com](https://haprofs.com/esb-networks-smart-meter-p1-port-home-assistant/).
  The configuration here was written independently from those documented facts.
- [ESPHome](https://esphome.io/) and its
  [DSMR component](https://esphome.io/components/sensor/dsmr/) do the real work.

## Licence

[MIT](LICENSE). Provided as is, with no warranty. See the
[disclaimer](DISCLAIMER.md).
