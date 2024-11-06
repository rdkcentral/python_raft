import websocket

class VDeviceMessageSender:
    def __init__(self, config):
        self.ws_port = config['command_port']
        self.supported_commands = config['supported_commands']
        
    def send_command(self, command_data):
        command = command_data.get('command')
        
        if command not in self.supported_commands:
            raise ValueError(f"Unsupported command: {command}")

        # Connect to the WebSocket and send the command
        ws_url = f"ws://localhost:{self.ws_port}"
        ws = websocket.create_connection(ws_url)
        print(f"Sending vDevice command '{command}' to WebSocket at {ws_url}")
        ws.send(command)
        ws.close()
