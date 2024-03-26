#! /bin/python3
#/* *****************************************************************************
#* Copyright (C) 2021 Sky group of companies, All Rights Reserved
#* ******************************************************************************
#*
#*   ** Project      : RAFT
#*   ** @addtogroup  : unittests
#*   ** @date        : 05/07/2021
#*   **
#*   ** @brief : log module test application
#*   **
#*
#* ******************************************************************************/
import os 
import sys

# Add the framework path to system
dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(dir_path+"/../../")

import framework.core.logModule as logModule

# Testing module if you run this class locally
if __name__ == "__main__":

    log = logModule("logging_tests.py")
    moduleLog = logModule("module")

    log.setFilename( "testLog.log" )

    log.setLevel( log.CRITICAL )

    end_time = log.testStart( "pythonLogTest", "PLT-0001", 1, 60 )
    log.info("end_time:"+str(end_time))
    log.testResult( "Test Completed" )

    loopCount=5
    end_time = log.testStart( "pythonLogTest", "PLT-0002", loopCount, 60 )
    for loop in range(loopCount):
        log.stepStart("loop step", "all loops complete")
        log.testLoop(loop)
        log.step( "in1" )
        log.step( "in2" )
        log.step( "in3" )
        log.step( "in4" )
        log.step( "in5" )
        log.testLoopComplete(loop)
        log.stepResult(True,"Loop [{}] Completed".format(int(loop)))
    log.testResult( "Test Completed" )

    log.setLevel( log.STEP_RESULT )

    end_time = log.testStart( "pythonLogTest", "PLT-0003", 1, 60 )
    log.stepStart( "Starting of this step", "Something to happen correctly")
    log.info("I should not be displayed")
    log.debug("I should not be displayed")
    log.warn("I will be displayed")
    log.step( "in1" )
    log.step( "in2" )
    log.step( "in3" )
    log.step( "in4" )
    log.step( "in5" )
    log.stepResult( True, "out1" )
    log.stepStart( "Starting of this step", "really something has to happen")
    log.step( "in2" )
    log.step( "in1" )
    log.step( "in2" )
    log.step( "in3" )
    log.step( "in4" )
    log.stepResult( False, "out2" )
    log.stepStart( "Starting of this step", "something more happens here")
    log.step( "in3" )
    log.step( "in1" )
    log.step( "in2" )
    log.step( "in3" )
    log.step( "in4" )
    log.stepResult( True, "out3" )
    log.stepStart( "Starting of this step", "lots happen here")
    log.step( "in99" )
    log.stepResult( False, "out4" )
    log.testResult( "Test PLT-0003" )

    # Default is info level this should not appear
    log.debug( "debug message SHOULD NOT APPEAR" )

    log.setLevel( log.DEBUG )

    log.debug( "debug message SHOULD APPEAR" )
    log.info( "Info Message" )
    log.warn( "Warning Message - SHOULD APPEAR" )

    log.setLevel( log.WARNING )

    log.info( "Info Message - SHOULD NOT APPEAR" )

    log.error( "Error Message" )
    log.critical( "Critical Message" )
    log.critical( "FATAL Message" )
#    log.Result( StatusCode.SUCCESS ,"Result was good" )

    moduleLog.debug("Message from the module, not shown")
    moduleLog.error("Error from the module")

