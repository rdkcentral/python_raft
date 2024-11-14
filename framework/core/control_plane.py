import sys
from os import path
import yaml

current_project_root = path.abspath(path.join(path.dirname(__file__), ".."))
sys.path.append(path.join("python_raft"))
sys.path.append(path.join(current_project_root, "..", "ut-raft"))

from framework.core.submodules.vdevice_message_sender import VDeviceMessageSender
from framework.core.commonRemote import commonRemoteClass
from framework.core.logModule import logModule
from submodules.ir import IR

class ControlPlane:    
    """
    Manages the control framework for both physical and virtual devices. 
    It initializes the appropriate device handlers and processes incoming commands based on the device configuration.
    """
   
    def __init__(self, config=None, virtualConfig=None):
        """
        Initializes the ControlPlane class.
        
        Args:
            config (dict, optional): Configuration dictionary for physical device handlers. Defaults to None.
            virtualConfig (dict, optional): Configuration for virtual device communication. Defaults to None.
        
        Attributes:
            config (dict): Holds the configuration for physical devices if provided.
            virtualConfig (dict): Holds the configuration for virtual devices if provided.
            handlers (dict): Dictionary of device handlers for physical devices.
            vdevice_sender (VDeviceMessageSender): Instance for handling virtual device messages if `virtualConfig` is provided.
        """
        self.config = None
        self.virtualConfig = None

        if config is not None:
            self.config = config

            # Initialize device-specific subclasses for physical devices
            self.handlers = {
                "IR": IR(),
                "HDMICEC": HDMICEC(),
                "Power": Power(),
                "DeepSleep": DeepSleep()
            }
        
        if virtualConfig is not None:
            self.virtualConfig = virtualConfig
            self.vdevice_sender = VDeviceMessageSender(virtualConfig)


    def process_message(self, message_yaml):
        """
        Processes a given YAML message and routes it to the appropriate handlers.

        Args:
            message_yaml (str): The message in YAML format to be parsed and processed.
        """
        # Parse the YAML message
        message = yaml.safe_load(message_yaml)

        # If device type is virtual, handle exclusively with Virtual Device Sender
        if self.virtualConfig is not None:
            self.vdevice_sender.send_command(message)
            print("Virtual device handler invoked.")
        else:
            # Route the message to all physical device handlers to be decoded
            for handler_name, handler in self.handlers.items():
                print(f"Sending message to {handler_name} handler")
                handler.process_command(message)
        

if __name__ == "__main__":
    try:
        config = {
            "control_devices": {
                "IR": {
                    "command_port": "/dev/irblaster",
                    "supported_commands": ["PowerOn", "PowerOff", "VolumeUp", "VolumeDown"]
                },
                "hdmicec": {
                    "ws_port": 8000,
                    "supported_commands": ["ImageViewOn", "ActiveSource", "Standby", "Hotplug"]
                }
            }
        }

        control_plane = ControlPlane(config=config)

        # Example message for IR Blaster command
        message_yaml_ir = """
        IR:
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
        message_yaml_hdmi = """
        hdmicec:
          command: ImageViewOn
        """
        print("Testing HDMI Command:")
        control_plane.process_message(message_yaml_hdmi)

    except Exception as e:
        print(f"An error occurred: {e}")