import time
import asyncio
from typing import List


class MessageType:
    SWITCH_ON = "SWITCH_ON"
    SWITCH_OFF = "SWITCH_OFF"
    PLAY_SONG = "PLAY_SONG"
    FLUSH = "FLUSH"
    CLEAN = "CLEAN"


class Message:
    def __init__(self, device_id: str,
                 type_: str,
                 content: str = None) -> None:
        self.device_id = device_id
        self.type = type_
        self.content = content


class IOTService:
    def __init__(self) -> None:
        self.devices = {}

    def register_device(self, device: str) -> None:
        device_id = str(len(self.devices) + 1)
        self.devices[device_id] = device
        print(f"Device {device.__class__.__name__} "
              f"registered with ID {device_id}")
        return device_id

    async def send_message(self, message: Message) -> None:
        """Asynchronously send a message to a device."""
        print(f"Sending message to device {message.device_id}: {message.type}")
        await asyncio.sleep(1)
        print(f"Message sent: {message.device_id} - {message.type}")


async def async_run_program(
        service: IOTService,
        program: List[Message]
) -> None:
    tasks = []
    for message in program:
        tasks.append(service.send_message(message))
    await asyncio.gather(*tasks)


async def main() -> None:
    service = IOTService()

    class HueLightDevice:
        pass

    class SmartSpeakerDevice:
        pass

    class SmartToiletDevice:
        pass

    hue_light = HueLightDevice()
    speaker = SmartSpeakerDevice()
    toilet = SmartToiletDevice()

    hue_light_id = service.register_device(hue_light)
    speaker_id = service.register_device(speaker)
    toilet_id = service.register_device(toilet)

    wake_up_program = [
        Message(hue_light_id, MessageType.SWITCH_ON),
        Message(speaker_id, MessageType.SWITCH_ON),
        Message(speaker_id, MessageType.PLAY_SONG,
                "Rick Astley - Never Gonna Give You Up"),
    ]

    sleep_program = [
        Message(hue_light_id, MessageType.SWITCH_OFF),
        Message(speaker_id, MessageType.SWITCH_OFF),
        Message(toilet_id, MessageType.FLUSH),
        Message(toilet_id, MessageType.CLEAN),
    ]

    await async_run_program(service, wake_up_program)
    await async_run_program(service, sleep_program)


if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()

    print("Elapsed:", end - start)
