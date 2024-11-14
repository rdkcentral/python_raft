import websocket

class VDeviceMessageSender:
    """
    VDeviceMessageSender class handles sending commands to a virtual device using WebSocket communication.
    """
    def __init__(self, config):
        """
        Initializes the VDeviceMessageSender instance.
        
        Args:
            config (dict): Configuration dictionary containing the command port and supported commands.
        
        Attributes:
            ws_port (int): The WebSocket port for sending commands.
            supported_commands (list): A list of supported commands that can be sent.
        """
        self.ws_port = config['command_port']
        self.supported_commands = config['supported_commands']
        
    def send_command(self, command_data):
        """
        Sends a command to the virtual device via WebSocket.

        Args:
            command_data (dict): Dictionary containing the command details to be sent.

        Raises:
            ValueError: If the command in `command_data` is not in the list of supported commands.
        """
        command = command_data.get('command')
        
        if command not in self.supported_commands:
            raise ValueError(f"Unsupported command: {command}")

        # Connect to the WebSocket and send the command
        ws_url = f"ws://localhost:{self.ws_port}"
        ws = websocket.create_connection(ws_url)
        print(f"Sending vDevice command '{command}' to WebSocket at {ws_url}")
        ws.send(command)
        ws.close()
