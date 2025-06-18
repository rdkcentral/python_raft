import asyncio

import os
import sys

# Add the framework path to system
dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(dir_path+"/../")

from framework.core.audioAmplifier.denon_controller import DenonAVRController

async def main():
    controller = DenonAVRController("10.242.30.236")
    await controller.update_state()  # Fetch current state
    status = controller.get_status()
    print("Power:", status["power"])
    print("Volume:", status["volume"])
    print("Input:", status["input"])
    print("Muted:", status["muted"])

asyncio.run(main())
