# Title

## Audience
Who is this document for?

## Document Scope
What is the purpose of this document?

## Background
Background for what the module designed here is for.

Why use it?

## What is the purpose of this module?
What does this module do?

## Functionality
More detailed explanation of the required functionality of the module

### Specific Function 1
What this does?

### Specific Function 2
What this does?

## Usage
How is this module expected to be used within the framework?

## Location
Where will this module be located in the framework file structure?

---
# *Example*

# Download Controller Design

## Audience
Engineering Team

## Background
Files required for testing are regularly stored on servers, both on the internet and the internal network. These files need to be retieved and placed in a known location within the test workspace to allow the tests to use them.

## What is the purpose of this module?
This module will provide the ability to retieve files from remote servers using many different transfers protocols.

The transfer protocol of the file can be determined from it's url, therefore this module will provide a transparent interface to the user to download from any of the protocols.

When these files are retrieved they will be placed into a specified, known location when the download is complete.

## Functionality
The following functionality is required for this module.

All the below functionality should be transparent to the user. The user should be able to download a file to a specified location, by simply passing the URL of the file and the output location to the download module.

### File retrieval via the SSH protocol
Downloaded a file/files to the specified location using the SSH transfer protocol.
### File retrieval via the FTP/FTPs protocol
Downloaded a file/files to the specified location using the FTP/FTPs transfer protocol.
### File retrieval via the http/https protocol
Downloaded a file/files to the specified location using the http/https transfer protocol.
### File retrival via the TFTP protocol
Downloaded a file/files to the specified location using the TFTP transfer protocol.

## Usage
This module will be instantiated an used by other modules as and when they need to download files.
