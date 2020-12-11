# -*- coding: utf-8 -*-
"""
Power Management during Covid-19 lay up period

Created between April 1st and xxx

@author: T.Rosenkranz thomas.rosenkranz@carnival-maritime.com
"""

import getpass
from tkinter import filedialog
import geopy.distance as gp
from math import sin, cos, sqrt, atan2

import csv
import os
import pandas as pd
import datetime
from datetime import timedelta
import inspect
import time
from time import strftime
import numpy as np
from matplotlib import path
from _LayUp_VARIABLES import *

dict_MASTER_WHAT_TO_DO = {
	"master_prepareRawData": 1,
	"master_analyseData": 0
}


# ######################################################################################################################
def f_loopAllFilesInThisFolderAndCreateNewSumFile(
):
	f_makeThePrintNiceStructured(True, "### START READING ALL FILES ", inspect.stack()[0][3])
	startTime = time
	startTime = f_doTheTimeMeasurementInThisFunction(startTime, flag_timeStart, inspect.stack()[0][3])
	# print(os.path.dirname(os.path.realpath(__file__)))
	
	df1 = pd.DataFrame()
	df2 = pd.DataFrame()
	
	# root = tk.Tk()
	# root.withdraw()
	
	print(getpass.getuser())
	print(os.path.dirname(os.path.realpath(__file__)))
	
	abs_dir = os.path.dirname(__file__)
	print(abs_dir)
	
	rel_dir = os.path.join(abs_dir, '')
	print(rel_dir)
	
	filesToBeTreated = filedialog.askopenfilenames()
	
	useFilePicker = True
	# region FILEPICKER
	if useFilePicker:
		for subFile in filesToBeTreated:
			print('JEA: ' + subFile)
			
			if df1.shape[0] == 0:  # df1 is empty
				print("FILL DF1 with FIRST FILE")
				
				df1 = pd.read_csv(subFile, sep=';', low_memory=False)
			else:
				print("FILL DF2 with further FILEs and add them to DF1")
				
				df2 = pd.read_csv(subFile, sep=';', low_memory=False)
				
				df1 = pd.concat([df1, df2])
		
		
		df1[flag_date] = pd.to_datetime(df1[flag_date])
		
		df1 = df1.round(decimals=4)
		
		df1 = df1.sort_values([flag_shipCode, flag_date], ascending=[True, True])
		
		df1 = df1.reset_index(drop=True)
		
		# f_exportDataframe(
		# 	print_sumOfRawData, fileExport_csv, df1,
		# 	("_" + "TF_" + str(timeAggregationPeriodInSeconds / 60) + "_STEP_01_NL_FileAggregation"))
		
		startTime = f_doTheTimeMeasurementInThisFunction(startTime, flag_timeEnd, inspect.stack()[0][3])
		
		return (df1)
	
	
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



if dict_MASTER_WHAT_TO_DO["master_prepareRawData"] == 1:
	f_makeThePrintNiceStructured(True, "### FILL START DATES ", inspect.stack()[0][3])
	startTime = time
	startTime = f_doTheTimeMeasurementInThisFunction(startTime, flag_timeStart, inspect.stack()[0][3])
	
	doTheAnalysisForOneShipOnly = False
	
	df_existingMasterFile = f_readExistingMasterFile()
	
	f_createCopyOfExistingMasterFileBeforeChangingIt(df_existingMasterFile, fileCopyBeforeAddRaw)
	
	dfSourceData = f_loopAllFilesInThisFolderAndCreateNewSumFile()
	
	for thisUniqueShip in dfSourceData[flag_NeptuneLab_Ship].unique():
		thisShipLongName = dict_shipNames[thisUniqueShip]
		
		print("\n############################################")
		print("RAW DATA TO BE PREPARED FOR NEXT SHIP >>> " + thisUniqueShip + " = " + thisShipLongName)
		
		dfSubDatasetForThisShip = dfSourceData[dfSourceData[flag_NeptuneLab_Ship] == thisUniqueShip]
		
		if \
			dict_rawDataStructure["sourceDataStructure_neptuneLab_RawData"] == 1 or \
				dict_rawDataStructure["sourceDataStructure_neptuneLab_preparedAverages"] == 1:
			
			dfFinal, minTimeStamp, maxTimeStamp = f_createNewAndEmptyDataframeWithPreparedTimeSlices(
				dfSubDatasetForThisShip)
			
			dfFinal, thisShipShortNameAsPerNLDataSet, minTimeStamp, maxTimeStamp = f_buildAveragesPerSignalPerTimeSlice(
				dfSubDatasetForThisShip, dfFinal)
		else:
			dfFinal = dfSubDatasetForThisShip
			# dfFinal[flag_finalFile_Ship] = thisShipLongName
			dfFinal.loc[:, flag_finalFile_Ship] = thisShipLongName
		
		dfFinal = f_doSomeTypeCasts(dfFinal)
		
		dfFinal = f_checkForTechnicalRestrictionInPort(dfFinal, thisShipLongName, print_dataAfterAddingSailingMode)
		
		dfFinal = f_getFuelTypePerEnginePerTimeslice(dfFinal, print_restructuredRawData)
		
		dfFinal = f_addTimeStampsPerHour(dfFinal, False)
		
		dfFinal = f_addFuelConsumptionToDF(dfFinal, thisShipLongName, print_dataAfterAddingFuelType)
		
		dfFinal = f_addColumnsForMissingNeptuneLabRawDataColumns(dfFinal, thisShipLongName,
																					print_finalPreparedNLRawData)
		
		df_existingMasterFile = f_addThisDataFrameAtTheEndOfTheExistingTotalFile(
			dfFinal,
			df_existingMasterFile,
			thisShipLongName
		)
		
		df_existingMasterFile = f_resortColumnsOfFinalTotalFileWithAllNeededColumns(df_existingMasterFile)
	
	# print("########################################")
	# print("BEFORE FINAL XLS export")
	# startTime = time
	# startTime = f_doTheTimeMeasurementInThisFunction(startTime, flag_timeStart, inspect.stack()[0][3])
	# f_exportDataframe(
	# 	True, fileExport_xls, df_existingMasterFile, "FINAL"
	# )
	# startTime = f_doTheTimeMeasurementInThisFunction(startTime, flag_timeEnd, inspect.stack()[0][3])
	
	print("########################################")
	print("DONE! DO THE FINAL CSV EXPORT")
	startTime = time
	startTime = f_doTheTimeMeasurementInThisFunction(startTime, flag_timeStart, inspect.stack()[0][3])
	
	f_exportDataframe(
		True, fileExport_csv, df_existingMasterFile, masterFile_ALL_csv
	)
	startTime = f_doTheTimeMeasurementInThisFunction(startTime, flag_timeEnd, inspect.stack()[0][3])