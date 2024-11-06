import sys
from os import path
import yaml

current_project_root = path.abspath(path.join(path.dirname(__file__), ".."))
sys.path.append(path.join("python_raft"))
sys.path.append(path.join(current_project_root, "..", "ut-raft"))

from framework.core.submodules.vdevice_message_sender import VDeviceMessageSender
from framework.core.commonRemote import commonRemoteClass
from framework.core.logModule import logModule

class ControlPlane:
    def __init__(self, device, device_type, config):
        # Load configuration
        self.device = device
        self.device_type = device_type
        self.config = config
        
        # Get device config and check if platform is virtual or not
        device_config = self.config.get("control_devices")[device]
        
        if device_type == "virtual":
            self.vdevice_sender = VDeviceMessageSender(device_config)
        else:
            self.common_remote = commonRemoteClass(log=logModule, remoteConfig=device_config)
        
    def process_message(self, message_yaml):
        # Parse the YAML message
        message = yaml.safe_load(message_yaml)
        
        # For virtual platforms, route to the vDevice message sender
        # For physical platforms, decode message
        
        command = message.get(self.device)
        if command:
            if self.device_type == 'virtual':
                self.vdevice_sender.send_command(command)
            else:
                self.send_command(command)

    def send_command(self, command_data):
        """
        Sends a command using commonRemoteClass.

        Args:
            command_data (dict): Dictionary containing 'command', 'delay', 'repeat', 'randomRepeat', etc.
        """
        keycode = {'name': command_data['command']}  # Command as keycode dictionary for sendKey
        
        # Send the command via commonRemote's sendKey
        self.common_remote.sendKey(
            keycode=keycode,
            delay=command_data.get('delay', 1),
            repeat=command_data.get('repeat', 1),
            randomRepeat=command_data.get('randomRepeat', 0)
        )


if __name__ == "__main__":
    try:
        config = {
            "control_devices": {
                "irblaster": {
                    "command_port": "/dev/irblaster",
                    "supported_commands": ["PowerOn", "PowerOff", "VolumeUp", "VolumeDown"]
                },
                "hdmicec": {
                    "ws_port": 8000,
                    "supported_commands": ["ImageViewOn", "ActiveSource", "Standby", "Hotplug"]
                }
            }
        }

        # Example message for IR Blaster command
        control_plane = ControlPlane("irblaster", "virtual", config)
        message_yaml_ir = """
        irblaster:
          command: PowerOn
          delay: 2
          repeat: 3
          randomRepeat: 1
          target_device: DUT
          code: "NUM_0"
        """
        print("Testing IR Blaster Command:")
        control_plane.process_message(message_yaml_ir)

        
        # Example message for HDMI command
        control_plane = ControlPlane("hdmicec", "physical", config)
        message_yaml_hdmi = """
        hdmicec:
          command: ImageViewOn
        """
        print("Testing HDMI Command:")
        control_plane.process_message(message_yaml_hdmi)

    except Exception as e:
        print(f"An error occurred: {e}")