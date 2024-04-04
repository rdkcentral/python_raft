# commandModules package

## Submodules

## commandModules.consoleInterface module

### *class* commandModules.consoleInterface.consoleInterface

Bases: `object`

#### *abstract* close()

Close the console session.

#### *abstract* open()

Abstract method. Define how to open the console session.

#### *abstract* read_all()

Abstract method. Define how to read all information displayed in the console.
Should return the data read.

#### *abstract* read_until(value)

Abstract method. Define how to read all the information displayed in the console,
: upto the point a defined string appears.
  Should return the data read.

* **Parameters:**
  **value** (*str*) – Message to wait for in the console.

#### *abstract* write(message)

Abstract method. Define how to write to the console.

* **Parameters:**
  **message** (*str*) – Message to write into the console.

## commandModules.serialClass module

## commandModules.sshConsole module

### *class* commandModules.sshConsole.sshConsole(address, username, password, key=None, known_hosts=None)

Bases: [`consoleInterface`](#commandModules.consoleInterface.consoleInterface)

sshConsole is a consoleInterface class to interface with SSH console sessions

* **Parameters:**
  * **address** (*str*) – IP address of the host to connect to.
  * **username** (*str*) – Username for logging into the host.
  * **password** (*str*) – Password for logging into the host.
  * **key** (*str* *,* *optional*) – Filepath of ssh key to use.
  * **known_hosts** (*str* *,* *optional*) – Filepath of known_hosts file to use.

#### close()

Close the SSH session

#### open()

Open the SSH session.

#### read_all()

Capture all lines that are displayed in the console.

* **Returns:**
  List of strings, with each being a line displayed in the console.
* **Return type:**
  List

#### read_until(value)

Read the console until a message appears.

* **Parameters:**
  **value** (*str*) – The message to wait for in the console.
* **Returns:**
  List of string, with each being a line displayed in the console up to the value entered.
* **Return type:**
  List

#### write(message)

Write a message into the console.

* **Parameters:**
  **message** (*str*) – String to write into the console.

## commandModules.telnetClass module

### *class* commandModules.telnetClass.telnet(log, workspacePath, host, username, password, port=23)

Bases: [`consoleInterface`](#commandModules.consoleInterface.consoleInterface)

telnet is a consoleInterface class to interface with telnet console sessions.

* **Parameters:**
  * **log** (*logModule*) – Log module to be used.
  * **workspacePath** (*str*) – Path of the tests worksapce to create the sesson.log file.
  * **host** (*str*) – IP address of the host to open a session with.
  * **username** (*str*) – Username to login to the session with.
  * **password** (*str*) – Password to login to the session with.
  * **port** (*int* *,* *optional*) – Listening telnet port on host. Defaults to 23.

#### close()

Close the telnet session

#### connect(username_prompt='login: ', password_prompt='Password: ')

Open the telnet session

* **Parameters:**
  * **username_prompt** (*str* *,* *optional*) – Expected prompt shown for entering the username.
  * **password_prompt** (*str* *,* *optional*) – Expected prompt shown for entering the password.
* **Returns:**
  True if session opened successfully.
* **Return type:**
  bool

#### disconnect()

Close the telnet session

* **Returns:**
  True
* **Return type:**
  bool

#### open()

Open the telnet session.

#### read_all()

Read all readily available information displayed in the console.

* **Returns:**
  Information currently displayed in the console.
* **Return type:**
  str

#### read_eager()

Read all readily available information displayed in the console.

* **Returns:**
  Information currently displayed in the console.
* **Return type:**
  str

#### read_some()

Read information displayed in the console until EOF hit.

* **Returns:**
  Information currently displayed in the console.
* **Return type:**
  str

#### read_until(value)

Read the console until a message appears.

* **Parameters:**
  **value** (*str*) – The message to wait for in the console.
* **Returns:**
  Information displayed in the console up to the value entered.
* **Return type:**
  str

#### read_very_eager()

Read all readily available information displayed in the console, without blocking I/O.

* **Returns:**
  Information currently displayed in the console.
* **Return type:**
  str

#### write(message)

Write a message into the session console.

* **Parameters:**
  **message** (*str*) – Message to write into the console.
* **Returns:**
  True when the message is successfully written to the console.
* **Return type:**
  bool

## Module contents
