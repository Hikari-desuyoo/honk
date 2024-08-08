import asyncio
from bleak import BleakClient, BleakScanner
import sqlite3
from datetime import datetime

CHAR_GENERAL_RW_1 = "000033f1-0000-1000-8000-00805f9b34fb"  # General RW characteristic UUID
CHAR_GENERAL_N_1 = "000033f2-0000-1000-8000-00805f9b34fb"  # General notify characteristic UUID
ENABLE_HEART_RATE_COMMAND = bytearray([0x18, 0x01])
HR_RESPONSE_FIRST_BYTES = bytes([229, 17, 0])
DEVICE_NAME = "Haylou Smart Watch 2"

async def record_heart_rates(address):
    async with BleakClient(address) as client:
        if client.is_connected:
            print(f"Connected to {address}")

            # Trigger heart rate measurement
            await client.write_gatt_char(CHAR_GENERAL_RW_1, ENABLE_HEART_RATE_COMMAND)

            def heart_rate_handler(sender, data):
                if data[:3] == HR_RESPONSE_FIRST_BYTES:
                    bpm = data[3]
                    print(f"[{datetime.now()}] {bpm} bpm")

                    # store heartrate
                    conn = sqlite3.connect('heart_rate.db')
                    cursor = conn.cursor()
                    cursor.execute("INSERT INTO heart_rate (date, bpm) VALUES (?, ?)", (datetime.now(), bpm))
                    conn.commit()
                    conn.close()

            await client.start_notify(CHAR_GENERAL_N_1, heart_rate_handler)

            while True:
                await asyncio.sleep(1)

# finding the device

address = None

async def scan_devices():
    global address
    devices = await BleakScanner.discover()
    for device in devices:
        if device.name == DEVICE_NAME:
            address = device.address
        print(f"[Search result] Device: {device.name}, Address: {device.address}")

while address is None:
    print("Looking for address...")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(scan_devices())

print(f"Found address: {address}")


# database initialization and setup

conn = sqlite3.connect('heart_rate.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS heart_rate
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT,
                    bpm INTEGER)''')
conn.commit()
conn.close()

# main loop

asyncio.run(record_heart_rates(address))
