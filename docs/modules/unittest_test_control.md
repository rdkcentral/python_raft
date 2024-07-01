## UnitTest Test Control

**Module Name:** `unittestTestControl.py`

**Directory:** `framework/core/unittestTestControl.py`

**Purpose:**

* Integrates the unittest framework into the existing test control infrastructure.
* Enables running tests using the unittest framework for better integration with existing Python testing tools and CI pipelines.
* Facilitates generating test reports in XML format for analysis and integration with tools like Jenkins.

**Key Features:**

1. **Integration with unittest:**
    * **Inheritance:** Inherits from the existing testControl class, preserving its core functionalities while adding unittest capabilities.
    * **Unittest Compatibility:** Allows test scripts to be run using the unittest framework, enabling standard unittest features such as test discovery and assertions.
    * **XML Reporting:** Supports running tests with pytest to generate XML reports, which can be used for continuous integration and automated test result analysis.

2. **Test Execution:**
    * **Setup and teardown:** Inherits the testPrepareFunction() from testController for setUp(),and respectively the testEndFunction() for tearDown()

**How to Use:**

1. **Create Test Scripts:**
    * Extend the unittestTestControl class within the test scripts.
    * Override the key functions:
        * testPrepareFunction: Set up the necessary environment for the test.
        * testFunction: Implement the core logic for the test (device interactions, verifications, assertions).
        * testEndFunction: Clean up after the test, such as powering down devices, closing browser sessions, etc.

2. **Provide Configuration Files:**
    * Rack Configuration: Defines racks, slots, devices, and their properties.
    * Test Configuration: Specifies test parameters, loop count, device images, etc.

3. **Run Tests:**

    * Use the run_tests.py script to execute your test suite, optionally passing command-line arguments for rack and slot selection.
    * Alternatively, run individual test scripts using pytest to generate XML reports.

* To run the tests using the run_tests.py script:
`python run_tests.py`
* *To run tests individually with pytest and generate an XML report:
`pytest testScript.py --junitxml=report.xml`