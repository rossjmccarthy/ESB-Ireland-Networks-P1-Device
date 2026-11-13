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
taking their power from the port, so it is very likely correct. Check with a
multimeter before connecting a board: you should see about 5 V between pin 1
and pin 6.

| RJ12 pin | Signal | Connect to |
| --- | --- | --- |
| 1 | +5 V power | ESP32 `5V` / `VIN` (see "Power" below) |
| 2 | Data request | RJ12 pin 1 (+5 V) |
| 3 | Data ground | ESP32 `GND` |
| 4 | Not connected | Leave unconnected |
| 5 | Data out | ESP32 RX GPIO, with a pull-up resistor to **3.3 V** |
| 6 | Power ground | ESP32 `GND` |

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
- power the board from USB instead and leave RJ12 pin 1 disconnected from the
  board's 5 V pin (pin 2 still goes to pin 1).

Do not connect USB power and the meter's 5 V to the board at the same time
unless you know your board isolates the two supplies. Many development boards
do not, and you would be back-feeding one supply into the other. The simplest
rule: when flashing over USB, unplug the RJ12 cable.

## Choosing a board

Any ESP32 board that ESPHome supports should work. Set `board` and `rx_pin` in
[`esphome/esb-p1-reader.yaml`](../esphome/esb-p1-reader.yaml) to match.

- Avoid strapping pins for RX (on the classic ESP32: GPIO0, 2, 5, 12 and 15).
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
