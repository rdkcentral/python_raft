## Outbound Client

**Module Name:** `outboundClientClass`

**Directory:** `framework/core/outboundClient.py`

**Purpose:**

* Provides a flexible way to exchange files with external systems during testing.
* Supports downloading files for test setup and uploading results/logs.
* Handles common network protocols for file transfer.

**Key Features:**

* **Supported Protocols**
    * **HTTP/HTTPS:** Downloads files from web servers. Useful for getting test images or configuration files.
    * **SFTP:** Secure file transfer for both downloading and uploading files to/from remote servers.

* **File Handling:**
   * Downloads files to a designated workspace directory.
   * Uploads files from the workspace to a configured upload location.
   * Can automatically determine filenames based on URLs if no specific filename is provided.

* **Progress Reporting:**
   * Displays progress bars during file transfers.
   * Provides human-readable file sizes.

* **Integration:**
   * Designed to be used within test scripts.
   * Can have a logging module passed to it or creates its own if needed.

**How to Use:**

1. **Initialization:**  Create an `outboundClientClass` object, providing:
   * (Optional) A logging module (`logModule`)
   * Workspace directory (local folder for downloads)
   * Upload URL (if uploading files)
   * HTTP Proxy (If required)

2. **Downloading Files:**
   * Use `downloadFile(url, filename=None)`.
   * The file will be saved in the workspace directory.
   * Example: `my_outbound.downloadFile("http://test-server/image.bin")`

3. **Uploading Files:**
   * Use `uploadFile(filename)`.
   * The file will be uploaded from the workspace to the configured upload location.
   * Example: `my_outbound.uploadFile("test_results.log")`

4. **Image Handling (`prepareOutboundWithImageFromUrl`)**
  * Combines downloading and uploading an image into a single convenient method.
  * Can translate image types (e.g., "PCI1") into the corresponding filenames

**Example Use Case:**

```python
# Initialize the outbound client
my_outbound = outboundClientClass(workspaceDirectory="./workspace", upload_url="sftp://upload-server/results")

# Download a test image
my_outbound.prepareOutboundWithImageFromUrl("imageType", "http://image-repo/latest_image.bin") 

# ... Run your tests ...

# Upload the test logs
my_outbound.uploadFile("test_logs.txt")