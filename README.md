# Raspberry Pi Pico W IoT Discord Notification Button

This kit and codebase is ideal for makers and remote workers looking to build a dedicated hardware shortcut for digital alerts. By pairing a physical tactile switch with the Raspberry Pi Pico W, this project bypasses bulky desktop software dependencies to trigger instant messages directly into your personal Discord channel using automated bot endpoints.

The code is optimized to work seamlessly with the [Raspberry Pi Pico 2W](https://links.pishop.io/track/6a3d082d4d9224c70fb125d4) found at PiShop SA. 

We show you how to build, wire, and write the backend code on our blog pages.
* Read the full step-by-step tutorial over at the [PiShop Africa Blog](https://blog.pishop.co.za/).

We also stock a wide selection of [buttons](https://www.pishop.co.za/store/buttons), [enclosures](https://www.pishop.co.za/store/enclosures), and [prototyping boards](https://www.pishop.co.za/store/raspberry-pi-pico_0) that you can use to upgrade or package your physical notification button.

### What's in the repo:

* `main.py` - The optimized standalone MicroPython production script.
* `hardware_tester.py` - A lightweight script to diagnose your tactile button wiring without an active internet connection.

### Table of Contents
* [Features](#features)
* [Tech Stack](#tech-stack)
* [System Architecture](#system-architecture)

---

### Features
* **Zero External Desktop Dependencies:** Uses lightweight MicroPython core features to talk directly to the Discord HTTP API.
* **Non-Chunked Data Transfer:** Embedded explicit packet length calculations to bypass strict server filtering restrictions.
* **Auto-Reconnection Daemon:** Built-in loop handlers dynamically monitor Wi-Fi stability and re-authenticate if router drops occur.
* **Hardware Debouncing:** Software time-locks filter out accidental double-clicks or mechanical noise on the physical pin.

### Tech Stack:
* **Hardware:** Raspberry Pi Pico W (2.4GHz Wi-Fi engine)
* **Firmware/Language:** MicroPython 1.20+
* **External Integration:** Discord Developer Portal Bot Gateway

### System Architecture

```mermaid
sequenceDiagram
    autonumber
    title Pico W Discord Bot Flow
    Pico W->>Local Wi-Fi Router: Establish 2.4GHz Network Connection
    Note over Pico W: LED turns SOLID when connected
    loop Active Idle Listener
        Pico W->>GP15 Pin: Poll Pin State (Internal Pull-Up)
        alt Button Pressed (Pin Drops to 0V)
            Note over Pico W: Trigger Debounce check (>2000ms)
            Pico W->>Discord API: Native POST Packet (Strict Content-Length)
            Discord API-->>Pico W: Respond Status Code (e.g. 200 OK)
        end
    end
