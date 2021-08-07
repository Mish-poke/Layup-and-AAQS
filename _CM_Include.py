

import datetime
import time
import pandas as pd
# ######################################################################################################################

flag_timeStart = 'FunctionTimeMeasurementStart'
flag_timeEnd = 'FunctionTimeMeasurementEnd'

# ### DEBUG VARs ##############
FORCE_fullDebugAllComments = False
avoidAnyComments = False

' #####################################################################################################################'
def f_downSizeThisColumn(thisDF, thisSignal, roundMe = -1):
    if thisSignal in thisDF.columns:
        thisDF[thisSignal] = \
                pd.to_numeric(thisDF[thisSignal], downcast ='float')

        if roundMe >= 0:
            thisDF[thisSignal] = thisDF[thisSignal].round(roundMe)

    return thisDF

# ######################################################################################################################
def f_makeThePrintNiceStructured(
	doThePrint,
	printThisText,
	recentFunction
):
	if FORCE_fullDebugAllComments or \
		(doThePrint and avoidAnyComments == False):
		print("############################################")
		print(printThisText + " in f: " + recentFunction)


# ######################################################################################################################
def f_doTheTimeMeasurementInThisFunction(
	startTime,
	flagType,
	timeMeasurementDoneForThisFunction
):
	if flagType == flag_timeStart:
		startTime = time.perf_counter()
	else:
		endTime = time.perf_counter()
		print(f" TIME ELAPSED {endTime - startTime:0.4f} seconds in Function: " + timeMeasurementDoneForThisFunction)
	
	return startTime


# ######################################################################################################################
def func_replaceNanInThisColumn(
	dfInput,
	columnFlag,
	newNanValue
):
	dfInput[columnFlag].fillna(newNanValue, inplace=True)
	
	return dfInput