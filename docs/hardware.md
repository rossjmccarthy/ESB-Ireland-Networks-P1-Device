# Hardware and wiring

Read the safety section of the [README](../README.md) first. Everything here
connects to the customer P1 socket only. Nothing in this project involves
opening the meter, breaking a seal or touching mains wiring.

## What the P1 port provides

| Property | Value |
| --- | --- |
| Connector | RJ12 (6P6C) |
| Serial | 115200 baud, 8 data bits, no parity, 1 stop bit |
| Data line | Open collector, logically inverted |
| Power | 5 V from the meter |
| Update rate | About one telegram per second |

The connector, serial settings and 5 V supply are as reported for an ESB
Networks Sagemcom XS211 (see [telegram.md](telegram.md) for the source).

## Pinout

ESB Networks has not published a pinout that this project could find. The table
below is the pinout from the Dutch DSMR 5.0.2 P1 Companion Standard. Readers
built to that pinout are reported to work on ESB Networks meters, including
taking their power from the port, so it is very likely correct.

![RJ12 pin numbering. On the plug, held with the gold contacts facing you, the tip pointing up and the latch tab on the back, pin 1 is the leftmost contact. On the meter socket, seen from the front with the latch notch at the bottom, pin 1 is the leftmost contact.](images/rj12-pinout.svg)

Pin numbers are fixed relative to the latch, not to left and right on your
meter. If the socket on your meter has its latch notch at the top, pin 1 is on
the right as you look at it.

| RJ12 pin | Signal | Connect to |
| --- | --- | --- |
| 1 | +5 V power | ESP32 `5V` / `VIN` (see "Power" below) |
| 2 | Data request | RJ12 pin 1 (+5 V) |
| 3 | Data ground | ESP32 `GND` |
| 4 | Not connected | Leave unconnected |
| 5 | Data out | ESP32 RX GPIO, with a pull-up resistor to **3.3 V** |
| 6 | Power ground | ESP32 `GND` |

### Check before you connect the board

Wiring this backwards swaps +5 V and ground, which can destroy the board. Do
all three checks first.

1. **Count the contacts.** The plug must have six gold contacts (RJ12, 6P6C).
   A plug with four is RJ11: it fits the socket but has no pin 1 or pin 6, so
   it carries no power.
2. **Do not trust wire colours or the cable.** Colours are not standardised.
   Many flat telephone-style cables are "reversed": pin 1 at one end is pin 6
   at the other. If you use a plug-to-plug cable into a breakout socket, a
   reversed cable flips the whole pinout. Use a multimeter's continuity mode
   to find which wire or terminal really goes to pin 1 of the plug that enters
   the meter.
3. **Measure the voltage and its polarity.** With the P1 port enabled, plug
   the cable into the meter with nothing connected at the other end, and keep
   the bare ends apart. Put the multimeter's red probe on the wire you believe
   is pin 1 and the black probe on pin 6. You should read about **+5 V**. A
   reading of about −5 V means the cable is reversed. No reading means the
   port is not enabled, the plug is not seated, or the cable lacks pins 1
   and 6.

Notes:

- **Data request (pin 2).** In the DSMR standard the meter only sends while
  this line is held at 5 V. Tying it to pin 1 makes the meter send
  continuously. Whether ESB Networks meters need this has not been confirmed
  here, and tying it high is harmless either way.
- **Pull-up on the data line (pin 5).** The output is open collector, so it
  needs a pull-up. Use a resistor of 1 kΩ to 4.7 kΩ from the data line to the
  ESP32's **3.3 V** pin. Do not pull it up to 5 V: ESP32 GPIOs are not 5 V
  tolerant.
- **Inversion.** The signal is inverted compared with normal UART. The config
  handles this in software with `inverted: true`, so no transistor is needed.

## Power

The DSMR standard allows a reader to draw up to 250 mA at 5 V from pin 1. An
ESP32 averages well under that, but its Wi-Fi transmit bursts can briefly
exceed it, and some meters are reported to supply less. If the board resets or
fails to boot when powered from the meter:

- add a bulk capacitor (470 µF or more) between 5 V and ground at the board, or
- lower the ESP32's power draw in the config (lower `cpu_frequency`, Wi-Fi
  `power_save_mode: HIGH`, reduced `output_power`), or
- power the board from a USB supply instead (see below).

Do not connect USB power and the meter's 5 V to the board at the same time
unless you know your board isolates the two supplies. Many development boards
do not, and you would be back-feeding one supply into the other. The simplest
rule: when flashing over USB, unplug the RJ12 cable.

### Running the board from USB power

If the board runs from a USB supply, the meter's 5 V must not reach the board's
5 V pin. The only wire that changes is the one from RJ12 pin 1 to the board:
leave it out.

| RJ12 pin | Powered by the meter | Powered by USB |
| --- | --- | --- |
| 1 (+5 V) | ESP32 `5V` **and** RJ12 pin 2 | RJ12 pin 2 **only** |
| 2 (Data request) | RJ12 pin 1 | RJ12 pin 1 |
| 3 (Data ground) | ESP32 `GND` | ESP32 `GND` |
| 5 (Data out) | RX GPIO, pull-up to 3.3 V | RX GPIO, pull-up to 3.3 V |
| 6 (Power ground) | ESP32 `GND` | ESP32 `GND` |

Pins 1 and 2 stay joined to each other in both cases. That link is what holds
the data request line at 5 V, using the meter's own supply, so the meter keeps
sending. It never touches the board when the board is on USB power. Both
ground pins stay connected in both cases: the data signal needs a shared
ground.

## Reference board: ESP32-C6-WROOM-1

The configuration defaults to an ESP32-C6-WROOM-1 module on an
ESP32-C6-DevKitC-1 board, with the P1 data line on **GPIO6**.

| Pins | Why to avoid them for RX |
| --- | --- |
| GPIO4, 5, 8, 9, 15 | Strapping pins, read at boot. GPIO8 also drives the DevKitC's RGB LED and GPIO9 is the BOOT button |
| GPIO12, 13 | Native USB (the DevKitC's "USB" port) |
| GPIO16, 17 | UART0, wired to the DevKitC's USB-to-serial chip ("UART" port) |

GPIO6 is none of these. If your module is on a different carrier board, check
that GPIO6 is broken out and free, or pick another pin outside the table and
change `rx_pin`.

The DevKitC-1 has two USB-C ports. Either can flash the board. ESPHome sends
its log to the native "USB" port by default on the C6, and the web flasher can
only ask for your Wi-Fi details over that port, so use the one labelled "USB".

The ESP32-C6 is a 2.4 GHz device (Wi-Fi 6). It does not use 5 GHz.

## Using a different board

Any ESP32 board that ESPHome supports should work. Set `board`, `variant` and
`rx_pin` in [`esphome/esb-p1-reader.yaml`](../esphome/esb-p1-reader.yaml) to
match, for example `esp32dev` and `esp32` for a classic ESP32.

- Avoid your chip's strapping pins for RX (on the classic ESP32: GPIO0, 2, 5,
  12 and 15).
- A small board is easier to fit. Meter boxes are tight and often outdoors.
- A ready-made P1 reader that already runs ESPHome needs no wiring at all.
  Use its manufacturer's pin assignment for `rx_pin`.

## Fitting it

- Keep the cable short. At 115200 baud the DSMR standard limits the cable to
  a couple of metres. Put the board at the meter and let Wi-Fi cover the
  distance.
- Check Wi-Fi reaches the meter box before you build anything.
- The device must be removable without tools. Do not glue, screw or tape
  anything to the meter. ESB Networks will unplug it if they exchange the meter.
- Outdoor meter boxes get damp. Put the board in an enclosure.
