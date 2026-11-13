# Disclaimer

Read this before you connect anything to your meter.

## No affiliation

This is an independent community project. It is not affiliated with, endorsed
by, approved by or supported by ESB Networks, ESB or any electricity supplier.
"ESB Networks" is used only to describe the meters this project is intended to
work with.

## ESB Networks' requirements apply to you

Use of the P1 port is on ESB Networks' terms, not this project's. Their current
conditions are published at
<https://www.esbnetworks.ie/about-us/company/data-and-digital/accessing-near-real-time-data>.
That page is the authority. Read it in full, and check it again before you
install, because the conditions can change. If anything in this repository
conflicts with it, follow ESB Networks.

As that page stood in November 2026, the conditions included:

- **Enablement.** The P1 port is disabled by default. It can only be enabled
  through an ESB Networks online account, not by a technician visit. A device
  will not work until the port shows as enabled.
- **No multi-meter locations.** You are not permitted to install a P1 device
  where your meter is in a multi-meter cabinet, such as in an apartment block.
  A device found there will be removed without notice.
- **Safety check first.** If you see water in the meter box, exposed wires,
  broken parts on the meter or other equipment, removed seals, or signs of
  heating or charring, stop. Do not attach anything, and contact ESB Networks
  immediately on 1800 372 999.
- **No tools.** Do not use any tool with a sharp edge or point, or any drill,
  in the meter box or close to the meter.
- **Detachable only.** The device must not be a permanent connection. If ESB
  Networks exchanges your meter, they will remove the device and leave it in
  the meter box, and the port may need to be enabled again afterwards.
- **No support or liability from ESB Networks.** ESB Networks does not supply,
  endorse or support third-party devices and does not guarantee compatibility.
  It accepts no liability for damage or issues arising from installing or using
  a device. Damage caused by incorrect installation is the customer's
  responsibility.
- **Certified devices.** ESB Networks advises that devices should come from a
  reputable manufacturer, meet the relevant European safety standards and carry
  the CE mark.
- **Your data, your responsibility.** ESB Networks is not the controller or
  processor of data obtained through the P1 port and is not responsible for
  managing or protecting it. Data read from the port is not validated by ESB
  Networks and may differ slightly from the data in your online account.

## A self-built device is not a certified product

A development board that you wire and flash yourself has not been tested or
certified as a finished product and does not carry a CE mark as one. It
therefore does not meet ESB Networks' advice on certified devices. Whether to
build one anyway is your decision and your risk. If you want a certified
device, buy a CE-marked P1 reader that runs ESPHome and load this project's
configuration onto it.

## What this project never asks you to do

- Open the meter or remove any cover other than the P1 port's own cover.
- Break, remove or tamper with a seal.
- Touch mains wiring or any terminal.
- Alter, bypass or interfere with metering.

Interfering with a meter is dangerous and is an offence. If any guide, including
a contribution to this repository, tells you to do one of these things, do not
follow it.

## No warranty

The software and documentation are provided "as is" under the
[MIT License](LICENSE), without warranty of any kind. The authors and
contributors accept no liability for damage to your meter, your equipment or
your property, for injury, for loss of data, for incorrect readings, or for any
dispute with ESB Networks or your supplier arising from use of this project.

The technical information here is incomplete. ESB Networks has not published a
technical specification for the P1 port, and parts of this project rely on
third-party reports and on the Dutch DSMR standard. See
[docs/telegram.md](docs/telegram.md) and [docs/hardware.md](docs/hardware.md)
for what is and is not confirmed.

## Not for billing

Readings from the P1 port are for your own information. Do not use them to
dispute a bill without also checking the validated data in your ESB Networks
online account.

## If in doubt

Do not connect the device. Contact ESB Networks (1800 372 757 for P1 port
queries, 1800 372 999 for safety concerns) or a registered electrical
contractor.
