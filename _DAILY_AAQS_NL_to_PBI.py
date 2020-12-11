# -*- coding: utf-8 -*-
"""
Analyse AAQS usage and calculate missed opportunities

Created on Thu Oct 19 2019
#<>
@author: T.Rosenkranz
#TODOx when ship is FS or PA and in South-America during a certain period, do not show any missed AAQS opportunity ... DONE
#TODO >> check the detox flow and only show any AAQS value in case of AAQS was really running >> this could be applied for all ships
"""

# TO DO
#1 AAQS restrictions time controlled !! ports are added over time >> DONE 2020-02-19
#2 if ship is using HFO+AAQS inside territorial waters, create a new AAQS assessment category to flag cases when ship maybe doing something wrong
#3 FILTER for data spikes while ship is in port / anchorage. e.g if avg pwr demand in last 7 days within xyz range (avg +/- stddev), then erase spikes above / below

#region IMPORTs
import getpass
from tkinter import filedialog
import geopy.distance as gp
from math import sin, cos, sqrt, atan2
import csv
import os
import pandas as pd
import datetime
from datetime import date
from datetime import timedelta
import inspect
import time
# from time import strftime
import numpy as np
from matplotlib import path
from playsound import playsound

from _DAILY_AAQS_Variables import *
from _CM_Include import *
from _LayUp_VARIABLES import *
from _DAILY_AAQS_FillReasonsVariables import *
#
# from _DAILY_AAQS_Missed_Navigation import *
from _EngineRunningHours import *
#endregion

#region VARs for ENGINE RUNNING HOURs
EngineRunningHours_Step01_createShipByShipFileWithActuals = False

EngineRunningHours_Step02_createFinalFileForPBI = False
EngineRunningHours_Step02_predictionVersion = 2

EngineRunningHours_Alternate_rhPrediction_Versions = 2
#endregion

#region VARs for Lay-Up and AAQS Analysis
printMinMaxDateValuePerShip_NOTHING_ELSE = 0
extractShipFiles_NOTHING_ELSE = 0

create_FINAL_FILE_AAQS_NOTHING_ELSE = 0
create_FINAL_FILE_LayUp_NOTHING_ELSE = 1
create_FINAL_FILE_LayUp_NOTHING_ELSE_including_averagesForPBI = 1
# this date defines the starting point for the calculation of the power demand averages.
# from time to time we can be increased a bit to save some calculation time
#0 = cut times out of master file // 1 = do a full new run, takes few hours
createCompletelyNewFileWithAllHistory = 1
eraseAllPBIDateFromThisTimeOnwardsAndCreateNewAverages = datetime.datetime(2020, 11, 10, 0, 0, 0)


create_FINAL_FILE_ShipFeedback = 0

addColumnWithPortName_NOTHING_ELSE = 0

ERASE_ALL_DATA_AFTER_CERTAIN_DATE_InEachShipFile_LayUpPBI = 0
ERASE_ALL_DATA_AFTER_CERTAIN_DATE_InEachShipFile_AAQS_PBI = 0
erase_allDataIncludingThisDay = datetime.datetime(2020, 11, 20, 0, 0, 0)
#endregion

#region create new pbi file for curve comparison based on two files
ONLY_THIS_MergeTheseFilesTogetherToSaveTime = 0
masterFile_LayUp_ALL_PowerDataForPBICurves = r'C:\Users\500095\Desktop\Lay Up Energy Monitoring\02_FinalFiles\PBI_LayUpFinalFile_PORT_ONLY_PowerOnlyPBICurve.csv'
OLD_masterFile_LayUp_ALL_PowerDataForPBICurves = r'C:\Users\500095\Desktop\Lay Up Energy Monitoring\02_FinalFiles\BA_PBI_LayUpFinalFile_PORT_ONLY_PowerOnlyPBICurve.csv'
NEW_masterFile_LayUp_ALL_PowerDataForPBICurves = r'C:\Users\500095\Desktop\Lay Up Energy Monitoring\02_FinalFiles\NEW_PBI_LayUpFinalFile_PORT_ONLY_PowerOnlyPBICurve.csv'
#endregion

#region VARSs LayUp & AAQS
# ##############################################################
dict_rawDataStructure = {
	"sourceDataStructure_neptuneLab_RawData": 				0
	,"sourceDataStructure_neptuneLab_preparedAverages": 	0
	,"sourceDataStructure_PBI_preparedColumns": 				1
}

dict_MASTER_WHAT_TO_DO = {
	"master_prepareRawData": 				0
	,"master_analyseData_AAQS_DAILY": 	0
	,"master_analyseData_LayUp": 			1
}

dict_PREPARE_RAW_DATA_FOR___ = {
	'DATA_APPROACH_AAQS_DAILY': 				0
	,'DATA_APPROACH_LayUpPowerManagement':	1
}

dict_DO_ALL_MANDATORY_STEPs_FOR_NEW_DATASET = {
	masterFlagAnalysisMode_AAQS: 1,
	masterFlagAnalysisMode_LayUp: 1
}

# #############################################################
# FINAL FILE EXPORT (or not)
export_DUMMY_TEST_FILE_ONLY = False
export_MASTER_CSV_FILE = True
export_PBI_XLS_File = False # oh yes baby, no more XLS

# #############################################################
# just load csv and save as xlsx.
load_csv_save_final_xlx_do_NOTHING_Else = False

# ######################################################################################################################
# ######################################################################################################################
# ###########################################################################
# Fill Time Stamps per Hour for PBI
# mandatoryForNewData_fillMissingTimeStampsPerHour = 0
# ERASE_ExistingTimeStampsPerHour = 0
dict_checkAndFillIfNeeded_timeStampsPerHour = {
	masterFlagAnalysisMode_AAQS: 1,
	masterFlagAnalysisMode_LayUp: 1
}
dict_ERASE_ExistingTimeStampsPerHour = {
	masterFlagAnalysisMode_AAQS: 0,
	masterFlagAnalysisMode_LayUp: 0
}

# ###########################################################################
# only needed if something in the fuel consumption algorithm is changed
dict_mandatoryForNewData_recalculateFuelConsumption = {
	masterFlagAnalysisMode_AAQS: 1,
	masterFlagAnalysisMode_LayUp: 1
}
# total fuel consumption per fuel type
dict_recalculateTotalConsumptionPerFuelType = {
	masterFlagAnalysisMode_AAQS: 1,
	masterFlagAnalysisMode_LayUp: 1
}

# ###########################################################################
# TOTAL PWR DEMAND and RollingAvgPWR Demand
dict_addTotalPowerDemand = {
	masterFlagAnalysisMode_AAQS: 1,
	masterFlagAnalysisMode_LayUp: 1
}
dict_doTheRollingAveragePowerDemand = {
	masterFlagAnalysisMode_AAQS: 0,
	masterFlagAnalysisMode_LayUp: 1
}

ERASE_DataSanityChecks = True #TODO this has to be true, data sanity is just temporär while the code is running
ERASE_EngineRunningCount = True

rollingAverageAmountOfTimeStamps = 120

# ###########################################################################
# Fill Speed - GAPs
dict_mandatoryForNewData_fixDataAndFillSpeedGaps = {
	masterFlagAnalysisMode_AAQS: 0,
	masterFlagAnalysisMode_LayUp: 1
}

# ###########################################################################
# PORT-NAMES && LEG-NAMES && LEG-DATES
dict_mandatoryForNewData_updatePortNames_LegNames_LegDates = {
	masterFlagAnalysisMode_AAQS: 0,
	masterFlagAnalysisMode_LayUp: 0
}
dict_ERASE_ALL_PortNames_LegNames_LegDates = {
	masterFlagAnalysisMode_AAQS: 0,
	masterFlagAnalysisMode_LayUp: 0
}

# ###########################################################################
# ENV RESTRICTIONS PER PORT
dict_mandatoryForNewData_fillEnvironmentalRestrictions = {
	masterFlagAnalysisMode_AAQS: 1,
	masterFlagAnalysisMode_LayUp: 0
}
dict_ERASE_EXISTING_ENV_CHECKUPS_AND_REFFRESH_ALL = {
	masterFlagAnalysisMode_AAQS: 0,
	masterFlagAnalysisMode_LayUp: 0
}

# ###########################################################################
# FUEL TYPE PER ENGINE
dict_mandatoryForNewData_fillFuelTypePerEngineRunning = {
	masterFlagAnalysisMode_AAQS: 0,
	masterFlagAnalysisMode_LayUp: 0
}
dict_ERASE_ALL_PREVIOUS_FuelTypePerEngines = {
	masterFlagAnalysisMode_AAQS: 1, # reset to 0 if nothing in the data or the algo was changed
	masterFlagAnalysisMode_LayUp: 1  # reset to 0 if nothing in the data or the algo was changed
}

# ###########################################################################
# WRONG FUEL USED?
dict_fillMissingRedFlagsForWrongFuel = {
	masterFlagAnalysisMode_AAQS: 0,
	masterFlagAnalysisMode_LayUp: 0
}

# ###########################################################################
# AAQS MISSED PORT
dict_mandatoryForNewData_fillMissedAAQSOpportunitiesDuringPortStay = {
	masterFlagAnalysisMode_AAQS: 1,
	masterFlagAnalysisMode_LayUp: 0
}
dict_ERASE_ALL_PREVIOUS_AAQS_PORT_ASSESSMENTS = {
	masterFlagAnalysisMode_AAQS: 0,
	masterFlagAnalysisMode_LayUp: 0
}

# ###########################################################################
# AAQS MISSED NAVIGATION
dict_mandatoryForNewData_fillMissedAAQSOpportunitiesDuringNavigation = {
	masterFlagAnalysisMode_AAQS: 1,
	masterFlagAnalysisMode_LayUp: 0
}
dict_ERASE_ALL_PREVIOUS_AAQS_ASSESSMENTS = {
	masterFlagAnalysisMode_AAQS: 0,
	masterFlagAnalysisMode_LayUp: 0
}

# ###########################################################################
# AAQS not possible due to change over time before NON-AAQS Ports
dict_mandatoryForNewData_fillChangeOverTimesBeforeAfterArrivalInNoAAQSPorts = {
	masterFlagAnalysisMode_AAQS: 0,
	masterFlagAnalysisMode_LayUp: 0
}

minutesNeededForFullFuelChangeoverBeforeArrivalInNoAAQSPort = 120

# ###########################################################################
# OUT OF ORDER ALGORITHM
dict_mandatoryForNewData_FillReasonsForOutOfOrder = {
	masterFlagAnalysisMode_AAQS: 0,
	masterFlagAnalysisMode_LayUp: 0
}
dict_ERASE_ALL_PREVIOUS_OutOfOrderAssessments = {
	masterFlagAnalysisMode_AAQS: 0,
	masterFlagAnalysisMode_LayUp: 0
}

# ###########################################################################
# Anchorage / Drifting
dict_addAnchorage_Drifting_Column = {
	masterFlagAnalysisMode_AAQS: 1,
	masterFlagAnalysisMode_LayUp: 0
}
dict_ERASE_ALL_PREVIOUS_DriftingAnchorageData = {
	masterFlagAnalysisMode_AAQS: 0,
	masterFlagAnalysisMode_LayUp: 0
}
#endregion

firstTimeTick = datetime.datetime(1970, 1, 1, 0, 0, 0)
noDriftOrAnchorageBeforeThatDate = datetime.datetime(2020, 2, 1, 0, 0, 0)



# endregion
# ######################################################################################################################
# ######################################################################################################################
def func_createFinalFileBasedOnSubFiles(

):
	dfSubset = pd.DataFrame()
	
	dfFinal = func_readAllShipFilesInThisFolder(True)
	
	print("len of final dataset: " + str(len(dfFinal)))
	
	#region prepare final file for LayUp with some more averages
	if create_FINAL_FILE_LayUp_NOTHING_ELSE:
		dfSubset = func_filterColumnInDataframeForOneCondition(
			dfFinal,
			flag_finalFile_typeOfSailing,
			flag_typeOfSailing_Port
		)
		# lenBeforeFilter = dfFinal.shape[0]
		#
		# dfSubset = dfFinal[(
		# 	(dfFinal[flag_finalFile_typeOfSailing] == flag_typeOfSailing_Port) |
		# 	(dfFinal[flag_finalFile_typeOfSailing] == flag_typeOfSailing_Anchorage) |
		# 	(dfFinal[flag_finalFile_DriftingAnchorage] == flag_typeOfSailing_Drifting))
		# ]
		#
		# lenAfterFilter = dfSubset.shape[0]
		# print("FILTER REMOVED " + str(lenBeforeFilter - lenAfterFilter) + " rows")
		#
		# dfSubset = dfSubset.reset_index(drop=True)
		#
		
		dfSubset = func_doTheRollingAverage(
			dfSubset,
			flag_finalFile_TotalPowerDemand,
			flag_finalFile_AvgPwrDemandOverTime,
			rollingAverageAmountOfTimeStamps,
			1
		)

		dfSubset = func_doTheRollingAverage(
			dfSubset,
			flag_finalFile_Temperature,
			flag_finalFile_AvgTemperatureOverTime,
			rollingAverageAmountOfTimeStamps,
			2
		)
		
		#print("RESORT FOR PBI")
		#dfFinal = dfFinal.sort_values([flag_finalFile_Ship, flag_finalFile_Date], ascending = [True, False]) #[True, False]
		#dfSubset = dfSubset.sort_values([flag_finalFile_Ship, flag_finalFile_Date], ascending=[True, False])  # [True, False]
	
	#endregion
	
	if EngineRunningHours_Step02_createFinalFileForPBI:
		dfFinal[flag_finalFile_Date] = pd.to_datetime(dfFinal[flag_finalFile_Date])
		dfFinal = dfFinal[dfFinal[flag_finalFile_Date] >= Infoship_runningHoursLastActualDate]
		
		func_EngineRunningHours_createStatistics(dfFinal, EngineRunningHours_Step02_predictionVersion)
		
	f_exportFinalFilesWithDataForWholeFleet(dfFinal, dfSubset)
	
	playsound('hammer_hitwall1.wav')
	
	exit()
		
# ######################################################################################################################
def func_createFeedbackFileBasedOnSingleShips(
):
	dfThisShip = pd.DataFrame()
	dfFinal = pd.DataFrame()
	
	filesToBeTreated = filedialog.askopenfilenames(
		initialdir=r'\\wrfile11\\cmg\\Fuel\\022 Energy\\Lay-Up Power Management\\Ship-Feedback'
	)
	
	useFilePicker = True
	# region LOOP Files and bring the together in one dataframe
	if useFilePicker:
		for subFile in filesToBeTreated:
			print("read file: " + subFile)
			thisShipFeedbackFile = pd.ExcelFile(subFile)
			
			dfThisShip = pd.read_excel(
				subFile,
				sheet_name='Sheet1',
				names=[
					flag_shipFeedback_C1_MainSystem,
					flag_shipFeedback_C2_SubSystem,
					flag_shipFeedback_C3_StepsTaken,
					flag_shipFeedback_C4_PercentageImplemented,
					flag_shipFeedback_C5_Comment,
					'not needed now 6',
					'not needed now 7',
					'not needed now 8'
				]
			)
			
			#print("SHIP: " + str(dfThisShip.loc[3,flag_shipFeedback_C2_SubSystem]))
			
			#region CELL SHIP NAME
			shipName = "Ship Name NOT Found"
			cellWithFlagForShipName = dfThisShip.where(dfThisShip == 'Name of Ship:').dropna(how='all').dropna(axis=1)
			if cellWithFlagForShipName.index > 0:
				shipName = dfThisShip.loc[
					cellWithFlagForShipName.index,
					flag_shipFeedback_C2_SubSystem
				]
				print("shipName: " + shipName)
			
			dfThisShip[flag_shipFeedback_C0_Ship] = dfThisShip.apply(lambda x: shipName, axis=1)
			#endregion
			
			#region CELL HVAC MODE
			hvacMode = "HVAC MODE NOT FOUND"
			cellWithFlagForHVACMode = dfThisShip.where(dfThisShip == 'HVAC mode:').dropna(how='all').dropna(axis=1)
			if cellWithFlagForHVACMode.index > 0:
				hvacMode = dfThisShip.loc[
					cellWithFlagForHVACMode.index,
					flag_shipFeedback_C4_PercentageImplemented
				]
				print("hvacMode: " + hvacMode)
				
			dfThisShip[flag_shipFeedback_C6_HVAC_Mode] = dfThisShip.apply(lambda x: hvacMode, axis=1)
			#endregion
			
			
			
			dfThisShip = func_replaceNanInThisColumn(dfThisShip, flag_shipFeedback_C1_MainSystem, 'empty')
			
			lastUsefulFlag_C1 = ""
			for ap in dfThisShip.index:
				if dfThisShip.loc[ap, flag_shipFeedback_C1_MainSystem] == 'empty':
					if lastUsefulFlag_C1 is not "":
						dfThisShip.loc[ap, flag_shipFeedback_C1_MainSystem] = lastUsefulFlag_C1
				else:
					lastUsefulFlag_C1 = dfThisShip.loc[ap, flag_shipFeedback_C1_MainSystem]
				
				if dfThisShip.loc[ap, flag_shipFeedback_C1_MainSystem] == 'Genneral Machinery':
					# print("typo correction for " + dfThisShip.loc[ap, flag_shipFeedback_C1_MainSystem] )
					dfThisShip.loc[ap, flag_shipFeedback_C1_MainSystem] = 'General Machinery'
				
				if dfThisShip.loc[ap, flag_shipFeedback_C3_StepsTaken] == 'Not Applicable':
					print("replace the string of " + dfThisShip.loc[ap, flag_shipFeedback_C3_StepsTaken] )
					dfThisShip.loc[ap, flag_shipFeedback_C3_StepsTaken] = 'n.a.'
				
				if dfThisShip.loc[ap, flag_shipFeedback_C4_PercentageImplemented] == 'Not Applicable':
					dfThisShip.loc[ap, flag_shipFeedback_C4_PercentageImplemented] = 'n.a.'
					
			dfThisShip = dfThisShip.drop([
				dfThisShip.index[0],
				dfThisShip.index[1],
				dfThisShip.index[2],
				dfThisShip.index[3]
			])
			
			dfThisShip = \
				dfThisShip[
					[
						flag_shipFeedback_C0_Ship,
						flag_shipFeedback_C1_MainSystem,
						flag_shipFeedback_C2_SubSystem,
						flag_shipFeedback_C3_StepsTaken,
						flag_shipFeedback_C4_PercentageImplemented,
						flag_shipFeedback_C5_Comment,
						flag_shipFeedback_C6_HVAC_Mode
					]
				]
			
			if dfFinal.shape[0] == 0:  # df1 is empty
				dfFinal = dfThisShip
			else:
				dfFinal = pd.concat([dfFinal, dfThisShip])
				
				# df1 = df1.sort_values([flag_finalFile_Ship, flag_finalFile_Date],
				# 							 ascending=[True, True])
				
			
			# print(dfThisShip.head(5))
	
	dfFinal.to_csv(
		'shipFeedbackFinal.csv',
		sep=';',
		decimal=',',
		index=False)
	
	playsound('hammer_hitwall1.wav')
	
	exit()


# ######################################################################################################################
def func_readAllShipFilesInThisFolder(
	sortNewData
):
	f_makeThePrintNiceStructured(True, "### READ ALL SHIP FILES ", inspect.stack()[0][3])
	startTime = time
	startTime = f_doTheTimeMeasurementInThisFunction(startTime, flag_timeStart, inspect.stack()[0][3])
	
	df1 = pd.DataFrame()
	
	if create_FINAL_FILE_LayUp_NOTHING_ELSE:
		filesToBeTreated = filedialog.askopenfilenames(
			initialdir="C:\\Users\\500095\\Desktop\\Lay Up Energy Monitoring\\02_FinalFiles\\SHIP_FILES")
	elif create_FINAL_FILE_AAQS_NOTHING_ELSE:
		filesToBeTreated = filedialog.askopenfilenames(
			initialdir="C:\\Users\\500095\\Desktop\\AAQS_FullTransparency\\Python_Code\\02_AAQS_FinalFiles\\SHIP_FILES")
	elif EngineRunningHours_Step02_createFinalFileForPBI:
		filesToBeTreated = filedialog.askopenfilenames(
			initialdir="C:\\Users\\500095\\Desktop\\Engine Running Hours\\02_FinalFiles\SHIP_FILES")
	else:
		filesToBeTreated = filedialog.askopenfilenames()
	
	useFilePicker = True
	# region LOOP Files and bring the together in one dataframe
	if useFilePicker:
		for subFile in filesToBeTreated:
			print("read " + subFile)
			
			if df1.shape[0] == 0:  # df1 is empty
				df1 = pd.read_csv(subFile, sep=';', low_memory=False)
			else:
				df2 = pd.read_csv(subFile, sep=';', low_memory=False)
				
				df1 = pd.concat([df1, df2])
			
			if sortNewData:
				df1 = df1.sort_values([flag_finalFile_Ship, flag_finalFile_Date],
										 ascending=[True, True])
		
		df1 = df1.reset_index(drop=True)
	# endregion
	
	startTime = f_doTheTimeMeasurementInThisFunction(startTime, flag_timeEnd, inspect.stack()[0][3])
	
	return df1


# ######################################################################################################################
def f_loopAllFilesInThisFolderAndCreateNewSumFile(
):
	f_makeThePrintNiceStructured(True, "### START READING ALL FILES ", inspect.stack()[0][3])
	startTime = time
	startTime = f_doTheTimeMeasurementInThisFunction(startTime, flag_timeStart, inspect.stack()[0][3])
	
	# print(os.path.dirname(os.path.realpath(__file__)))
	
	df1 = pd.DataFrame()
	
	filesToBeTreated = filedialog.askopenfilenames(initialdir="C:\\Users\\500095\\Downloads")
	
	useFilePicker = True
	# region LOOP Files and bring the together in one dataframe
	if useFilePicker:
		for subFile in filesToBeTreated:
			print("read " + subFile)
			
			if df1.shape[0] == 0:  # df1 is empty
				if dict_rawDataStructure["sourceDataStructure_PBI_preparedColumns"] == 1:
						df1 = pd.read_csv(subFile, sep=',', decimal=".", low_memory=False)
				else:
					df1 = pd.read_csv(subFile, sep=';', low_memory=False)
				
				df1 = func_prepareColumnStructureAndAddSignalTagColumn(df1)
				
			else:
				if dict_rawDataStructure["sourceDataStructure_PBI_preparedColumns"] == 1:
					df2 = pd.read_csv(subFile, sep=',', decimal=".", low_memory=False)
				else:
					df2 = pd.read_csv(subFile, sep=';', low_memory=False)
				
				df2 = func_prepareColumnStructureAndAddSignalTagColumn(df2)
				
				df1 = pd.concat([df1, df2])
		
		df1 = func_replaceColumnNamesIfNeeded(df1)
		
		df1[flag_finalFile_Date] = pd.to_datetime(df1[flag_finalFile_Date])
		
		df1 = df1.round(decimals=4)
		
		if dict_rawDataStructure["sourceDataStructure_PBI_preparedColumns"] == 1:
			df1 = df1.sort_values([flag_finalFile_Ship, flag_finalFile_Date],
										 ascending=[True, True])
		else:
			df1 = df1.sort_values([flag_finalFile_Ship, flag_finalFile_Date, flag_NeptuneLab_combinedFlags],
										 ascending=[True, True, True])
		
		df1 = df1.reset_index(drop=True)
	#endregion
	
	startTime = f_doTheTimeMeasurementInThisFunction(startTime, flag_timeEnd, inspect.stack()[0][3])
	
	return (df1)


# ######################################################################################################################
def func_replaceColumnNamesIfNeeded(
	dfInput
):
	dfInput = func_searchAndReplaceThisColumnName(dfInput, flag_layUp_date, flag_finalFile_Date)
	dfInput = func_searchAndReplaceThisColumnName(dfInput, flag_layUp_SOG, flag_finalFile_SOG)
	
	dfInput = func_searchAndReplaceThisColumnName(dfInput, flag_layUp_shipCode, flag_finalFile_Ship)
	dfInput = func_searchAndReplaceThisColumnName(dfInput, flag_layUp_DG1_ACTIVE_POWER, flag_finalFile_DG1_ACTIVE_POWER)
	dfInput = func_searchAndReplaceThisColumnName(dfInput, flag_layUp_DG2_ACTIVE_POWER, flag_finalFile_DG2_ACTIVE_POWER)
	dfInput = func_searchAndReplaceThisColumnName(dfInput, flag_layUp_DG3_ACTIVE_POWER, flag_finalFile_DG3_ACTIVE_POWER)
	dfInput = func_searchAndReplaceThisColumnName(dfInput, flag_layUp_DG4_ACTIVE_POWER, flag_finalFile_DG4_ACTIVE_POWER)
	dfInput = func_searchAndReplaceThisColumnName(dfInput, flag_layUp_DG5_ACTIVE_POWER, flag_finalFile_DG5_ACTIVE_POWER)
	dfInput = func_searchAndReplaceThisColumnName(dfInput, flag_layUp_DG6_ACTIVE_POWER, flag_finalFile_DG6_ACTIVE_POWER)

	return dfInput


# ######################################################################################################################
def func_searchAndReplaceThisColumnName(
	dfInput,
	columnNameToBeSearchedFor,
	newColumnName
):
	if columnNameToBeSearchedFor in dfInput.columns:
		dfInput = dfInput.rename(columns={columnNameToBeSearchedFor: newColumnName})
		print("REPLACE COLUMN HEADER (" +columnNameToBeSearchedFor+") with ("+newColumnName+")" )
	
	return dfInput
	

# ######################################################################################################################
def func_prepareColumnStructureAndAddSignalTagColumn(
	dfInput
):
	if \
		dict_rawDataStructure["sourceDataStructure_neptuneLab_RawData"] == 1 or \
		dict_rawDataStructure["sourceDataStructure_neptuneLab_preparedAverages"] == 1:
		
		if dict_rawDataStructure["sourceDataStructure_neptuneLab_RawData"] == 1:
			dfInput[flag_NeptuneLab_value] = dfInput[flag_NeptuneLab_value].astype(float)
		
		if dict_rawDataStructure["sourceDataStructure_neptuneLab_preparedAverages"] == 1:
			dfInput[flag_NeptuneLab_Averages_value] = dfInput[flag_NeptuneLab_Averages_value].astype(float)
		
		dfInput[flag_NeptuneLab_StandardTag] = dfInput[flag_NeptuneLab_StandardTag].astype(str)
		dfInput[flag_NeptuneLab_SignalDesription] = dfInput[flag_NeptuneLab_SignalDesription].astype(str)
		
		dfInput[flag_NeptuneLab_combinedFlags] = dfInput.apply(lambda x: f_concatenateColumns(
			x[flag_NeptuneLab_StandardTag],
			x[flag_NeptuneLab_SignalDesription]
		), axis=1)
	
	return dfInput


# ######################################################################################################################
def f_concatenateColumns(
	string_01,
	string_02
):
	return str(string_01) + "___" + str(string_02)


# ######################################################################################################################
def f_createNewAndEmptyDataframeWithPreparedTimeSlices(
	dfInput
):
	f_makeThePrintNiceStructured(True, "### Read Source File + Create empty DF with TimeSlices ", inspect.stack()[0][3])
	startTime = time
	startTime = f_doTheTimeMeasurementInThisFunction(startTime, flag_timeStart, inspect.stack()[0][3])
	
	dfFinal = pd.DataFrame()
	
	minTimeStamp = dfInput[flag_finalFile_Date].min()
	maxTimeStamp = dfInput[flag_finalFile_Date].max()
	
	print("minTimeStamp: " + str(minTimeStamp))
	print("maxTimeStamp: " + str(maxTimeStamp))
	
	dateTimeFormat = '%Y-%m-%d %H:%M:%S'
	
	# region create empty pandas dataframe with prepared time slices
	if dict_rawDataStructure["sourceDataStructure_neptuneLab_RawData"] == 1:
		dfFinal = func_createEmptyDataframeWithDefinedTimeStampStructure(
			minTimeStamp,
			maxTimeStamp,
			timeAggregationPeriodInSeconds
		)
		
		#ap = 0
		#thisTime = minTimeStamp
		#while thisTime < maxTimeStamp:
		#	ap += 1
		#	thisTime = thisTime + timedelta(seconds=timeAggregationPeriodInSeconds)
		#	dfFinal = dfFinal.append({flag_finalFile_Date: thisTime}, ignore_index=True)
	# endregion
	
	startTime = f_doTheTimeMeasurementInThisFunction(startTime, flag_timeEnd, inspect.stack()[0][3])
	
	return dfFinal, minTimeStamp, maxTimeStamp


# ######################################################################################################################
def func_createEmptyDataframeWithDefinedTimeStampStructure(
	minTimeStamp,
	maxTimeStamp,
	secondsBetweenTimeStamps
):
	dfFinal = pd.DataFrame()
	
	print("minTimeStamp: " + str(minTimeStamp))
	print("maxTimeStamp: " + str(maxTimeStamp))
	
	dateTimeFormat = '%Y-%m-%d %H:%M:%S'
	print(secondsBetweenTimeStamps)
	print(minTimeStamp)
	ap = 0
	# thisTime = datetime.datetime.strptime(minTimeStamp, dateTimeFormat)
	# maxTimeStamp = datetime.datetime.strptime(maxTimeStamp, dateTimeFormat)
	thisTime = minTimeStamp
	
	while thisTime < maxTimeStamp:
		ap += 1
		thisTime = thisTime + datetime.timedelta(seconds=secondsBetweenTimeStamps)
		#print(thisTime)
		dfFinal = dfFinal.append({flag_finalFile_Date: thisTime}, ignore_index=True)
	
	return dfFinal
	
	
# ######################################################################################################################
def f_buildAveragesPerSignalPerTimeSlice(
	dfInput,
	dfOutput
):
	f_makeThePrintNiceStructured(True, "### Create Averages per TimeSlice ", inspect.stack()[0][3])
	startTime = time
	startTime = f_doTheTimeMeasurementInThisFunction(startTime, flag_timeStart, inspect.stack()[0][3])
	
	if dict_rawDataStructure["sourceDataStructure_neptuneLab_RawData"] == 1:
		for uniqueSignal in dfInput[flag_NeptuneLab_combinedFlags].unique():
			print("### BUILD AVERAGES FOR " + uniqueSignal)
			uniqueSignal = str(uniqueSignal)
			subDF = dfInput[dfInput[flag_NeptuneLab_combinedFlags] == uniqueSignal]
			
			# flagThisSignalName = str(subDF.loc[subDF.head().index[0], flag_StandardTag]) ... Longitude does not work. god knows why
			flagThisSignalName = subDF.iloc[1, 2]
			flagThisSignalNameCounter = 'count_' + flagThisSignalName
			
			if FORCE_fullDebugAllComments:
				print("SIGNAL NAME BEFORE CHECK: " + flagThisSignalName)
			
			flagThisSignalName = f_reconvertSignalNamesForComplianceData(
				str(flagThisSignalName).strip()
			)
			
			if FORCE_fullDebugAllComments:
				print("FINAL SIGNAL NAME: " + flagThisSignalName)
			
			dfOutput[flagThisSignalName] = dfOutput.apply(lambda x: f_analyseThisRangeValues(
				x[flag_finalFile_Date],
				subDF,
				flag_return_average), axis=1)
			
			dfOutput[flagThisSignalNameCounter] = dfOutput.apply(lambda x: f_analyseThisRangeValues(
				x[flag_finalFile_Date],
				subDF,
				flag_return_count), axis=1)
	else:
		logSomeDetailsInThisFunction = False
		initialSetupDone = False
		
		for uniqueSignal in dfInput[flag_NeptuneLab_combinedFlags].unique():
			print("### BUILD AVERAGES FOR " + uniqueSignal)
			uniqueSignal = str(uniqueSignal)
			subDF = dfInput[dfInput[flag_NeptuneLab_combinedFlags] == uniqueSignal]
			
			flagThisSignalName = subDF[flag_NeptuneLab_StandardTag].iloc[1]
			
			subDF = subDF[[flag_NeptuneLab_Date, flag_NeptuneLab_Averages_value, flag_NeptuneLab_Ship]]
			if initialSetupDone == False:
				if logSomeDetailsInThisFunction:
					print("FIRST SETUP OF DF OUTPUT ... FILL DATEs AND SHIP")
				initialSetupDone = True
				dfOutput = subDF[[flag_NeptuneLab_Date, flag_NeptuneLab_Ship]]
				
				dfOutput = dfOutput.reset_index(drop=True)
			
			if logSomeDetailsInThisFunction:
				print(subDF[flag_NeptuneLab_Averages_value].head(5))
			
			flagThisSignalName = f_reconvertSignalNamesForComplianceData(
				str(flagThisSignalName).strip()
			)
			
			if logSomeDetailsInThisFunction:
				print("    final_column_name: " + flagThisSignalName)
			
			dfOutput[flagThisSignalName] = ''
			if logSomeDetailsInThisFunction:
				print("dfOutput")
				print(dfOutput.head(5))
			
			i = dfOutput.index[0]
			if logSomeDetailsInThisFunction:
				print("START WITH " + str(i))
			
			for ap in subDF.index:
				dfOutput.loc[i, flagThisSignalName] = subDF.loc[ap, flag_NeptuneLab_Averages_value]
				i += 1
			
			if logSomeDetailsInThisFunction:
				print(dfOutput.head(5))
	
	
	dfOutput = f_fillGapsWithPreviousValue(dfOutput)
	
	thisShipShortNameAsPerNLDataSet = subDF.loc[subDF.head().index[0], flag_finalFile_Ship].strip()
	print("thisShipShortNameAsPerNLDataSet: " + thisShipShortNameAsPerNLDataSet)
	
	if dict_PREPARE_RAW_DATA_FOR___['DATA_APPROACH_AAQS_DAILY'] == 1:
		thisShipLongName = dict_shipShortCodesToLongNames[str(thisShipShortNameAsPerNLDataSet)]
	else:
		thisShipLongName = dict_shipShortCodesToLongNames_LayUp[str(thisShipShortNameAsPerNLDataSet)]
	
	dfOutput[flag_finalFile_Ship] = thisShipLongName
	
	startTime = f_doTheTimeMeasurementInThisFunction(startTime, flag_timeEnd, inspect.stack()[0][3])
	
	return dfOutput, thisShipShortNameAsPerNLDataSet, minTimeStamp, maxTimeStamp


# ######################################################################################################################
def f_analyseThisRangeValues(
	thisFrameEndingTime,
	dfInput,
	flagReturnType
):
	# print(thisFrameEndingTime)
	signalsInFrame = 0
	totalValueInFrame = 0
	thisFrameStartingTime = thisFrameEndingTime - timedelta(seconds=timeAggregationPeriodInSeconds)
	
	dfInput = dfInput[
		(dfInput[flag_finalFile_Date] <= thisFrameEndingTime) &
		(dfInput[flag_finalFile_Date] >= thisFrameStartingTime)
		]
	
	# print("average for time between " + str(thisFrameStartingTime) + " to " + str(thisFrameEndingTime))
	
	if flagReturnType == flag_return_average:
		for ap in dfInput.index:
			signalsInFrame += 1
			if dict_rawDataStructure["sourceDataStructure_neptuneLab_RawData"] == 1:
				totalValueInFrame = totalValueInFrame + dfInput.loc[ap, flag_NeptuneLab_value]
			else:
				totalValueInFrame = totalValueInFrame + dfInput.loc[ap, flag_NeptuneLab_Averages_value]
		
		if signalsInFrame > 0:
			totalValueInFrame = totalValueInFrame / signalsInFrame
	
	else:
		for ap in dfInput.index:
			signalsInFrame += 1
	
	# print(flag_uniqueSignal + " @ " + str(thisFrameEndingTime) + " Ø-Value: " + str(totalValueInFrame))
	
	if flagReturnType == flag_return_average:
		return round(totalValueInFrame, 4)
	else:
		return signalsInFrame


# ######################################################################################################################
def f_fillGapsWithPreviousValue(
	dfInput
):
	dfInput = f_fillGapsForThisValue(dfInput, flag_finalFile_DG1_FUEL_OIL_IN_TE, flag_signalCounter_DG1_FUEL_OIL_IN_TE)
	dfInput = f_fillGapsForThisValue(dfInput, flag_finalFile_DG2_FUEL_OIL_IN_TE, flag_signalCounter_DG2_FUEL_OIL_IN_TE)
	dfInput = f_fillGapsForThisValue(dfInput, flag_finalFile_DG3_FUEL_OIL_IN_TE, flag_signalCounter_DG3_FUEL_OIL_IN_TE)
	dfInput = f_fillGapsForThisValue(dfInput, flag_finalFile_DG4_FUEL_OIL_IN_TE, flag_signalCounter_DG4_FUEL_OIL_IN_TE)
	dfInput = f_fillGapsForThisValue(dfInput, flag_finalFile_DG5_FUEL_OIL_IN_TE, flag_signalCounter_DG5_FUEL_OIL_IN_TE)
	dfInput = f_fillGapsForThisValue(dfInput, flag_finalFile_DG6_FUEL_OIL_IN_TE, flag_signalCounter_DG6_FUEL_OIL_IN_TE)
	
	dfInput = f_fillGapsForThisValue(dfInput, flag_finalFile_Latitude, flag_signalCounter_Latitude)
	dfInput = f_fillGapsForThisValue(dfInput, flag_finalFile_Longitude, flag_signalCounter_Longitude)
	
	return dfInput


# ######################################################################################################################
def f_fillGapsForThisValue(
	dfInput,
	thisFlag,
	incomingFlag_datapointsPerTimeSlice
):
	if thisFlag in dfInput.columns:
		print("fill gaps for " + thisFlag)
		lastValue = 0
		for ap in dfInput.index:
			if dict_rawDataStructure["sourceDataStructure_neptuneLab_RawData"] == 1:
				if \
					dfInput.loc[ap, thisFlag] == 0 and \
						dfInput.loc[ap, incomingFlag_datapointsPerTimeSlice] == 0:
					
					dfInput.loc[ap, thisFlag] = lastValue
				else:
					lastValue = dfInput.loc[ap, thisFlag]
			else:
				if \
					dfInput.loc[ap, thisFlag] == 0:
					
					dfInput.loc[ap, thisFlag] = lastValue
				else:
					lastValue = dfInput.loc[ap, thisFlag]
	
	return dfInput


# ######################################################################################################################
def f_reconvertSignalNamesForComplianceData(
	flagThisSignalName
):
	if flagThisSignalName in dict_nlComplianceComputerShortCuts.keys():
		flagThisSignalName = dict_nlComplianceComputerShortCuts[flagThisSignalName]
		print("this flag (" + str(flagThisSignalName) + ") does exist in dict >> " + str(flagThisSignalName))
	
	return flagThisSignalName


# ######################################################################################################################
def func_convertColumnNamesForFinalFile(
	dfInput
):
	print("### BEFORE RENAME ###")
	# print(dfInput.head(5))
	print(dfInput.columns)
	
	# for thisColumn in dfInput.columns:
	# 	print("JEA. " + thisColumn)
	
	dfOutput = dfInput.rename(columns={'SOG': "asfdasdfasdfasdf"}, axis='columns')
	
	# 'lastupdateutc': flag_finalFile_Date,
	# 'SOG': flag_finalFile_SOG,
	# 'DG1POW': flag_finalFile_DG1_ACTIVE_POWER,
	# 'DG2POW': flag_finalFile_DG2_ACTIVE_POWER,
	# 'DG3POW': flag_finalFile_DG3_ACTIVE_POWER,
	# 'DG4POW': flag_finalFile_DG4_ACTIVE_POWER,
	# 'DG5POW': flag_finalFile_DG5_ACTIVE_POWER,
	# 'DG6POW': flag_finalFile_DG6_ACTIVE_POWER,
	# 'DG1 SW to DeSOx Tower: FLOW  [m^3/h]': flag_finalFile_DG1_DeSOx_FLOW,
	# 'DG2 SW to DeSOx Tower: FLOW  [m^3/h]': flag_finalFile_DG2_DeSOx_FLOW,
	# 'DG3 SW to DeSOx Tower: FLOW  [m^3/h]': flag_finalFile_DG3_DeSOx_FLOW,
	# 'DG4 SW to DeSOx Tower: FLOW  [m^3/h]': flag_finalFile_DG4_DeSOx_FLOW,
	# 'DG5 SW to DeSOx Tower: FLOW  [m^3/h]': flag_finalFile_DG5_DeSOx_FLOW,
	# 'DG6 SW to DeSOx Tower: FLOW  [m^3/h]': flag_finalFile_DG6_DeSOx_FLOW
	
	print("### AFTER RENAME ###")
	# print(dfInput.head(5))
	print(dfOutput.columns)
	
	return dfOutput

# ######################################################################################################################
def f_checkForTechnicalRestrictionInPort(
	dfInput,
	thisShipLongName,
	exportDataframeAfterItWasTweakedInThisFunction
):
	f_makeThePrintNiceStructured(True, "### START CHECKUP FOR Technical Limitations ", inspect.stack()[0][3])
	
	thisShip = dfInput[flag_finalFile_Ship].iloc[1]
	
	print("dic_AAQS_PlannedForPortUsage[thisShip] :" + str(dic_AAQS_PlannedForPortUsage[thisShip]))
	
	dfInput[flag_finalFile_SOG] = dfInput[flag_finalFile_SOG].astype(float)
	
	if flag_finalFile_DriftingAnchorage not in dfInput.columns:
		dfInput[flag_finalFile_DriftingAnchorage] = ""
	
	# if thisShipLongName != "AIDAnova" and thisShipLongName != "Costa Smeralda":
	if dic_AAQS_PlannedForPortUsage[thisShipLongName] == 0 and dict_AAQS_available[thisShipLongName]:
		dfInput[flag_finalFile_technicalRestriction] = dfInput.apply(lambda x: f_adjustTechnicalRestriction(
			x[flag_finalFile_SOG],
			x[flag_finalFile_DriftingAnchorage],
			x[flag_finalFile_Date]
		), axis=1)
	
	return dfInput


# ######################################################################################################################
def f_adjustTechnicalRestriction(
	flagSpeed,
	flag_finalFile_DriftingAnchorage,
	flag_thisTimestamp
):
	if \
		flagSpeed <= flag_maxSOG_ToBeCountedAsPortStay and \
		flag_finalFile_DriftingAnchorage != flag_typeOfSailing_Anchorage and \
		flag_thisTimestamp < dict_ENV_regulationChange_AllShipsShouldTryAAQSInPort:
		return flag_AAQS_notPortReady
	
	return ""


# ######################################################################################################################
def f_checkForEnvironmentalRestrictionInPort(
	dfInput
):
	f_makeThePrintNiceStructured(True, "### CHECKUP FOR Environmental Limitations ", inspect.stack()[0][3])
	startTime = time
	startTime = f_doTheTimeMeasurementInThisFunction(startTime, flag_timeStart, inspect.stack()[0][3])
	
	dfPorts = pd.DataFrame()
	dfPorts = pd.read_csv(masterFile_PORTs, sep=';', decimal=',', encoding='latin-1', low_memory=False) #sourceFile_Non_AAAQS_ports
	
	dfPorts = func_replaceNanInThisColumn(dfPorts, flag_PORTDB_scrubberBanStartDate, 0)
	dfPorts = func_replaceNanInThisColumn(dfPorts, flag_PORTDB_scrubbersAreAllowed, -1)
	
	dfPorts[flag_PortDB_LAT] = dfPorts[flag_PortDB_LAT].astype(str)
	dfPorts[flag_PortDB_LAT] = dfPorts[flag_PortDB_LAT].str.replace(',', '.')
	dfPorts[flag_PortDB_LAT] = dfPorts[flag_PortDB_LAT].astype(float)
	
	dfPorts[flag_PortDB_LONG] = dfPorts[flag_PortDB_LONG].astype(str)
	dfPorts[flag_PortDB_LONG] = dfPorts[flag_PortDB_LONG].str.replace(',', '.')
	dfPorts[flag_PortDB_LONG] = dfPorts[flag_PortDB_LONG].astype(float)
	
	dfPorts[flag_PORTDB_scrubberBanStartDate] = dfPorts[flag_PORTDB_scrubberBanStartDate].astype('datetime64[ns]')
	
	dfInput[flag_finalFile_Latitude] = dfInput[flag_finalFile_Latitude].astype(float)
	dfInput[flag_finalFile_Longitude] = dfInput[flag_finalFile_Longitude].astype(float)
	
	dfInput[flag_finalFile_legPortName] = dfInput[flag_finalFile_legPortName].astype(str)
	
	if dict_ERASE_EXISTING_ENV_CHECKUPS_AND_REFFRESH_ALL[analysisType] == 1:
		print(chr(10) + " ERASE EXISTING ENV CHECKUP!!")
		dfInput[flag_finalFile_environmentalRestriction] = ''
	
	if funcThisShipIsAnAAQSShip(useOnlyThisShip):
		for ap in dfInput.index:
			restrictionFound = False
			
			if \
				dfInput.loc[ap, flag_finalFile_environmentalRestriction] == flag_ENV_Restriction_AAQS_NOT_allowedInThisPort or \
				dfInput.loc[ap, flag_finalFile_environmentalRestriction] == flag_ENV_Restriction_AAQS_isAllowedInThisPort:
				continue
				
			if dfInput.loc[ap, flag_finalFile_typeOfSailing] == flag_typeOfSailing_Port:
				if f_previousLineWasForSameShipInSamePort(dfInput, ap):
					continue
				
				origin = (dfInput.loc[ap, flag_finalFile_Latitude], dfInput.loc[ap, flag_finalFile_Longitude])
				for ap_ports in dfPorts.index:
					if func_thisPortDoesNotAllowScrubberAtThatTime(ap, ap_ports, dfInput, dfPorts):
						dist = (dfPorts.loc[ap_ports, flag_PortDB_LAT], dfPorts.loc[ap_ports, flag_PortDB_LONG])
						
						thisDistance = gp.geodesic(origin, dist).miles / 1.15078
						
						if thisDistance < 25:
							
								print("NO AAQS in " + dfPorts.loc[ap_ports, flag_PortDB_ports_name] + " @ " + str(
									dfInput.loc[ap, flag_finalFile_Date]
								))
								dfInput.loc[
									ap, flag_finalFile_environmentalRestriction] = flag_ENV_Restriction_AAQS_NOT_allowedInThisPort
								restrictionFound = True
								break
				
				if not restrictionFound:
					dfInput.loc[ap, flag_finalFile_environmentalRestriction] = flag_ENV_Restriction_AAQS_isAllowedInThisPort
	
	startTime = f_doTheTimeMeasurementInThisFunction(startTime, flag_timeEnd, inspect.stack()[0][3])
	
	return dfInput


# ######################################################################################################################
def funcThisShipIsAnAAQSShip(
	thisShip
):
	
	if \
		thisShip != "Costa Smeralda" and \
		thisShip != "AIDAnova" and \
		thisShip != "AIDAaura" and \
		thisShip != "AIDAcara":
		
		return True

	return False
	

# ######################################################################################################################
def func_thisPortDoesNotAllowScrubberAtThatTime(
	ap,
	ap_ports,
	dfInput,
	dfPorts
):
	flag_print = False
	
	# if dfPorts.loc[ap_ports, flag_PortDB_ports_name] == 'Hamburg':
	# 	# flag_print = True
	# 	print(chr(10) + " THIS IS HAMBURG")
	
	if flag_print:
		print("dfPorts.loc[ap_ports, flag_PORTDB_scrubberBanStartDate]" + str (dfPorts.loc[
			ap_ports, flag_PORTDB_scrubberBanStartDate]))
		print("len dfPorts.loc[ap_ports, flag_PORTDB_scrubberBanStartDate]" + str(len(str(dfPorts.loc[
			ap_ports, flag_PORTDB_scrubberBanStartDate]))))
		
	if dfPorts.loc[ap_ports, flag_PORTDB_scrubbersAreAllowed] == 0:
		if dfPorts.loc[ap_ports, flag_PORTDB_scrubberBanStartDate] == firstTimeTick:
			if flag_print:
				print("AAQS NOT ALLOWED. NO START TIME")
			
			return True
	
	if dfPorts.loc[ap_ports, flag_PORTDB_scrubberBanStartDate] > firstTimeTick:
		if dfInput.loc[ap, flag_finalFile_Date] >= dfPorts.loc[ap_ports, flag_PORTDB_scrubberBanStartDate]:
			if flag_print:
				print("AAQS NOT ALLOWED. DATE AFTER START TIME")
				
			return True
	
	if flag_print:
		print("UPS: HAMBURG")
		
	return False
	

# ######################################################################################################################
def f_previousLineWasForSameShipInSamePort(
	dfInput,
	ap
):
	if ap > 0:
		if dfInput.loc[ap - 1, flag_finalFile_typeOfSailing] == flag_typeOfSailing_Port and \
			dfInput.loc[ap, flag_finalFile_Ship] == dfInput.loc[ap - 1, flag_finalFile_Ship]:
			if f_thisLatLongRemainsTheSameAndPreviousLineHasPortName(dfInput, ap):
				# print("same port, no env change")
				dfInput.loc[ap, flag_finalFile_environmentalRestriction] = \
					dfInput.loc[ap - 1, flag_finalFile_environmentalRestriction]
				
				return True
	
	return False


# ######################################################################################################################
def f_checkIfPortBelongsTo_AAQS_NoUseArea(
	typeOfSailing,
	lat,
	long,
	db_ports
):
	if typeOfSailing == flag_typeOfSailing_Port:
		print("check that")
		origin = (lat, long)
		
		# for index, row in db_ports.iterrows():
		for ap in db_ports.index:
			dist = (db_ports.loc[ap, flag_PortDB_LAT], db_ports.loc[ap, flag_PortDB_LONG])
			
			thisDistance = gp.geodesic(origin, dist).miles / 1.15078
			
			if thisDistance < 15:
				return flag_ENV_Restriction_AAQS_NOT_allowedInThisPort
		
		return flag_ENV_Restriction_AAQS_isAllowedInThisPort
	
	return ''


# ######################################################################################################################
def func_updateSeaStateDependingOfAdvancedAnchorageAlgo(
	dfInput, analysisType
):
	#region change SAILING to PORT if Anchorage is detected
	dfInput.loc[ \
		(dfInput[flag_finalFile_typeOfSailing] == flag_typeOfSailing_Sailing) &
		(dfInput[flag_finalFile_DriftingAnchorage] == flag_typeOfSailing_Anchorage) &
		(dfInput[flag_finalFile_SOG_GAP_Filled] is not "Changed Type Of Sailing"),
		flag_finalFile_SOG_GAP_Filled
	] = "CHANGED to Port bcs of Anchorage"
	
	dfInput.loc[ \
		(dfInput[flag_finalFile_typeOfSailing] == flag_typeOfSailing_Sailing) &
		(dfInput[flag_finalFile_DriftingAnchorage] == flag_typeOfSailing_Anchorage) &
		(dfInput[flag_finalFile_SOG_GAP_Filled] is not "Changed Type Of Sailing"),
		flag_finalFile_typeOfSailing
	] = flag_typeOfSailing_Port
	#endregion
	
	# region change SAILING to PORT if Anchorage is detected
	dfInput.loc[ \
		(dfInput[flag_finalFile_typeOfSailing] == flag_typeOfSailing_Port) &
		(dfInput[flag_finalFile_DriftingAnchorage] == flag_typeOfSailing_Drifting) &
		(dfInput[flag_finalFile_SOG_GAP_Filled] is not "Changed Type Of Sailing"),
		flag_finalFile_SOG_GAP_Filled
	] = "CHANGED to Sailing bcs of Drifting"
	
	dfInput.loc[ \
		(dfInput[flag_finalFile_typeOfSailing] == flag_typeOfSailing_Port) &
		(dfInput[flag_finalFile_DriftingAnchorage] == flag_typeOfSailing_Drifting) &
		(dfInput[flag_finalFile_SOG_GAP_Filled] is not "Changed Type Of Sailing"),
		flag_finalFile_typeOfSailing
	] = flag_typeOfSailing_Sailing
	
	return dfInput
	
	#endregion

# ######################################################################################################################
def func_analyseAnchorageDrifting(
	dfInput,
	analysisType
):
	f_makeThePrintNiceStructured(True, "### DETECT Anchorage / Drifting in ", inspect.stack()[0][3])
	startTime = time
	startTime = f_doTheTimeMeasurementInThisFunction(startTime, flag_timeStart, inspect.stack()[0][3])
	
	debugInThisFunction = True
	
	step02_fillGaps = True
	step03_checkMinDuration = True
	step04_checkMinDurationBelowOnHour = False
	step05_fillGaps = False
	step06_checkTimeBetweenTwoAnchoragePositions = True
	step07_checkTimeBetweenTwoDriftingPositions = True
	
	totalAmountOfMissingItems = 0
	firstIndexWithoutDistance = 0
	
	if flag_finalFile_DriftingAnchorage not in dfInput.columns:
		print("if these columns are missing we have to do something ...")
		dict_ERASE_ALL_PREVIOUS_DriftingAnchorageData[analysisType] = 1
		
	# 	dfInput[flag_finalFile_DriftingAnchorage] = ''
	# 	dfInput[flag_finalFile_DistanceThisSlice] = 0
	# else:
	if dict_ERASE_ALL_PREVIOUS_DriftingAnchorageData[analysisType]:
		print("ERASE_ALL_PREVIOUS_DriftingAnchorageData!")
		dfInput[flag_finalFile_DriftingAnchorage] = ''
		dfInput[flag_finalFile_DistanceThisSlice] = 0
		firstIndexWithoutDistance = - 1
	
	dfInput[flag_finalFile_DistanceThisSlice] = dfInput[flag_finalFile_DistanceThisSlice].astype(float)
	
	maxIndex = dfInput.index.max()
	
	totalAmountOfMissingItems = func_getCountOf_NANs_inColumn(dfInput, flag_finalFile_DistanceThisSlice)
	print("TOTAL AMOUNT oF MISSING flag_finalFile_DistanceThisSlice " + str(totalAmountOfMissingItems))
	
	#region get distance sailed last 15min
	if totalAmountOfMissingItems > 0 or dict_ERASE_ALL_PREVIOUS_DriftingAnchorageData[analysisType]:
		timeSlicesBetweenDistance = 5
		
		for ap in dfInput.index:
			# if dfInput.loc[ap, flag_finalFile_DistanceThisSlice] == '':
			if ap > timeSlicesBetweenDistance:
				
				if func_divisonPossible(ap, progressPrintCounter):
					func_printProgress(ap, 0, maxIndex, inspect.stack()[0][3])
					
				if not dict_ERASE_ALL_PREVIOUS_DriftingAnchorageData[analysisType]:
					if firstIndexWithoutDistance == 0:
						print("Oh YEA, here it starts ... there is no distance @ " + str(ap))
						firstIndexWithoutDistance = ap
				
				thisDistance = 0
				
				if \
					abs(dfInput.loc[ap, flag_finalFile_Latitude]) - \
						abs(dfInput.loc[ap - timeSlicesBetweenDistance, flag_finalFile_Latitude]) > 0.0005:
					if \
						abs(dfInput.loc[ap, flag_finalFile_Longitude]) - \
							abs(dfInput.loc[ap - timeSlicesBetweenDistance, flag_finalFile_Longitude]) > 0.0005:
						
						origin = (dfInput.loc[ap - timeSlicesBetweenDistance, flag_finalFile_Latitude], dfInput.loc[ap - timeSlicesBetweenDistance , flag_finalFile_Longitude])
						dist = (dfInput.loc[ap, flag_finalFile_Latitude], dfInput.loc[ap, flag_finalFile_Longitude])
						
						thisDistance = gp.geodesic(origin, dist).miles / 1.15078
				
				# print("thisDistance" + str(thisDistance))
				dfInput.loc[ap, flag_finalFile_DistanceThisSlice] = thisDistance
	#endregion
	
	print("take the shortcut and only calculate new values beginning from: " + str(firstIndexWithoutDistance))
	
	#region detect Drifting / Anchorage
	if totalAmountOfMissingItems > 0 or dict_ERASE_ALL_PREVIOUS_DriftingAnchorageData[analysisType]:
		for ap in dfInput.index:
			if ap < firstIndexWithoutDistance and not dict_ERASE_ALL_PREVIOUS_DriftingAnchorageData[analysisType]:
				continue
			
			if func_divisonPossible(ap, progressPrintCounter):
				func_printProgress(ap, 0, maxIndex, inspect.stack()[0][3])
				
			if dfInput.loc[ap, flag_finalFile_Date] > noDriftOrAnchorageBeforeThatDate:
				
				longTermAverageSpeedSlices = \
					minTimeDriftingInMinutes / 60 * dfInput.loc[ap, flag_finalFile_timestampsPerHour]
				
				averageSpeedLongTerm = dfInput.loc[ap - longTermAverageSpeedSlices:ap, flag_finalFile_SOG].mean()
				if averageSpeedLongTerm > maxAverageSpeedDrifting or averageSpeedLongTerm < minAvgSpeedAtAnchor:
					continue
				
				stdDevLongTerm = dfInput.loc[ap-longTermAverageSpeedSlices:ap, flag_finalFile_SOG].std()
				avgDistanceSailedLastDPs = dfInput.loc[ap - 5:ap, flag_finalFile_DistanceThisSlice].mean()
				
				if \
					averageSpeedLongTerm > minAvgSpeedAtAnchor and \
					averageSpeedLongTerm <= maxAvgSpeedAtAnchor and \
					stdDevLongTerm <= maxAvgSpeedAtAnchor * 0.5 and \
					avgDistanceSailedLastDPs < flag_anchorage_max_avgDistanceBetweenDPs and \
					dfInput.loc[ap, flag_finalFile_SOG] <= 2*maxAvgSpeedAtAnchor:
					
					dfInput.loc[ap, flag_finalFile_DriftingAnchorage] = flag_typeOfSailing_Anchorage
					
				if \
					averageSpeedLongTerm > minAverageSpeedDrifting and \
					averageSpeedLongTerm <= maxAverageSpeedDrifting and \
					stdDevLongTerm <= maxAverageSpeedDrifting * 0.5 and \
					avgDistanceSailedLastDPs < flag_drifting_max_avgDistanceBetweenDPs and \
					dfInput.loc[ap, flag_finalFile_SOG] <= 2*maxAverageSpeedDrifting:
					
					dfInput.loc[ap, flag_finalFile_DriftingAnchorage] = flag_typeOfSailing_Drifting
	#endregion
	
	startBlankAfterDrift = 0
	blankCounterAfterDrift = 0
	
	startBlankAfterAnchorage = 0
	blankCounterAfterAnchorage = 0
	
	#region step02_fillGaps >> FILL GAPs, mainly caused by repositioning or little fluctuations in the data
	if step02_fillGaps:
		if totalAmountOfMissingItems > 0 or dict_ERASE_ALL_PREVIOUS_DriftingAnchorageData[analysisType]:
			print(chr(10) + " step02_fillGaps >>> fill DRIFT/ANCHORAGE GAPs ")
			for ap in dfInput.index:
				if ap < firstIndexWithoutDistance and not dict_ERASE_ALL_PREVIOUS_DriftingAnchorageData[analysisType]:
					continue
					
				if ap > 0:
					
					if \
						dfInput.loc[ap - 1, flag_finalFile_DriftingAnchorage] == flag_typeOfSailing_Drifting and \
						dfInput.loc[ap, flag_finalFile_DriftingAnchorage] == '':
						
						# print("START startBlankAfterDrift @ " + str(ap) + " @ " + str(
						# 	dfInput.loc[ap, flag_finalFile_Date]))
						
						startBlankAfterDrift = ap
						blankCounterAfterDrift = 1
						
						startBlankAfterAnchorage = 0
						blankCounterAfterAnchorage = 0
						
						continue
					
					if \
						dfInput.loc[ap - 1, flag_finalFile_DriftingAnchorage] == flag_typeOfSailing_Anchorage and \
						dfInput.loc[ap, flag_finalFile_DriftingAnchorage] == '':
						
						# print("START blankCounterAfterAnchorage @ " + str(ap) + " @ " + str(
						# 	dfInput.loc[ap, flag_finalFile_Date]))
						
						startBlankAfterAnchorage = ap
						blankCounterAfterAnchorage = 1
						
						startBlankAfterDrift = 0
						blankCounterAfterDrift = 0
						
						continue
					
					if dfInput.loc[ap, flag_finalFile_DriftingAnchorage] == '':
						if blankCounterAfterDrift > 0:
							blankCounterAfterDrift += 1
							continue
						
						if blankCounterAfterAnchorage > 0:
							blankCounterAfterAnchorage += 1
							continue
					
					if \
						dfInput.loc[ap, flag_finalFile_DriftingAnchorage] == flag_typeOfSailing_Drifting and \
						blankCounterAfterDrift > 0:
						
						# print("END blankCounterAfterDrift: " + str(blankCounterAfterDrift) + " @ " + str(dfInput.loc[ap, flag_finalFile_Date]))
						# print("OVERWRITE blanks between " + str(startBlankAfterDrift) + " and " + str(ap))
						
						
						if \
							blankCounterAfterDrift < 30 or ( blankCounterAfterDrift < 160 and \
								dfInput.loc[startBlankAfterDrift:ap - 1, flag_finalFile_SOG].mean() > minAverageSpeedDrifting and \
								dfInput.loc[startBlankAfterDrift:ap - 1, flag_finalFile_SOG].mean() <= maxAverageSpeedDrifting
							):
							
							print("CONVERT GAP between " + str(startBlankAfterDrift) + " and " + str(ap) +
									" into DRIFT >>> avg speed during this period: " +
									str(dfInput.loc[startBlankAfterDrift:ap - 1,flag_finalFile_SOG].mean())
							)
							
							dfInput.loc[
								startBlankAfterDrift:ap - 1, flag_finalFile_DriftingAnchorage] = flag_typeOfSailing_Drifting
						
						blankCounterAfterDrift = 0
						blankCounterAfterAnchorage = 0
						continue
					
					if \
						dfInput.loc[ap, flag_finalFile_DriftingAnchorage] == flag_typeOfSailing_Anchorage and \
						blankCounterAfterAnchorage > 0:
						
						useOldAlgoWithJustSpeed = False
						
						if useOldAlgoWithJustSpeed:
							if \
								blankCounterAfterAnchorage < 30 or (blankCounterAfterAnchorage < 160 and \
									dfInput.loc[startBlankAfterAnchorage:ap - 1, flag_finalFile_SOG].mean() > 0 and \
									dfInput.loc[startBlankAfterAnchorage:ap - 1, flag_finalFile_SOG].mean() <= maxAvgSpeedAtAnchor
								):
								
								print("CONVERT GAP between " + str(startBlankAfterAnchorage) + " and " + str(ap) +
										" into ANCHORAGE >>> avg speed during this period: " +
										str(dfInput.loc[startBlankAfterAnchorage:ap - 1, flag_finalFile_SOG].mean())
								)
								
								dfInput.loc[
									startBlankAfterAnchorage:ap - 1, flag_finalFile_DriftingAnchorage] = flag_typeOfSailing_Anchorage
						else:
							
							print(chr(10) +
									"ANALYSE LAT LONG between two anchorage positions " +
									str(dfInput.loc[startBlankAfterAnchorage, flag_finalFile_Date]) + "("+
									str(startBlankAfterAnchorage) + ") and " +
									str(dfInput.loc[ap, flag_finalFile_Date]) + "(" +
									str(ap) +
									") into ANCHORAGE >>> avg speed during this period: " +
									str(dfInput.loc[startBlankAfterAnchorage:ap - 1, flag_finalFile_SOG].mean())
									)
							
							lastAnchoragePlace = (
								dfInput.loc[startBlankAfterAnchorage - 1, flag_finalFile_Latitude],
								dfInput.loc[startBlankAfterAnchorage - 1, flag_finalFile_Longitude]
							)
							
							maxDistance = 0
							thisGapAp = startBlankAfterAnchorage - 1
							while thisGapAp < ap:
								thisGapAp += 1
								thisGapPosition = (
									dfInput.loc[thisGapAp, flag_finalFile_Latitude],
									dfInput.loc[thisGapAp, flag_finalFile_Longitude]
								)
							
								thisDistance = gp.geodesic(lastAnchoragePlace, thisGapPosition).miles / 1.15078
								# print("thisDistance: " + str(thisDistance))
								if thisDistance > maxDistance:
									maxDistance = thisDistance
							
							print(chr(10) + " maxDistance during this period: " + str(maxDistance))
							
							if maxDistance < 1:
								dfInput.loc[
								startBlankAfterAnchorage:ap - 1, flag_finalFile_DriftingAnchorage] = flag_typeOfSailing_Anchorage
							else:
								print("STOP. DO NOT CONVERT TO ANCHORAGE")
						
						blankCounterAfterDrift = 0
						blankCounterAfterAnchorage = 0
						continue
	# endregion
	
	#region step03_checkMinDuration >> CHECK if min duration was fullfilled to avoid pointless spikes
	if step03_checkMinDuration:
		if totalAmountOfMissingItems > 0 or dict_ERASE_ALL_PREVIOUS_DriftingAnchorageData[analysisType]:
			consecutiveSlices = minTimeDriftingInMinutes / 60 * dfInput.loc[ap, flag_finalFile_timestampsPerHour]
			
			consecutiveAnchorage = 0
			consecutiveDrifting = 0
			
			for ap in dfInput.index:
				if ap < firstIndexWithoutDistance and not dict_ERASE_ALL_PREVIOUS_DriftingAnchorageData[analysisType]:
					continue
					
				if dfInput.loc[ap, flag_finalFile_DriftingAnchorage] == flag_typeOfSailing_Anchorage:
					consecutiveAnchorage +=1
					# if debugInThisFunction:
					# 	print(
					# 		"consecutiveAnchorage datapoints @ " + str(dfInput.loc[ap, flag_finalFile_Date]) + " = " + str(consecutiveAnchorage))
					
					if consecutiveDrifting > 0 and consecutiveDrifting < consecutiveSlices:
						if debugInThisFunction:
							print("STEP 1: erase drifting between " +
									str(dfInput.loc[ap - consecutiveDrifting, flag_finalFile_Date]) + " and " +
									str(dfInput.loc[ap, flag_finalFile_Date]) + " and " +
									" >>> consecutiveDrifting datapoints only " + str(consecutiveDrifting))
							
						dfInput.loc[ap-consecutiveDrifting:ap, flag_finalFile_DriftingAnchorage] = ''
					
					consecutiveDrifting = 0
					
					continue
				
				if dfInput.loc[ap, flag_finalFile_DriftingAnchorage] == flag_typeOfSailing_Drifting:
					consecutiveDrifting +=1
					# if debugInThisFunction:
					# 	print(
					# 		"consecutiveDrifting  @ " + str(dfInput.loc[ap, flag_finalFile_Date]) + " = " + str(consecutiveDrifting))
					
					if consecutiveAnchorage > 0:
						avgDistancePerSliceLastAnchorage = \
							dfInput.loc[ap - consecutiveAnchorage:ap, flag_finalFile_DistanceThisSlice].mean()
						
						if avgDistancePerSliceLastAnchorage > flag_drifting_min_avgDistanceBetweenDPs:
							if debugInThisFunction:
								print("CONVERT ANCHORAGE TO DRIFTING between " +
										str(dfInput.loc[ap - consecutiveAnchorage, flag_finalFile_Date]) + " and " +
										str(dfInput.loc[ap, flag_finalFile_Date]) +
										" because of high avg distance per slice")
							
							dfInput.loc[ap - consecutiveAnchorage:ap, flag_finalFile_DriftingAnchorage] = flag_typeOfSailing_Drifting
							consecutiveDrifting = consecutiveDrifting + consecutiveAnchorage
						else:
							if consecutiveAnchorage > 0 and consecutiveAnchorage < consecutiveSlices:
								if debugInThisFunction:
									print("STEP 1: erase anchorage between "  +
											str(dfInput.loc[ap - consecutiveAnchorage, flag_finalFile_Date]) + " and " +
											str(dfInput.loc[ap, flag_finalFile_Date]) +
											" >>> consecutiveAnchorage datapoints only " + str(consecutiveAnchorage))
								
								dfInput.loc[ap - consecutiveAnchorage:ap, flag_finalFile_DriftingAnchorage] = ''
					
					consecutiveAnchorage = 0
					
					continue
				
				if consecutiveDrifting > 0 and consecutiveDrifting < consecutiveSlices:
					if debugInThisFunction:
						print("STEP 2: erase drifting between " +
								str(dfInput.loc[ap - consecutiveDrifting, flag_finalFile_Date]) + " and " +
								str(dfInput.loc[ap, flag_finalFile_Date]) +
								" >>> consecutiveDrifting only " + str(consecutiveDrifting))
						
					dfInput.loc[ap - consecutiveDrifting:ap, flag_finalFile_DriftingAnchorage] = ''
					consecutiveDrifting = 0
					
				if consecutiveAnchorage > 0 and consecutiveAnchorage < consecutiveSlices:
					if debugInThisFunction:
						print("STEP 2: erase anchorage between " +
								str(dfInput.loc[ap - consecutiveAnchorage, flag_finalFile_Date]) + " and " +
								str(dfInput.loc[ap, flag_finalFile_Date]) +
								" >>> consecutiveAnchorage only " + str(consecutiveAnchorage))
					
					dfInput.loc[ap - consecutiveAnchorage:ap, flag_finalFile_DriftingAnchorage] = ''
					consecutiveAnchorage = 0
				
				consecutiveDrifting = 0
				consecutiveAnchorage = 0
	#endregion
	
	#region step04_checkMinDurationBelowOnHour >> delete very short periods of Anchorage and Drifting (below 3hours)
	if step04_checkMinDurationBelowOnHour:
		if totalAmountOfMissingItems > 0 or dict_ERASE_ALL_PREVIOUS_DriftingAnchorageData[analysisType]:
			driftingCounter = 0
			driftStartAp = 0
			
			anchorageCounter = 0
			anchorageStartAp = 0
			
			for ap in dfInput.index:
				if ap < firstIndexWithoutDistance and not dict_ERASE_ALL_PREVIOUS_DriftingAnchorageData[analysisType]:
					continue
					
				if dfInput.loc[ap, flag_finalFile_DriftingAnchorage] == flag_typeOfSailing_Drifting:
					driftingCounter +=1
					driftStartAp = ap
				
				if dfInput.loc[ap, flag_finalFile_DriftingAnchorage] == flag_typeOfSailing_Anchorage:
					anchorageCounter +=1
					anchorageStartAp = ap
				
				if dfInput.loc[ap, flag_finalFile_DriftingAnchorage] == '':
					if driftingCounter > 0 and driftingCounter < 60:
						if debugInThisFunction:
							print("STEP 3: erase drifting between " +
									str(dfInput.loc[driftStartAp, flag_finalFile_Date]) + " and " +
									str(dfInput.loc[ap, flag_finalFile_Date]) +
									" >>> driftingCounter < 60 >>> only: " + str(consecutiveAnchorage))
						
						dfInput.loc[driftStartAp:ap, flag_finalFile_DriftingAnchorage] = ''
					
					if anchorageCounter > 0 and anchorageCounter < 60:
						if debugInThisFunction:
							print("STEP 3: erase anchorage between " +
									str(dfInput.loc[anchorageStartAp, flag_finalFile_Date]) + " and " +
									str(dfInput.loc[ap, flag_finalFile_Date]) +
									" >>> anchorageCounter < 60 >>> only: " + str(consecutiveAnchorage))
							
						dfInput.loc[anchorageStartAp:ap, flag_finalFile_DriftingAnchorage] = ''
					
					anchorageCounter = 0
					anchorageStartAp = 0
					
					driftingCounter = 0
					driftStartAp = 0
	#endregion)
	
	# region step05_fillGaps >> FILL GAPs, mainly caused by repositioning or little fluctuations in the data
	if step05_fillGaps:
		if totalAmountOfMissingItems > 0 or dict_ERASE_ALL_PREVIOUS_DriftingAnchorageData[analysisType]:
			startBlankAfterDrift = 0
			blankCounterAfterDrift = 0
			
			startBlankAfterAnchorage = 0
			blankCounterAfterAnchorage = 0
			
			print("fill DRIFT/ANCHORAGE GAPs ")
			for ap in dfInput.index:
				if ap < firstIndexWithoutDistance and not dict_ERASE_ALL_PREVIOUS_DriftingAnchorageData[analysisType]:
					continue
					
				if ap > 0:
					
					if \
						dfInput.loc[ap - 1, flag_finalFile_DriftingAnchorage] == flag_typeOfSailing_Drifting and \
							dfInput.loc[ap, flag_finalFile_DriftingAnchorage] == '':
						# print("START startBlankAfterDrift @ " + str(ap) + " @ " + str(
						# 	dfInput.loc[ap, flag_finalFile_Date]))
						
						startBlankAfterDrift = ap
						blankCounterAfterDrift = 1
						
						startBlankAfterAnchorage = 0
						blankCounterAfterAnchorage = 0
						
						continue
					
					if \
						dfInput.loc[ap - 1, flag_finalFile_DriftingAnchorage] == flag_typeOfSailing_Anchorage and \
							dfInput.loc[ap, flag_finalFile_DriftingAnchorage] == '':
						# print("START blankCounterAfterAnchorage @ " + str(ap) + " @ " + str(
						# 	dfInput.loc[ap, flag_finalFile_Date]))
						
						startBlankAfterAnchorage = ap
						blankCounterAfterAnchorage = 1
						
						startBlankAfterDrift = 0
						blankCounterAfterDrift = 0
						
						continue
					
					if dfInput.loc[ap, flag_finalFile_DriftingAnchorage] == '':
						if blankCounterAfterDrift > 0:
							blankCounterAfterDrift += 1
							continue
						
						if blankCounterAfterAnchorage > 0:
							blankCounterAfterAnchorage += 1
							continue
					
					if \
						dfInput.loc[ap, flag_finalFile_DriftingAnchorage] == flag_typeOfSailing_Drifting and \
							blankCounterAfterDrift > 0:
						
						# print("END blankCounterAfterDrift: " + str(blankCounterAfterDrift) + " @ " + str(dfInput.loc[ap, flag_finalFile_Date]))
						
						
						if blankCounterAfterDrift < 60:
							if debugInThisFunction:
								print(
									"STEP 4: OVERWRITE blanks with DRIFTING!! between " +
									str(dfInput.loc[startBlankAfterDrift, flag_finalFile_Date]) + " and " +
									str(dfInput.loc[ap - 1, flag_finalFile_Date])
								)
							
							dfInput.loc[startBlankAfterDrift:ap - 1, flag_finalFile_DriftingAnchorage] = flag_typeOfSailing_Drifting
						
						blankCounterAfterDrift = 0
						blankCounterAfterAnchorage = 0
						continue
					
					if \
						dfInput.loc[ap, flag_finalFile_DriftingAnchorage] == flag_typeOfSailing_Anchorage and \
							blankCounterAfterAnchorage > 0:
						
						if blankCounterAfterAnchorage < 60:
							if debugInThisFunction:
								print(
									"STEP 4: OVERWRITE blanks with ANCHORAGE!! between " +
									str(dfInput.loc[startBlankAfterAnchorage, flag_finalFile_Date]) + " and " +
									str(dfInput.loc[ap - 1, flag_finalFile_Date])
								)
							
							dfInput.loc[startBlankAfterAnchorage:ap - 1,	flag_finalFile_DriftingAnchorage] = flag_typeOfSailing_Anchorage
						
						blankCounterAfterDrift = 0
						blankCounterAfterAnchorage = 0
						continue
	# endregion
	
	#region step06_checkTimeBetweenTwoAnchoragePositions >> check for distance and speed between two anchorage positions
	if step06_checkTimeBetweenTwoAnchoragePositions:
		if totalAmountOfMissingItems > 0 or dict_ERASE_ALL_PREVIOUS_DriftingAnchorageData[analysisType]:
			print(chr(10) + " step06_checkTimeBetweenTwoAnchoragePositions")
			
			for ap in dfInput.index:
				if ap < firstIndexWithoutDistance and not dict_ERASE_ALL_PREVIOUS_DriftingAnchorageData[analysisType]:
					continue
					
				if ap > 0:
					if \
						dfInput.loc[ap-1, flag_finalFile_DriftingAnchorage] == flag_typeOfSailing_Anchorage and \
						dfInput.loc[ap, flag_finalFile_DriftingAnchorage] != flag_typeOfSailing_Anchorage:
						startBlankAfterAnchorage = ap
					
					if \
						startBlankAfterAnchorage > 0 and \
						dfInput.loc[ap, flag_finalFile_DriftingAnchorage] == flag_typeOfSailing_Anchorage and \
						dfInput.loc[ap - 1, flag_finalFile_DriftingAnchorage] != flag_typeOfSailing_Anchorage:
						
						avgSpeedDuringBetweenAnchoragePlaces = dfInput.loc[startBlankAfterAnchorage:ap - 1,
																			flag_finalFile_SOG].mean()
						
						print(chr(10) +
								"ANALYSE LAT LONG between two anchorage postions " +
								str(dfInput.loc[startBlankAfterAnchorage, flag_finalFile_Date]) + "(" +
								str(startBlankAfterAnchorage) + ") and " +
								str(dfInput.loc[ap, flag_finalFile_Date]) + "(" +
								str(ap) +
								") into ANCHORAGE >>> avg speed: " +
								str(avgSpeedDuringBetweenAnchoragePlaces)
							)
						
						useSpeedCheck = False
						
						if \
							useSpeedCheck is False or ( useSpeedCheck and \
							dfInput.loc[startBlankAfterAnchorage:ap - 1, flag_finalFile_SOG].mean() > 0 and \
							dfInput.loc[startBlankAfterAnchorage:ap - 1, flag_finalFile_SOG].mean() <= maxAvgSpeedAtAnchor):
							
							#region get max distance between last anchorage and all lat longs until next anchorage
							lastAnchoragePlace = (
								dfInput.loc[startBlankAfterAnchorage-1, flag_finalFile_Latitude],
								dfInput.loc[startBlankAfterAnchorage-1, flag_finalFile_Longitude]
							)
							
							maxDistance = 0
							thisGapAp = startBlankAfterAnchorage - 1
							while thisGapAp < ap:
								thisGapAp += 1
								thisGapPosition = (
									dfInput.loc[thisGapAp, flag_finalFile_Latitude],
									dfInput.loc[thisGapAp, flag_finalFile_Longitude]
								)
								
								thisDistance = gp.geodesic(lastAnchoragePlace, thisGapPosition).miles / 1.15078
								# print("thisDistance: " + str(thisDistance))
								if thisDistance > maxDistance:
									maxDistance = thisDistance
							
							print(chr(10) + " maxDistance during this period: " + str(maxDistance))
							#endregion
							
							if maxDistance < 1:
								dfInput.loc[
								startBlankAfterAnchorage:ap - 1, flag_finalFile_DriftingAnchorage] = flag_typeOfSailing_Anchorage
							else:
								print("STOP. DO NOT CONVERT TO ANCHORAGE")
						else:
							print("AVG SPEED to high ... this can not be anchorage, ship is moving")
						
						startBlankAfterAnchorage = 0
			
	#endregion
	
	# region step07_checkTimeBetweenTwoDriftingPositions >> check for distance and speed between two drifting positions
	if step07_checkTimeBetweenTwoDriftingPositions:
		print(chr(10) + " step07_checkTimeBetweenTwoDriftingPositions")
		
		for ap in dfInput.index:
			if ap < firstIndexWithoutDistance and not dict_ERASE_ALL_PREVIOUS_DriftingAnchorageData[analysisType]:
				continue
				
			if ap > 0:
				if \
					dfInput.loc[ap - 1, flag_finalFile_DriftingAnchorage] == flag_typeOfSailing_Drifting and \
					dfInput.loc[ap, flag_finalFile_DriftingAnchorage] != flag_typeOfSailing_Drifting:
					
					startBlankAfterDrift = ap
				
				if \
					startBlankAfterDrift > 0 and \
						dfInput.loc[ap, flag_finalFile_DriftingAnchorage] == flag_typeOfSailing_Drifting and \
						dfInput.loc[ap - 1, flag_finalFile_DriftingAnchorage] != flag_typeOfSailing_Drifting:
					
					avgSpeedBetweenDriftingPlaces = dfInput.loc[startBlankAfterDrift:ap - 1,
																		flag_finalFile_SOG].mean()
					
					print(chr(10) +
							"ANALYSE LAT LONG between two drifting postions " +
							str(dfInput.loc[startBlankAfterDrift, flag_finalFile_Date]) + "(" +
							str(startBlankAfterDrift) + ") and " +
							str(dfInput.loc[ap, flag_finalFile_Date]) + "(" +
							str(ap) +
							") into DRFITING >>> avg speed: " +
							str(avgSpeedBetweenDriftingPlaces)
							)
					
					useSpeedCheck = True
					
					if \
						useSpeedCheck is False or (
							useSpeedCheck and \
							(startBlankAfterDrift < 30 or
							 (dfInput.loc[startBlankAfterDrift:ap - 1, flag_finalFile_SOG].mean() > minAverageSpeedDrifting and \
							dfInput.loc[startBlankAfterDrift:ap - 1, flag_finalFile_SOG].mean() <= maxAverageSpeedDrifting))):
					
						dfInput.loc[
							startBlankAfterDrift:ap - 1,
							flag_finalFile_DriftingAnchorage] = flag_typeOfSailing_Drifting
					
					startBlankAfterDrift = 0
	
	startTime = f_doTheTimeMeasurementInThisFunction(startTime, flag_timeEnd, inspect.stack()[0][3])
	
	return dfInput


# ######################################################################################################################
def f_addSailingMode(
	dfInput
):
	f_makeThePrintNiceStructured(True, "### 1st STEP SAILING TPYE depending of speed in ", inspect.stack()[0][3])
	startTime = time
	startTime = f_doTheTimeMeasurementInThisFunction(startTime, flag_timeStart, inspect.stack()[0][3])
	
	dfInput[flag_finalFile_typeOfSailing] = dfInput.apply(lambda x: f_getSailingType(
		x[flag_finalFile_SOG]
	), axis=1)
	
	startTime = f_doTheTimeMeasurementInThisFunction(startTime, flag_timeEnd, inspect.stack()[0][3])
	
	return dfInput


# ######################################################################################################################
def f_getSailingType(
	thisSpeed
):
	if thisSpeed <= flag_maxSOG_ToBeCountedAsPortStay:
		return flag_typeOfSailing_Port
	else:
		return flag_typeOfSailing_Sailing
	

# ######################################################################################################################
def func_reloopAllLinesAndCorrectLittleSpeedFluctuations(
	dfInput
):
	f_makeThePrintNiceStructured(True, "### 1st STEP SAILING TPYE >> CORRECT TYPE OF SAILING FOR FLUCTUATIONs ", inspect.stack()[0][3])
	startTime = time
	startTime = f_doTheTimeMeasurementInThisFunction(startTime, flag_timeStart, inspect.stack()[0][3])
	
	cnt_linesOfSailing = 0
	ap_startOfSailing = 0
	
	cnt_linesOfPort = 0
	ap_startOfPort = 0
	
	lastMode = ''
	
	for ap in dfInput.index:
		if dfInput.loc[ap, flag_finalFile_SOG] < flag_maxSOG_ToBeCountedAsPortStay:
			if lastMode == flag_typeOfSailing_Sailing:
				if cnt_linesOfPort > 5 and cnt_linesOfSailing < 5:
					if ap_startOfSailing > 0:
						dfInput = func_overwriteTypeOfSailing(dfInput, ap_startOfSailing, ap, flag_typeOfSailing_Port)
				
				cnt_linesOfPort = 1
				ap_startOfPort = ap
			else:
				cnt_linesOfPort += 1
			
			lastMode = flag_typeOfSailing_Port
		
		
		if dfInput.loc[ap, flag_finalFile_SOG] >= flag_maxSOG_ToBeCountedAsPortStay:
			if lastMode == flag_typeOfSailing_Port:
				if cnt_linesOfPort < 5 and cnt_linesOfSailing > 5:
					if ap_startOfPort > 0:
						dfInput = func_overwriteTypeOfSailing(dfInput, ap_startOfPort, ap, flag_typeOfSailing_Sailing)
				
				cnt_linesOfSailing = 1
				ap_startOfSailing = ap
				
			else:
				cnt_linesOfSailing += 1
			
			lastMode = flag_typeOfSailing_Sailing
	
	startTime = f_doTheTimeMeasurementInThisFunction(startTime, flag_timeEnd, inspect.stack()[0][3])
	
	return dfInput


# ######################################################################################################################
def func_overwriteTypeOfSailing(
	dfInput,
	ap_startFlagToBeChanged,
	ap_endFlagToBeChanged,
	flag_newTypeOfSailing
):
	thisAp = ap_startFlagToBeChanged
	
	# print("TYPE OF SAILING will be changed between " + str(ap_startFlagToBeChanged) + " and " + str(ap_endFlagToBeChanged))
	
	while thisAp < ap_endFlagToBeChanged:
		# print("change flag type of sailing @ place " +str(thisAp) + " from " + dfInput.loc[thisAp, flag_finalFile_typeOfSailing] + " to " +flag_newTypeOfSailing )
		dfInput.loc[thisAp, flag_finalFile_typeOfSailing] = flag_newTypeOfSailing
		
		if flag_newTypeOfSailing == flag_typeOfSailing_Sailing:
			dfInput.loc[thisAp, flag_finalFile_legPortName] = ""
			
		dfInput.loc[thisAp, flag_finalFile_SOG_GAP_Filled] = "Changed Type Of Sailing"
		thisAp += 1
	
	return dfInput


# ######################################################################################################################
def func_getCountOf_NANs_inColumn(
	dfInput,
	thisColumn
):
	nanColumns = 0
	if thisColumn in dfInput.columns:
		nanColumns = dfInput[thisColumn].isnull().sum(axis=0)
	
	return nanColumns


# ######################################################################################################################
def func_checkForResetOfFuelTypeAndAAQSAssessment(
	dfInput,
	flag_thisEngineFuelType
):
	forceRefreshOfAllData = False
	
	if dict_ERASE_ALL_PREVIOUS_FuelTypePerEngines[analysisType] or \
		dict_ERASE_ALL_PREVIOUS_AAQS_PORT_ASSESSMENTS[analysisType] or \
		dict_ERASE_ALL_PREVIOUS_AAQS_ASSESSMENTS[analysisType]:
		
		print("RESET ALL FUEL TYPE VALUES FOR DG# " + flag_thisEngineFuelType)
		
		forceRefreshOfAllData = True
		
		dfInput[flag_thisEngineFuelType] = ''
	
	return dfInput, forceRefreshOfAllData


# ######################################################################################################################
def func_getThisEngineColumns(
	thisEngineNumber
):
	if thisEngineNumber == 1:
		flag_enginePowerAbsolut = flag_finalFile_DG1_ACTIVE_POWER
		flag_thisEngineFuelType = flag_finalFile_fuelType_DG01
		flag_thisEngineFuelInletTemp = flag_finalFile_DG1_FUEL_OIL_IN_TE
		flag_thisDeSoxFlowRate = flag_finalFile_DG1_DeSOx_FLOW
	
	if thisEngineNumber == 2:
		flag_enginePowerAbsolut = flag_finalFile_DG2_ACTIVE_POWER
		flag_thisEngineFuelType = flag_finalFile_fuelType_DG02
		flag_thisEngineFuelInletTemp = flag_finalFile_DG2_FUEL_OIL_IN_TE
		flag_thisDeSoxFlowRate = flag_finalFile_DG2_DeSOx_FLOW

	if thisEngineNumber == 3:
		flag_enginePowerAbsolut = flag_finalFile_DG3_ACTIVE_POWER
		flag_thisEngineFuelType = flag_finalFile_fuelType_DG03
		flag_thisEngineFuelInletTemp = flag_finalFile_DG3_FUEL_OIL_IN_TE
		flag_thisDeSoxFlowRate = flag_finalFile_DG3_DeSOx_FLOW

	if thisEngineNumber == 4:
		flag_enginePowerAbsolut = flag_finalFile_DG4_ACTIVE_POWER
		flag_thisEngineFuelType = flag_finalFile_fuelType_DG04
		flag_thisEngineFuelInletTemp = flag_finalFile_DG4_FUEL_OIL_IN_TE
		flag_thisDeSoxFlowRate = flag_finalFile_DG4_DeSOx_FLOW

	if thisEngineNumber == 5:
		flag_enginePowerAbsolut = flag_finalFile_DG5_ACTIVE_POWER
		flag_thisEngineFuelType = flag_finalFile_fuelType_DG05
		flag_thisEngineFuelInletTemp = flag_finalFile_DG5_FUEL_OIL_IN_TE
		flag_thisDeSoxFlowRate = flag_finalFile_DG5_DeSOx_FLOW

	if thisEngineNumber == 6:
		flag_enginePowerAbsolut = flag_finalFile_DG6_ACTIVE_POWER
		flag_thisEngineFuelType = flag_finalFile_fuelType_DG06
		flag_thisEngineFuelInletTemp = flag_finalFile_DG6_FUEL_OIL_IN_TE
		flag_thisDeSoxFlowRate = flag_finalFile_DG6_DeSOx_FLOW
	
	return flag_enginePowerAbsolut, flag_thisEngineFuelType, flag_thisEngineFuelInletTemp, flag_thisDeSoxFlowRate


# ######################################################################################################################
def f_getFuelTypePerEnginePerTimeslice(
	dfInput,
	thisShipLongName
):
	f_makeThePrintNiceStructured(True, "### ENGINE ON/OFF & FUEL TYPE PER ENGINE ", inspect.stack()[0][3])
	
	thisEngine = 1
	while thisEngine <= 6:
		print(chr(10) + thisShipLongName + " FUELTYPE @ DG#" + str(thisEngine))
		
		flag_enginePowerAbsolut, \
		flag_thisEngineFuelType, \
		flag_thisEngineFuelInletTemp,\
		flag_thisDeSoxFlowRate = func_getThisEngineColumns(thisEngine)
		
		if flag_thisDeSoxFlowRate not in dfInput.columns:
			dfInput[flag_thisDeSoxFlowRate] = 0
		else:
			dfInput = func_replaceNanInThisColumn(dfInput, flag_thisDeSoxFlowRate, 1)
			dfInput = f_doTheTypeCastForThisColumn(dfInput, flag_thisDeSoxFlowRate)
		
		# dfInput[flag_thisDeSoxFlowRate] = dfInput[flag_thisDeSoxFlowRate].astype(float)
		
		
		if flag_enginePowerAbsolut in dfInput.columns:
			if flag_thisEngineFuelType not in dfInput.columns:
				dfInput[flag_thisEngineFuelType] = ''
			
			dfInput, forceRefreshOfAllData = func_checkForResetOfFuelTypeAndAAQSAssessment(dfInput, flag_thisEngineFuelType)
			
			if \
				func_getCountOf_NANs_inColumn(dfInput, flag_thisEngineFuelType) > 0 or \
				dict_MASTER_WHAT_TO_DO["master_prepareRawData"] == 1 or \
				forceRefreshOfAllData:
				
				dfInput[flag_thisEngineFuelType] = dfInput.apply(lambda x: f_analyseBurnedFuelType(
					x[flag_enginePowerAbsolut],
					x[flag_thisEngineFuelInletTemp],
					x[flag_thisDeSoxFlowRate],
					x[flag_finalFile_Ship],
					x[flag_thisEngineFuelType],
					x[flag_finalFile_Date],
					thisEngine,
					forceRefreshOfAllData,
					thisShipLongName
				), axis=1)
			else:
				print("NO NAN columns for column " + flag_thisEngineFuelType)
		else:
			dfInput[flag_thisEngineFuelType] = "DG"+str(thisEngine)+" NOT AVAILABLE"
			dfInput[flag_enginePowerAbsolut] = ""
			dfInput[flag_thisEngineFuelInletTemp] = ""
		# endregion
		
		thisEngine += 1
	
	
	return dfInput


# ######################################################################################################################
def f_analyseBurnedFuelType(
	thisPointPwr,
	fuelOilTemp,
	deSoxFlowRate,
	shipName,
	existingFuelTypeFlagThisEngine,
	thisDate,
	engineFlag,
	forceRefreshOfAllData,
	thisShipLongName
):
	if not forceRefreshOfAllData:
		if len(str(existingFuelTypeFlagThisEngine)) > 3:
				return existingFuelTypeFlagThisEngine
	
	engineFlag = engineFlag - 1
	
	if dict_AAQS_engines[shipName][engineFlag] > -1:
		if thisPointPwr < minEngineLoadInKWToBeCountedAsOn:
			return fuel_flag_EngineIsOff
		else:
			
			lngVessel = func_shipIsAnLNGShip(shipName)
			
			# TODO >> this will change very soon and we then need to introduce a start / end date for that
			if \
				(thisShipLongName == "Costa Fascinosa" and thisDate <= FS_backToNormalFuelIn2020) or \
				(thisShipLongName == "Costa Pacifica" and thisDate <= PA_backToNormalFuelIn2020):
				return fuel_flag_VLSFO
			
			if thisShipLongName == "AIDAaura" or thisShipLongName == "AIDAcara":
				return fuel_flag_MGO
			
			if not lngVessel:
				if fuelOilTemp >= flag_hfo_mgo_fuelTempSplit:
					if \
						(
							(
								thisShipLongName == "Costa Serena" or \
								thisShipLongName == "Costa Pacifica" or \
								thisShipLongName == "Costa Fascinosa" \
							) and \
						 	(
								deSoxFlowRate > flag_minDeSowFlowRate
							)
						) or \
						(
							thisShipLongName != "Costa Serena" and \
							thisShipLongName != "Costa Pacifica" and \
							thisShipLongName != "Costa Fascinosa" \
						):
						# if deSoxFlowRate > flag_minDeSowFlowRate:
						# print("deSoxFlowRate this engine: " + str(deSoxFlowRate) + " > " + str(flag_minDeSowFlowRate))
						return fuel_flag_HFO
					else:
						# print(thisShipLongName + " BURNING VLSFO")
						if (
							thisShipLongName == "Costa Serena" or \
							(thisShipLongName == "Costa Pacifica" and thisDate < PA_backToNormalFuelIn2020) or \
							(thisShipLongName == "Costa Fascinosa" and thisDate < FS_backToNormalFuelIn2020) \
							):
							return fuel_flag_VLSFO
						else:
							return fuel_flag_MGO
				else:
					return fuel_flag_MGO
			else:
				if fuelOilTemp >= flag_MGO_LNG_fuelTempSplit:
					return fuel_flag_MGO
				else:
					return fuel_flag_LNG
	else:
		return "DG#" + str(engineFlag+1) + " NOT AVAILABLE"


# ######################################################################################################################
def func_shipIsAnLNGShip(
	shipName
):
	lngVessel = False
	
	if shipName == "AIDAnova" or shipName == "Costa Smeralda":
		lngVessel = True
		
	return lngVessel

# ######################################################################################################################
def func_thisEngineForThatShipDoesExist(
	thisShip,
	engineFlag
):
	if dict_AAQS_engines[thisShip][engineFlag - 1] < 0:
		return False
	
	return True


# ######################################################################################################################
def f_resortColumnsOfFinalTotalFileWithAllNeededColumns(
	dfInput
):
	f_makeThePrintNiceStructured(True, "### START EXPORT FILE ", inspect.stack()[0][3])
	startTime = time
	startTime = f_doTheTimeMeasurementInThisFunction(startTime, flag_timeStart, inspect.stack()[0][3])
	
	if EngineRunningHours_Step01_createShipByShipFileWithActuals:
		dfInput = func_resortColumns_EngineRunningHours_Approach(dfInput)
	else:
		if dict_PREPARE_RAW_DATA_FOR___['DATA_APPROACH_AAQS_DAILY'] == 1:
			dfInput = func_resortColumns_AAQS_Approach(dfInput)
		else:
			dfInput = func_resortColumns_LayUp_Approach(dfInput)
		
		dfInput[flag_finalFile_legPortDate] = dfInput[flag_finalFile_legPortDate].astype('datetime64[ns]')
	
	
	dfInput[flag_finalFile_Date] = dfInput[flag_finalFile_Date].astype('datetime64[ns]')
	
	startTime = f_doTheTimeMeasurementInThisFunction(startTime, flag_timeEnd, inspect.stack()[0][3])
	
	return dfInput


# ######################################################################################################################
def func_resortColumns_EngineRunningHours_Approach(
	dfInput
):
	dfInput = \
		dfInput[
			[
				flag_finalFile_Date,
				flag_finalFile_Ship,
				flag_engineRunningHours_DG1,
				flag_engineRunningHours_DG2,
				flag_engineRunningHours_DG3,
				flag_engineRunningHours_DG4,
				flag_engineRunningHours_DG5,
				flag_engineRunningHours_DG6,
				flag_engineRunningHoursCumulatedSinceLastInfoshipUpdate_DG1,
				flag_engineRunningHoursCumulatedSinceLastInfoshipUpdate_DG2,
				flag_engineRunningHoursCumulatedSinceLastInfoshipUpdate_DG3,
				flag_engineRunningHoursCumulatedSinceLastInfoshipUpdate_DG4,
				flag_engineRunningHoursCumulatedSinceLastInfoshipUpdate_DG5,
				flag_engineRunningHoursCumulatedSinceLastInfoshipUpdate_DG6,
				flag_engineRunningHoursCumulatedSinceLastInfoshipUpdate_ALL_DGs,
				flag_rhPredictionThisDay_DG1,
				flag_rhPredictionThisDay_DG2,
				flag_rhPredictionThisDay_DG3,
				flag_rhPredictionThisDay_DG4,
				flag_rhPredictionThisDay_DG5,
				flag_rhPredictionThisDay_DG6,
				flag_runningHourPredictionCumulatedSinceLastInfoship_DG1,
				flag_runningHourPredictionCumulatedSinceLastInfoship_DG2,
				flag_runningHourPredictionCumulatedSinceLastInfoship_DG3,
				flag_runningHourPredictionCumulatedSinceLastInfoship_DG4,
				flag_runningHourPredictionCumulatedSinceLastInfoship_DG5,
				flag_runningHourPredictionCumulatedSinceLastInfoship_DG6,
				flag_runningHourPredictionCumulatedSinceLastInfoship_ALL_DGs
			]
		]
	
	return dfInput

# ######################################################################################################################
def func_resortColumns_LayUp_Approach(
	dfInput
):
	dfInput = \
		dfInput[
			[
				flag_finalFile_Date,
				flag_finalFile_timestampsPerHour,
				flag_finalFile_Ship,
				flag_finalFile_SOG,
				flag_finalFile_SOG_GAP_Filled,
				flag_finalFile_Latitude,
				flag_finalFile_Longitude,
				flag_finalFile_typeOfSailing,
				flag_finalFile_DriftingAnchorage,
				flag_finalFile_DistanceThisSlice,
				flag_finalFile_legPortName,
				flag_finalFile_legPortDate,
				flag_finalFile_DG1_ACTIVE_POWER,
				flag_finalFile_DG2_ACTIVE_POWER,
				flag_finalFile_DG3_ACTIVE_POWER,
				flag_finalFile_DG4_ACTIVE_POWER,
				flag_finalFile_DG5_ACTIVE_POWER,
				flag_finalFile_DG6_ACTIVE_POWER,
				flag_finalFile_TotalPowerDemand,
				flag_finalFile_dataSanity,
				flag_finalFile_AvgPwrDemandOverTime,
				flag_finalFile_AvgEngineUsagePercentNow,
				flag_finalFile_Temperature,
				flag_finalFile_AvgTemperatureOverTime,
				flag_finalFile_DG1_FUEL_OIL_IN_TE,
				flag_finalFile_DG2_FUEL_OIL_IN_TE,
				flag_finalFile_DG3_FUEL_OIL_IN_TE,
				flag_finalFile_DG4_FUEL_OIL_IN_TE,
				flag_finalFile_DG5_FUEL_OIL_IN_TE,
				flag_finalFile_DG6_FUEL_OIL_IN_TE,
				flag_finalFile_environmentalRestriction,
				flag_finalFile_technicalRestriction,
				flag_finalFile_fuelType_DG01,
				flag_finalFile_fuelType_DG02,
				flag_finalFile_fuelType_DG03,
				flag_finalFile_fuelType_DG04,
				flag_finalFile_fuelType_DG05,
				flag_finalFile_fuelType_DG06,
				flag_finalFile_DG1_fuelConsumption,
				flag_finalFile_DG2_fuelConsumption,
				flag_finalFile_DG3_fuelConsumption,
				flag_finalFile_DG4_fuelConsumption,
				flag_finalFile_DG5_fuelConsumption,
				flag_finalFile_DG6_fuelConsumption,
				flag_finalFile_EnginesRunning,
				flag_finalFile_DG1_LoadPercent,
				flag_finalFile_DG2_LoadPercent,
				flag_finalFile_DG3_LoadPercent,
				flag_finalFile_DG4_LoadPercent,
				flag_finalFile_DG5_LoadPercent,
				flag_finalFile_DG6_LoadPercent,
				flag_finalFile_totalFuel_HFO,
				flag_finalFile_totalFuel_MGO,
				flag_finalFile_totalFuel_LNG
			]
		]
	
	return dfInput


# ######################################################################################################################
def func_resortColumns_AAQS_Approach(
	dfInput
):
	dfInput = \
		dfInput[
			[
				flag_finalFile_Date,
				flag_finalFile_timestampsPerHour,
				flag_finalFile_Ship,
				flag_finalFile_SOG,
				flag_finalFile_SOG_GAP_Filled,
				flag_finalFile_Latitude,
				flag_finalFile_Longitude,
				flag_finalFile_typeOfSailing,
				flag_finalFile_DriftingAnchorage,
				flag_finalFile_DistanceThisSlice,
				flag_finalFile_legPortName,
				flag_finalFile_legPortDate,
				flag_finalFile_DG1_ACTIVE_POWER,
				flag_finalFile_DG2_ACTIVE_POWER,
				flag_finalFile_DG3_ACTIVE_POWER,
				flag_finalFile_DG4_ACTIVE_POWER,
				flag_finalFile_DG5_ACTIVE_POWER,
				flag_finalFile_DG6_ACTIVE_POWER,
				flag_finalFile_TotalPowerDemand,
				flag_finalFile_DG1_LoadPercent,
				flag_finalFile_DG2_LoadPercent,
				flag_finalFile_DG3_LoadPercent,
				flag_finalFile_DG4_LoadPercent,
				flag_finalFile_DG5_LoadPercent,
				flag_finalFile_DG6_LoadPercent,
				flag_finalFile_DG1_SFOC,
				flag_finalFile_DG2_SFOC,
				flag_finalFile_DG3_SFOC,
				flag_finalFile_DG4_SFOC,
				flag_finalFile_DG5_SFOC,
				flag_finalFile_DG6_SFOC,
				flag_finalFile_DG1_FUEL_OIL_IN_TE,
				flag_finalFile_DG2_FUEL_OIL_IN_TE,
				flag_finalFile_DG3_FUEL_OIL_IN_TE,
				flag_finalFile_DG4_FUEL_OIL_IN_TE,
				flag_finalFile_DG5_FUEL_OIL_IN_TE,
				flag_finalFile_DG6_FUEL_OIL_IN_TE,
				flag_finalFile_DG1_DeSOx_FLOW,
				flag_finalFile_DG2_DeSOx_FLOW,
				flag_finalFile_DG3_DeSOx_FLOW,
				flag_finalFile_DG4_DeSOx_FLOW,
				flag_finalFile_DG5_DeSOx_FLOW,
				flag_finalFile_DG6_DeSOx_FLOW,
				flag_finalFile_DG1_DeSOx_PumpPWR,
				flag_finalFile_DG2_DeSOx_PumpPWR,
				flag_finalFile_DG3_DeSOx_PumpPWR,
				flag_finalFile_DG4_DeSOx_PumpPWR,
				flag_finalFile_DG5_DeSOx_PumpPWR,
				flag_finalFile_DG6_DeSOx_PumpPWR,
				flag_finalFile_environmentalRestriction,
				flag_finalFile_technicalRestriction,
				flag_finalFile_fuelType_DG01,
				flag_finalFile_fuelType_DG02,
				flag_finalFile_fuelType_DG03,
				flag_finalFile_fuelType_DG04,
				flag_finalFile_fuelType_DG05,
				flag_finalFile_fuelType_DG06,
				flag_finalFile_DG1_fuelConsumption,
				flag_finalFile_DG2_fuelConsumption,
				flag_finalFile_DG3_fuelConsumption,
				flag_finalFile_DG4_fuelConsumption,
				flag_finalFile_DG5_fuelConsumption,
				flag_finalFile_DG6_fuelConsumption,
				flag_finalFile_AAQS_AssessmentDone,
				flag_finalFile_DG1_AAQS_DowntimeReason,
				flag_finalFile_DG1_AAQS_DowntimeMissedPower,
				flag_finalFile_DG2_AAQS_DowntimeReason,
				flag_finalFile_DG2_AAQS_DowntimeMissedPower,
				flag_finalFile_DG3_AAQS_DowntimeReason,
				flag_finalFile_DG3_AAQS_DowntimeMissedPower,
				flag_finalFile_DG4_AAQS_DowntimeReason,
				flag_finalFile_DG4_AAQS_DowntimeMissedPower,
				flag_finalFile_DG5_AAQS_DowntimeReason,
				flag_finalFile_DG5_AAQS_DowntimeMissedPower,
				flag_finalFile_DG6_AAQS_DowntimeReason,
				flag_finalFile_DG6_AAQS_DowntimeMissedPower
			]
		]
	
	return dfInput


# ######################################################################################################################
def f_exportDataframe(
	flagFileType,
	dfInput,
	fileName,
	thisShipOnly,
	decimalSeperator = ".",
	runningHourPredictionVersion = "0"
):
	f_makeThePrintNiceStructured(True, "### START EXPORT FILE ", inspect.stack()[0][3])
	startTime = time
	startTime = f_doTheTimeMeasurementInThisFunction(startTime, flag_timeStart, inspect.stack()[0][3])
	
	#region xls export
	if flagFileType == fileExport_xls:
		if fileName.find('.xlsx') < 0:
			fileName = fileName + '.xlsx'
		
		sheet_name = 'Sheet1'
		writer = pd.ExcelWriter(fileName, engine='xlsxwriter')
		dfInput.to_excel(writer, sheet_name=sheet_name, index=False)
		writer.save()
		
		# df.to_excel(fileName, sheet_name=sheet_name, index=False)
	#endregion
	
	#region csv export
	if flagFileType == fileExport_csv:
		if fileName.find('.csv') < 0:
			fileName = fileName + '.csv'
		
		#region export this dataset for one particular ship only
		if len(thisShipOnly) > 0:
			
			if EngineRunningHours_Step01_createShipByShipFileWithActuals:
				masterFileName = masterFile_EngineRunningHours_csv.replace(
					str("02_FinalFiles"),
					"02_FinalFiles\SHIP_FILES")
				
				fileName = masterFileName.replace(
					'.csv',
					("_OPTION_" + str(runningHourPredictionVersion) + "_" + thisShipOnly + '.csv')
				)
				
				print("SAVE Engine-Running Hour FILE FOR " + thisShipOnly + " right here: " + fileName)
				
			else:
				if dict_PREPARE_RAW_DATA_FOR___['DATA_APPROACH_AAQS_DAILY'] == 1:
					masterFileName = masterFile_AAQS_ALL_csv.replace(
						str("02_AAQS_FinalFiles"),
						"02_AAQS_FinalFiles\SHIP_FILES")
					
					fileName = masterFileName.replace('.csv', ("_" + thisShipOnly + '.csv'))
					
					print("SAVE FINAL AAQS FILE FOR " + thisShipOnly + " right here: " + fileName)
				else:
					masterFileName = masterFile_LayUp_ALL_csv.replace(
						str("02_FinalFiles"),
						"02_FinalFiles\SHIP_FILES")
					
					fileName = masterFileName.replace('.csv', ("_" + thisShipOnly + '.csv'))
					
					print("SAVE FINAL LAY-UP FILE FOR " + thisShipOnly + " right here: " + fileName)
		#endregion
		
		if EngineRunningHours_Step02_createFinalFileForPBI:
			fileName = masterFile_EngineRunningHours_csv.replace(
				'.csv',
				("Option_" + str(EngineRunningHours_Step02_predictionVersion) + '.csv')
			)
			
			print("SAVE FINAL PBI Engine-Running Hour FILE FOR rh prediction version " +
					str(EngineRunningHours_Step02_predictionVersion) + " right here: " + fileName)
			
		dfInput.to_csv(
			fileName,
			sep=';',
			decimal=decimalSeperator,
			index=False)
	#endregion
	
	startTime = f_doTheTimeMeasurementInThisFunction(startTime, flag_timeEnd, inspect.stack()[0][3])


# ######################################################################################################################
def f_addColumnsForMissingNeptuneLabRawDataColumns(
	dfInput,
	thisShipLongName,
	exportDataframeAfterItWasTweakedInThisFunction
):
	f_makeThePrintNiceStructured(True, "### CHECK FOR MISSING COLUMNs ", inspect.stack()[0][3])
	startTime = time
	startTime = f_doTheTimeMeasurementInThisFunction(startTime, flag_timeStart, inspect.stack()[0][3])
	
	dfInput = f_checkForMissingBlankColumnAndAddIfNeeded(dfInput, flag_finalFile_legPortName)
	dfInput = f_checkForMissingBlankColumnAndAddIfNeeded(dfInput, flag_finalFile_legPortDate)
	
	if dict_PREPARE_RAW_DATA_FOR___['DATA_APPROACH_AAQS_DAILY'] == 1:
		dfInput = f_checkForMissingBlankColumnAndAddIfNeeded(dfInput, flag_finalFile_DG1_DeSOx_FLOW)
		dfInput = f_checkForMissingBlankColumnAndAddIfNeeded(dfInput, flag_finalFile_DG2_DeSOx_FLOW)
		dfInput = f_checkForMissingBlankColumnAndAddIfNeeded(dfInput, flag_finalFile_DG3_DeSOx_FLOW)
		dfInput = f_checkForMissingBlankColumnAndAddIfNeeded(dfInput, flag_finalFile_DG4_DeSOx_FLOW)
		dfInput = f_checkForMissingBlankColumnAndAddIfNeeded(dfInput, flag_finalFile_DG5_DeSOx_FLOW)
		dfInput = f_checkForMissingBlankColumnAndAddIfNeeded(dfInput, flag_finalFile_DG6_DeSOx_FLOW)
		dfInput = f_checkForMissingBlankColumnAndAddIfNeeded(dfInput, flag_finalFile_DG1_DeSOx_PumpPWR)
		dfInput = f_checkForMissingBlankColumnAndAddIfNeeded(dfInput, flag_finalFile_DG2_DeSOx_PumpPWR)
		dfInput = f_checkForMissingBlankColumnAndAddIfNeeded(dfInput, flag_finalFile_DG3_DeSOx_PumpPWR)
		dfInput = f_checkForMissingBlankColumnAndAddIfNeeded(dfInput, flag_finalFile_DG4_DeSOx_PumpPWR)
		dfInput = f_checkForMissingBlankColumnAndAddIfNeeded(dfInput, flag_finalFile_DG5_DeSOx_PumpPWR)
		dfInput = f_checkForMissingBlankColumnAndAddIfNeeded(dfInput, flag_finalFile_DG6_DeSOx_PumpPWR)
	
	if dict_PREPARE_RAW_DATA_FOR___['DATA_APPROACH_LayUpPowerManagement'] == 1:
		dfInput = f_checkForMissingBlankColumnAndAddIfNeeded(dfInput, flag_finalFile_AvgPwrDemandOverTime)
		dfInput = f_checkForMissingBlankColumnAndAddIfNeeded(dfInput, flag_finalFile_AvgTemperatureOverTime)
		dfInput = f_checkForMissingBlankColumnAndAddIfNeeded(dfInput, flag_finalFile_AvgEngineUsagePercentNow)
		dfInput = f_checkForMissingBlankColumnAndAddIfNeeded(dfInput, flag_finalFile_dataSanity)
		
		
	dfInput = f_checkForMissingBlankColumnAndAddIfNeeded(dfInput, flag_finalFile_environmentalRestriction)
	dfInput = f_checkForMissingBlankColumnAndAddIfNeeded(dfInput, flag_finalFile_AAQS_AssessmentDone)
	dfInput = f_checkForMissingBlankColumnAndAddIfNeeded(dfInput, flag_finalFile_SOG_GAP_Filled)
	dfInput = f_checkForMissingBlankColumnAndAddIfNeeded(dfInput, flag_finalFile_timestampsPerHour)
	
	dfInput[flag_finalFile_Date] = dfInput[flag_finalFile_Date].astype('datetime64[ns]')
	
	startTime = f_doTheTimeMeasurementInThisFunction(startTime, flag_timeEnd, inspect.stack()[0][3])
	
	
	return dfInput


# ######################################################################################################################
def f_checkForMissingBlankColumnAndAddIfNeeded(
	dfInput,
	thisFlag
):
	if thisFlag in dfInput.columns:
		# print("all fine, no column missing")
		a = 1
	else:
		print("add missing column for " + thisFlag)
		dfInput[thisFlag] = ""
	# print(dfInput.head(1))
	
	return dfInput


# ######################################################################################################################
def f_readExistingMasterFile(
	thisShipOnly
):
	f_makeThePrintNiceStructured(True, "### READ EXISTING MASTER FILE ", inspect.stack()[0][3])
	startTime = time
	startTime = f_doTheTimeMeasurementInThisFunction(startTime, flag_timeStart, inspect.stack()[0][3])
	
	masterFileThisShipDoesExist = True
	
	df_existingMasterFile = pd.DataFrame()
	
	if thisShipOnly == '':
		if dict_PREPARE_RAW_DATA_FOR___['DATA_APPROACH_AAQS_DAILY'] == 1:
			print("READ THE AAQS FILE:" + masterFile_AAQS_ALL_csv)
			df_existingMasterFile = pd.read_csv(masterFile_AAQS_ALL_csv, sep=';', decimal=',', low_memory=False)
		else:
			print("READ THE LAY-UP FILE:" + masterFile_LayUp_ALL_csv)
			df_existingMasterFile = pd.read_csv(masterFile_LayUp_ALL_csv, sep=';', decimal=',', low_memory=False)
	else:
		if dict_PREPARE_RAW_DATA_FOR___['DATA_APPROACH_AAQS_DAILY'] == 1:
			masterFileName = masterFile_AAQS_ALL_csv.replace(
				str("02_AAQS_FinalFiles"),
				"02_AAQS_FinalFiles\SHIP_FILES")
			
			masterFileName = masterFileName.replace('.csv', ("_" + thisShipOnly + '.csv'))
			print("READ THE AAQS FILE for this SHIP:" + masterFileName)
			
			if os.path.exists(masterFileName):
				df_existingMasterFile = pd.read_csv(masterFileName, sep=';', decimal=',', low_memory=False)
			else:
				print("THIS FILE DOES NOT EXIST; NEXT SHIP")
				masterFileThisShipDoesExist = False
				
		else:
			masterFileName = masterFile_LayUp_ALL_csv.replace(
				str("02_FinalFiles"),
				"02_FinalFiles\SHIP_FILES")
			
			masterFileName = masterFileName.replace('.csv', ("_" + thisShipOnly + '.csv'))
			print("READ THE LAY_UP FILE for this SHIP:" + masterFileName)
			
			df_existingMasterFile = pd.read_csv(masterFileName, sep=';', decimal=',', low_memory=False)
		
	startTime = f_doTheTimeMeasurementInThisFunction(startTime, flag_timeEnd, inspect.stack()[0][3])
	
	return df_existingMasterFile, masterFileThisShipDoesExist


# ######################################################################################################################
def f_createCopyOfExistingMasterFileBeforeChangingIt(
	dfInput,
	typeFlag,
	thisShipOnly
):
	f_makeThePrintNiceStructured(True, "### CREATE COPY OF MASTER FILE ", inspect.stack()[0][3])
	startTime = time
	startTime = f_doTheTimeMeasurementInThisFunction(startTime, flag_timeStart, inspect.stack()[0][3])
	
	if dict_PREPARE_RAW_DATA_FOR___['DATA_APPROACH_AAQS_DAILY'] == 1:
		masterFileName = masterFile_AAQS_ALL_csv.replace(
			str("02_AAQS_FinalFiles"),
			"02_AAQS_FinalFiles\SHIP_FILES\PY_CODE_AUTOBACKUPs")
		
		masterFileName = masterFileName.replace('.csv', ("_" + thisShipOnly + '.csv'))
	else:
		masterFileName = masterFile_LayUp_ALL_csv.replace(
			str("02_FinalFiles"),
			"02_FinalFiles\SHIP_FILES\PY_CODE_AUTOBACKUPs")
		
		masterFileName = masterFileName.replace('.csv', ("_" + thisShipOnly + '.csv'))
		
	
	currentDT = datetime.datetime.now()
	thisTimeNow = str(currentDT.strftime("%Y-%m-%d %H-%M-%S"))
	
	finalNewStringAtTheEndOFTheBackupFile = str('_SAFETY_COPY_' + typeFlag + thisTimeNow + '.csv')
	
	fileName = masterFileName.replace('.csv', finalNewStringAtTheEndOFTheBackupFile)
	
	if dict_PREPARE_RAW_DATA_FOR___['DATA_APPROACH_AAQS_DAILY'] == 1:
		print("CREATE AAQS BACKUP FILE FOR THIS SHIP:" + fileName)
	else:
		print("CREATE LAY-UP BACKUP FILE FOR THIS SHIP:" + fileName)
		
	dfInput.to_csv(
		fileName,
		sep=';',
		decimal='.',
		index=False)
	
	startTime = f_doTheTimeMeasurementInThisFunction(startTime, flag_timeEnd, inspect.stack()[0][3])


# ######################################################################################################################
def f_addThisDataFrameAtTheEndOfTheExistingTotalFile(
	dfInput,
	df_currentMasterFile,
	thisShipLongName
):
	f_makeThePrintNiceStructured(True, "### ADD PREPARED RAW DATA @ THE END ", inspect.stack()[0][3])
	startTime = time
	startTime = f_doTheTimeMeasurementInThisFunction(startTime, flag_timeStart, inspect.stack()[0][3])
	
	df_newMasterDF = pd.DataFrame()
	
	dfInput[flag_finalFile_Date] = dfInput[flag_finalFile_Date].astype('datetime64[ns]')
	
	dfInput, thisDataframeTimeCoparison = f_thisShipAndTimeframeExistAlreadyInMasterFile(
		dfInput,
		df_currentMasterFile,
		thisShipLongName
	)
	
	print("thisDataframeTimeCoparison: " + thisDataframeTimeCoparison)
	
	if thisDataframeTimeCoparison is timeCheck_noGo:
		print("ATTENTION: this ship " + thisShipLongName + " with this timeframe exists in the master file")
		df_newMasterDF = df_currentMasterFile
	
	if \
		thisDataframeTimeCoparison == timeCheck_perfect or \
		thisDataframeTimeCoparison == timeCheck_cutTheBeginningOfTheNewFile:
		
		print("ADD prepared NL data for " + thisShipLongName + " at the end of the existing master file")
		print("Lines in Master DF BEFORE adding anything " + str(df_currentMasterFile[flag_finalFile_Ship].count()))
		df_newMasterDF = pd.concat([df_currentMasterFile, dfInput], sort=True, ignore_index=True)
		print("Lines in Master DF AFTER adding anything " + str(df_newMasterDF[flag_finalFile_Ship].count()))
		
		df_newMasterDF = f_sortThisDataframeByShipnameAndDate(
			df_newMasterDF,
			flag_finalFile_Ship,
			flag_finalFile_Date
		)
	
	startTime = f_doTheTimeMeasurementInThisFunction(startTime, flag_timeEnd, inspect.stack()[0][3])
	
	return df_newMasterDF


# ######################################################################################################################
def f_thisShipAndTimeframeExistAlreadyInMasterFile(
	dfInput,
	df_existingMasterFile,
	thisShipLongName
):
	print("FILTER FOR incoming ship data only " + thisShipLongName)
	
	dfSubFileThisShip = df_existingMasterFile[
		df_existingMasterFile[flag_finalFile_Ship] == thisShipLongName]
	
	dfSubFileThisShip[flag_finalFile_Date] = dfSubFileThisShip[flag_finalFile_Date].astype('datetime64[ns]')
	
	minTimeStampMasterFile = dfSubFileThisShip[flag_finalFile_Date].min()
	maxTimeStampMasterFile = dfSubFileThisShip[flag_finalFile_Date].max()
	print("minTimeStampMasterFile: " + str(minTimeStampMasterFile))
	print("maxTimeStampMasterFile: " + str(maxTimeStampMasterFile))
	
	minTimeStampPreparedRawData = dfInput[flag_NeptuneLab_Date].min()
	maxTimeStampPreparedRawData = dfInput[flag_NeptuneLab_Date].max()
	print("minTimeStampPreparedRawData: " + str(minTimeStampPreparedRawData))
	print("maxTimeStampPreparedRawData: " + str(maxTimeStampPreparedRawData))
	
	if \
		maxTimeStampPreparedRawData < minTimeStampMasterFile or \
			minTimeStampPreparedRawData > maxTimeStampMasterFile or \
			str(maxTimeStampMasterFile) == 'NaT':
		print("PERFECT! NL raw data does not overlap with data in existing master file >> add this data to master file")
		return dfInput, timeCheck_perfect
	else:
		if maxTimeStampPreparedRawData > maxTimeStampMasterFile:
			print("NEW FILE is ending after existing data ... we need to cut the new data to avoid overlap")
			dfInput = dfInput[dfInput[flag_finalFile_Date] > maxTimeStampMasterFile]
			minTimeStampPreparedRawData = dfInput[flag_NeptuneLab_Date].min()
			maxTimeStampPreparedRawData = dfInput[flag_NeptuneLab_Date].max()
			print("minTimeStampPreparedRawData: " + str(minTimeStampPreparedRawData))
			print("maxTimeStampPreparedRawData: " + str(maxTimeStampPreparedRawData))
			
			return dfInput, timeCheck_cutTheBeginningOfTheNewFile
		else:
			print("ATTENTION: TIME FRAMES THIS SHIP are overlapping >> NO DATA will be added to master file")
			return dfInput, timeCheck_noGo


# ######################################################################################################################
def f_getThisBrand(
	thisShipLongName
):
	if thisShipLongName[0:4] == flag_brand_AIDA:
		return flag_brand_AIDA
	
	if thisShipLongName[0:5] == flag_brand_Costa:
		return flag_brand_Costa
	
	return ''
	

# ######################################################################################################################
def func_getDataframeColumnsThisEngine(
	thisEngine
):
	if thisEngine == 1:
		thisEngineConsumptionFlag = flag_finalFile_DG1_fuelConsumption
		thisEngine_SFOC = flag_finalFile_DG1_SFOC
		thisEngine_loadAbsolut = flag_finalFile_DG1_ACTIVE_POWER
		thisEngine_loadPercent = flag_finalFile_DG1_LoadPercent
		thisEngine_FuelType = flag_finalFile_fuelType_DG01
	
	if thisEngine == 2:
		thisEngineConsumptionFlag = flag_finalFile_DG2_fuelConsumption
		thisEngine_SFOC = flag_finalFile_DG2_SFOC
		thisEngine_loadAbsolut = flag_finalFile_DG2_ACTIVE_POWER
		thisEngine_loadPercent = flag_finalFile_DG2_LoadPercent
		thisEngine_FuelType = flag_finalFile_fuelType_DG02
	
	if thisEngine == 3:
		thisEngineConsumptionFlag = flag_finalFile_DG3_fuelConsumption
		thisEngine_SFOC = flag_finalFile_DG3_SFOC
		thisEngine_loadAbsolut = flag_finalFile_DG3_ACTIVE_POWER
		thisEngine_loadPercent = flag_finalFile_DG3_LoadPercent
		thisEngine_FuelType = flag_finalFile_fuelType_DG03
	
	if thisEngine == 4:
		thisEngineConsumptionFlag = flag_finalFile_DG4_fuelConsumption
		thisEngine_SFOC = flag_finalFile_DG4_SFOC
		thisEngine_loadAbsolut = flag_finalFile_DG4_ACTIVE_POWER
		thisEngine_loadPercent = flag_finalFile_DG4_LoadPercent
		thisEngine_FuelType = flag_finalFile_fuelType_DG04
	
	if thisEngine == 5:
		thisEngineConsumptionFlag = flag_finalFile_DG5_fuelConsumption
		thisEngine_SFOC = flag_finalFile_DG5_SFOC
		thisEngine_loadAbsolut = flag_finalFile_DG5_ACTIVE_POWER
		thisEngine_loadPercent = flag_finalFile_DG5_LoadPercent
		thisEngine_FuelType = flag_finalFile_fuelType_DG05
	
	if thisEngine == 6:
		thisEngineConsumptionFlag = flag_finalFile_DG6_fuelConsumption
		thisEngine_SFOC = flag_finalFile_DG6_SFOC
		thisEngine_loadAbsolut = flag_finalFile_DG6_ACTIVE_POWER
		thisEngine_loadPercent = flag_finalFile_DG6_LoadPercent
		thisEngine_FuelType = flag_finalFile_fuelType_DG06
	
	return thisEngineConsumptionFlag, thisEngine_SFOC, thisEngine_loadAbsolut, thisEngine_loadPercent, thisEngine_FuelType
	

# ######################################################################################################################
def f_addFuelConsumptionToDF(
	dfInput,
	thisShipLongName,
	recalculateFuelConsumption
):
	f_makeThePrintNiceStructured(True, "### FUEL CONSUMPTION per ENGINE" , inspect.stack()[0][3])
	startTime = time
	startTime = f_doTheTimeMeasurementInThisFunction(startTime, flag_timeStart, inspect.stack()[0][3])
	
	thisEngine = 1
	while thisEngine <= 6:
		print(chr(10) + thisShipLongName + " FUEL @ DG#" + str(thisEngine))
		
		thisEngineConsumptionFlag, \
		thisEngine_SFOC, \
		thisEngine_loadAbsolut, \
		thisEngine_loadPercent, \
		thisEngine_FuelType = func_getDataframeColumnsThisEngine(thisEngine)
		
		dfInput = \
			func_resetConsumptionFiguresIfNeeded(
				dfInput,
				thisShipLongName,
				thisEngineConsumptionFlag,
				thisEngine_SFOC,
				recalculateFuelConsumption
			)
		
		if \
			func_getCountOf_NANs_inColumn(dfInput, thisEngineConsumptionFlag) > 0 or \
			dict_MASTER_WHAT_TO_DO["master_prepareRawData"] == 1 or \
			recalculateFuelConsumption:
			
			print(" ... SFOC @ DG#" + str(thisEngine))
			dfInput[thisEngine_SFOC] = dfInput.apply(lambda x: func_getThisEngineAndFueltypeSFOC(
				x[thisEngine_loadPercent],
				x[thisEngine_FuelType]
			), axis=1)
			
			print(" ... Fuel Consumption @ DG#" + str(thisEngine))
			dfInput[thisEngineConsumptionFlag] = dfInput.apply(lambda x: f_calculateFuelConsumption(
				x[thisEngine_loadAbsolut],
				x[thisEngine_SFOC],
				x[flag_finalFile_timestampsPerHour]
			), axis=1)
		
		thisEngine += 1
	
	startTime = f_doTheTimeMeasurementInThisFunction(startTime, flag_timeEnd, inspect.stack()[0][3])
	
	return dfInput


# ######################################################################################################################
def func_resetConsumptionFiguresIfNeeded(
	dfInput,
	thisShipLongName,
	thisEngineConsumptionFlag,
	thisEngine_SFOC,
	recalculateFuelConsumption
):
	if thisEngineConsumptionFlag not in dfInput.columns:
		dfInput[thisEngineConsumptionFlag] = 0
	
	if thisEngine_SFOC not in dfInput.columns:
		dfInput[thisEngine_SFOC] = 0
	
	if recalculateFuelConsumption:
		dfInput.loc[dfInput[flag_finalFile_Ship] == thisShipLongName, thisEngineConsumptionFlag] = 0
		dfInput.loc[dfInput[flag_finalFile_Ship] == thisShipLongName, thisEngine_SFOC] = 0
	
	return dfInput


# ######################################################################################################################
def func_addTotalFuelConsumptionPerFuelType(
	dfInput,
	thisShipLongName,
	fuelType
):
	f_makeThePrintNiceStructured(True, "### TOTAL Fuel Consumption per Fuel-Type " + fuelType, inspect.stack()[0][3])
	startTime = time
	startTime = f_doTheTimeMeasurementInThisFunction(startTime, flag_timeStart, inspect.stack()[0][3])
	
	if fuelType == "HFO":
		dfInput.loc[dfInput[flag_finalFile_Ship] == thisShipLongName, flag_finalFile_totalFuel_HFO] = 0
	
	if fuelType == "MGO":
		dfInput.loc[dfInput[flag_finalFile_Ship] == thisShipLongName, flag_finalFile_totalFuel_MGO] = 0
	
	if fuelType == "LNG":
		dfInput.loc[dfInput[flag_finalFile_Ship] == thisShipLongName, flag_finalFile_totalFuel_LNG] = 0
	
	flag_dg1_fuel = 'flag_dg1_fuel'
	flag_dg2_fuel = 'flag_dg2_fuel'
	flag_dg3_fuel = 'flag_dg3_fuel'
	flag_dg4_fuel = 'flag_dg4_fuel'
	flag_dg5_fuel = 'flag_dg5_fuel'
	flag_dg6_fuel = 'flag_dg6_fuel'
	
	dfInput.loc[dfInput[flag_finalFile_Ship] == thisShipLongName, flag_dg1_fuel] = 0
	dfInput.loc[dfInput[flag_finalFile_Ship] == thisShipLongName, flag_dg2_fuel] = 0
	dfInput.loc[dfInput[flag_finalFile_Ship] == thisShipLongName, flag_dg3_fuel] = 0
	dfInput.loc[dfInput[flag_finalFile_Ship] == thisShipLongName, flag_dg4_fuel] = 0
	dfInput.loc[dfInput[flag_finalFile_Ship] == thisShipLongName, flag_dg5_fuel] = 0
	dfInput.loc[dfInput[flag_finalFile_Ship] == thisShipLongName, flag_dg6_fuel] = 0
	

	#region loop all engines and create sub column with MGO consumption
	thisEngine = 0
	while thisEngine <= 5:
		thisEngine += 1
		if dict_Ship_MaxPowerOfEngines[thisShipLongName][thisEngine-1] > 0:
			engineFlagFuelType, engineFlagFuelConsumption, mgoThisEngine = func_getEngineFlags(thisEngine)
			#
			# print("engineFlagFuelType " + engineFlagFuelType)
			# print("engineFlagFuelConsumption " + engineFlagFuelConsumption)
			# print("mgoThisEngine " + mgoThisEngine)
			#
			if fuelType == "MGO":
				dfInput.loc[ \
					(dfInput[flag_finalFile_Ship] == thisShipLongName),
					mgoThisEngine
				] =+ \
					(
						dfInput.loc[ \
							(dfInput[flag_finalFile_Ship] == thisShipLongName) &
							(
								(dfInput[engineFlagFuelType] == fuel_flag_MGO) |
								(dfInput[engineFlagFuelType] == fuel_flag_AAQS_Missed_NAVIGATION) |
								(dfInput[engineFlagFuelType] == fuel_flag_AAQS_Missed_PORT) |
								(dfInput[engineFlagFuelType] == fuel_flag_MGO_InsideTerritorialWater)
							),
							engineFlagFuelConsumption]
					)
				dfInput[mgoThisEngine].fillna(0, inplace=True)
			
			if fuelType == "HFO":
				dfInput.loc[ \
					(dfInput[flag_finalFile_Ship] == thisShipLongName),
					mgoThisEngine
				] =+ \
					(
						dfInput.loc[ \
							(dfInput[flag_finalFile_Ship] == thisShipLongName) &
							(
								(dfInput[engineFlagFuelType] == fuel_flag_HFO) |
								(dfInput[engineFlagFuelType] == fuel_flag_HFO_NOAAQS) |
								(dfInput[engineFlagFuelType] == fuel_flag_HFO_InsideTerritorialWater)
							),
							engineFlagFuelConsumption]
					)
				dfInput[mgoThisEngine].fillna(0, inplace=True)
			
			if fuelType == "LNG":
				dfInput.loc[ \
					(dfInput[flag_finalFile_Ship] == thisShipLongName),
					mgoThisEngine
				] =+ \
					(
						dfInput.loc[ \
							(dfInput[flag_finalFile_Ship] == thisShipLongName) &
							(
								(dfInput[engineFlagFuelType] == fuel_flag_LNG)
							),
							engineFlagFuelConsumption]
					)
				dfInput[mgoThisEngine].fillna(0, inplace=True)
	#endregion
	
	finalFuelFlagThisFuelType = ''
	if fuelType == "HFO":
		finalFuelFlagThisFuelType = flag_finalFile_totalFuel_HFO
	
	if fuelType == "MGO":
		finalFuelFlagThisFuelType = flag_finalFile_totalFuel_MGO
		
	if fuelType == "LNG":
		finalFuelFlagThisFuelType = flag_finalFile_totalFuel_LNG
		
	dfInput.loc[dfInput[flag_finalFile_Ship] == thisShipLongName, finalFuelFlagThisFuelType] = \
		dfInput.loc[dfInput[flag_finalFile_Ship] == thisShipLongName, flag_dg1_fuel] + \
		dfInput.loc[dfInput[flag_finalFile_Ship] == thisShipLongName, flag_dg2_fuel] + \
		dfInput.loc[dfInput[flag_finalFile_Ship] == thisShipLongName, flag_dg3_fuel] + \
		dfInput.loc[dfInput[flag_finalFile_Ship] == thisShipLongName, flag_dg4_fuel] + \
		dfInput.loc[dfInput[flag_finalFile_Ship] == thisShipLongName, flag_dg5_fuel] + \
		dfInput.loc[dfInput[flag_finalFile_Ship] == thisShipLongName, flag_dg6_fuel]
	
	dfInput.loc[
		(dfInput[flag_finalFile_Ship] == thisShipLongName) &
		(dfInput[finalFuelFlagThisFuelType] >= 2.5),
		flag_finalFile_dataSanity] = 3
	
	dfInput.loc[
		(dfInput[flag_finalFile_Ship] == thisShipLongName) &
		(dfInput[finalFuelFlagThisFuelType] >= 2.5),
		finalFuelFlagThisFuelType] = 0
	
	dfInput.loc[
		(dfInput[flag_finalFile_Ship] == thisShipLongName) &
		(dfInput[finalFuelFlagThisFuelType] < 0),
		flag_finalFile_dataSanity] = 4
	
	dfInput.loc[
		(dfInput[flag_finalFile_Ship] == thisShipLongName) &
		(dfInput[finalFuelFlagThisFuelType] < 0),
		finalFuelFlagThisFuelType] = 0
	
	startTime = f_doTheTimeMeasurementInThisFunction(startTime, flag_timeEnd, inspect.stack()[0][3])
	
	return dfInput

# ######################################################################################################################
def func_getEngineFlags(
	engineFlag
):
	flag_dg1_fuel = 'flag_dg1_fuel'
	flag_dg2_fuel = 'flag_dg2_fuel'
	flag_dg3_fuel = 'flag_dg3_fuel'
	flag_dg4_fuel = 'flag_dg4_fuel'
	flag_dg5_fuel = 'flag_dg5_fuel'
	flag_dg6_fuel = 'flag_dg6_fuel'
	
	if engineFlag == 1:
		return flag_finalFile_fuelType_DG01, flag_finalFile_DG1_fuelConsumption, flag_dg1_fuel
	
	if engineFlag == 2:
		return flag_finalFile_fuelType_DG02, flag_finalFile_DG2_fuelConsumption, flag_dg2_fuel
	
	if engineFlag == 3:
		return flag_finalFile_fuelType_DG03, flag_finalFile_DG3_fuelConsumption, flag_dg3_fuel
	
	if engineFlag == 4:
		return flag_finalFile_fuelType_DG04, flag_finalFile_DG4_fuelConsumption, flag_dg4_fuel
	
	if engineFlag == 5:
		return flag_finalFile_fuelType_DG05, flag_finalFile_DG5_fuelConsumption, flag_dg5_fuel
	
	if engineFlag == 6:
		return flag_finalFile_fuelType_DG06, flag_finalFile_DG6_fuelConsumption, flag_dg6_fuel
	
	
# ######################################################################################################################
def func_addTotalPowerDemand(
	dfInput
):
	f_makeThePrintNiceStructured(True, "### ADD TOTAL PWR DEMAND", inspect.stack()[0][3])
	startTime = time
	startTime = f_doTheTimeMeasurementInThisFunction(startTime, flag_timeStart, inspect.stack()[0][3])
	
	dfInput[flag_finalFile_TotalPowerDemand] = \
		dfInput[flag_finalFile_DG1_ACTIVE_POWER] + \
		dfInput[flag_finalFile_DG2_ACTIVE_POWER] + \
		dfInput[flag_finalFile_DG3_ACTIVE_POWER] + \
		dfInput[flag_finalFile_DG4_ACTIVE_POWER] + \
		dfInput[flag_finalFile_DG5_ACTIVE_POWER] + \
		dfInput[flag_finalFile_DG6_ACTIVE_POWER]
	
	startTime = f_doTheTimeMeasurementInThisFunction(startTime, flag_timeEnd, inspect.stack()[0][3])
	
	return dfInput


# ######################################################################################################################
def func_addAvgEngineLoad(
	dfInput
):
	f_makeThePrintNiceStructured(True, "### AVG ENGINE LOAD @ ", inspect.stack()[0][3])
	startTime = time
	startTime = f_doTheTimeMeasurementInThisFunction(startTime, flag_timeStart, inspect.stack()[0][3])
	
	markFrozenStartingFromThisAmountOfSignals = 3
	
	if useOnlyThisShip is not '':
		totalNansEngineRunningCount = func_getCountOf_NANs_inColumn(
			dfInput[dfInput[flag_finalFile_Ship] == useOnlyThisShip],
			flag_finalFile_EnginesRunning
		)
	else:
		totalNansEngineRunningCount = func_getCountOf_NANs_inColumn(
			dfInput,
			flag_finalFile_EnginesRunning
		)
	
	dict_engineLoadFlag = func_defineDictWithFlagsForEngineLoadColumns()
	
	dict_engineLoadPercentFlag = func_defineDictWithFlagsForEngineLoadPercentColumns()
	
	
	print("   totalNansEngineRunningCount " + str(totalNansEngineRunningCount))
	
	if totalNansEngineRunningCount > 0 or ERASE_EngineRunningCount:
		
		minIndexThisShip, maxIndexThisShip = func_getIndexRangeForThisShipsDate(dfInput, useOnlyThisShip)
		
		dfInput.loc[minIndexThisShip:maxIndexThisShip, flag_finalFile_EnginesRunning] = 0
		dfInput.loc[minIndexThisShip:maxIndexThisShip, flag_finalFile_AvgEngineUsagePercentNow] = 0
		
		dfInput.loc[minIndexThisShip:maxIndexThisShip, flag_finalFile_DG1_LoadPercent] = 0
		dfInput.loc[minIndexThisShip:maxIndexThisShip, flag_finalFile_DG2_LoadPercent] = 0
		dfInput.loc[minIndexThisShip:maxIndexThisShip, flag_finalFile_DG3_LoadPercent] = 0
		dfInput.loc[minIndexThisShip:maxIndexThisShip, flag_finalFile_DG4_LoadPercent] = 0
		dfInput.loc[minIndexThisShip:maxIndexThisShip, flag_finalFile_DG5_LoadPercent] = 0
		dfInput.loc[minIndexThisShip:maxIndexThisShip, flag_finalFile_DG6_LoadPercent] = 0
	
		engineCountFlag = 0
		while engineCountFlag < 6:
			#region sum up total amount of engines running
			dfInput.loc[ \
					(dfInput[flag_finalFile_Ship] == useOnlyThisShip) &
					(dfInput[dict_engineLoadFlag[engineCountFlag]] > minPowerDemandAccepted_kW),
					flag_finalFile_EnginesRunning
				] = dfInput.loc[ \
					(dfInput[flag_finalFile_Ship] == useOnlyThisShip) &
					(dfInput[dict_engineLoadFlag[engineCountFlag]] > minPowerDemandAccepted_kW),
					flag_finalFile_EnginesRunning
				] + 1
			#endregion
			
			#region get individual engine load per engine
			if dict_Ship_MaxPowerOfEngines[useOnlyThisShip][engineCountFlag] > -1:
				dfInput.loc[ \
					(dfInput[flag_finalFile_Ship] == useOnlyThisShip) &
					(dfInput[dict_engineLoadFlag[engineCountFlag]] > minPowerDemandAccepted_kW),
					dict_engineLoadPercentFlag[engineCountFlag]
				] = \
					round(
						dfInput.loc[
							(dfInput[flag_finalFile_Ship] == useOnlyThisShip) &
							(dfInput[dict_engineLoadFlag[engineCountFlag]] > minPowerDemandAccepted_kW),
							dict_engineLoadFlag[engineCountFlag]
						] /
						dict_Ship_MaxPowerOfEngines[useOnlyThisShip][engineCountFlag], 3
					)
			else:
				dfInput.loc[ \
					(dfInput[flag_finalFile_Ship] == useOnlyThisShip),
					dict_engineLoadPercentFlag[engineCountFlag]
				] = 0
			#endregion
			
			engineCountFlag += 1
		
		#region get average engine load all engines running
		dfInput.loc[ \
			(dfInput[flag_finalFile_Ship] == useOnlyThisShip),
			flag_finalFile_AvgEngineUsagePercentNow
		] = \
			round(
				(
				dfInput.loc[ \
					(dfInput[flag_finalFile_Ship] == useOnlyThisShip),
					flag_finalFile_DG1_LoadPercent] +
				dfInput.loc[ \
					(dfInput[flag_finalFile_Ship] == useOnlyThisShip),
					flag_finalFile_DG2_LoadPercent] +
				dfInput.loc[ \
					(dfInput[flag_finalFile_Ship] == useOnlyThisShip),
					flag_finalFile_DG3_LoadPercent] +
				dfInput.loc[ \
					(dfInput[flag_finalFile_Ship] == useOnlyThisShip),
					flag_finalFile_DG4_LoadPercent] +
				dfInput.loc[ \
					(dfInput[flag_finalFile_Ship] == useOnlyThisShip),
					flag_finalFile_DG5_LoadPercent] +
				dfInput.loc[ \
					(dfInput[flag_finalFile_Ship] == useOnlyThisShip),
					flag_finalFile_DG6_LoadPercent]
			) / dfInput.loc[ \
					(dfInput[flag_finalFile_Ship] == useOnlyThisShip),
					flag_finalFile_EnginesRunning],
				3
			)
	#endregion
	
	startTime = f_doTheTimeMeasurementInThisFunction(startTime, flag_timeEnd, inspect.stack()[0][3])
	
	return dfInput


# ######################################################################################################################
def func_divisonPossible(number, divisor):
    return number % divisor == 0


# ######################################################################################################################
def func_doTheDataSanityCheckForTotalPowerDemand(
	dfInput
):
	f_makeThePrintNiceStructured(True, "### DATA SANITY CHECK @ TOTAL PWR DEMAND", inspect.stack()[0][3])
	startTime = time
	startTime = f_doTheTimeMeasurementInThisFunction(startTime, flag_timeStart, inspect.stack()[0][3])
	
	markFrozenStartingFromThisAmountOfSignals = 3
	
	if useOnlyThisShip is not '':
		totalNansInSanityCheck = func_getCountOf_NANs_inColumn(
			dfInput[dfInput[flag_finalFile_Ship] == useOnlyThisShip],
			flag_finalFile_dataSanity
		)
	else:
		# TODO count of nans does not work. result is always 0, even with new data
		totalNansInSanityCheck = func_getCountOf_NANs_inColumn(
			dfInput,
			flag_finalFile_dataSanity
		)
	
	print("NANs in dfInput for flag_finalFile_dataSanity " + str(totalNansInSanityCheck))
	
	frozenSignalsFound = 0
	totalFrozenSignals = 0
	
	if totalNansInSanityCheck > 0 or ERASE_DataSanityChecks:
		minIndexThisShip, maxIndexThisShip = func_getIndexRangeForThisShipsDate(dfInput, useOnlyThisShip)
		print("func_doTheDataSanityCheckForTotalPowerDemand minIndexThisShip " + str(minIndexThisShip))
		print("func_doTheDataSanityCheckForTotalPowerDemand maxIndexThisShip " + str(maxIndexThisShip))
		
		dfInput.loc[minIndexThisShip:maxIndexThisShip, flag_finalFile_dataSanity] = 1
		
		ap = minIndexThisShip
		while ap <= maxIndexThisShip - markFrozenStartingFromThisAmountOfSignals:
			ap += markFrozenStartingFromThisAmountOfSignals
			
			if func_divisonPossible(ap, progressPrintCounter):
				func_printProgress(ap, minIndexThisShip, maxIndexThisShip, inspect.stack()[0][3])
			
			if \
				dfInput.loc[ap, flag_finalFile_TotalPowerDemand] == \
				dfInput.loc[ap-1, flag_finalFile_TotalPowerDemand] == \
				dfInput.loc[ap-2, flag_finalFile_TotalPowerDemand] == \
				dfInput.loc[ap-3, flag_finalFile_TotalPowerDemand]:
				
				frozenSignalsFound += markFrozenStartingFromThisAmountOfSignals
				# print(useOnlyThisShip + " >>> frozen engine data last 4 datapoints @ " + str(ap) + " @ " + str(dfInput.loc[ap, flag_finalFile_Date]))
				totalFrozenSignals += 4
				
				dfInput.loc[ap - markFrozenStartingFromThisAmountOfSignals - 1:ap, flag_finalFile_dataSanity] = 0
		
		print(useOnlyThisShip + " TOTAL frozen engine data signals: " + str(totalFrozenSignals))
	
	# dataSlicesToCheckForSuddenSpikes = 3000 #around 6 days with 3min slices
	# for ap in dfInput.index:
	# 	if func_divisonPossible(ap, 1000):
	# 		func_printProgress(ap, minIndexThisShip, maxIndexThisShip, inspect.stack()[0][3])
	#
	# 	if dfInput.loc[ap, flag_finalFile_typeOfSailing] == flag_typeOfSailing_Port:
	# 		if dfInput.loc[ap, flag_finalFile_dataSanity] == 1:
	# 			if ap >= dataSlicesToCheckForSuddenSpikes:
	# 				thisTotalPowerMeanDuringPortStay = dfInput.loc[ap-dataSlicesToCheckForSuddenSpikes:ap, flag_finalFile_TotalPowerDemand][
	# 					(dfInput.loc[ap-dataSlicesToCheckForSuddenSpikes:ap, flag_finalFile_dataSanity] == 1) &
	# 					(dfInput.loc[ap-dataSlicesToCheckForSuddenSpikes:ap, flag_finalFile_typeOfSailing] == flag_typeOfSailing_Port) &
	# 					(dfInput.loc[ap-dataSlicesToCheckForSuddenSpikes:ap, flag_finalFile_TotalPowerDemand] > minPowerDemandAccepted_kW)
	# 				].mean()
	#
	# 				thisTotalPowerStdDevDuringPortStay = \
	# 				dfInput.loc[ap - dataSlicesToCheckForSuddenSpikes:ap, flag_finalFile_TotalPowerDemand][
	# 					(dfInput.loc[ap - dataSlicesToCheckForSuddenSpikes:ap, flag_finalFile_dataSanity] == 1) &
	# 					(dfInput.loc[ap - dataSlicesToCheckForSuddenSpikes:ap,
	# 					 flag_finalFile_typeOfSailing] == flag_typeOfSailing_Port) &
	# 					(dfInput.loc[ap - dataSlicesToCheckForSuddenSpikes:ap,
	# 					 flag_finalFile_TotalPowerDemand] > minPowerDemandAccepted_kW)
	# 					].std()
	#
	# 				if \
	# 					dfInput.loc[ap, flag_finalFile_TotalPowerDemand] >= \
	# 					thisTotalPowerMeanDuringPortStay + thisTotalPowerStdDevDuringPortStay or \
	# 					dfInput.loc[ap, flag_finalFile_TotalPowerDemand] <= \
	# 					thisTotalPowerMeanDuringPortStay - thisTotalPowerStdDevDuringPortStay:
	# 					dfInput.loc[ap, flag_finalFile_dataSanity] = 77
				
	thisTotalPowerMeanDuringPortStay = dfInput[flag_finalFile_TotalPowerDemand][
		(dfInput[flag_finalFile_Ship] == useOnlyThisShip) &
		(dfInput[flag_finalFile_dataSanity] == 1) &
		(dfInput[flag_finalFile_typeOfSailing] == flag_typeOfSailing_Port) &
		(dfInput[flag_finalFile_TotalPowerDemand] > minPowerDemandAccepted_kW)
	].mean()

	thisTotalPowerStdDevDuringPortStay = dfInput[flag_finalFile_TotalPowerDemand][
		(dfInput[flag_finalFile_Ship] == useOnlyThisShip) &
		(dfInput[flag_finalFile_dataSanity] == 1) &
		(dfInput[flag_finalFile_typeOfSailing] == flag_typeOfSailing_Port) &
		(dfInput[flag_finalFile_TotalPowerDemand] > minPowerDemandAccepted_kW)
		].std()

	# print("thisTotalPowerMean " + str(thisTotalPowerMean))
	# print("thisTotalPowerStdDev " + str(thisTotalPowerStdDev))
	maxPowerPossibleDuringPortStay = thisTotalPowerMeanDuringPortStay + 3 * thisTotalPowerStdDevDuringPortStay

	dfInput.loc[ \
		(dfInput[flag_finalFile_Ship] == useOnlyThisShip) &
		(dfInput[flag_finalFile_typeOfSailing] == flag_typeOfSailing_Port) &
		(dfInput[flag_finalFile_TotalPowerDemand] > maxPowerPossibleDuringPortStay),
		flag_finalFile_dataSanity
	] = 2

	dfInput.loc[ \
		(dfInput[flag_finalFile_Ship] == useOnlyThisShip) &
		(dfInput[flag_finalFile_typeOfSailing] == flag_typeOfSailing_Anchorage) &
		(dfInput[flag_finalFile_TotalPowerDemand] > maxPowerPossibleDuringPortStay),
		flag_finalFile_dataSanity
	] = 2
	
	dfInput.loc[ \
		(dfInput[flag_finalFile_Ship] == useOnlyThisShip) &
		(dfInput[flag_finalFile_TotalPowerDemand] < minPowerDemandAccepted_kW),
		flag_finalFile_dataSanity
	] = 0
	
	startTime = f_doTheTimeMeasurementInThisFunction(startTime, flag_timeEnd, inspect.stack()[0][3])
	
	print(useOnlyThisShip + " TOTAL FROZEN PWR " +str(frozenSignalsFound))
	return dfInput


# ######################################################################################################################
def func_printProgress(
	ap,
	minIndexThisShip,
	maxIndexThisShip,
	functionName
):
	print(functionName + " progress @ " + str(ap) + " RANGE: (" + str(minIndexThisShip) + " to " + str(maxIndexThisShip) + ")")


# ######################################################################################################################
def func_doTheRollingAverage(
	dfInput,
	dataToBeAveraged,
	newColumnNameForAverage,
	amountOfDatapoints,
	numberOfDigitsAfterRounding
):
	f_makeThePrintNiceStructured(True, "### BUILD THE ROLLING AVG for column " + dataToBeAveraged, inspect.stack()[0][3])
	startTime = time
	startTime = f_doTheTimeMeasurementInThisFunction(startTime, flag_timeStart, inspect.stack()[0][3])
	
	for thisUniqueShip in dfInput[flag_finalFile_Ship].unique():
		print("rolling average for ship: " + thisUniqueShip)
		#dfInput[newColumnNameForAverage] = dfInput[dataToBeAveraged].rolling(amountOfDatapoints).mean()
		dfInput.loc[
				(dfInput[flag_finalFile_Ship] == thisUniqueShip) &
				(dfInput[flag_finalFile_dataSanity] == 1), newColumnNameForAverage] = \
			dfInput.loc[
				(dfInput[flag_finalFile_Ship] == thisUniqueShip) &
				(dfInput[flag_finalFile_dataSanity] == 1)
			, dataToBeAveraged].rolling(amountOfDatapoints).mean()
	
	dfInput[newColumnNameForAverage] = dfInput[newColumnNameForAverage].round(decimals=numberOfDigitsAfterRounding)
	
	startTime = f_doTheTimeMeasurementInThisFunction(startTime, flag_timeEnd, inspect.stack()[0][3])
	
	return dfInput


# ######################################################################################################################
def func_getThisEngineAndFueltypeSFOC(
	flag_LoadPercent,
	flag_fuelType
):
	sfoc = 220
	flag_LoadPercent = flag_LoadPercent * 100
	
	if \
		flag_fuelType == fuel_flag_HFO or \
		flag_fuelType == fuel_flag_VLSFO:
		# 	=-0,0004059*POWER(A2;3) + 0,07729 *POWER(A2;2) - 4,914 *A2 + 321,1
		# sfoc = 220
		sfoc = \
			-0.0001252 * pow(flag_LoadPercent, 3) + \
			0.03754 * pow(flag_LoadPercent, 2) - \
			3.461 * flag_LoadPercent + \
			305.3
		
		# print("HFO/VLSFO SFOC:" + str(sfoc))
	
	if flag_fuelType == fuel_flag_MGO:
		# 	=-0,00008347*POWER(A2;3) + 0,02777*POWER(A2;2) - 2,757 * A2 + 277,6
		# sfoc = 210
		sfoc = \
			-0.00008347 * pow(flag_LoadPercent, 3) + \
			0.02777 * pow(flag_LoadPercent, 2) - \
			2.757 * flag_LoadPercent + \
			277.6
	
	# print("MGO SFOC:" + str(sfoc))
	
	if flag_fuelType == fuel_flag_LNG:
		sfoc = \
			- 0.000001131 * pow(flag_LoadPercent, 5) + \
			0.0003238 * pow(flag_LoadPercent, 4) + \
			- 0.03558 * pow(flag_LoadPercent,3) + \
			1.871 * pow(flag_LoadPercent, 2) + \
			-47.44 * pow(flag_LoadPercent, 1) + \
			+ 650.1
		
		# print("LNG SFOC:" + str(sfoc))
		
		# sfoc = 172
		
	return sfoc

# ######################################################################################################################
def f_calculateFuelConsumption(
	flag_activePWR,
	flag_thisSFOC,
	timestampsPerHour
):
	sfoc = 0
	thisTimeSliceConsumption = 0
	
	if flag_activePWR != '' and timestampsPerHour > 0:  # is not
		thisTimeSliceConsumption = round(float(flag_activePWR) * flag_thisSFOC / 1000 / 1000 / timestampsPerHour, 4)
	else:
		print("ERROR in f_calculateFuelConsumption!")
		print("timestampsPerHour " + str(timestampsPerHour))
		print("flag_activePWR " + str(flag_activePWR))
		print("sfoc " + str(sfoc))
		thisTimeSliceConsumption = -0.001
		
	return thisTimeSliceConsumption


# ######################################################################################################################
def f_eraseExistingPortName_LegNames_LegDates(
	dfInput
):
	if dict_ERASE_ALL_PortNames_LegNames_LegDates[analysisType] == 1:
		print("ERASE PORT & LEG NAMEs & START DATES FOR " + useOnlyThisShip + " only")
		dfInput.loc[dfInput[flag_finalFile_Ship] == useOnlyThisShip, flag_finalFile_legPortName] = ""
		dfInput.loc[dfInput[flag_finalFile_Ship] == useOnlyThisShip, flag_finalFile_legPortDate] = ""
		dfInput.loc[dfInput[flag_finalFile_Ship] == useOnlyThisShip, flag_finalFile_typeOfSailing] = ""

	return dfInput

# ######################################################################################################################
def f_insertPortNames(
	dfInput,
	dfPorts,
	useSpeedOnlyAsFilter
):
	f_makeThePrintNiceStructured(True, "### FILL PORT NAMES ", inspect.stack()[0][3])
	startTime = time
	startTime = f_doTheTimeMeasurementInThisFunction(startTime, flag_timeStart, inspect.stack()[0][3])
	
	if flag_finalFile_legPortName in dfInput.columns:
		dfInput[flag_finalFile_legPortName] = dfInput[flag_finalFile_legPortName].astype(str)
	
	dfPorts = f_readPortDbIntoDedicatedDF(dfPorts)
	
	dfInput = f_loopThroughDataAndAddMissingPortNames(dfInput, dfPorts, useSpeedOnlyAsFilter)
	
	startTime = f_doTheTimeMeasurementInThisFunction(startTime, flag_timeEnd, inspect.stack()[0][3])
	
	return dfInput, dfPorts


# ######################################################################################################################
def f_loopThroughDataAndAddMissingPortNames(
	dfInput,
	db_allPorts,
	useSpeedOnlyAsFilter
):
	f_makeThePrintNiceStructured(True, "### FILL PORT NAMES ", inspect.stack()[0][3])
	startTime = time
	startTime = f_doTheTimeMeasurementInThisFunction(startTime, flag_timeStart, inspect.stack()[0][3])
	
	if flag_finalFile_legPortName not in dfInput.columns:
		dfInput[flag_finalFile_legPortName] = ''
	
	foundTheShipThatWeNeedToAnalyse = False
	
	for ap in dfInput.index:
		if \
			(useSpeedOnlyAsFilter is False and dfInput.loc[ap, flag_finalFile_typeOfSailing] == flag_typeOfSailing_Port) or \
			(useSpeedOnlyAsFilter and float(dfInput.loc[ap, "SOG"]) <= 0.1):
			
			if len(dfInput.loc[ap, flag_finalFile_legPortName]) <= 3:
				
				origin = (dfInput.loc[ap, flag_finalFile_Latitude], dfInput.loc[ap, flag_finalFile_Longitude])
				
				dfInput, thisPortName = func_findRelatedPortAndUpdateDataframe(
					dfInput, db_allPorts, ap, origin
				)
				
				dfInput = func_insertThisPortNameInAllBlankFieldsWithSimilarLatLong(
					dfInput, ap, thisPortName)
				
	
	startTime = f_doTheTimeMeasurementInThisFunction(startTime, flag_timeEnd, inspect.stack()[0][3])
	
	return dfInput


# ######################################################################################################################
def func_findRelatedPortAndUpdateDataframe(
	dfInput,
	db_allPorts,
	ap,
	origin
):
	
	portFoundForThisLatLong = False
	thisPortName = ''
	
	for i in db_allPorts.index:
		dist = (db_allPorts.loc[i, flag_PortDB_LAT], db_allPorts.loc[i, flag_PortDB_LONG])
		
		thisDistance = gp.geodesic(origin, dist).miles / 1.15078
		
		if thisDistance < flag_maxDistanceForPortDetection:
			portFoundForThisLatLong = True
			print(
				# dfInput.loc[ap, flag_finalFile_Ship] + ": "+
				str(dfInput.loc[ap, flag_finalFile_Latitude]) + " " +
				str(dfInput.loc[ap, flag_finalFile_Longitude]) +
				" 1. CORRESPONDS to: " +
				db_allPorts.loc[i, flag_PortDB_ports_name])
			
			dfInput.loc[ap, flag_finalFile_legPortName] = db_allPorts.loc[i, flag_PortDB_ports_name]
			dfInput.loc[ap, flag_finalFile_typeOfSailing] = flag_typeOfSailing_Port
			
			thisPortName = db_allPorts.loc[i, flag_PortDB_ports_name]
			
			break
	
	if not portFoundForThisLatLong:
		for i in db_allPorts.index:
			dist = (db_allPorts.loc[i, flag_PortDB_LAT], db_allPorts.loc[i, flag_PortDB_LONG])
			
			thisDistance = gp.geodesic(origin, dist).miles / 1.15078
			
			if thisDistance < 2*flag_maxDistanceForPortDetection:
				portFoundForThisLatLong = True
				print(
					# dfInput.loc[ap, flag_finalFile_Ship] + ": " +
					str(dfInput.loc[ap, flag_finalFile_Latitude]) + " " +
					str(dfInput.loc[ap, flag_finalFile_Longitude]) +
					" 2. CORRESPONDS to: " +
					db_allPorts.loc[i, flag_PortDB_ports_name])
				
				dfInput.loc[ap, flag_finalFile_legPortName] = db_allPorts.loc[i, flag_PortDB_ports_name]
				dfInput.loc[ap, flag_finalFile_typeOfSailing] = flag_typeOfSailing_Port
				
				thisPortName = db_allPorts.loc[i, flag_PortDB_ports_name]
				
				break
	
	if not portFoundForThisLatLong:
		print("LAT LONG WITHOUT PORT IN PORT DB @ " + str(ap))
		dfInput.loc[ap, flag_finalFile_legPortName] = "PORT MISSING IN DB??"
		thisPortName = "PORT MISSING IN DB??"
	
	return dfInput, thisPortName


# ######################################################################################################################
def f_analyseDataForOneShipOnly(
):
	if len(useOnlyThisShip) > 0:
		return True
	else:
		return False


# ######################################################################################################################
def func_changeDataForThatShip(
	thisShip,
	doTheAnalysisForOneShipOnly
):
	if doTheAnalysisForOneShipOnly == False:
		return True
	
	if thisShip == useOnlyThisShip:
		return True
	
	return False


# ######################################################################################################################
def f_printWhenEverNextShipIsReached(
	dfInput,
	ap,
	thisShip,
	lastShip,
	stringBeforeShipName
):
	newShipFound = False
	
	thisShip = dfInput.loc[ap, flag_finalFile_Ship]
	if thisShip != lastShip:  # is not
		print('##############################################')
		print(stringBeforeShipName + dfInput.loc[ap, flag_finalFile_Ship])
		lastShip = dfInput.loc[ap, flag_finalFile_Ship]
		newShipFound = True
	
	return thisShip, lastShip, newShipFound


# ######################################################################################################################
def f_readPortDbIntoDedicatedDF(
	dfPorts
):
	print("len of port db " + str(len(dfPorts)))
	if len(dfPorts) == 0:
		dfPorts = pd.read_csv(masterFile_PORTs, sep=';', decimal=',', encoding='latin-1') #sourceFile_ports
		
		dfPorts[flag_PortDB_LAT] = dfPorts[flag_PortDB_LAT].astype(float)
		dfPorts[flag_PortDB_LONG] = dfPorts[flag_PortDB_LONG].astype(float)
	
	return dfPorts


# ######################################################################################################################
def f_averageOfSurroundingDataPointsIndicateAchoragePattern(
	dfInput,
	incomingAP
):
	avgSpeedSurroundingDataPoints = 0
	cnt_dataPointsSurrounding = 0
	allSurroundingDPsBelowMaxSpeedAndAboveZero = True
	
	avgSpeedUpcomingDataPoints = 0
	cnt_upcomingDataPoints = 0
	
	for ap in dfInput.index:
		if ap >= incomingAP - anchorage_amountOfSurroundingDPsToBeCheckedBeforeAfter:
			avgSpeedSurroundingDataPoints = avgSpeedSurroundingDataPoints + dfInput.loc[ap, flag_finalFile_SOG]
			cnt_dataPointsSurrounding = cnt_dataPointsSurrounding + 1
			allSurroundingDPsBelowMaxSpeedAndAboveZero = f_checkThisSpeedAgainstAnchorageSpeedPattern(
				dfInput.loc[ap, flag_finalFile_SOG]
			)
			if not allSurroundingDPsBelowMaxSpeedAndAboveZero:
				break
		
		if ap >= incomingAP:
			avgSpeedUpcomingDataPoints = avgSpeedUpcomingDataPoints + dfInput.loc[ap, flag_finalFile_SOG]
			cnt_upcomingDataPoints = cnt_upcomingDataPoints + 1
		
		if ap >= incomingAP + anchorage_amountOfSurroundingDPsToBeCheckedBeforeAfter:
			break
	
	if not allSurroundingDPsBelowMaxSpeedAndAboveZero:
		return False
	
	if cnt_dataPointsSurrounding > 0:
		avgSpeedSurroundingDataPoints = avgSpeedSurroundingDataPoints / cnt_dataPointsSurrounding
	
	if cnt_upcomingDataPoints > 0:
		avgSpeedUpcomingDataPoints = avgSpeedUpcomingDataPoints / cnt_upcomingDataPoints
	
	if \
		anchorage_maxAvgSpeedSurroundingDPs >= avgSpeedSurroundingDataPoints >= flag_maxSOG_ToBeCountedAsPortStay and \
			avgSpeedUpcomingDataPoints <= anchorage_maxAvgSpeedUpcomingDPs:
		# print("ANCHORAGE?!")
		return True
	
	return False


# ######################################################################################################################
def f_checkThisSpeedAgainstAnchorageSpeedPattern(
	thisSpeed
):
	if thisSpeed <= 0:
		return False
	
	return True


# ######################################################################################################################
def f_thisLatLongRemainsTheSameAndPreviousLineHasPortName(
	dfInput,
	ap
):
	if ap > 0:
		if len(dfInput.loc[ap - 1, flag_finalFile_legPortName]) > 3:
			if \
				abs(dfInput.loc[ap, flag_finalFile_Latitude]) - abs(dfInput.loc[ap - 1, flag_finalFile_Latitude]) < 0.05 and \
				abs(dfInput.loc[ap, flag_finalFile_Longitude]) - abs(dfInput.loc[ap - 1, flag_finalFile_Longitude]) < 0.05:
				# print("UNCHANGED LAT LONG >>> reuse " + dfInput.loc[ap - 1, flag_legPortName])
				return True
	
	return False


# ######################################################################################################################
def func_insertThisPortNameInAllBlankFieldsWithSimilarLatLong(
	dfInput,
	thisPortAP,
	thisPortName
):
	portNameFilledIn = 0
	
	thisPortLat = dfInput.loc[thisPortAP, flag_finalFile_Latitude]
	thisPortLong = dfInput.loc[thisPortAP, flag_finalFile_Longitude]
	
	thisPortLatRound3 = round(dfInput.loc[thisPortAP, flag_finalFile_Latitude], 3)
	thisPortLongRound3 = round(dfInput.loc[thisPortAP, flag_finalFile_Longitude], 3)
	
	# print("thisPortLat:  " + str(thisPortLat))
	# print("thisPortLong: " + str(thisPortLong))
	#
	# print("thisPortLatRound3:  " + str(thisPortLatRound3))
	# print("thisPortLongRound3: " + str(thisPortLongRound3))
	
	if flag_finalFile_SOG in dfInput.columns:
		dfInput.loc[ \
			(round(dfInput[flag_finalFile_Latitude],3) == thisPortLatRound3) &
			(round(dfInput[flag_finalFile_Longitude], 3) == thisPortLongRound3) &
			(dfInput[flag_finalFile_SOG] <= flag_maxSOG_ToBeCountedAsPortStay),
			flag_finalFile_legPortName
		] = thisPortName
		
		dfInput.loc[ \
			(round(dfInput[flag_finalFile_Latitude], 3) == thisPortLatRound3) &
			(round(dfInput[flag_finalFile_Longitude], 3) == thisPortLongRound3) &
			(dfInput[flag_finalFile_SOG] <= flag_maxSOG_ToBeCountedAsPortStay),
			flag_finalFile_typeOfSailing
		] = flag_typeOfSailing_Port
		
	else:
		dfInput.loc[ \
			(round(dfInput[flag_finalFile_Latitude], 3) == thisPortLatRound3) &
			(round(dfInput[flag_finalFile_Longitude], 3) == thisPortLongRound3) &
			(dfInput["SOG"] <= flag_maxSOG_ToBeCountedAsPortStay),
			flag_finalFile_legPortName
		] = thisPortName
		
		dfInput.loc[ \
			(round(dfInput[flag_finalFile_Latitude], 3) == thisPortLatRound3) &
			(round(dfInput[flag_finalFile_Longitude], 3) == thisPortLongRound3) &
			(dfInput["SOG"] <= flag_maxSOG_ToBeCountedAsPortStay),
			flag_finalFile_typeOfSailing
		] = flag_typeOfSailing_Port
		
	
	
	
	# print(" >>> " + thisPortName + " matched " + str(portNameFilledIn))
	return dfInput


# ######################################################################################################################
def func_botLatLongPairsHaveSamePrefic(
	lat1,
	long1,
	lat2,
	long2
):
	if lat1 < 0 and lat2 > 0:
		return False
	
	if lat1 > 0 and lat2 < 0:
		return False
	
	if long1 < 0 and long2 > 0:
		return False
	
	if long1 > 0 and long2 < 0:
		return False
	
	return True
	
	
# ######################################################################################################################
def f_fillGapsForLittlePortFluctuations(
	dfInput
):
	f_makeThePrintNiceStructured(True, "### FILL LITTLE PORT GAPS ", inspect.stack()[0][3])
	startTime = time
	startTime = f_doTheTimeMeasurementInThisFunction(startTime, flag_timeStart, inspect.stack()[0][3])
	
	dfInput[flag_finalFile_legPortName] = dfInput[flag_finalFile_legPortName].astype(str)
	
	lastPortName = ''
	
	for ap in dfInput.index:
		if len(dfInput.loc[ap, flag_finalFile_legPortName]) <= 3:
			if len(lastPortName) > 3:
				if f_thisPortWasNotLeftYet(dfInput, ap, lastPortName):
					# print(str(ap) + " >>> JEA FILL GAP with " + lastPortName)
					dfInput.loc[ap, flag_finalFile_legPortName] = lastPortName
					dfInput.loc[ap, flag_finalFile_typeOfSailing] = flag_typeOfSailing_Port
				else:
					lastPortName = ''
		else:
			if lastPortName != dfInput.loc[ap, flag_finalFile_legPortName]:
				lastPortName = dfInput.loc[ap, flag_finalFile_legPortName]
				# print(str(ap) + " >>> NEW LAST PORT NAME " + str(lastPortName))
	
	startTime = f_doTheTimeMeasurementInThisFunction(startTime, flag_timeEnd, inspect.stack()[0][3])
	
	return dfInput


# ######################################################################################################################
def f_thisPortWasNotLeftYet(
	dfInput,
	ap,
	lastPortName
):
	for subAp in dfInput.index:
		if subAp > ap:
			if dfInput.loc[subAp, flag_finalFile_legPortName] == lastPortName:
				# print("FILL LITTLE GAP FOR " + lastPortName)
				return True
		
		if subAp > ap + maxMissingLinesForPortInterruption:
			return False
	
	return False


# ######################################################################################################################
def f_fillRandomSpeedGaps(
	dfInput,
	doTheAnalysisForOneShipOnly
):
	f_makeThePrintNiceStructured(True, "### FILL SPEED GAPs (for NL averaged data) ", inspect.stack()[0][3])
	startTime = time
	startTime = f_doTheTimeMeasurementInThisFunction(startTime, flag_timeStart, inspect.stack()[0][3])
	
	gapStartsAt = 0
	
	if func_getCountOf_NANs_inColumn(dfInput, flag_finalFile_SOG) > 0:
	
		minIndexThisShip, maxIndexThisShip = func_getIndexRangeForThisShipsDate(dfInput, useOnlyThisShip)
		
		ap = minIndexThisShip - 1
		while ap < maxIndexThisShip:
			ap += 1
			
			if func_divisonPossible(ap, progressPrintCounter):
				func_printProgress(ap, minIndexThisShip, maxIndexThisShip, inspect.stack()[0][3])
			
			if dfInput.loc[ap, flag_finalFile_SOG] >= 3:
				if gapStartsAt > 0:
					if ap - gapStartsAt <= dfInput.loc[ap, flag_finalFile_SOG] / 3:
						print("fill speed gap between " + str(gapStartsAt) + " and " + str(ap))
						dfInput.loc[gapStartsAt:ap - 1, flag_finalFile_SOG] = dfInput.loc[ap, flag_finalFile_SOG]
						dfInput.loc[gapStartsAt:ap - 1, flag_finalFile_SOG_GAP_Filled] = 'SOG_GAP_FILLED'
				
				gapStartsAt = 0
			else:
				if gapStartsAt == 0:
					gapStartsAt = ap
		
	
	startTime = f_doTheTimeMeasurementInThisFunction(startTime, flag_timeEnd, inspect.stack()[0][3])
	
	return dfInput


# ######################################################################################################################
def f_insertLegNames(
	dfInput
):
	f_makeThePrintNiceStructured(True, "### FILL LEG NAMES ", inspect.stack()[0][3])
	startTime = time
	startTime = f_doTheTimeMeasurementInThisFunction(startTime, flag_timeStart, inspect.stack()[0][3])
	
	initalLegPortName = ''
	
	firstPortName = ''
	firstPortEnd_AP = 0
	
	lastPortName = ''
	lastPortStart_AP = 0
	
	dfInput[flag_finalFile_legPortName] = dfInput[flag_finalFile_legPortName].astype(str)
	
	minIndexThisShip, maxIndexThisShip = func_getIndexRangeForThisShipsDate(dfInput, useOnlyThisShip)

	ap = minIndexThisShip - 1
	while ap < maxIndexThisShip:
		ap += 1
		
		if func_divisonPossible(ap, progressPrintCounter):
			func_printProgress(ap, minIndexThisShip, maxIndexThisShip, inspect.stack()[0][3])
			
		if firstPortName == '':
			if len(dfInput.loc[ap, flag_finalFile_legPortName]) > 3:
				firstPortName = str(dfInput.loc[ap, flag_finalFile_legPortName])
				# print("firstPortName: " + firstPortName + " @ " + str(ap))
		else:
			if firstPortEnd_AP == 0:
				if firstPortName is not str(dfInput.loc[ap, flag_finalFile_legPortName]):
					if len(dfInput.loc[ap, flag_finalFile_legPortName]) <= 3 and firstPortEnd_AP == 0:
						firstPortEnd_AP = ap
						# print("firstPortEnd_AP: " + str(ap))
					
		if firstPortEnd_AP > 0 and firstPortName is not '':
			if lastPortName == '':
				if len(dfInput.loc[ap, flag_finalFile_legPortName]) > 3:
					# print("lastPortName: " + lastPortName + " @ " + str(ap))
					lastPortName = dfInput.loc[ap, flag_finalFile_legPortName]
					lastPortStart_AP = ap
		
		if lastPortStart_AP > 0:
			thisLegName = firstPortName + " to " + lastPortName
			
			print(
					str(dfInput.loc[ap, flag_finalFile_Ship]) +
					" >>> LEG: " + firstPortName + " to " + lastPortName +
					' KEY: ' + str(firstPortEnd_AP) + ' to ' + str(lastPortStart_AP)
			)
			
			dfInput.loc[firstPortEnd_AP:lastPortStart_AP-1, flag_finalFile_legPortName] = thisLegName
			
			firstPortName = ''
			firstPortEnd_AP = 0
			
			lastPortName = ''
			lastPortStart_AP = 0
	
	startTime = f_doTheTimeMeasurementInThisFunction(startTime, flag_timeEnd, inspect.stack()[0][3])
	
	return dfInput


# ######################################################################################################################
def f_sortThisDataframeByShipnameAndDate(
	dfInput,
	flag_Ship,
	flag_Date
):
	dfInput[flag_Date] = pd.to_datetime(dfInput[flag_Date])
	
	dfInput = dfInput.sort_values(by=[flag_Ship, flag_Date])
	
	dfInput = dfInput.reset_index(drop=True)
	
	return dfInput


# ######################################################################################################################
def f_insertMissingStartDates(
	dfInput,
	doTheAnalysisForOneShipOnly
):
	f_makeThePrintNiceStructured(True, "### FILL START DATES ", inspect.stack()[0][3])
	startTime = time
	startTime = f_doTheTimeMeasurementInThisFunction(startTime, flag_timeStart, inspect.stack()[0][3])
	
	dfInput[flag_finalFile_Date] = pd.to_datetime(dfInput[flag_finalFile_Date])
	dfInput[flag_finalFile_legPortName] = dfInput[flag_finalFile_legPortName].astype(str)
	
	thisLegPortStartDate = ''
	lastLinePortOrLegName = ''
	
	minIndexThisShip, maxIndexThisShip = func_getIndexRangeForThisShipsDate(dfInput, useOnlyThisShip)
	
	# print("minIndexThisShip: " + str(minIndexThisShip))
	
	ap = minIndexThisShip - 1
	# while ap < maxIndexThisShip:
	for ap in dfInput.index:
		if ap > 1:
			if len(str(dfInput.loc[ap, flag_finalFile_legPortDate])) > 3:
				if \
					(dfInput.loc[ap, flag_finalFile_legPortDate]) is not \
					(dfInput.loc[ap-1, flag_finalFile_legPortDate]):
					
					thisLegPortStartDate = dfInput.loc[ap, flag_finalFile_legPortDate]
					lastLinePortOrLegName = dfInput.loc[ap, flag_finalFile_legPortName]
				
				continue
			
			if dfInput.loc[ap, flag_finalFile_legPortName] != lastLinePortOrLegName:
				if len(dfInput.loc[ap, flag_finalFile_legPortName]) > 3:
					thisLegPortStartDate = dfInput.loc[ap, flag_finalFile_Date]
					lastLinePortOrLegName = dfInput.loc[ap, flag_finalFile_legPortName]
					print(
						dfInput.loc[ap, flag_finalFile_Ship] + " >>> NEW LEG/PORT START DATE @ " +
						str(thisLegPortStartDate) + " for " +
						str(lastLinePortOrLegName))
					
					dfInput.loc[ap, flag_finalFile_legPortDate] = thisLegPortStartDate
			else:
				dfInput.loc[ap, flag_finalFile_legPortDate] = thisLegPortStartDate
	
	startTime = f_doTheTimeMeasurementInThisFunction(startTime, flag_timeEnd, inspect.stack()[0][3])
	
	return dfInput


# ######################################################################################################################
def f_insertWarningsForWrongFuel(
	dfInput
):
	f_makeThePrintNiceStructured(True, "### CHECK FUEL TYPE FOR NON AAQS ENGINES!!! ", inspect.stack()[0][3])
	startTime = time
	startTime = f_doTheTimeMeasurementInThisFunction(startTime, flag_timeStart, inspect.stack()[0][3])
	
	# DG01 CHECK FUEL TYPE BURNED
	if dict_AAQS_engines[useOnlyThisShip][0] == 0:
		print("CHECK FUEL TYPE FOR NON AAQS ENGINE #1")
		dfInput[flag_finalFile_fuelType_DG01] = dfInput.apply(lambda x: f_markWrongFuelType(
			x[flag_finalFile_fuelType_DG01],
			x[flag_finalFile_environmentalRestriction],
			x[flag_finalFile_Ship],
			1
		), axis=1)
	# endregion
	
	# DG02 CHECK FUEL TYPE BURNED
	if dict_AAQS_engines[useOnlyThisShip][1] == 0:
		print("CHECK FUEL TYPE FOR NON AAQS ENGINE #2")
		dfInput[flag_finalFile_fuelType_DG02] = dfInput.apply(lambda x: f_markWrongFuelType(
			x[flag_finalFile_fuelType_DG02],
			x[flag_finalFile_environmentalRestriction],
			x[flag_finalFile_Ship],
			2
		), axis=1)
	# endregion
	
	# DG03 CHECK FUEL TYPE BURNED
	if dict_AAQS_engines[useOnlyThisShip][2] == 0:
		print("CHECK FUEL TYPE FOR NON AAQS ENGINE #3")
		dfInput[flag_finalFile_fuelType_DG03] = dfInput.apply(lambda x: f_markWrongFuelType(
			x[flag_finalFile_fuelType_DG03],
			x[flag_finalFile_environmentalRestriction],
			x[flag_finalFile_Ship],
			3
		), axis=1)
	# endregion
	
	# DG04 CHECK FUEL TYPE BURNED
	if dict_AAQS_engines[useOnlyThisShip][3] == 0:
		print("CHECK FUEL TYPE FOR NON AAQS ENGINE #4")
		dfInput[flag_finalFile_fuelType_DG04] = dfInput.apply(lambda x: f_markWrongFuelType(
			x[flag_finalFile_fuelType_DG04],
			x[flag_finalFile_environmentalRestriction],
			x[flag_finalFile_Ship],
			4
		), axis=1)
	
	# endregion
	
	# DG05 CHECK FUEL TYPE BURNED
	if dict_AAQS_engines[useOnlyThisShip][4] == 0:
		print("CHECK FUEL TYPE FOR NON AAQS ENGINE #5")
		dfInput[flag_finalFile_fuelType_DG05] = dfInput.apply(lambda x: f_markWrongFuelType(
			x[flag_finalFile_fuelType_DG05],
			x[flag_finalFile_environmentalRestriction],
			x[flag_finalFile_Ship],
			5
		), axis=1)
	# endregion
	
	# DG06 CHECK FUEL TYPE BURNED
	if dict_AAQS_engines[useOnlyThisShip][5] == 0:
		print("CHECK FUEL TYPE FOR NON AAQS ENGINE #6")
		dfInput[flag_finalFile_fuelType_DG06] = dfInput.apply(lambda x: f_markWrongFuelType(
			x[flag_finalFile_fuelType_DG06],
			x[flag_finalFile_environmentalRestriction],
			x[flag_finalFile_Ship],
			6
		), axis=1)
	# endregion
	
	startTime = f_doTheTimeMeasurementInThisFunction(startTime, flag_timeEnd, inspect.stack()[0][3])
	
	return dfInput


# ######################################################################################################################
def f_markWrongFuelType(
	fuelType,
	envRestriction,
	shipName,
	engineFlag
):
	engineFlag = engineFlag - 1
	
	if fuelType == fuel_flag_HFO:
		if dict_AAQS_engines[shipName][engineFlag] == 0:
			if fuelType.find('NOT AVAILABLE') < 0:
				print("WRONG FUEL TYPE! for " + shipName + " burning " + fuelType)
				return fuel_flag_HFO_NOAAQS
	
	return fuelType


# ######################################################################################################################
def f_markMissedOpportunitiesDuringPortStay(
	dfInput,
	useOnlyThisShip
):
	f_makeThePrintNiceStructured(True, "### FILL MISSED AAQS DURING PORT STAY ", inspect.stack()[0][3])
	startTime = time
	startTime = f_doTheTimeMeasurementInThisFunction(startTime, flag_timeStart, inspect.stack()[0][3])
	
	area_malaysia = path.Path(np.array(npa_territorialWaters_Lat_Long_Malaysia))
	
	# if dic_AAQS_PlannedForPortUsage[useOnlyThisShip] == 0:
	# 	print("SHIP NOT READY FOR AAQS in PORT >>> SKIP THIS CHECK")
	
	for ap in dfInput.index:
		if \
			dfInput.loc[ap, flag_finalFile_Ship] == 'Costa Fascinosa' or \
			dict_AAQS_available[useOnlyThisShip] == False:
			continue
		
		if dfInput.loc[ap, flag_finalFile_Ship] == 'Costa Favolosa':
			if dfInput.loc[ap, flag_finalFile_legPortName] == 'Civitavecchia (Rome)':
				if dfInput.loc[ap, flag_finalFile_Date] >= FA_noMoreAAQSAllowanceInCivi:
					continue
		
		if dic_AAQS_PlannedForPortUsage[useOnlyThisShip] == 0 and \
			dfInput.loc[ap, flag_finalFile_Date] < dict_ENV_regulationChange_AllShipsShouldTryAAQSInPort:
			continue
		
		if area_malaysia.contains_points(
			[(dfInput.loc[ap, flag_finalFile_Latitude], dfInput.loc[ap, flag_finalFile_Longitude])]
		):
			dfInput.loc[ap, flag_finalFile_AAQS_AssessmentDone] = flag_AAQS_Usage_NotAllowedInThisParticularRegion
			dfInput = f_markFuelTypeInCaseOfSailingInsideNonAAQSRegion(thisShip, dfInput, ap)
			continue
		
		if \
			dfInput.loc[ap, flag_finalFile_typeOfSailing] != flag_typeOfSailing_Port and \
			dfInput.loc[ap, flag_finalFile_DriftingAnchorage] != flag_typeOfSailing_Anchorage:
			continue
		
		if \
			dfInput.loc[ap, flag_finalFile_typeOfSailing] == flag_typeOfSailing_Port and \
			dfInput.loc[ap, flag_finalFile_environmentalRestriction] == flag_ENV_Restriction_AAQS_NOT_allowedInThisPort:
			continue
		
		if \
			dic_AAQS_PlannedForPortUsage[dfInput.loc[ap, flag_finalFile_Ship]] == 1 or \
			dfInput.loc[ap, flag_finalFile_DriftingAnchorage] == flag_typeOfSailing_Anchorage or \
			(
				dic_AAQS_PlannedForPortUsage[useOnlyThisShip] == 0 and \
				dfInput.loc[ap, flag_finalFile_Date] >= dict_ENV_regulationChange_AllShipsShouldTryAAQSInPort
			):
			
			
			dfInput = f_markEnginesRunningWithMGOAsPossibleLoss(ap, dfInput, fuel_flag_AAQS_Missed_PORT)
		
		# if dic_AAQS_PlannedForPortUsage[dfInput.loc[ap, flag_finalFile_Ship]] != 1:
		# 	dfInput.loc[ap, flag_finalFile_AAQS_AssessmentDone] = flag_AAQS_Usage_Assessment_WashWaterFilterMissing
		# 	dfInput = f_markEnginesRunningWithMGOAsPossibleLoss(ap, dfInput, flag_AAQS_Usage_Assessment_WashWaterFilterMissing)
		# else:
		# 	dfInput = f_markEnginesRunningWithMGOAsPossibleLoss(ap, dfInput, fuel_flag_AAQS_Missed_PORT)
	
	startTime = f_doTheTimeMeasurementInThisFunction(startTime, flag_timeEnd, inspect.stack()[0][3])
	
	return dfInput


# ######################################################################################################################
def func_getIndexRangeForThisShipsDate(
	dfInput,
	useOnlyThisShip
):
	# f_makeThePrintNiceStructured(True, "### GET INDEX RANGE FOR SHIP: " + useOnlyThisShip, inspect.stack()[0][3])
	
	if useOnlyThisShip is not '':
		subDF = dfInput[dfInput[flag_finalFile_Ship] == useOnlyThisShip]
	else:
		subDF = dfInput
	
	# print(subDF.index.min())
	# print(subDF.index.max())
	
	print("   data index this ship between " + str(subDF.index.min()) + " and " + str(subDF.index.max()))
	
	return subDF.index.min(), subDF.index.max()


# ######################################################################################################################
def f_addTimeStampsPerHour(
	dfInput,
	doTheAnalysisForOneShipOnly
):
	f_makeThePrintNiceStructured(True, "### Fill amount of datapoints per hour ", inspect.stack()[0][3])
	startTime = time
	startTime = f_doTheTimeMeasurementInThisFunction(startTime, flag_timeStart, inspect.stack()[0][3])
	
	if flag_finalFile_timestampsPerHour in dfInput.columns:
		dfInput[flag_finalFile_timestampsPerHour] = dfInput[flag_finalFile_timestampsPerHour].astype(float)
	else:
		dfInput[flag_finalFile_timestampsPerHour] = 0
	
	if dict_ERASE_ExistingTimeStampsPerHour[analysisType] == 1:
		dfInput.loc[dfInput[flag_finalFile_Ship] == useOnlyThisShip, flag_finalFile_timestampsPerHour] = 0
	
	lastTimeStampThisShip = ''
	
	minIndexThisShip, maxIndexThisShip = func_getIndexRangeForThisShipsDate(dfInput, useOnlyThisShip)
	
	ap = minIndexThisShip - 1
	while ap < maxIndexThisShip:
		ap += 1
		
		if func_divisonPossible(ap, 5000):
			func_printProgress(ap, minIndexThisShip, maxIndexThisShip, inspect.stack()[0][3])
		
		if dfInput.loc[ap, flag_finalFile_timestampsPerHour] > 1:
			# print("ALL fine")
			lastTimeStampThisShip = dfInput.loc[ap, flag_finalFile_Date]
			continue
		
		thisPlaceTimeStamp = dfInput.loc[ap, flag_finalFile_Date]
		# print("thisPlaceTimeStamp " + str(thisPlaceTimeStamp))
		
		if lastTimeStampThisShip == thisPlaceTimeStamp:
			print("UPS. double line@ " + str(dfInput.loc[ap, flag_finalFile_Date]) + " drop one")
			dfInput = dfInput.drop(ap)
			continue

		if ap > 0 and lastTimeStampThisShip != '':
			# print("ship:						" + str(dfInput.loc[ap, flag_finalFile_Ship]))
			# print("lastTimeStampThisShip:						" + str(lastTimeStampThisShip))
			# print("dfInput.loc[ap, flag_finalFile_Date]: " + str(dfInput.loc[ap, flag_finalFile_Date]))

			delta = round((60 / ((thisPlaceTimeStamp - lastTimeStampThisShip).total_seconds() / 60)), 2)
			# print("delta " + str(delta))
			if delta > 0:
				dfInput.loc[ap, flag_finalFile_timestampsPerHour] = delta
				# print("update df @ " + str(ap) + " using this new value " + str(dfFinal.loc[ap, flag_finalFile_timestampsPerHour]))
			else:
				dfInput.loc[ap, flag_finalFile_timestampsPerHour] = 5
		else:
			dfInput.loc[ap, flag_finalFile_timestampsPerHour] = 5

		lastTimeStampThisShip = thisPlaceTimeStamp
	
	dfInput[flag_finalFile_timestampsPerHour] = dfInput[flag_finalFile_timestampsPerHour].astype(float)
	
	startTime = f_doTheTimeMeasurementInThisFunction(startTime, flag_timeEnd, inspect.stack()[0][3])
	
	return dfInput


# ######################################################################################################################
def f_markEnginesRunningWithMGOAsPossibleLoss(
	ap,
	dfInput,
	commentFlag
):
	if dfInput.loc[ap, flag_finalFile_fuelType_DG01] == fuel_flag_MGO:
		# print(dfInput.loc[ap, flag_finalFile_Ship] + " MISSED AAQS IN PORT FOR DG1")
		dfInput.loc[ap, flag_finalFile_fuelType_DG01] = commentFlag
	
	if dfInput.loc[ap, flag_finalFile_fuelType_DG02] == fuel_flag_MGO:
		# print(dfInput.loc[ap, flag_finalFile_Ship] + " MISSED AAQS IN PORT FOR DG1")
		dfInput.loc[ap, flag_finalFile_fuelType_DG02] = commentFlag
	
	if dfInput.loc[ap, flag_finalFile_fuelType_DG03] == fuel_flag_MGO:
		# print(dfInput.loc[ap, flag_finalFile_Ship] + " MISSED AAQS IN PORT FOR DG3")
		dfInput.loc[ap, flag_finalFile_fuelType_DG03] = commentFlag
	
	if dfInput.loc[ap, flag_finalFile_fuelType_DG04] == fuel_flag_MGO:
		# print(dfInput.loc[ap, flag_finalFile_Ship] + " MISSED AAQS IN PORT FOR DG4")
		dfInput.loc[ap, flag_finalFile_fuelType_DG04] = commentFlag
	
	if dfInput.loc[ap, flag_finalFile_fuelType_DG05] == fuel_flag_MGO:
		# print(dfInput.loc[ap, flag_finalFile_Ship] + " MISSED AAQS IN PORT FOR DG5")
		dfInput.loc[ap, flag_finalFile_fuelType_DG05] = commentFlag
	
	if dfInput.loc[ap, flag_finalFile_fuelType_DG06] == fuel_flag_MGO:
		# print(dfInput.loc[ap, flag_finalFile_Ship] + " MISSED AAQS IN PORT FOR DG6")
		dfInput.loc[ap, flag_finalFile_fuelType_DG06] = commentFlag
	
	return dfInput


# ######################################################################################################################
def f_eraseThatColumnIfItExists(
	dfInput,
	thisFlag
):
	if thisFlag in dfInput.columns:
		dfInput[thisFlag] = ''
	
	return dfInput


# ######################################################################################################################
def f_markFuelTypeInCaseOfSailingInsideNonAAQSRegion(
	thisShip,
	dfInput,
	ap
):
	engineUsage = f_getEngineUsageForThisSlice(dfInput, ap, flag_engineDate_fuelType)
	fuelOilInTemp = f_getEngineUsageForThisSlice(dfInput, ap, flag_engineDate_FuelTemp)
	
	thisEngine = 0
	while thisEngine < 6:
		if \
			engineUsage[thisEngine] != fuel_flag_EngineIsOff and \
				fuelOilInTemp[thisEngine] > 20:
			
			if fuelOilInTemp[thisEngine] >= flag_hfo_mgo_fuelTempSplit:
				dfInput.loc[ap, switch_getDataframeFlagThisEngine(thisEngine + 1)] = fuel_flag_HFO_InsideTerritorialWater
			else:
				dfInput.loc[ap, switch_getDataframeFlagThisEngine(thisEngine + 1)] = fuel_flag_MGO_InsideTerritorialWater
		
		thisEngine += 1
	
	return dfInput


# ######################################################################################################################
def f_getCorrectIssueFileForThatShip(
	useOnlyThisShip,
	aaqsIssues_AIDA,
	aaqsIssues_Costa
):
	
	if f_getThisBrand(useOnlyThisShip) == flag_brand_AIDA:
		aaqsIssueFile = aaqsIssues_AIDA
	else:
		aaqsIssueFile = aaqsIssues_Costa
		
	return aaqsIssueFile


# ######################################################################################################################
def f_erasePreviousOutOfOrderAssessments(
	dfInput
):
	dfInput = func_eraseContentForThatShipInThatColumnWithThisValue(
		dfInput, useOnlyThisShip, flag_finalFile_DG1_AAQS_DowntimeReason, '')
	dfInput = func_eraseContentForThatShipInThatColumnWithThisValue(
		dfInput, useOnlyThisShip, flag_finalFile_DG2_AAQS_DowntimeReason, '')
	dfInput = func_eraseContentForThatShipInThatColumnWithThisValue(
		dfInput, useOnlyThisShip, flag_finalFile_DG3_AAQS_DowntimeReason, '')
	dfInput = func_eraseContentForThatShipInThatColumnWithThisValue(
		dfInput, useOnlyThisShip, flag_finalFile_DG4_AAQS_DowntimeReason, '')
	dfInput = func_eraseContentForThatShipInThatColumnWithThisValue(
		dfInput, useOnlyThisShip, flag_finalFile_DG5_AAQS_DowntimeReason, '')
	dfInput = func_eraseContentForThatShipInThatColumnWithThisValue(
		dfInput, useOnlyThisShip, flag_finalFile_DG6_AAQS_DowntimeReason, '')
	
	dfInput = func_eraseContentForThatShipInThatColumnWithThisValue(
		dfInput, useOnlyThisShip, flag_finalFile_DG1_AAQS_DowntimeMissedPower, '')
	dfInput = func_eraseContentForThatShipInThatColumnWithThisValue(
		dfInput, useOnlyThisShip, flag_finalFile_DG2_AAQS_DowntimeMissedPower, '')
	dfInput = func_eraseContentForThatShipInThatColumnWithThisValue(
		dfInput, useOnlyThisShip, flag_finalFile_DG3_AAQS_DowntimeMissedPower, '')
	dfInput = func_eraseContentForThatShipInThatColumnWithThisValue(
		dfInput, useOnlyThisShip, flag_finalFile_DG4_AAQS_DowntimeMissedPower, '')
	dfInput = func_eraseContentForThatShipInThatColumnWithThisValue(
		dfInput, useOnlyThisShip, flag_finalFile_DG5_AAQS_DowntimeMissedPower, '')
	dfInput = func_eraseContentForThatShipInThatColumnWithThisValue(
		dfInput, useOnlyThisShip, flag_finalFile_DG6_AAQS_DowntimeMissedPower, '')

	return dfInput


# ######################################################################################################################
def func_eraseContentForThatShipInThatColumnWithThisValue(
	dfInput,
	thisShip,
	thisColumn,
	thisNewContent
):
	if thisColumn in dfInput.columns:
		dfInput.loc[dfInput[flag_finalFile_Ship] == thisShip, thisColumn] = thisNewContent
	else:
		dfInput[thisColumn] = thisNewContent
	
	return dfInput
	
# ######################################################################################################################
def fillReasonsForAAQSOutOfOrder(
	dfInput,
	aaqsIssueFile
):
	f_makeThePrintNiceStructured(True, "### MARK KNOWN AAQS ISSUES in ", inspect.stack()[0][3])
	startTime = time
	startTime = f_doTheTimeMeasurementInThisFunction(startTime, flag_timeStart, inspect.stack()[0][3])
	
	df_thisShipIssues = f_readTheIssueFile(aaqsIssueFile)
	
	# print(df_thisShipIssues[flag_issuesFile_startDate])
	
	df_thisShipIssues[flag_issuesFile_startDate] = pd.to_datetime(
		df_thisShipIssues[flag_issuesFile_startDate],
		format="%d.%m.%Y") #, infer_datetime_format=False, exact=True
	
	df_thisShipIssues[flag_issuesFile_endDate] = pd.to_datetime(
		df_thisShipIssues[flag_issuesFile_endDate],
		format="%d.%m.%Y")
	
	# df_thisShipIssues[flag_issuesFile_startDate] = df_thisShipIssues[flag_issuesFile_startDate].astype('datetime64[ns]')
	# df_thisShipIssues[flag_issuesFile_endDate] = df_thisShipIssues[flag_issuesFile_endDate].astype('datetime64[ns]')
	
	# for ap in df_thisShipIssues.index:
	# 	if len(str(df_thisShipIssues.loc[ap, flag_issuesFile_issue])) > 3:
			# print("START-DATE: " + str(df_thisShipIssues.loc[ap, flag_issuesFile_startDate]))
			# print("END-DATE: " + str(df_thisShipIssues.loc[ap, flag_issuesFile_endDate]))
			# print("DG(s): " + str(df_thisShipIssues.loc[ap, flag_issuesFile_affectedDG]))
			# print("Reason: " + str(df_thisShipIssues.loc[ap, flag_issuesFile_issue]))
			# print("Comment: " + str(df_thisShipIssues.loc[ap, flag_issuesFile_Comments]))
		
	for ap in df_thisShipIssues.index:
		if \
			len(str(df_thisShipIssues.loc[ap, flag_issuesFile_affectedDG])) > 0 and \
			str(df_thisShipIssues.loc[ap, flag_issuesFile_affectedDG]) != "nan":
			
			if func_EngineNumberGivenInTheReasonFile(int(df_thisShipIssues.loc[ap, flag_issuesFile_affectedDG][-1])):
				if len(str(df_thisShipIssues.loc[ap, flag_issuesFile_issue])) > 3:
					print("CHECK THAT REASON")
					dfInput = f_analyseEngineUsageDataAndFillReasonIfNecessary(ap, df_thisShipIssues, dfInput)
		else:
			print("SHIP: " + useOnlyThisShip +" AAQS ooo reasons: NO engine number given for reason ("+
					str(df_thisShipIssues.loc[ap, flag_issuesFile_issue])+")"
					)
			
	startTime = f_doTheTimeMeasurementInThisFunction(startTime, flag_timeEnd, inspect.stack()[0][3])
	
	return dfInput


# ######################################################################################################################
def func_EngineNumberGivenInTheReasonFile(
	engineNumber
):
	if \
		engineNumber == 1 or \
		engineNumber == 2 or \
		engineNumber == 3 or \
		engineNumber == 4 or \
		engineNumber == 5 or \
		engineNumber == 6:
		return True
	
	return False


# ######################################################################################################################
def f_analyseEngineUsageDataAndFillReasonIfNecessary(
	ap_inIssuesFile,
	thisIssue,
	dfInput
):
	logTheDetailsInThatFunction = False
	countCasesFound = 0
	
	print("########################################")
	print("   FILL DATA FOR REASON: " + thisIssue.loc[ap_inIssuesFile, flag_issuesFile_issue] + " START-Date: " +
			str(thisIssue.loc[ap_inIssuesFile, flag_issuesFile_startDate]) + " END-Date: " +
			str(thisIssue.loc[ap_inIssuesFile, flag_issuesFile_endDate]) + " ENGINE: " +
			str(thisIssue.loc[ap_inIssuesFile, flag_issuesFile_affectedDG][-1]) + " AREA: " +
			str(thisIssue.loc[ap_inIssuesFile, flag_issuesFile_Area]))
	
	issueStartDate = thisIssue.loc[ap_inIssuesFile, flag_issuesFile_startDate]
	issueEndDate = thisIssue.loc[ap_inIssuesFile, flag_issuesFile_endDate]
	affectedEngine = int(thisIssue.loc[ap_inIssuesFile, flag_issuesFile_affectedDG][-1])
	affectedRegion = thisIssue.loc[ap_inIssuesFile, flag_issuesFile_Area]
	
	for ap in dfInput.index:
		if not func_changeDataForThatShip(dfInput.loc[ap, flag_finalFile_Ship], doTheAnalysisForOneShipOnly):
			continue
		
		#region Actual Date has to be within Issue Period
		if not func_actualTimeIsWithinIssuePeriod(
			dfInput.loc[ap, flag_finalFile_Date],
			issueStartDate,
			issueEndDate,
			logTheDetailsInThatFunction
		):
			continue
		#endregion
		
		#region Actual Area has to match with AREA of issue
		if not func_ReasonAreaForOutOfOrderSameAsActualRegion(
			affectedRegion,
			dfInput.loc[ap, flag_finalFile_typeOfSailing],
			False
		):
			continue
		#endregion
		
		#region NO REASON for that engine available at this time
		actualData_downtimeReasons = f_getEngineUsageForThisSlice(dfInput, ap, flag_engineDate_DowntimeReasons)
		if func_downtimeReasonAlreadyAvailableInExistingData(
			actualData_downtimeReasons,
			affectedEngine,
			logTheDetailsInThatFunction
		):
			continue
		#endregion
		
		actualData_fuelTypeAssessment = f_getEngineUsageForThisSlice(dfInput, ap, flag_engineDate_fuelType)
		
		enginesWithMissedAAQSThisDatapoint = \
			sum(1 for el in actualData_fuelTypeAssessment if
				 (el == fuel_flag_AAQS_Missed_NAVIGATION or el == fuel_flag_AAQS_Missed_PORT))
		
		enginesThatAreFilledWithAReason = \
			sum(1 for el in actualData_downtimeReasons if len(str(el)) > 3)
		
		if enginesThatAreFilledWithAReason < enginesWithMissedAAQSThisDatapoint:
			if logTheDetailsInThatFunction:
				print("#############################################")
				print("REASON FOUND && ENGINE WITH MISSED OPPORTUNITY FOUND @ " + str(dfInput.loc[ap, flag_finalFile_Date]))
				print("enginesWithMissedAAQSThisDatapoint " + str(enginesWithMissedAAQSThisDatapoint))
				print("enginesThatAreFilledWithAReason " + str(enginesThatAreFilledWithAReason))
			
			if len(str(actualData_downtimeReasons[affectedEngine-1])) <= 4:
				if logTheDetailsInThatFunction:
					print("FILL THE REASON: " + thisIssue.loc[ap_inIssuesFile, flag_issuesFile_issue])
				
				if func_thisEngineWasOffOrRunningWithWrongFuelType(
					dfInput.loc[ap, switch_getDataframeFlagThisEngine(affectedEngine)],
					logTheDetailsInThatFunction
				):
					dfInput.loc[ap, switch_getDataframeFlagThisEngineReason(affectedEngine)] = \
						thisIssue.loc[ap_inIssuesFile, flag_issuesFile_issue]
					
					actualData_enginePower = f_getEngineUsageForThisSlice(dfInput, ap, flag_engineDate_EnginePower)
					
					missedPower = func_thisEngineWasRunningButAAQSWasOff(
						dfInput.loc[ap, switch_getDataframeFlagThisEngine(affectedEngine)],
						actualData_enginePower[affectedEngine - 1],
						affectedEngine,
						logTheDetailsInThatFunction
					)
					
					#region if the engine with the AAQS issue was not running, we search for the next best engine running
					# that was flagged with the missed opportunity flag to use this engine power as missed opportunity
					if missedPower == 0:
						missedPower = func_getEnginePowerOfRunningEngineWithFlagMissedOpportunity(
							actualData_fuelTypeAssessment,
							actualData_enginePower,
							enginesThatAreFilledWithAReason,
							logTheDetailsInThatFunction
						)
					#endregion
					
					if logTheDetailsInThatFunction:
						print("   #######################")
						print("   DONE >>> MISSED OPPORTUNITY FOR ENGINE "+str(affectedEngine))
						print("   missedPower: " + str(missedPower))
						print("   issue: " + str(thisIssue.loc[ap_inIssuesFile, flag_issuesFile_issue]))
					
					countCasesFound += 1
					
					dfInput.loc[ap, switch_getDataframeFlagThisEngineReason(affectedEngine)] = \
						thisIssue.loc[ap_inIssuesFile, flag_issuesFile_issue]
					
					dfInput.loc[ap, switch_getDataframeFlagThisEngineMissedPower(affectedEngine)] = \
						missedPower
				
					
				else:
					if logTheDetailsInThatFunction:
						print("AFFECTED ENGINE WAS RUNNING WITH PERFECT FUEL!!! NO MISSED OPPORTUNITY")
						print("FUEL ASSESSMENT: " + dfInput.loc[ap, switch_getDataframeFlagThisEngine(affectedEngine)])
			else:
				print("UPS: there is already a reason for the affected engine. no double counting!")
		else:
			if logTheDetailsInThatFunction:
				print("#############################################")
				print("NO ADDITIONAL MISSED OPPORTUNITY CAN BE FOUND FOR THAT REASON @ " + str(dfInput.loc[ap, flag_finalFile_Date]))
				print("enginesWithMissedAAQSThisDatapoint " + str(enginesWithMissedAAQSThisDatapoint))
				print("enginesThatAreFilledWithAReason " + str(enginesThatAreFilledWithAReason))
					
	# else:
	# 	print("ups, there is a reason available @ " + str(dfInput.loc[ap, flag_finalFile_Date]))
	# 	print(actualData_downtimeReasons)
	
	print("countCasesFound: " + str(countCasesFound))
	
	return dfInput


# ######################################################################################################################
def func_thisEngineWasRunningButAAQSWasOff(
	thisEngineDowntimeReasonRightNow,
	thisEnginePower,
	affectedEngine,
	logInHere
):
	missedPower = 0
	if \
		thisEngineDowntimeReasonRightNow == fuel_flag_AAQS_Missed_NAVIGATION or \
		thisEngineDowntimeReasonRightNow == fuel_flag_AAQS_Missed_PORT:
		
		missedPower = thisEnginePower
		
		if logInHere:
			print("AAQS engine was not using AAQS >>> use this power as lost opportunity = ("+str(missedPower)+")")
	
	if logInHere:
		if thisEngineDowntimeReasonRightNow == fuel_flag_EngineIsOff:
			print("AFFECTED ENGINE #"+str(affectedEngine)+" was OFF >>> missedPower can not be used from that engine")
	
	return missedPower
	
	
# ######################################################################################################################
def func_actualTimeIsWithinIssuePeriod(
	actualDate,
	issueStartDate,
	issueEndDate,
	logInHere
):
	# if \
	# 	dfInput.loc[ap, flag_finalFile_Date] >= issueStartDate and \
	# 	(len(str(issueEndDate)) <= 3 or dfInput.loc[ap, flag_finalFile_Date] < issueEndDate):
	
	if \
		actualDate >= issueStartDate and \
		(len(str(issueEndDate)) <= 3 or actualDate < issueEndDate):
		if logInHere:
			print("actual date ("+str(actualDate) + ") is within issue time range between." +
					" START-Date ("+str(issueStartDate) + ") END-DATE ("+str(issueEndDate) + ")"
					)
		return True
	
	return False
	

# ######################################################################################################################
def func_ReasonAreaForOutOfOrderSameAsActualRegion(
	affectedRegion,
	thisTimeStateOfSailingOrPort,
	logInHere
):
	if affectedRegion == flag_issueArea_Harbour_and_See:
		if logInHere:
			print(
				"REGION MATCH >>> AFFECTED AREA: " + affectedRegion + " = actual region: " + thisTimeStateOfSailingOrPort)
		return True
	
	if \
		affectedRegion == flag_issueArea_Harbour and \
		(
			thisTimeStateOfSailingOrPort == flag_typeOfSailing_Port or
			thisTimeStateOfSailingOrPort == flag_typeOfSailing_Anchorage):
		if logInHere:
			print(
				"REGION MATCH >>> AFFECTED AREA: " + affectedRegion + " = actual region: " + thisTimeStateOfSailingOrPort)
			
		return True
		
	if \
		affectedRegion == flag_issueArea_See and \
		thisTimeStateOfSailingOrPort == flag_typeOfSailing_Sailing:
		if logInHere:
			print(
				"REGION MATCH >>> AFFECTED AREA: " + affectedRegion + " = actual region: " + thisTimeStateOfSailingOrPort)
			
		return True
	
	if logInHere:
		print("AFFECTED AREA: " + affectedRegion + " does not match with actual region: " + thisTimeStateOfSailingOrPort)
	
	return False
	
# ######################################################################################################################
def func_thisEngineWasOffOrRunningWithWrongFuelType(
	thisEngineDowntimeReasonRightNow,
	logInHere
):
	if \
		thisEngineDowntimeReasonRightNow == fuel_flag_AAQS_Missed_NAVIGATION or \
		thisEngineDowntimeReasonRightNow == fuel_flag_AAQS_Missed_PORT or \
		thisEngineDowntimeReasonRightNow == fuel_flag_EngineIsOff:
		if logInHere:
			print("ATTENTION: AAQS Opportunity missed for that engine. thisEngineDowntimeReasonRightNow: " + thisEngineDowntimeReasonRightNow)
		return True
	
	
	
	# if logInHere:
	# 	print(
	# 		"NO AAQS Opportunity missed for that engine. thisEngineDowntimeReasonRightNow: " + thisEngineDowntimeReasonRightNow)
		
	return False
	
# ######################################################################################################################
def func_getEnginePowerOfRunningEngineWithFlagMissedOpportunity(
	actualData_fuelTypeAssessment,
	actualData_enginePower,
	enginesThatAreFilledWithAReason,
	logTheDetailsInThatFunction
):
	missedPower = 0
	thisEngine = 0
	enginesThatAreFlaggedAsMissedOpportunity = 0
	
	for el in actualData_fuelTypeAssessment:
		thisEngine += 1
		if el == fuel_flag_AAQS_Missed_NAVIGATION or el == fuel_flag_AAQS_Missed_PORT:
			enginesThatAreFlaggedAsMissedOpportunity += 1
			if enginesThatAreFlaggedAsMissedOpportunity > enginesThatAreFilledWithAReason:
				if logTheDetailsInThatFunction:
					print("USE PWR FROM ENGINE " + str(thisEngine) + " with " + str(actualData_enginePower[thisEngine - 1]) + "kW as missed opportunity pwr" )
				
				missedPower = actualData_enginePower[thisEngine - 1]
				break
	
	return missedPower
	

# ######################################################################################################################
def func_downtimeReasonAlreadyAvailableInExistingData(
	actualData_downtimeReasons,
	affectedEngine,
	logInHere
):
	if len(str(actualData_downtimeReasons[affectedEngine-1])) > 4:
		if logInHere:
			print("REASON FOR THAT ENGINE ("+str(affectedEngine-1) +") AVAILABLE ALREADY. DO NOT OVERRIDE. REASON: " + str(actualData_downtimeReasons[affectedEngine-1]))
		return True
	
	return False
	

# ######################################################################################################################
def switch_getDataframeFlagThisEngineReason(
	thisEngine
):
	flagInMasterFile = {
		1: flag_finalFile_DG1_AAQS_DowntimeReason,
		2: flag_finalFile_DG2_AAQS_DowntimeReason,
		3: flag_finalFile_DG3_AAQS_DowntimeReason,
		4: flag_finalFile_DG4_AAQS_DowntimeReason,
		5: flag_finalFile_DG5_AAQS_DowntimeReason,
		6: flag_finalFile_DG6_AAQS_DowntimeReason
	}
	return (flagInMasterFile.get(thisEngine, "ENGINE DOES NOT EXIST"))


# ######################################################################################################################
def switch_getDataframeFlagThisEngineMissedPower(
	thisEngine
):
	flagInMasterFile = {
		1: flag_finalFile_DG1_AAQS_DowntimeMissedPower,
		2: flag_finalFile_DG2_AAQS_DowntimeMissedPower,
		3: flag_finalFile_DG3_AAQS_DowntimeMissedPower,
		4: flag_finalFile_DG4_AAQS_DowntimeMissedPower,
		5: flag_finalFile_DG5_AAQS_DowntimeMissedPower,
		6: flag_finalFile_DG6_AAQS_DowntimeMissedPower
	}
	return (flagInMasterFile.get(thisEngine, "ENGINE DOES NOT EXIST"))



# ######################################################################################################################
def f_getEngineUsageForThisSlice(
	dfInput,
	ap,
	flag_engineDataType
):
	if flag_engineDataType == flag_engineDate_fuelType:
		thisEngineData = [
			dfInput.loc[ap, flag_finalFile_fuelType_DG01],
			dfInput.loc[ap, flag_finalFile_fuelType_DG02],
			dfInput.loc[ap, flag_finalFile_fuelType_DG03],
			dfInput.loc[ap, flag_finalFile_fuelType_DG04],
			dfInput.loc[ap, flag_finalFile_fuelType_DG05],
			dfInput.loc[ap, flag_finalFile_fuelType_DG06]
		]
	
	if flag_engineDataType == flag_engineDate_EnginePower:
		thisEngineData = [
			dfInput.loc[ap, flag_finalFile_DG1_ACTIVE_POWER],
			dfInput.loc[ap, flag_finalFile_DG2_ACTIVE_POWER],
			dfInput.loc[ap, flag_finalFile_DG3_ACTIVE_POWER],
			dfInput.loc[ap, flag_finalFile_DG4_ACTIVE_POWER],
			dfInput.loc[ap, flag_finalFile_DG5_ACTIVE_POWER],
			dfInput.loc[ap, flag_finalFile_DG6_ACTIVE_POWER]
		]
	
	if flag_engineDataType == flag_engineDate_FuelTemp:
		thisEngineData = [
			dfInput.loc[ap, flag_finalFile_DG1_FUEL_OIL_IN_TE],
			dfInput.loc[ap, flag_finalFile_DG2_FUEL_OIL_IN_TE],
			dfInput.loc[ap, flag_finalFile_DG3_FUEL_OIL_IN_TE],
			dfInput.loc[ap, flag_finalFile_DG4_FUEL_OIL_IN_TE],
			dfInput.loc[ap, flag_finalFile_DG5_FUEL_OIL_IN_TE],
			dfInput.loc[ap, flag_finalFile_DG6_FUEL_OIL_IN_TE]
		]
	
	if flag_engineDataType == flag_engineDate_DowntimeReasons:
		thisEngineData = [
			dfInput.loc[ap, flag_finalFile_DG1_AAQS_DowntimeReason],
			dfInput.loc[ap, flag_finalFile_DG2_AAQS_DowntimeReason],
			dfInput.loc[ap, flag_finalFile_DG3_AAQS_DowntimeReason],
			dfInput.loc[ap, flag_finalFile_DG4_AAQS_DowntimeReason],
			dfInput.loc[ap, flag_finalFile_DG5_AAQS_DowntimeReason],
			dfInput.loc[ap, flag_finalFile_DG6_AAQS_DowntimeReason]
		]
		
	return thisEngineData
	
	
# ######################################################################################################################
def f_readTheIssueFile(
	aaqsIssueFile
):
	df_thisShipIssues = pd.read_excel(
		aaqsIssueFile,
		sheet_name=dict_shipNamesScrubberIssueFile[useOnlyThisShip],
		skiprows=1
	)
	
	return df_thisShipIssues


# ######################################################################################################################
def f_markChangeOverTimesBeforeArrival(
	dfInput,
	doTheAnalysisForOneShipOnly
):
	f_makeThePrintNiceStructured(True, "### MARK CHANGE-OVER TIME BEFORE ARRIVAL ", inspect.stack()[0][3])
	startTime = time
	startTime = f_doTheTimeMeasurementInThisFunction(startTime, flag_timeStart, inspect.stack()[0][3])
	
	dfInput[flag_finalFile_AAQS_AssessmentDone] = dfInput[flag_finalFile_AAQS_AssessmentDone].astype(str)
	
	ap_ThisPortWithNoAAQSAllowanceArrival = 0
	
	firstLineThisShip = 0
	
	consecutiveDatapoints = 25
	maxIndex = dfInput.index.max()
	
	for ap in dfInput.index:
		if ap-1 < consecutiveDatapoints:
			continue
		
		if ap >= maxIndex - consecutiveDatapoints:
			continue
		
		if firstLineThisShip == 0:
			firstLineThisShip = ap
		
		if ap > 0:
			if dfInput.loc[ap, flag_finalFile_environmentalRestriction] == flag_ENV_Restriction_AAQS_NOT_allowedInThisPort:
				if \
					dfInput.loc[ap - 5, flag_finalFile_typeOfSailing] == flag_typeOfSailing_Sailing and \
					dfInput.loc[ap - 4, flag_finalFile_typeOfSailing] == flag_typeOfSailing_Sailing and \
					dfInput.loc[ap - 3, flag_finalFile_typeOfSailing] == flag_typeOfSailing_Sailing and \
					dfInput.loc[ap - 2, flag_finalFile_typeOfSailing] == flag_typeOfSailing_Sailing and \
					dfInput.loc[ap - 1, flag_finalFile_typeOfSailing] == flag_typeOfSailing_Sailing and \
					dfInput.loc[ap + 0, flag_finalFile_typeOfSailing] == flag_typeOfSailing_Port and \
					dfInput.loc[ap + 1, flag_finalFile_typeOfSailing] == flag_typeOfSailing_Port and \
					dfInput.loc[ap + 2, flag_finalFile_typeOfSailing] == flag_typeOfSailing_Port and \
					dfInput.loc[ap + 3, flag_finalFile_typeOfSailing] == flag_typeOfSailing_Port and \
					dfInput.loc[ap + 4, flag_finalFile_typeOfSailing] == flag_typeOfSailing_Port and \
					dfInput.loc[ap + 5, flag_finalFile_typeOfSailing] == flag_typeOfSailing_Port:
				
				# print("ap - consecutiveDatapoints " + str(ap - consecutiveDatapoints))
				# print("ap - 1 " + str(ap - 1))
				# print("ap + consecutiveDatapoints " + str(ap + consecutiveDatapoints))
				# TODO >> how to compare this long range against one condition without loop???
				# if dfInput.loc[ap - consecutiveDatapoints :ap - 1,
				# 		flag_finalFile_typeOfSailing] == flag_typeOfSailing_Sailing and \
				# 	dfInput.loc[ap : ap+consecutiveDatapoints,
				# 		flag_finalFile_typeOfSailing] == flag_typeOfSailing_Port:
					
					ap_ThisPortWithNoAAQSAllowanceArrival = ap
					print("FUEL CHANGEOVER!!! ARRIVAL IN (" +
							dfInput.loc[ap, flag_finalFile_legPortName] +
							") WITH NO AAQS ALLOWANCE @ " + str(ap)
							)
		
			if ap_ThisPortWithNoAAQSAllowanceArrival > 0:
				ap_ChangeOverStartTime = func_getChangeOverStartOrEndTime(
					dfInput, firstLineThisShip, ap, flag_getChangeOverStartTimeBeforeArrival)
				
				if ap_ChangeOverStartTime > 0:
					dfInput = f_updateAAQSAssessmentWithFuelChangeoverNeeded_BEFORE_ARRIVAL(
						dfInput, ap_ChangeOverStartTime, ap)
					
					ap_ThisPortWithNoAAQSAllowanceArrival = 0
	
	startTime = f_doTheTimeMeasurementInThisFunction(startTime, flag_timeEnd, inspect.stack()[0][3])
	
	return dfInput


# ######################################################################################################################
def func_getChangeOverStartOrEndTime(
	dfInput,
	firstLineThisShip,
	ap_Start_or_EndOfThisPortCall,
	flag_typeOfStartEndTime
):
	ap_ChangeOverStartTime = 0
	thisAp = ap_Start_or_EndOfThisPortCall
	
	thisShip = dfInput.loc[ap_Start_or_EndOfThisPortCall, flag_finalFile_Ship]
	
	lenOfDataframe = len(dfInput[flag_finalFile_Ship])
	
	if flag_typeOfStartEndTime == flag_getChangeOverStartTimeBeforeArrival:
		changeoverStart_or_EndTime = \
			dfInput.loc[ap_Start_or_EndOfThisPortCall, flag_finalFile_Date] - \
			timedelta(minutes=minutesNeededForFullFuelChangeoverBeforeArrivalInNoAAQSPort)
		# print("START TIME OF PORT CALL " + str(dfInput.loc[ap_Start_or_EndOfThisPortCall, flag_finalFile_Date]))
		# print("CHANGE OVER START TIME  " + str(changeoverStart_or_EndTime))
	else:
		changeoverStart_or_EndTime = \
			dfInput.loc[ap_Start_or_EndOfThisPortCall, flag_finalFile_Date] + \
			timedelta(minutes=minutesNeededForFullFuelChangeoverBeforeArrivalInNoAAQSPort)
		
		# print("END TIME OF PORT CALL " + str(dfInput.loc[ap_Start_or_EndOfThisPortCall, flag_finalFile_Date]))
		# print("CHANGE OVER END TIME  " + str(changeoverStart_or_EndTime))
	
	if flag_typeOfStartEndTime == flag_getChangeOverStartTimeBeforeArrival:
		while thisAp > firstLineThisShip and thisAp > 0:
			thisAp = thisAp - 1
			if dfInput.loc[thisAp, flag_finalFile_Date] < changeoverStart_or_EndTime:
				ap_ChangeOverStartTime = thisAp
				print("   >>> Changeover should start right here @ ap " + str(ap_ChangeOverStartTime) +
						"(" + str(dfInput.loc[thisAp, flag_finalFile_Date]) + ")")
				break
	else:
		while \
			dfInput.loc[thisAp, flag_finalFile_Ship] == thisShip and \
			dfInput.loc[thisAp, flag_finalFile_typeOfSailing] == flag_typeOfSailing_Sailing and \
			thisAp + 1 < lenOfDataframe:
			
			thisAp = thisAp + 1
			if dfInput.loc[thisAp, flag_finalFile_Date] > changeoverStart_or_EndTime:
				ap_ChangeOverStartTime = thisAp
				print("   >>> Changeover will end right here @ ap " + str(ap_ChangeOverStartTime) +
						"(" + str(dfInput.loc[thisAp, flag_finalFile_Date]) + ")")
				break
	
	return ap_ChangeOverStartTime


# ######################################################################################################################
def f_updateAAQSAssessmentWithFuelChangeoverNeeded_BEFORE_ARRIVAL(
	dfInput,
	ap_ChangeOverStartTime,
	ap_startOfPortCall
):
	thisAP = ap_ChangeOverStartTime
	
	while thisAP < ap_startOfPortCall:
		# region change fuel type back if the previous assessment was "missed opportunity"
		fuelTypePerEngine = [
			dfInput.loc[thisAP, flag_finalFile_fuelType_DG01],
			dfInput.loc[thisAP, flag_finalFile_fuelType_DG02],
			dfInput.loc[thisAP, flag_finalFile_fuelType_DG03],
			dfInput.loc[thisAP, flag_finalFile_fuelType_DG04],
			dfInput.loc[thisAP, flag_finalFile_fuelType_DG05],
			dfInput.loc[thisAP, flag_finalFile_fuelType_DG06]
		]
		
		thisEngine = 0
		while thisEngine < 6:
			if dict_AAQS_engines[useOnlyThisShip][thisEngine] > -1:
				if fuelTypePerEngine[thisEngine] == fuel_flag_AAQS_Missed_NAVIGATION:
					dfInput.loc[thisAP, switch_getDataframeFlagThisEngine(thisEngine + 1)] = fuel_flag_MGO
			
			thisEngine += 1
		# endregion
		
		if dfInput.loc[thisAP, flag_finalFile_AAQS_AssessmentDone] != flag_AAQS_Usage_NotAllowedInThisParticularRegion:
			dfInput.loc[thisAP, flag_finalFile_AAQS_AssessmentDone] = \
				flag_AAQS_Usage_Assessment_FuelChangeoverMandatoryBeforeArrival
		
		thisAP = thisAP + 1
	
	return dfInput


# ######################################################################################################################
def f_markChangeOverTimesAfterDeparture(
	dfInput,
	doTheAnalysisForOneShipOnly
):
	f_makeThePrintNiceStructured(True, "### MARK CHANGE-OVER TIME AFTER DEPARTURE ", inspect.stack()[0][3])
	startTime = time
	startTime = f_doTheTimeMeasurementInThisFunction(startTime, flag_timeStart, inspect.stack()[0][3])
	
	dfInput[flag_finalFile_AAQS_AssessmentDone] = dfInput[flag_finalFile_AAQS_AssessmentDone].astype(str)
	
	ap_ThisPortWithNoAAQSAllowanceDeparture = 0
	
	firstLineThisShip = 0
	
	consecutiveDatapoints = 25
	maxIndex = dfInput.index.max()
	
	for ap in dfInput.index:
		if ap-1 < consecutiveDatapoints:
			continue
		
		if ap >= maxIndex - consecutiveDatapoints:
			continue
		
		if firstLineThisShip == 0:
			firstLineThisShip = ap
		
		if ap > 0:
			if \
				dfInput.loc[ap-1, flag_finalFile_environmentalRestriction] == flag_ENV_Restriction_AAQS_NOT_allowedInThisPort:
				# TODO >> how to compare this long range against one condition without loop???
				if \
					dfInput.loc[ap + 5, flag_finalFile_typeOfSailing] == flag_typeOfSailing_Sailing and \
					dfInput.loc[ap + 4, flag_finalFile_typeOfSailing] == flag_typeOfSailing_Sailing and \
					dfInput.loc[ap + 3, flag_finalFile_typeOfSailing] == flag_typeOfSailing_Sailing and \
					dfInput.loc[ap + 2, flag_finalFile_typeOfSailing] == flag_typeOfSailing_Sailing and \
					dfInput.loc[ap + 1, flag_finalFile_typeOfSailing] == flag_typeOfSailing_Sailing and \
					dfInput.loc[ap + 0, flag_finalFile_typeOfSailing] == flag_typeOfSailing_Sailing and \
					dfInput.loc[ap - 1, flag_finalFile_typeOfSailing] == flag_typeOfSailing_Port and \
					dfInput.loc[ap - 2, flag_finalFile_typeOfSailing] == flag_typeOfSailing_Port and \
					dfInput.loc[ap - 3, flag_finalFile_typeOfSailing] == flag_typeOfSailing_Port and \
					dfInput.loc[ap - 4, flag_finalFile_typeOfSailing] == flag_typeOfSailing_Port and \
					dfInput.loc[ap - 5, flag_finalFile_typeOfSailing] == flag_typeOfSailing_Port:
				# if \
				# 	dfInput.loc[ap:ap+consecutiveDatapoints, flag_finalFile_typeOfSailing] == \
				# 		flag_typeOfSailing_Sailing and \
				# 	dfInput.loc[ap - consecutiveDatapoints:ap-1, flag_finalFile_typeOfSailing] == \
				# 		flag_typeOfSailing_Port:
					
					ap_ThisPortWithNoAAQSAllowanceDeparture = ap
					print("FUEL CHANGEOVER!!! DEPARTURE FROM (" +
							dfInput.loc[ap, flag_finalFile_legPortName] + ") WITH NO AAQS ALLOWANCE @ " + str(ap) +
							" (" +
							str(dfInput.loc[ap, flag_finalFile_Date]) + ")")
		
			if ap_ThisPortWithNoAAQSAllowanceDeparture > 0:
				ap_ChangeOverEnd = func_getChangeOverStartOrEndTime(
					dfInput, firstLineThisShip, ap, flag_getChangeOverEndeTimeAfterDeparture)
				
				if ap_ChangeOverEnd > 0:
					dfInput = f_updateAAQSAssessmentWithFuelChangeoverNeeded_AFTER_DEPARTURE(
						dfInput, ap, ap_ChangeOverEnd)
					
				ap_ThisPortWithNoAAQSAllowanceDeparture = 0
	
	startTime = f_doTheTimeMeasurementInThisFunction(startTime, flag_timeEnd, inspect.stack()[0][3])
	
	return dfInput


# ######################################################################################################################
def f_updateAAQSAssessmentWithFuelChangeoverNeeded_AFTER_DEPARTURE(
	dfInput,
	ap_DepartureStart,
	ap_EndOfDepartureChangeoverTime
):
	thisAP = ap_DepartureStart
	
	while thisAP < ap_EndOfDepartureChangeoverTime:
		# region change fuel type back if the previous assessment was "missed opportunity"
		fuelTypePerEngine = [
			dfInput.loc[thisAP, flag_finalFile_fuelType_DG01],
			dfInput.loc[thisAP, flag_finalFile_fuelType_DG02],
			dfInput.loc[thisAP, flag_finalFile_fuelType_DG03],
			dfInput.loc[thisAP, flag_finalFile_fuelType_DG04],
			dfInput.loc[thisAP, flag_finalFile_fuelType_DG05],
			dfInput.loc[thisAP, flag_finalFile_fuelType_DG06]
		]
		
		thisEngine = 0
		while thisEngine < 6:
			if dict_AAQS_engines[useOnlyThisShip][thisEngine] > -1:
				if fuelTypePerEngine[thisEngine] == fuel_flag_AAQS_Missed_NAVIGATION:
					dfInput.loc[thisAP, switch_getDataframeFlagThisEngine(thisEngine + 1)] = fuel_flag_MGO
			
			thisEngine += 1
		# endregion
		
		if dfInput.loc[thisAP, flag_finalFile_AAQS_AssessmentDone] != flag_AAQS_Usage_NotAllowedInThisParticularRegion:
			dfInput.loc[thisAP, flag_finalFile_AAQS_AssessmentDone] = \
				flag_AAQS_Usage_Assessment_FuelChangeoverMandatoryAfterDeparture
		
		thisAP = thisAP + 1
	
	return dfInput


# ######################################################################################################################
def switch_getDataframeFlagThisEngine(
	thisEngine
):
	fuelTypePerEngineFlags = {
		1: flag_finalFile_fuelType_DG01,
		2: flag_finalFile_fuelType_DG02,
		3: flag_finalFile_fuelType_DG03,
		4: flag_finalFile_fuelType_DG04,
		5: flag_finalFile_fuelType_DG05,
		6: flag_finalFile_fuelType_DG06
	}
	return (fuelTypePerEngineFlags.get(thisEngine, "ENGINE DOES NOT EXIST"))


# ######################################################################################################################
def f_getAmountOfScrubberForThisShip(
	thisShip
):
	scrubberEngines = 0
	thisEngine = 0
	while thisEngine < 6:
		if dict_AAQS_engines[thisShip][thisEngine] > 0:
			scrubberEngines += 1
		
		if dict_AAQS_engines[thisShip][thisEngine] < 0:
			break
		
		thisEngine += 1
	
	return scrubberEngines


# ######################################################################################################################
def f_doSomeTypeCasts(
	dfSource
):
	#TODO
	dfInput = dfSource.copy() #just to avoid the stupid error message
	
	f_doTheTypeCastForThisColumn(dfInput, flag_finalFile_SOG)
	f_doTheTypeCastForThisColumn(dfInput, flag_finalFile_STW)
	f_doTheTypeCastForThisColumn(dfInput, flag_finalFile_Temperature)
	f_doTheTypeCastForThisColumn(dfInput, flag_finalFile_Humidity)
	f_doTheTypeCastForThisColumn(dfInput, flag_finalFile_STW)
	
	f_doTheTypeCastForThisColumn(dfInput, flag_finalFile_DG1_FUEL_OIL_IN_TE)
	f_doTheTypeCastForThisColumn(dfInput, flag_finalFile_DG2_FUEL_OIL_IN_TE)
	f_doTheTypeCastForThisColumn(dfInput, flag_finalFile_DG3_FUEL_OIL_IN_TE)
	f_doTheTypeCastForThisColumn(dfInput, flag_finalFile_DG4_FUEL_OIL_IN_TE)
	f_doTheTypeCastForThisColumn(dfInput, flag_finalFile_DG5_FUEL_OIL_IN_TE)
	f_doTheTypeCastForThisColumn(dfInput, flag_finalFile_DG6_FUEL_OIL_IN_TE)
	
	f_doTheTypeCastForThisColumn(dfInput, flag_finalFile_DG1_ACTIVE_POWER)
	f_doTheTypeCastForThisColumn(dfInput, flag_finalFile_DG2_ACTIVE_POWER)
	f_doTheTypeCastForThisColumn(dfInput, flag_finalFile_DG3_ACTIVE_POWER)
	f_doTheTypeCastForThisColumn(dfInput, flag_finalFile_DG4_ACTIVE_POWER)
	f_doTheTypeCastForThisColumn(dfInput, flag_finalFile_DG5_ACTIVE_POWER)
	f_doTheTypeCastForThisColumn(dfInput, flag_finalFile_DG6_ACTIVE_POWER)
	f_doTheTypeCastForThisColumn(dfInput, flag_finalFile_EnginesRunning)
	
	f_doTheTypeCastForThisColumn(dfInput, flag_finalFile_DG1_LoadPercent)
	f_doTheTypeCastForThisColumn(dfInput, flag_finalFile_DG2_LoadPercent)
	f_doTheTypeCastForThisColumn(dfInput, flag_finalFile_DG3_LoadPercent)
	f_doTheTypeCastForThisColumn(dfInput, flag_finalFile_DG4_LoadPercent)
	f_doTheTypeCastForThisColumn(dfInput, flag_finalFile_DG5_LoadPercent)
	f_doTheTypeCastForThisColumn(dfInput, flag_finalFile_DG6_LoadPercent)
	
	f_doTheTypeCastForThisColumn(dfInput, flag_finalFile_DG1_fuelConsumption)
	f_doTheTypeCastForThisColumn(dfInput, flag_finalFile_DG2_fuelConsumption)
	f_doTheTypeCastForThisColumn(dfInput, flag_finalFile_DG3_fuelConsumption)
	f_doTheTypeCastForThisColumn(dfInput, flag_finalFile_DG4_fuelConsumption)
	f_doTheTypeCastForThisColumn(dfInput, flag_finalFile_DG5_fuelConsumption)
	f_doTheTypeCastForThisColumn(dfInput, flag_finalFile_DG6_fuelConsumption)
	
	f_doTheTypeCastForThisColumn(dfInput, flag_finalFile_AvgPwrDemandOverTime)
	f_doTheTypeCastForThisColumn(dfInput, flag_finalFile_AvgEngineUsagePercentNow)
	f_doTheTypeCastForThisColumn(dfInput, flag_finalFile_AvgTemperatureOverTime)
	
	f_doTheTypeCastForThisColumn(dfInput, flag_finalFile_DG1_DeSOx_PumpPWR)
	f_doTheTypeCastForThisColumn(dfInput, flag_finalFile_DG2_DeSOx_PumpPWR)
	f_doTheTypeCastForThisColumn(dfInput, flag_finalFile_DG3_DeSOx_PumpPWR)
	f_doTheTypeCastForThisColumn(dfInput, flag_finalFile_DG4_DeSOx_PumpPWR)
	f_doTheTypeCastForThisColumn(dfInput, flag_finalFile_DG5_DeSOx_PumpPWR)
	f_doTheTypeCastForThisColumn(dfInput, flag_finalFile_DG6_DeSOx_PumpPWR)
	
	f_doTheTypeCastForThisColumn(dfInput, flag_finalFile_Latitude)
	f_doTheTypeCastForThisColumn(dfInput, flag_finalFile_Longitude)
	
	f_doTheTypeCastForThisColumn(dfInput, flag_finalFile_timestampsPerHour)
	
	f_doTheTypeCastForThisColumn(dfInput, flag_finalFile_DG1_AAQS_DowntimeMissedPower)
	f_doTheTypeCastForThisColumn(dfInput, flag_finalFile_DG2_AAQS_DowntimeMissedPower)
	f_doTheTypeCastForThisColumn(dfInput, flag_finalFile_DG3_AAQS_DowntimeMissedPower)
	f_doTheTypeCastForThisColumn(dfInput, flag_finalFile_DG4_AAQS_DowntimeMissedPower)
	f_doTheTypeCastForThisColumn(dfInput, flag_finalFile_DG5_AAQS_DowntimeMissedPower)
	f_doTheTypeCastForThisColumn(dfInput, flag_finalFile_DG6_AAQS_DowntimeMissedPower)
	
	f_doTheTypeCastForThisColumn(dfInput, flag_finalFile_totalFuel_HFO)
	f_doTheTypeCastForThisColumn(dfInput, flag_finalFile_totalFuel_MGO)
	f_doTheTypeCastForThisColumn(dfInput, flag_finalFile_totalFuel_LNG)
	
	return dfInput


# ######################################################################################################################
def f_doTheTypeCastForThisColumn(
	dfInput,
	thisFlag
):
	if thisFlag in dfInput.columns:
		dfInput[thisFlag] = dfInput[thisFlag].astype(str)
		dfInput[thisFlag] = dfInput[thisFlag].str.replace("'", '')
		dfInput[thisFlag] = dfInput[thisFlag].str.replace(',', '.')
		dfInput[thisFlag] = dfInput[thisFlag].astype(float)
	
	return dfInput

# ######################################################################################################################
def f_printMinMaxDateForThisShip(
	thisShip, dfInput
):
	dfInput = dfInput[dfInput[flag_finalFile_Ship] == thisShip]
	
	minTimeStampMasterFile = dfInput[flag_NeptuneLab_Date].min()
	maxTimeStampMasterFile = dfInput[flag_NeptuneLab_Date].max()
	
	print('######################################################')
	print(thisShip + ' minTimeStampMasterFile: ' + str(minTimeStampMasterFile))
	print(thisShip + ' maxTimeStampMasterFile: ' + str(maxTimeStampMasterFile))


# ######################################################################################################################
def f_markLatLongInsideTerritorialWaters(
	dfInput
):
	f_makeThePrintNiceStructured(True, "### MARK SHIPS THAT ARE IN SPECIAL REGIONS WITH AAQS NON ALLOWANCE ",
										  inspect.stack()[0][3])
	startTime = time
	startTime = f_doTheTimeMeasurementInThisFunction(startTime, flag_timeStart, inspect.stack()[0][3])
	
	myNewLatArray = pd.Series(dfInput[flag_finalFile_Latitude])
	myNewLongArray = pd.Series(dfInput[flag_finalFile_Longitude])
	# myNewLatArray = pd.Series(dfFinal[flag_finalFile_Latitude][dfFinal[flag_finalFile_Ship] == useOnlyThisShip])
	# myNewLongArray = pd.Series(dfFinal[flag_finalFile_Longitude][dfFinal[flag_finalFile_Ship] == useOnlyThisShip])
	
	finalLatLongAsTwoDArray = np.column_stack((myNewLatArray, myNewLongArray))
	
	dfInput = f_doTheCheckupForThisCountry(
		dfInput,
		finalLatLongAsTwoDArray,
		npa_territorialWaters_Lat_Long_Malaysia,
		territorial_Name_Malaysia
	)
	
	dfInput = f_doTheCheckupForThisCountry(
		dfInput,
		finalLatLongAsTwoDArray,
		npa_territorialWaters_Lat_Long_BohaiRim,
		territorial_Name_China_BohaiRim
	)
	
	dfInput = f_doTheCheckupForThisCountry(
		dfInput,
		finalLatLongAsTwoDArray,
		npa_territorialWaters_Lat_Long_ChinaMainCountry,
		territorial_Name_China_MainLand
	)
	
	dfInput = f_doTheCheckupForThisCountry(
		dfInput,
		finalLatLongAsTwoDArray,
		npa_territorialWaters_Lat_Long_Suez,
		territorial_Name_SuezChannel
	)
	
	dfInput = f_doTheCheckupForThisCountry(
		dfInput,
		finalLatLongAsTwoDArray,
		npa_territorialWaters_Lat_Long_Germany_NorthSea,
		territorial_Name_Germany_NorthSea
	)
	
	dfInput = f_doTheCheckupForThisCountry(
		dfInput,
		finalLatLongAsTwoDArray,
		npa_territorialWaters_Lat_Long_Gran_Canaria,
		territorial_Name_Gran_Canaria,
		aaqsBanCanaryIslands
	)
	
	dfInput = f_doTheCheckupForThisCountry(
		dfInput,
		finalLatLongAsTwoDArray,
		npa_territorialWaters_Lat_Long_Tenerife_La_Gomera,
		territorial_Name_Tenerife_La_Gomera,
		aaqsBanCanaryIslands
	)
	
	dfInput = f_doTheCheckupForThisCountry(
		dfInput,
		finalLatLongAsTwoDArray,
		npa_territorialWaters_Lat_Long_La_Palma,
		territorial_Name_La_Palma,
		aaqsBanCanaryIslands
	)
	
	dfInput = f_doTheCheckupForThisCountry(
		dfInput,
		finalLatLongAsTwoDArray,
		npa_territorialWaters_Lat_Long_Fuerte_Lanzarote,
		territorial_Name_Fuerte_Lanzarote,
		aaqsBanCanaryIslands
	)
	
	startTime = f_doTheTimeMeasurementInThisFunction(startTime, flag_timeEnd, inspect.stack()[0][3])
	
	return dfInput


# ######################################################################################################################
def f_doTheCheckupForThisCountry(
	dfInput,
	finalLatLongAsTwoDArray,
	terretorialWaters_Lats_Longs,
	countryName,
	aaqsBanStartDate = ""
):
	f_makeThePrintNiceStructured(True, "### Territorial Water Checkup for " + countryName, inspect.stack()[0][3])
	startTime = time
	startTime = f_doTheTimeMeasurementInThisFunction(startTime, flag_timeStart, inspect.stack()[0][3])
	
	dfSubset = pd.DataFrame()
	
	p = path.Path(np.array(terretorialWaters_Lats_Longs))
	dfSubset[flag_finalFile_environmentalRestriction] = p.contains_points(np.array(finalLatLongAsTwoDArray))
	
	for ap in dfInput.index:
		if aaqsBanStartDate == "" or \
			(aaqsBanStartDate != "" and dfInput.loc[ap, flag_finalFile_Date] >= aaqsBanStartDate):
		
			if len(str(dfSubset.loc[ap, flag_finalFile_environmentalRestriction])) > 3:
				continue
				
			if dfSubset.loc[ap, flag_finalFile_environmentalRestriction]:
				print(str(dfInput.loc[ap, flag_finalFile_Date]) +
						" >>> " +  territorialWater_NO_AAQS_ALLOWED + " " + countryName)
				
				dfInput.loc[
					ap, flag_finalFile_environmentalRestriction] = territorialWater_NO_AAQS_ALLOWED + " " + countryName
	
	startTime = f_doTheTimeMeasurementInThisFunction(startTime, flag_timeEnd, inspect.stack()[0][3])
	
	return dfInput


# ######################################################################################################################
def f_readScrubberIssuesMasterFile(
	flag_brand
):
	if flag_brand == flag_brand_AIDA:
		xlsFile_ScrubberIssues = pd.ExcelFile(masterFile_technicalIssues_AIDA)
	else:
		xlsFile_ScrubberIssues = pd.ExcelFile(masterFile_technicalIssues_Costa)
	
	# xlsFile_ScrubberIssues = xlsFile_ScrubberIssues[flag_issuesFile_startDate].astype('datetime64[ns]')
	# xlsFile_ScrubberIssues = xlsFile_ScrubberIssues[flag_issuesFile_endDate].astype('datetime64[ns]')
	
	# print(xlsFile_ScrubberIssues_AIDA.sheet_names)
	
	return xlsFile_ScrubberIssues


# ######################################################################################################################
def f_exportFinalFilesWithDataForWholeFleet(
	dfFinal,
	dfSubset
):
	#region EXPORT DATA TO DUMMY FILES
	if export_DUMMY_TEST_FILE_ONLY:
		print("EXPORT INTO DUMMY FILES")
		if dict_MASTER_WHAT_TO_DO["master_analyseData_AAQS_DAILY"] == 1:
			f_exportDataframe(
				fileExport_csv, dfFinal, dummyTestFile_AAQS, ''
			)
		if dict_MASTER_WHAT_TO_DO["master_analyseData_LayUp"] == 1:
			if export_MASTER_CSV_FILE:
				f_exportDataframe(
					fileExport_csv, dfFinal, masterFile_LayUp_ALL_csv_DUMMY, ''
				)
				
				f_exportDataframe(
					fileExport_csv, dfSubset, masterFile_LayUp_ALL_PORT_ONLY_DATA_csv_DUMMY, ''
				)
	#endregion
	
	#region EXPORT DATA TO REAL FINAL FILES
	if not export_DUMMY_TEST_FILE_ONLY:
		print("EXPORT DATAFRAMES INTO FILES")
		
		# if dict_MASTER_WHAT_TO_DO["master_analyseData_AAQS_DAILY"] == 1:
		if create_FINAL_FILE_AAQS_NOTHING_ELSE:
			print("EXPORT INTO AAQS MASTER FILES")
			
			# dfFinal = func_replaceAllDotsForCommaInFinalCSVForThePBI(dfFinal)
			
			if export_MASTER_CSV_FILE:
				print(chr(10) + "EXPORT masterFile_AAQS_ALL_csv to: " + masterFile_AAQS_ALL_csv)
				f_exportDataframe(
					fileExport_csv, dfFinal, masterFile_AAQS_ALL_csv, '', ','
				)
			
			if export_PBI_XLS_File:
				print(chr(10) + "EXPORT masterFile_AAQS_ALL_XLS to: " + masterFile_AAQS_ALL_XLS)
				f_exportDataframe(
					fileExport_xls, dfFinal, masterFile_AAQS_ALL_XLS, ''
				)
		
		# if dict_MASTER_WHAT_TO_DO["master_analyseData_LayUp"] == 1:
		if create_FINAL_FILE_LayUp_NOTHING_ELSE:
			
			if create_FINAL_FILE_LayUp_NOTHING_ELSE_including_averagesForPBI:
				df_powerDataFor_PBI_Curves = \
					func_createSubDataframeForPbiCurveComparisonModel(dfFinal)
				
				f_exportDataframe(
					fileExport_csv, df_powerDataFor_PBI_Curves, masterFile_LayUp_ALL_PowerDataForPBICurves, ''
				)
				
			if export_MASTER_CSV_FILE:
				f_exportDataframe(
					fileExport_csv, dfFinal, masterFile_LayUp_ALL_csv, ''
				)
				
				f_exportDataframe(
					fileExport_csv, dfSubset, masterFile_LayUp_ALL_PORT_ONLY_DATA_csv, ''
				)
				
			
			
		
		if EngineRunningHours_Step02_createFinalFileForPBI:
			if export_MASTER_CSV_FILE:
				f_exportDataframe(
					fileExport_csv, dfFinal, masterFile_EngineRunningHours_csv, ''
				)
			
	#endregion


# ######################################################################################################################
def func_createSubDataframeForPbiCurveComparisonModel(
	dfInput
):
	f_makeThePrintNiceStructured(True, "### BUILD new DF mit averaged values for PBI curve comparsion to avoid 150k datapoints overflow in PBI ", inspect.stack()[0][3])
	startTimeThisFunction = time
	startTimeThisFunction = f_doTheTimeMeasurementInThisFunction(startTimeThisFunction, flag_timeStart, inspect.stack()[0][3])
	
	dfInput[flag_finalFile_Date] = dfInput[flag_finalFile_Date].astype('datetime64[ns]')
	
	print(dfInput.head(3))
	
	dfInput = dfInput[dfInput[flag_finalFile_typeOfSailing] == flag_typeOfSailing_Port]		# dfInput[flag_finalFile_DriftingAnchorage] == flag_typeOfSailing_Port
	
	if createCompletelyNewFileWithAllHistory == 0:
		dfInput = dfInput[dfInput[flag_finalFile_Date] >= eraseAllPBIDateFromThisTimeOnwardsAndCreateNewAverages]
	 
	dfFinal = pd.DataFrame()
	dfFinal_raw = pd.DataFrame()
	
	minTimeStamp = dfInput[flag_finalFile_Date].min()
	maxTimeStamp = dfInput[flag_finalFile_Date].max()
	
	dfFinal_rawPWR = func_createEmptyDataframeWithDefinedTimeStampStructure(
		minTimeStamp,
		maxTimeStamp,
		900
	)
	
	initialIndex = dfFinal_rawPWR.index.max()
	# print("initialIndex before DF Multiply for many ships " + str(initialIndex))
	
	# amountOfDifferentShips = dfInput[flag_finalFile_Ship].nunique()
	# for thisShip in dfInput[flag_finalFile_Ship].unique():
	# 	dfFinal = pd.concat([dfFinal, dfFinal_rawPWR], ignore_index=True)
	#
	# dfFinal = dfFinal.reset_index(drop=True)
	
	# maxIndex = dfFinal.index.max()
	# print("maxIndex after DF Multiply for many ships " + str(maxIndex))
	
	dfFinal_rawPWR[flag_finalFile_TotalPowerDemand] = 0
	dfFinal_rawPWR[flag_finalFile_AvgPwrDemandOverTime] = 0
	dfFinal_rawPWR[flag_finalFile_Ship] = ""
	
	dfFinal_rawPWR[flag_finalFile_Date] = dfFinal_rawPWR[flag_finalFile_Date].astype('datetime64[ns]')
	
	# #<>
	shipCnt = -1
	for thisShip in dfInput[flag_finalFile_Ship].unique():
		shipCnt += 1
		
		dfSubset = pd.DataFrame()
		
		dfThisShip = dfFinal_rawPWR
		dfThisShip[flag_finalFile_TotalPowerDemand] = 0
		dfThisShip[flag_finalFile_AvgPwrDemandOverTime] = 0
		
		dfSubset = dfInput[dfInput[flag_finalFile_Ship] == thisShip]
		
		dfThisShip.loc[
			0 : dfThisShip.index.max(), flag_finalFile_Ship] = thisShip
		
		# print("build new column with avg pw demand for thisShip: " + thisShip)
		
		# print("lines between " +
		# 		str(shipCnt * initialIndex) + " and " +
		# 		str((shipCnt + 1) * initialIndex - 1) + " belong to " + thisShip)
		
		startTime = time
		startTime = f_doTheTimeMeasurementInThisFunction(startTime, flag_timeStart, " get averages for " + thisShip)
		
		ap = 1
		while ap >= 1 and ap < initialIndex:
			ap+=1
			
			# apFinalFile = ap + shipCnt*initialIndex
			dfThisShip.loc[ap, flag_finalFile_TotalPowerDemand] = \
				dfSubset[flag_finalFile_TotalPowerDemand][
					(dfSubset[flag_finalFile_Date] >= dfThisShip.loc[ap - 1, flag_finalFile_Date]) &
					(dfSubset[flag_finalFile_Date] < dfThisShip.loc[ap, flag_finalFile_Date]) &
					(dfSubset[flag_finalFile_dataSanity] == 1)
				].mean()
		
		# dfInput.loc[
		# 	(dfInput[flag_finalFile_Ship] == thisUniqueShip) &
		# 	(dfInput[flag_finalFile_dataSanity] == 1), newColumnNameForAverage] = \
		# 	dfInput.loc[
		# 		(dfInput[flag_finalFile_Ship] == thisUniqueShip) &
		# 		(dfInput[flag_finalFile_dataSanity] == 1)
		# 		, dataToBeAveraged].rolling(amountOfDatapoints).mean()
		startTime = f_doTheTimeMeasurementInThisFunction(startTime, flag_timeEnd, " get averages for " + thisShip)
		
		dfFinal = pd.concat([dfFinal, dfThisShip])
	
	
	dfFinal.dropna(axis=0, subset=[flag_finalFile_Ship], inplace=True)
	
	dfFinal = dfFinal.reset_index(drop=True)
		
			# dfFinal.loc[ap + shipCnt*initialIndex, flag_finalFile_AvgPwrDemandOverTime] = \
			# 	dfSubset[flag_finalFile_AvgPwrDemandOverTime][
			# 		(dfSubset[flag_finalFile_Date] >= dfFinal.loc[ap + shipCnt*initialIndex - 1, flag_finalFile_Date]) &
			# 		(dfSubset[flag_finalFile_Date] < dfFinal.loc[ap + shipCnt*initialIndex, flag_finalFile_Date])
			# 		].mean()

	for thisUniqueShip in dfFinal[flag_finalFile_Ship].unique():
		print("rolling average for ship: " + thisUniqueShip)
		#dfInput[newColumnNameForAverage] = dfInput[dataToBeAveraged].rolling(amountOfDatapoints).mean()
		dfFinal.loc[dfFinal[flag_finalFile_Ship] == thisUniqueShip, flag_finalFile_AvgPwrDemandOverTime] = \
			dfFinal.loc[
				dfFinal[flag_finalFile_Ship] == thisUniqueShip,
				flag_finalFile_TotalPowerDemand].rolling(24).mean()
		
	dfFinal[flag_finalFile_TotalPowerDemand] = dfFinal[flag_finalFile_TotalPowerDemand].round(decimals=2)
	dfFinal[flag_finalFile_AvgPwrDemandOverTime] = dfFinal[flag_finalFile_AvgPwrDemandOverTime].round(decimals=2)
	
	print(dfFinal.head(3))
	
	startTimeThisFunction = f_doTheTimeMeasurementInThisFunction(startTimeThisFunction, flag_timeEnd, inspect.stack()[0][3])
	
	return dfFinal


# ######################################################################################################################
def func_replaceAllDotsForCommaInFinalCSVForThePBI(
	dfInput
):
	
	for thisColumn in dfInput.columns:
		print("replace all dots in column " + thisColumn)
		dfInput[thisColumn] = dfInput[thisColumn].str.replace('.', ',')
	
	return dfInput

# ######################################################################################################################
def func_doTheCSVFileConversionAndStopTool():
	print("### LOAD CSV >>> SAVE AS XLSX >>> NOTHING ELSE >>> STOP TOOL")
	dfToBeConvertedIntoXLS, masterFileThisShipDoesExist = f_readExistingMasterFile()
	
	dfToBeConvertedIntoXLS = f_doSomeTypeCasts(dfToBeConvertedIntoXLS)
	
	dfToBeConvertedIntoXLS = f_resortColumnsOfFinalTotalFileWithAllNeededColumns(dfToBeConvertedIntoXLS)
	
	if dict_MASTER_WHAT_TO_DO["master_analyseData_AAQS_DAILY"] == 1:
		f_exportDataframe(
			fileExport_xls, dfToBeConvertedIntoXLS, masterFile_AAQS_ALL_XLS, ''
		)
	
	playsound('hammer_hitwall1.wav')
	
	exit()
	

# ######################################################################################################################
def func_doThePrintoutOfTimeframesAndStopTool():
	print("### PRINT MIN/MAX TIME PER SHIP IN CSV >>> NOTHING ELSE >>> STOP TOOL")
	df_existingMasterFile, masterFileThisShipDoesExist = f_readExistingMasterFile('')
	
	df_existingMasterFile[flag_NeptuneLab_Date] = df_existingMasterFile[flag_NeptuneLab_Date].astype('datetime64[ns]')
	
	for thisShip in df_existingMasterFile[flag_finalFile_Ship].unique():
		f_printMinMaxDateForThisShip(thisShip, df_existingMasterFile)
	
	playsound('hammer_hitwall1.wav')
	
	exit()


# ######################################################################################################################
def func_createIndividualShipFiles(

):
	f_makeThePrintNiceStructured(True, "### CREATE INDIVIDUAL SHIP FILES", inspect.stack()[0][3])
	startTime = time
	startTime = f_doTheTimeMeasurementInThisFunction(startTime, flag_timeStart, inspect.stack()[0][3])
	
	df_existingMasterFile, masterFileThisShipDoesExist = f_readExistingMasterFile('')
	
	if dict_PREPARE_RAW_DATA_FOR___['DATA_APPROACH_AAQS_DAILY'] == 1:
		masterFileName = masterFile_AAQS_ALL_csv.replace(str("02_AAQS_FinalFiles"), "02_AAQS_FinalFiles\SHIP_FILES")
	else:
		masterFileName = masterFile_LayUp_ALL_csv.replace(str("02_FinalFiles"), "02_FinalFiles\SHIP_FILES")
		
	for thisUniqueShip in df_existingMasterFile[flag_NeptuneLab_Ship].unique():
		print("sub file for " + thisUniqueShip)
		
		finalNewStringAtTheEndOFTheBackupFile = str('_' + thisUniqueShip + '.csv')
		
		fileName = masterFileName.replace('.csv', finalNewStringAtTheEndOFTheBackupFile)
		
		dfSubFile = df_existingMasterFile[df_existingMasterFile[flag_finalFile_Ship] == thisUniqueShip]
		
		dfSubFile.to_csv(
			fileName,
			sep=';',
			decimal='.',
			index=False)
	
	startTime = f_doTheTimeMeasurementInThisFunction(startTime, flag_timeEnd, inspect.stack()[0][3])
	
	playsound('hammer_hitwall1.wav')
	
	exit()
	
	
# ######################################################################################################################
def func_fillNanWithZeroForSomeColumns(
	dfInput
):
	f_makeThePrintNiceStructured(True, "### REMOVE NANs in FEW COLUMNs", inspect.stack()[0][3])
	startTime = time
	startTime = f_doTheTimeMeasurementInThisFunction(startTime, flag_timeStart, inspect.stack()[0][3])
	
	dfInput = func_replaceNanInThisColumn(dfInput, flag_finalFile_DG1_ACTIVE_POWER, 0)
	dfInput = func_replaceNanInThisColumn(dfInput, flag_finalFile_DG2_ACTIVE_POWER, 0)
	dfInput = func_replaceNanInThisColumn(dfInput, flag_finalFile_DG3_ACTIVE_POWER, 0)
	dfInput = func_replaceNanInThisColumn(dfInput, flag_finalFile_DG4_ACTIVE_POWER, 0)
	dfInput = func_replaceNanInThisColumn(dfInput, flag_finalFile_DG5_ACTIVE_POWER, 0)
	dfInput = func_replaceNanInThisColumn(dfInput, flag_finalFile_DG6_ACTIVE_POWER, 0)
	
	startTime = f_doTheTimeMeasurementInThisFunction(startTime, flag_timeEnd, inspect.stack()[0][3])
	
	return dfInput


##################################################################################################################
def func_oneTimeOffAddColumnWithPortNames(
):
	dfPorts = pd.DataFrame()
	
	dfFinal = func_readAllShipFilesInThisFolder(False)
	
	dfFinal = f_doTheTypeCastForThisColumn(dfFinal, flag_finalFile_Latitude)
	dfFinal = f_doTheTypeCastForThisColumn(dfFinal, flag_finalFile_Longitude)
	dfFinal = f_doTheTypeCastForThisColumn(dfFinal, "SOG")
	
	dfFinal.dropna(axis=0, subset=["SOG", flag_finalFile_Latitude], inplace=True)
	dfFinal = dfFinal.reset_index(drop=True)
	
	
	dfFinal, dfPorts = f_insertPortNames(dfFinal, dfPorts, True)
	dfFinal = f_fillGapsForLittlePortFluctuations(dfFinal)
	
	f_exportDataframe(
		fileExport_csv, dfFinal, "SHIP_WITH_PORT_NAMEs", '', ','
	)
	
	playsound('hammer_hitwall1.wav')
	
	exit()
	

##################################################################################################################
def func_filterColumnInDataframeForOneCondition(
	dfInput,
	columnToBeFiltered,
	conditionToBeMatched
):
	# print(dfInput.head())
	# print(dfInput.loc[1, flag_finalFile_TotalPowerDemand])
	
	if columnToBeFiltered in dfInput.columns:
		lenBeforeFilter = dfInput.shape[0]
		dfInput = dfInput[dfInput[columnToBeFiltered] == conditionToBeMatched]
		lenAfterFilter = dfInput.shape[0]
		print("FILTER REMOVED " + str(lenBeforeFilter - lenAfterFilter) + " rows")
	
	dfInput = dfInput.reset_index(drop=True)
	
	return dfInput


# ######################################################################################################################
def func_getAnalysisMasterFlag(
	flagForWhat
):
	currentMasterFlag = ""
	
	if flagForWhat == 0:
		if dict_MASTER_WHAT_TO_DO["master_analyseData_AAQS_DAILY"] == 1:
			currentMasterFlag = masterFlagAnalysisMode_AAQS
		
		if dict_MASTER_WHAT_TO_DO["master_analyseData_LayUp"] == 1:
			currentMasterFlag = masterFlagAnalysisMode_LayUp
	else:
		if dict_PREPARE_RAW_DATA_FOR___['DATA_APPROACH_AAQS_DAILY'] == 1:
			currentMasterFlag = masterFlagAnalysisMode_AAQS
		else:
			currentMasterFlag = masterFlagAnalysisMode_LayUp
		
	return currentMasterFlag


# ######################################################################################################################
def func_adjustMandatoryProcessStepsIfRequested(
):
	if dict_DO_ALL_MANDATORY_STEPs_FOR_NEW_DATASET[analysisType]:
		if dict_MASTER_WHAT_TO_DO["master_analyseData_AAQS_DAILY"] == 1:
				dict_mandatoryForNewData_fixDataAndFillSpeedGaps[analysisType] = 1
				dict_mandatoryForNewData_updatePortNames_LegNames_LegDates[analysisType] = 1
				dict_mandatoryForNewData_fillEnvironmentalRestrictions[analysisType] = 1
				dict_mandatoryForNewData_fillFuelTypePerEngineRunning[analysisType] = 1
				dict_mandatoryForNewData_recalculateFuelConsumption[analysisType] = 1
				dict_mandatoryForNewData_fillMissedAAQSOpportunitiesDuringPortStay[analysisType] = 1
				dict_mandatoryForNewData_fillMissedAAQSOpportunitiesDuringNavigation[analysisType] = 1
				dict_mandatoryForNewData_fillChangeOverTimesBeforeAfterArrivalInNoAAQSPorts[analysisType] = 1
				dict_mandatoryForNewData_FillReasonsForOutOfOrder[analysisType] = 1
		
		if dict_MASTER_WHAT_TO_DO["master_analyseData_LayUp"] == 1:
				dict_mandatoryForNewData_fixDataAndFillSpeedGaps[analysisType] = 1
				dict_mandatoryForNewData_updatePortNames_LegNames_LegDates[analysisType] = 1 # NOT SURE.
				dict_mandatoryForNewData_fillEnvironmentalRestrictions[analysisType] = 0 # NOT NEEDED FOR LAy UP
				dict_mandatoryForNewData_fillFuelTypePerEngineRunning[analysisType] = 1
				dict_mandatoryForNewData_recalculateFuelConsumption[analysisType] = 1
				dict_mandatoryForNewData_fillMissedAAQSOpportunitiesDuringPortStay[analysisType] = 0 # NOT NEEDED FOR LAy UP
				dict_mandatoryForNewData_fillMissedAAQSOpportunitiesDuringNavigation[analysisType] = 0 # NOT NEEDED FOR LAy UP
				dict_mandatoryForNewData_fillChangeOverTimesBeforeAfterArrivalInNoAAQSPorts[analysisType] = 0 # NOT NEEDED FOR LAy UP
				dict_mandatoryForNewData_FillReasonsForOutOfOrder[analysisType] = 0 # NOT NEEDED FOR LAy UP


# ######################################################################################################################
def f_markMissedOpportunitiesDuringNavigation(
	dfInput,
	useOnlyThisShip
):
	f_makeThePrintNiceStructured(True, "### FILL MISSED AAQS DURING NAVIGATION for " + useOnlyThisShip,
										  inspect.stack()[0][3])
	startTime = time
	startTime = f_doTheTimeMeasurementInThisFunction(startTime, flag_timeStart, inspect.stack()[0][3])
	
	if dict_ERASE_ALL_PREVIOUS_AAQS_ASSESSMENTS[analysisType] == 1:
		print("dict_ERASE_ALL_PREVIOUS_AAQS_ASSESSMENTS == TRUE >> ERASE all AAQS assessments")
		dfInput.loc[dfInput[flag_finalFile_Ship] == useOnlyThisShip, flag_finalFile_AAQS_AssessmentDone] = ''
	
	dfInput[flag_finalFile_AAQS_AssessmentDone] = dfInput[flag_finalFile_AAQS_AssessmentDone].astype(str)
	dfInput[flag_finalFile_environmentalRestriction] = dfInput[flag_finalFile_environmentalRestriction].astype(str)
	
	dfInput = f_markLatLongInsideTerritorialWaters(dfInput)
	
	scrubberAvailable = f_getAmountOfScrubberForThisShip(useOnlyThisShip)
	print("CHECK MISSED AAQS DURING NAVIGATION for: " + useOnlyThisShip + " # of AAQS: " + str(scrubberAvailable))
	
	if dict_AAQS_available[useOnlyThisShip]:
		if scrubberAvailable > 0:
			dfInput = f_loopThroughSailingTimeAndCheckForMissedScrubberUsage(dfInput, thisShip, scrubberAvailable)
	
	startTime = f_doTheTimeMeasurementInThisFunction(startTime, flag_timeEnd, inspect.stack()[0][3])
	
	return dfInput


# ######################################################################################################################
def f_loopThroughSailingTimeAndCheckForMissedScrubberUsage(
	dfInput,
	thisShip,
	scrubberAvailable
):
	area_malaysia = path.Path(np.array(npa_territorialWaters_Lat_Long_Malaysia))
	area_bohaiRim = path.Path(np.array(npa_territorialWaters_Lat_Long_BohaiRim))
	area_ChinaMain = path.Path(np.array(npa_territorialWaters_Lat_Long_ChinaMainCountry))
	area_SuezChannel = path.Path(np.array(npa_territorialWaters_Lat_Long_Suez))
	area_GermanyNorthSea = path.Path(np.array(npa_territorialWaters_Lat_Long_Germany_NorthSea))
	area_CI_GranCanaria = path.Path(np.array(npa_territorialWaters_Lat_Long_Gran_Canaria))
	area_CI_Tenerife_LaGomera = path.Path(np.array(npa_territorialWaters_Lat_Long_Tenerife_La_Gomera))
	area_CI_La_Palma = path.Path(np.array(npa_territorialWaters_Lat_Long_La_Palma))
	area_CI_Fuerte_Lanzarote = path.Path(np.array(npa_territorialWaters_Lat_Long_Fuerte_Lanzarote))
	
	for ap in dfInput.index:
		if dfInput.loc[ap, flag_finalFile_Ship] == 'Costa Fascinosa':
			continue
		
		if dfInput.loc[ap, flag_finalFile_SOG] <= 0.1:
			continue
		
		if dfInput.loc[ap, flag_finalFile_environmentalRestriction] == flag_ENV_Restriction_AAQS_NOT_allowedInThisPort:
			continue
		
		if dict_ERASE_ALL_PREVIOUS_AAQS_ASSESSMENTS[analysisType] == 0:
			if len(dfInput.loc[ap, flag_finalFile_AAQS_AssessmentDone]) > 3:
				continue
		
		scrubberEnginesRunningUsing_HFO, \
		scrubberEnginesRunningUsing_MGO, \
		nonScrubberEnginesRunningUsing_HFO, \
		nonScrubberEnginesRunningUsing_MGO, \
		totalEnginesRunning = \
			f_getAmountOfEnginesRunningWithAndWithoutAAQS(ap, dfInput, thisShip)
		
		# region MALAYSIA: SHIP is sailing inside special area with NO AAQS allowance
		if area_malaysia.contains_points(
			[(dfInput.loc[ap, flag_finalFile_Latitude], dfInput.loc[ap, flag_finalFile_Longitude])]):
			dfInput.loc[ap, flag_finalFile_AAQS_AssessmentDone] = flag_AAQS_Usage_NotAllowedInThisParticularRegion
			dfInput = f_markFuelTypeInCaseOfSailingInsideNonAAQSRegion(thisShip, dfInput, ap)
			continue
		# endregion
		
		# region BOHAI RIM: SHIP is sailing inside special area with NO AAQS allowance
		if area_bohaiRim.contains_points(
			[(dfInput.loc[ap, flag_finalFile_Latitude], dfInput.loc[ap, flag_finalFile_Longitude])]):
			dfInput.loc[ap, flag_finalFile_AAQS_AssessmentDone] = flag_AAQS_Usage_NotAllowedInThisParticularRegion
			dfInput = f_markFuelTypeInCaseOfSailingInsideNonAAQSRegion(thisShip, dfInput, ap)
			continue
		# endregion
		
		# region CHINA MAIN: SHIP is sailing inside special area with NO AAQS allowance
		if area_ChinaMain.contains_points(
			[(dfInput.loc[ap, flag_finalFile_Latitude], dfInput.loc[ap, flag_finalFile_Longitude])]):
			dfInput.loc[ap, flag_finalFile_AAQS_AssessmentDone] = flag_AAQS_Usage_NotAllowedInThisParticularRegion
			dfInput = f_markFuelTypeInCaseOfSailingInsideNonAAQSRegion(thisShip, dfInput, ap)
			continue
		# endregion
		
		# region BOHAI RIM: SHIP is sailing inside special area with NO AAQS allowance
		if area_SuezChannel.contains_points(
			[(dfInput.loc[ap, flag_finalFile_Latitude], dfInput.loc[ap, flag_finalFile_Longitude])]):
			dfInput.loc[ap, flag_finalFile_AAQS_AssessmentDone] = flag_AAQS_Usage_NotAllowedInThisParticularRegion
			dfInput = f_markFuelTypeInCaseOfSailingInsideNonAAQSRegion(thisShip, dfInput, ap)
			continue
		# endregion
		
		# region GERMANY NORTH SEA: SHIP is sailing inside special area with NO AAQS allowance
		if area_GermanyNorthSea.contains_points(
			[(dfInput.loc[ap, flag_finalFile_Latitude], dfInput.loc[ap, flag_finalFile_Longitude])]):
			dfInput.loc[ap, flag_finalFile_AAQS_AssessmentDone] = flag_AAQS_Usage_NotAllowedInThisParticularRegion
			dfInput = f_markFuelTypeInCaseOfSailingInsideNonAAQSRegion(thisShip, dfInput, ap)
			continue
		# endregion
		
		# region AAQS BAN Canary Islands after this date
		if dfInput.loc[ap, flag_finalFile_Date] >= aaqsBanCanaryIslands:
			# region Canary Islands - Gran Canaria: SHIP is sailing inside special area with NO AAQS allowance
			if area_CI_GranCanaria.contains_points(
				[(dfInput.loc[ap, flag_finalFile_Latitude], dfInput.loc[ap, flag_finalFile_Longitude])]):
				dfInput.loc[ap, flag_finalFile_AAQS_AssessmentDone] = flag_AAQS_Usage_NotAllowedInThisParticularRegion
				dfInput = f_markFuelTypeInCaseOfSailingInsideNonAAQSRegion(thisShip, dfInput, ap)
				continue
			# endregion
			
			# region Canary Islands - Tenerife & La Gomera: SHIP is sailing inside special area with NO AAQS allowance
			if area_CI_Tenerife_LaGomera.contains_points(
				[(dfInput.loc[ap, flag_finalFile_Latitude], dfInput.loc[ap, flag_finalFile_Longitude])]):
				dfInput.loc[ap, flag_finalFile_AAQS_AssessmentDone] = flag_AAQS_Usage_NotAllowedInThisParticularRegion
				dfInput = f_markFuelTypeInCaseOfSailingInsideNonAAQSRegion(thisShip, dfInput, ap)
				continue
			# endregion
			
			# region Canary Islands - La Palma: SHIP is sailing inside special area with NO AAQS allowance
			if area_CI_La_Palma.contains_points(
				[(dfInput.loc[ap, flag_finalFile_Latitude], dfInput.loc[ap, flag_finalFile_Longitude])]):
				dfInput.loc[ap, flag_finalFile_AAQS_AssessmentDone] = flag_AAQS_Usage_NotAllowedInThisParticularRegion
				dfInput = f_markFuelTypeInCaseOfSailingInsideNonAAQSRegion(thisShip, dfInput, ap)
				continue
			# endregion
			
			# region Canary Islands - Fuerte and Lanzarote: SHIP is sailing inside special area with NO AAQS allowance
			if area_CI_Fuerte_Lanzarote.contains_points(
				[(dfInput.loc[ap, flag_finalFile_Latitude], dfInput.loc[ap, flag_finalFile_Longitude])]):
				dfInput.loc[ap, flag_finalFile_AAQS_AssessmentDone] = flag_AAQS_Usage_NotAllowedInThisParticularRegion
				dfInput = f_markFuelTypeInCaseOfSailingInsideNonAAQSRegion(thisShip, dfInput, ap)
				continue
		# endregion
		# endregion
		
		# region PERFECT AAQS RUN
		perfectRun, dfInput = func_PERFECT_AAQS_run(
			dfInput, ap, totalEnginesRunning,
			scrubberAvailable,
			scrubberEnginesRunningUsing_HFO
		)
		if perfectRun:
			continue
		# endregion
		
		# region AAQS DESASTER
		if scrubberEnginesRunningUsing_HFO == 0:
			# print("AAQS FULL DESASTER scrubberEnginesMissed: " + str(scrubberEnginesMissed))
			
			dfInput.loc[ap, flag_finalFile_AAQS_AssessmentDone] = flag_AAQS_Usage_Assessment_Desaster
			
			scrubberEnginesMissed = f_getAmountOfMissingScrubberEngines(
				scrubberEnginesRunningUsing_HFO,
				totalEnginesRunning,
				scrubberAvailable)
			
			dfInput = f_findNextBestAvailableAAQSEngine(
				thisShip, dfInput, ap, scrubberEnginesMissed)
			
			continue
		# endregion
		
		# region AAQS USAGE POTENTIAL LEFT
		if \
			scrubberEnginesRunningUsing_HFO > 0 and \
				scrubberEnginesRunningUsing_HFO < scrubberAvailable and \
				totalEnginesRunning > scrubberEnginesRunningUsing_HFO:
			dfInput.loc[ap, flag_finalFile_AAQS_AssessmentDone] = flag_AAQS_Usage_Assessment_semi_PERFECT
			
			scrubberEnginesMissed = f_getAmountOfMissingScrubberEngines(
				scrubberEnginesRunningUsing_HFO,
				totalEnginesRunning,
				scrubberAvailable)
			
			dfInput = f_findNextBestAvailableAAQSEngine(
				thisShip, dfInput, ap, scrubberEnginesMissed)
			
			continue
		# endregion
		
		dfInput.loc[ap, flag_finalFile_AAQS_AssessmentDone] = "WHAT IS LEFT"
	
	return dfInput


# ######################################################################################################################
def func_PERFECT_AAQS_run(
	dfInput,
	ap,
	totalEnginesRunning,
	scrubberAvailable,
	scrubberEnginesRunningUsing_HFO
):
	# PERFECT >> all AAQS are up and running, no possibility to improve BUT: we could check engine load to find further improvement
	if scrubberEnginesRunningUsing_HFO == scrubberAvailable or \
		scrubberEnginesRunningUsing_HFO == totalEnginesRunning:
		dfInput.loc[ap, flag_finalFile_AAQS_AssessmentDone] = flag_AAQS_Usage_Assessment_PERFECT
		return True, dfInput
	
	return False, dfInput


# ######################################################################################################################
def f_getAmountOfMissingScrubberEngines(
	scrubberEnginesRunningUsing_HFO,
	totalEnginesRunning,
	scrubberAvailable
):
	scrubberEnginesMissed = 0
	
	if totalEnginesRunning <= scrubberAvailable:
		scrubberEnginesMissed = totalEnginesRunning - scrubberEnginesRunningUsing_HFO
	
	if totalEnginesRunning > scrubberAvailable:
		scrubberEnginesMissed = scrubberAvailable - scrubberEnginesRunningUsing_HFO
	
	return scrubberEnginesMissed


# ######################################################################################################################
def f_findNextBestAvailableAAQSEngine(
	thisShip,
	dfInput,
	ap,
	scrubberEnginesMissed
):
	engineUsage = f_getEngineUsageForThisSlice(dfInput, ap, flag_engineDate_fuelType)
	
	# engineUsage = [
	# 	dfInput.loc[ap, flag_finalFile_fuelType_DG01],
	# 	dfInput.loc[ap, flag_finalFile_fuelType_DG02],
	# 	dfInput.loc[ap, flag_finalFile_fuelType_DG03],
	# 	dfInput.loc[ap, flag_finalFile_fuelType_DG04],
	# 	dfInput.loc[ap, flag_finalFile_fuelType_DG05],
	# 	dfInput.loc[ap, flag_finalFile_fuelType_DG06]
	# ]
	
	thisEngine = 0
	missedScrubberEnginesFilledUp = 0
	while thisEngine < 6:
		if \
			dict_AAQS_engines[thisShip][thisEngine] == 1 and \
				(engineUsage[thisEngine] == fuel_flag_HFO_NOAAQS or engineUsage[thisEngine] == fuel_flag_MGO):
			missedScrubberEnginesFilledUp += 1
			dfInput.loc[ap, switch_getDataframeFlagThisEngine(thisEngine + 1)] = fuel_flag_AAQS_Missed_NAVIGATION
		
		if missedScrubberEnginesFilledUp == scrubberEnginesMissed:
			break
		
		if dict_AAQS_engines[thisShip][thisEngine] < 0:
			break
		
		thisEngine += 1
	
	# this case is needed for the case that we have for example 3 AAQS engines, but only one has been running.
	# in this case the first loop will mark the AAQS engine if she has been used with MGO and the next loop will
	# mark the non AAQS engines as missed opportunity since we have more AAQs engines
	if missedScrubberEnginesFilledUp < scrubberEnginesMissed:
		thisEngine = 0
		while thisEngine < 6:
			if \
				dict_AAQS_engines[thisShip][thisEngine] == 0 and \
					engineUsage[thisEngine] == fuel_flag_MGO:
				# print("FILL fuel flag missed for engine " + str(thisEngine))
				# print("corresponding column " + str(switch_getDataframeFlagThisEngine(thisEngine+1)))
				missedScrubberEnginesFilledUp += 1
				dfInput.loc[ap, switch_getDataframeFlagThisEngine(thisEngine + 1)] = fuel_flag_AAQS_Missed_NAVIGATION
			
			if missedScrubberEnginesFilledUp == scrubberEnginesMissed:
				break
			
			if dict_AAQS_engines[thisShip][thisEngine] < 0:
				break
			
			thisEngine += 1
	
	return dfInput


# ######################################################################################################################
def f_getAmountOfEnginesRunningWithAndWithoutAAQS(
	ap,
	dfInput,
	thisShip
):
	engineUsage = f_getEngineUsageForThisSlice(dfInput, ap, flag_engineDate_fuelType)
	
	scrubberEnginesRunningUsing_HFO = 0
	scrubberEnginesRunningUsing_MGO = 0
	nonScrubberEnginesRunningUsing_HFO = 0
	nonScrubberEnginesRunningUsing_MGO = 0
	
	totalEnginesRunning = 0
	thisEngine = 0
	while thisEngine < 6:
		
		if dict_AAQS_engines[thisShip][thisEngine] == 1:
			if engineUsage[thisEngine] == fuel_flag_HFO:
				scrubberEnginesRunningUsing_HFO += 1
			
			if engineUsage[thisEngine] == fuel_flag_MGO:
				scrubberEnginesRunningUsing_MGO += 1
		
		if dict_AAQS_engines[thisShip][thisEngine] == 0:
			if engineUsage[thisEngine] == fuel_flag_HFO_NOAAQS:
				nonScrubberEnginesRunningUsing_MGO += 1
			
			if engineUsage[thisEngine] == fuel_flag_MGO:
				nonScrubberEnginesRunningUsing_MGO += 1
		
		if dict_AAQS_engines[thisShip][thisEngine] < 0:
			break
		
		thisEngine += 1
	
	totalEnginesRunning = \
		scrubberEnginesRunningUsing_HFO + \
		scrubberEnginesRunningUsing_MGO + \
		nonScrubberEnginesRunningUsing_HFO + \
		nonScrubberEnginesRunningUsing_MGO
	
	return \
		scrubberEnginesRunningUsing_HFO, \
		scrubberEnginesRunningUsing_MGO, \
		nonScrubberEnginesRunningUsing_HFO, \
		nonScrubberEnginesRunningUsing_MGO, \
		totalEnginesRunning


# ######################################################################################################################
def func_eraseDataInEachSingleShipFile():
	if ERASE_ALL_DATA_AFTER_CERTAIN_DATE_InEachShipFile_LayUpPBI:
		filesToBeTreated = filedialog.askopenfilenames(
			initialdir="C:\\Users\\500095\\Desktop\\Lay Up Energy Monitoring\\02_FinalFiles\\SHIP_FILES")
	 # ERASE_ALL_DATA_AFTER_CERTAIN_DATE_InEachShipFile_AAQS_PBI
	else:
		filesToBeTreated = filedialog.askopenfilenames(
			initialdir="C:\\Users\\500095\\Desktop\\AAQS_FullTransparency\\Python_Code\\02_AAQS_FinalFiles\\SHIP_FILES")
	
	# erase_allDataIncludingThisDay = datetime.datetime(2020, 11, 17, 0, 0, 0)
	
	# >
	# region LOOP Files and filter out everything after above mentioned date and save it again
	for subFile in filesToBeTreated:
		print("\n############################################")
		print("read file: " + subFile)
		
		df_thisShip = pd.read_csv(subFile, sep=';', low_memory=False)
		
		df_thisShip[flag_finalFile_Date] = pd.to_datetime(df_thisShip[flag_finalFile_Date])
		
		print("LEN FILE BEFORE DATE CUT " + str(len(df_thisShip[flag_finalFile_Date])))
		
		df_thisShip = df_thisShip[df_thisShip[flag_finalFile_Date] < erase_allDataIncludingThisDay]
		
		print("LEN FILE AFTER DATE CUT " + str(len(df_thisShip[flag_finalFile_Date])))
		
		df_thisShip.to_csv(
			subFile,
			sep=';',
			decimal=',',
			index=False)
		
		print("file saved again same folder same name, less data ... " + subFile)
	# endregion
	
	print("ALL FILES are updated")
	
	playsound('hammer_hitwall1.wav')


# ######################################################################################################################
def func_doThePBIDataFileMerging():
	# masterFile_LayUp_ALL_PowerDataForPBICurves = r'C:\Users\500095\Desktop\Lay Up Energy Monitoring\02_FinalFiles\PBI_LayUpFinalFile_PORT_ONLY_PowerOnlyPBICurve.csv'
	# OLD_masterFile_LayUp_ALL_PowerDataForPBICurves = r'C:\Users\500095\Desktop\Lay Up Energy Monitoring\02_FinalFiles\BA_PBI_LayUpFinalFile_PORT_ONLY_PowerOnlyPBICurve.csv'
	
	df_existingMasterFile = pd.read_csv(OLD_masterFile_LayUp_ALL_PowerDataForPBICurves, sep=';', low_memory=False)
	df_newMasterFile = pd.read_csv(masterFile_LayUp_ALL_PowerDataForPBICurves, sep=';', low_memory=False)
	
	df_existingMasterFile[flag_finalFile_Date] = pd.to_datetime(df_existingMasterFile[flag_finalFile_Date])
	df_newMasterFile[flag_finalFile_Date] = pd.to_datetime(df_newMasterFile[flag_finalFile_Date])
	
	# the existing data is used for everything before the date where we restart the avg pwr demand calculation
	df_existingMasterFile = df_existingMasterFile[eraseAllPBIDateFromThisTimeOnwardsAndCreateNewAverages >= df_existingMasterFile[flag_finalFile_Date]]
	
	dfAllTogether = pd.concat([df_existingMasterFile, df_newMasterFile])

	dfAllTogether = dfAllTogether.sort_values(
		[flag_finalFile_Ship, flag_finalFile_Date],
		ascending=[True, True])

	dfAllTogether = dfAllTogether.reset_index(drop=True)
	
	dfAllTogether.to_csv(
		NEW_masterFile_LayUp_ALL_PowerDataForPBICurves,
		sep=';',
		decimal=',',
		index=False)
	
	playsound('hammer_hitwall1.wav')
	
	exit()
	

# ######################################################################################################################
# ######################################################################################################################
# ######################################################################################################################



print("### START ANALYSIS ###")
# _DAILY_AAQS_Variables.init()

dfPorts = pd.DataFrame()

# print('thisShipLongName: ' + thisShipLongName)

# for thisShip in dict_analyseTheseShips:
# 	print("thisShip " + thisShip + " dict_analyseTheseShips " + str(dict_analyseTheseShips[thisShip]))

if load_csv_save_final_xlx_do_NOTHING_Else:
	func_doTheCSVFileConversionAndStopTool()

if addColumnWithPortName_NOTHING_ELSE:
	func_oneTimeOffAddColumnWithPortNames()

if printMinMaxDateValuePerShip_NOTHING_ELSE:
	func_doThePrintoutOfTimeframesAndStopTool()
	
if extractShipFiles_NOTHING_ELSE:
	func_createIndividualShipFiles()


if \
	create_FINAL_FILE_LayUp_NOTHING_ELSE or \
	create_FINAL_FILE_AAQS_NOTHING_ELSE or \
	EngineRunningHours_Step02_createFinalFileForPBI:
	
	func_createFinalFileBasedOnSubFiles()


if create_FINAL_FILE_ShipFeedback:
	func_createFeedbackFileBasedOnSingleShips()

analysisType = func_getAnalysisMasterFlag(1)

if (
		dict_MASTER_WHAT_TO_DO["master_analyseData_AAQS_DAILY"] == 1 or \
		dict_MASTER_WHAT_TO_DO["master_analyseData_LayUp"] == 1
	):
	func_adjustMandatoryProcessStepsIfRequested()

if (
	ERASE_ALL_DATA_AFTER_CERTAIN_DATE_InEachShipFile_LayUpPBI or \
	ERASE_ALL_DATA_AFTER_CERTAIN_DATE_InEachShipFile_AAQS_PBI):
	
	func_eraseDataInEachSingleShipFile()
	
	exit()

if ONLY_THIS_MergeTheseFilesTogetherToSaveTime:
	func_doThePBIDataFileMerging()


#region FINAL DATA ANALYSIS
if \
	(
		dict_MASTER_WHAT_TO_DO["master_analyseData_AAQS_DAILY"] == 1 or \
		dict_MASTER_WHAT_TO_DO["master_analyseData_LayUp"] == 1 or \
		EngineRunningHours_Step01_createShipByShipFileWithActuals
	) \
	and \
	( \
			dict_checkAndFillIfNeeded_timeStampsPerHour[analysisType] == 1 or \
			dict_mandatoryForNewData_recalculateFuelConsumption[analysisType] == 1 or \
			dict_recalculateTotalConsumptionPerFuelType[analysisType] == 1 or \
			dict_mandatoryForNewData_fixDataAndFillSpeedGaps[analysisType] == 1 or \
			dict_mandatoryForNewData_updatePortNames_LegNames_LegDates[analysisType] == 1 or \
			dict_mandatoryForNewData_fillEnvironmentalRestrictions[analysisType] == 1 or \
			dict_mandatoryForNewData_fillFuelTypePerEngineRunning[analysisType] == 1 or \
			dict_fillMissingRedFlagsForWrongFuel[analysisType] == 1 or \
			dict_mandatoryForNewData_fillMissedAAQSOpportunitiesDuringPortStay[analysisType] == 1 or \
			dict_mandatoryForNewData_fillMissedAAQSOpportunitiesDuringNavigation[analysisType] == 1 or \
			dict_mandatoryForNewData_fillChangeOverTimesBeforeAfterArrivalInNoAAQSPorts[analysisType] == 1 or \
			dict_mandatoryForNewData_FillReasonsForOutOfOrder[analysisType] == 1
	):
	
	startTime = time
	startTime = f_doTheTimeMeasurementInThisFunction(startTime, flag_timeStart, inspect.stack()[0][3])
	
	dfSubset = pd.DataFrame()
	
	if dict_mandatoryForNewData_FillReasonsForOutOfOrder[analysisType] == 1:
		xlsFile_ScrubberIssues_AIDA = f_readScrubberIssuesMasterFile(flag_brand_AIDA)
		xlsFile_ScrubberIssues_Costa = f_readScrubberIssuesMasterFile(flag_brand_Costa)
	
	if EngineRunningHours_Step01_createShipByShipFileWithActuals:
		df_rhPrediction = func_EngineRunningHours_ReadRunningHourPrediction()
		
	# region loop through data ship by ship
	for thisShip in dict_analyseTheseShips:
		if dict_analyseTheseShips[thisShip] == 1:
			useOnlyThisShip = thisShip
			
			if \
				EngineRunningHours_Step01_createShipByShipFileWithActuals:
				
				if useOnlyThisShip not in dict_ShipsToPlanEngineRunningHours:
					continue
				else:
					if dict_ShipsToPlanEngineRunningHours[useOnlyThisShip] == 0:
						continue
			
			if len(useOnlyThisShip) > 0:
				print(chr(10) + "###############################################")
				print("### NEXT SHIP #################### " + useOnlyThisShip)
			
			dfFinal, masterFileThisShipDoesExist = f_readExistingMasterFile(useOnlyThisShip)
			
			if dict_PREPARE_RAW_DATA_FOR___['DATA_APPROACH_AAQS_DAILY'] == 1:
				if not masterFileThisShipDoesExist:
					print("AAQS AAPROACH >> SHIP DOES NOT EXIST >> NEXT SHIP")
					continue
			
			if not EngineRunningHours_Step01_createShipByShipFileWithActuals:
				f_createCopyOfExistingMasterFileBeforeChangingIt(dfFinal, fileCopyBeforeSmartAlgo, useOnlyThisShip)
			
			dfFinal = f_doSomeTypeCasts(dfFinal)
			
			dfFinal = f_sortThisDataframeByShipnameAndDate(dfFinal, flag_finalFile_Ship, flag_finalFile_Date)
			
			dfLenBefore = dfFinal.shape[0]
			dfFinal.dropna(axis=0, subset=[flag_finalFile_SOG, flag_finalFile_Latitude], inplace=True)
			dfLenAfter = dfFinal.shape[0]
			
			print("LINES WO SOG and WO LAT DROPPED " + str(dfLenBefore - dfLenAfter))
			
			dfFinal = dfFinal.reset_index(drop=True)
			
			dfFinal = func_fillNanWithZeroForSomeColumns(dfFinal)
			
			doTheAnalysisForOneShipOnly = f_analyseDataForOneShipOnly()
			
			#region Engine Running Hours Actual & Prediction
			if EngineRunningHours_Step01_createShipByShipFileWithActuals:
				if useOnlyThisShip in dict_ShipsToPlanEngineRunningHours:
					dfActualRunningHourData = func_EngineRunningHours_createShipByShipEngineRunningHourFile(dfFinal)
					
					dfActualRunningHourData = func_EngineRunningHours_getValuesAggregatedDayByDay(
						dfActualRunningHourData, useOnlyThisShip)
					
					dfActualRunningHourData = func_EngineRunningHours_createCumulatedActualSinceLastInfoshipUpdate(
						dfActualRunningHourData)
					
					thisRunningHourVersion = 1
					while thisRunningHourVersion <= EngineRunningHours_Alternate_rhPrediction_Versions:
						df_rhPrediction = func_EngineRunnings_createRunningHourPrediction(
							df_rhPrediction, useOnlyThisShip, thisRunningHourVersion)
						
						dfFinal = func_EngineRunningHours_combineActualAndPredictionInJustOnFile(
							dfActualRunningHourData, df_rhPrediction, useOnlyThisShip)

						dfFinal = func_EngineRunningHours_createCumulatedPredictionSinceLastInfoshipUpdate(dfFinal)

						dfFinal = func_updateAllFiguresWithLastActual(dfFinal, useOnlyThisShip)

						dfFinal = f_resortColumnsOfFinalTotalFileWithAllNeededColumns(dfFinal)

						f_exportDataframe(
							fileExport_csv, dfFinal, masterFile_EngineRunningHours_csv,
							useOnlyThisShip, ".", thisRunningHourVersion)

						thisRunningHourVersion += 1
					# exit()
					
				continue
			#region fillMissingTimeStampsPerHour
			if dict_checkAndFillIfNeeded_timeStampsPerHour[analysisType] == 1:
				dfFinal = f_addTimeStampsPerHour(dfFinal, doTheAnalysisForOneShipOnly)
			#endregion
			
			# region check for Anchorage / Drifting
			if dict_addAnchorage_Drifting_Column[analysisType] == 1:
				dfFinal = func_analyseAnchorageDrifting(dfFinal, analysisType)
			# endregion
			
			# region addTotalPowerDemand
			if dict_addTotalPowerDemand[analysisType] == 1:
				dfFinal = func_addTotalPowerDemand(dfFinal)
				dfFinal = func_addAvgEngineLoad(dfFinal)
			# endregion
			
			#region recalculateFuelConsumption
			if dict_mandatoryForNewData_recalculateFuelConsumption[analysisType] == 1:
				dfFinal = f_addFuelConsumptionToDF(dfFinal, useOnlyThisShip, True)
			#endregion
			
			#region total consumption per fuel type
			if dict_recalculateTotalConsumptionPerFuelType[analysisType] == 1 or \
				dict_mandatoryForNewData_recalculateFuelConsumption[analysisType] == 1:
				dfFinal = func_addTotalFuelConsumptionPerFuelType(dfFinal, useOnlyThisShip, "HFO")
				dfFinal = func_addTotalFuelConsumptionPerFuelType(dfFinal, useOnlyThisShip, "MGO")
				dfFinal = func_addTotalFuelConsumptionPerFuelType(dfFinal, useOnlyThisShip, "LNG")
			#endregion
			
			#region fixDataAndFillSpeedGaps
			if dict_mandatoryForNewData_fixDataAndFillSpeedGaps[analysisType]:
				dfFinal = f_fillRandomSpeedGaps(dfFinal, doTheAnalysisForOneShipOnly)
			#endregion
			
			#region updatePortNames_LegNames_LegDates
			if dict_mandatoryForNewData_updatePortNames_LegNames_LegDates[analysisType]:
				dfFinal = f_eraseExistingPortName_LegNames_LegDates(dfFinal)
				
				dfFinal = f_addSailingMode(dfFinal)
				dfFinal = func_reloopAllLinesAndCorrectLittleSpeedFluctuations(dfFinal)
				
				dfFinal, dfPorts = f_insertPortNames(dfFinal, dfPorts, False)
				dfFinal = f_fillGapsForLittlePortFluctuations(dfFinal)
				
				# if dict_PREPARE_RAW_DATA_FOR___['DATA_APPROACH_AAQS_DAILY'] == 1:
				dfFinal = f_insertLegNames(dfFinal)
				
				if dict_PREPARE_RAW_DATA_FOR___['DATA_APPROACH_AAQS_DAILY'] == 1:
					dfFinal = f_insertMissingStartDates(dfFinal, doTheAnalysisForOneShipOnly)
			#endregion
			
			#region fillEnvironmentalRestrictions
			if dict_mandatoryForNewData_fillEnvironmentalRestrictions[analysisType] == 1:
				dfFinal = f_checkForEnvironmentalRestrictionInPort(dfFinal)
			#endregion
			
			#region fillFuelTypePerEngineRunning
			if \
				dict_mandatoryForNewData_fillFuelTypePerEngineRunning[analysisType] == 1 or \
				dict_ERASE_ALL_PREVIOUS_AAQS_PORT_ASSESSMENTS[analysisType] == 1 or \
				dict_ERASE_ALL_PREVIOUS_AAQS_ASSESSMENTS[analysisType] == 1:
				
				dfFinal = f_getFuelTypePerEnginePerTimeslice(dfFinal, useOnlyThisShip)
			#endregion
			
			# region update Sea State
			# from Sailing to Port for all Anchorage situation and
			# from Port to Sailing for all Drifting situation
			if dict_addAnchorage_Drifting_Column[analysisType] == 1:
				dfFinal = func_updateSeaStateDependingOfAdvancedAnchorageAlgo(dfFinal, analysisType)
			# endregion
			
			#region fillMissingRedFlagsForWrongFuel
			if dict_MASTER_WHAT_TO_DO["master_analyseData_AAQS_DAILY"] == 1:
				if dict_fillMissingRedFlagsForWrongFuel[analysisType] == 1 or \
					(
						dict_mandatoryForNewData_fillFuelTypePerEngineRunning[analysisType] == 1 and
						dict_ERASE_ALL_PREVIOUS_FuelTypePerEngines[analysisType] == 1
					):
					dfFinal = f_insertWarningsForWrongFuel(dfFinal)
			#endregion
			
			#region fillMissedAAQSOpportunitiesDuringPortStay
			if dict_MASTER_WHAT_TO_DO["master_analyseData_AAQS_DAILY"] == 1:
				if \
					dict_mandatoryForNewData_fillMissedAAQSOpportunitiesDuringPortStay[analysisType] == 1 or \
					dict_ERASE_ALL_PREVIOUS_AAQS_PORT_ASSESSMENTS[analysisType] == 1 or \
					(
						dict_mandatoryForNewData_fillFuelTypePerEngineRunning[analysisType] == 1 and
						dict_ERASE_ALL_PREVIOUS_FuelTypePerEngines[analysisType] == 1
					):
					dfFinal = f_markMissedOpportunitiesDuringPortStay(dfFinal, useOnlyThisShip)
			#endregion
			
			#region fillMissedAAQSOpportunitiesDuringNavigation
			if dict_MASTER_WHAT_TO_DO["master_analyseData_AAQS_DAILY"] == 1:
				if \
					dict_mandatoryForNewData_fillMissedAAQSOpportunitiesDuringNavigation[analysisType] == 1 or \
						dict_ERASE_ALL_PREVIOUS_AAQS_ASSESSMENTS or \
					(
						dict_mandatoryForNewData_fillFuelTypePerEngineRunning[analysisType] == 1 and
						dict_ERASE_ALL_PREVIOUS_FuelTypePerEngines[analysisType] == 1
					):
					dfFinal = f_markMissedOpportunitiesDuringNavigation(dfFinal, useOnlyThisShip)
			#endregion
			
			#region fillChangeOverTimesBeforeAfterArrival
			if dict_MASTER_WHAT_TO_DO["master_analyseData_AAQS_DAILY"] == 1:
				if dict_mandatoryForNewData_fillChangeOverTimesBeforeAfterArrivalInNoAAQSPorts[analysisType] == 1 or \
					(
						dict_mandatoryForNewData_fillFuelTypePerEngineRunning[analysisType] == 1 and
						dict_ERASE_ALL_PREVIOUS_FuelTypePerEngines[analysisType] == 1
					):
					dfFinal = f_markChangeOverTimesBeforeArrival(dfFinal, doTheAnalysisForOneShipOnly)
					dfFinal = f_markChangeOverTimesAfterDeparture(dfFinal, doTheAnalysisForOneShipOnly)
			#endregion
			
			#region FillReasonsForOutOfOrder
			if dict_mandatoryForNewData_FillReasonsForOutOfOrder[analysisType] == 1:
				if \
					useOnlyThisShip != "AIDAaura" and \
					useOnlyThisShip != "AIDAcara" and \
					useOnlyThisShip != "AIDAstella" and \
					useOnlyThisShip != "AIDAnova" and \
					useOnlyThisShip != "Costa Smeralda":
					
					aaqsIssueFile = f_getCorrectIssueFileForThatShip(
						useOnlyThisShip,
						xlsFile_ScrubberIssues_AIDA,
						xlsFile_ScrubberIssues_Costa
					)
					
					if dict_ERASE_ALL_PREVIOUS_OutOfOrderAssessments[analysisType] == 1:
						dfFinal = f_erasePreviousOutOfOrderAssessments(dfFinal)
					
					dfFinal = fillReasonsForAAQSOutOfOrder(dfFinal, aaqsIssueFile)
			#endregion
			
			#region DATA SANITY CHECK FOR Lay-Up while in port ... for AAQS need to add the new column
			if dict_addTotalPowerDemand[analysisType] == 1:
				# region this can not be done before the state of sailing is clear
				dfFinal = func_doTheDataSanityCheckForTotalPowerDemand(dfFinal)
			#endregion
			
			dfFinal = f_resortColumnsOfFinalTotalFileWithAllNeededColumns(dfFinal)
			
			#region export final file for this ship
			if dict_PREPARE_RAW_DATA_FOR___['DATA_APPROACH_AAQS_DAILY'] == 1:
				f_exportDataframe(fileExport_csv, dfFinal, masterFile_AAQS_ALL_csv, useOnlyThisShip)
			else:
				f_exportDataframe(fileExport_csv, dfFinal, masterFile_LayUp_ALL_csv, useOnlyThisShip)
			#endregion
	
	# endregion
	
	playsound('hammer_hitwall1.wav')
	
	startTime = f_doTheTimeMeasurementInThisFunction(startTime, flag_timeEnd, inspect.stack()[0][3])
#endregion
#endregion

# PREPARE RAW DATA #####################################################################################################
#region PREPARE RAW DATA
if dict_MASTER_WHAT_TO_DO["master_prepareRawData"] == 1:
	f_makeThePrintNiceStructured(True, "### FILL START DATES ", inspect.stack()[0][3])
	startTime = time
	startTime = f_doTheTimeMeasurementInThisFunction(startTime, flag_timeStart, inspect.stack()[0][3])
	
	analysisType = func_getAnalysisMasterFlag(2)
	
	doTheAnalysisForOneShipOnly = False
	
	dfSourceData = f_loopAllFilesInThisFolderAndCreateNewSumFile()
	
	#region loop through dataframe and work on data ship by ship
	for thisUniqueShip in dfSourceData[flag_NeptuneLab_Ship].unique():
		
		# if thisUniqueShip != "A-BE":
		# 	continue
		
		# if thisUniqueShip != "C-ME":
		# 	continue
		
		print("thisUniqueShip: " + thisUniqueShip)
		
		if dict_PREPARE_RAW_DATA_FOR___['DATA_APPROACH_AAQS_DAILY'] == 1:
			thisShipLongName = dict_shipShortCodesToLongNames[thisUniqueShip]
		else:
			if thisUniqueShip in dict_shipShortCodesToLongNames_LayUp:
				thisShipLongName = dict_shipShortCodesToLongNames_LayUp[thisUniqueShip]
			else:
				thisShipLongName = dict_shipShortCodesToLongNames[thisUniqueShip]
		
		if thisShipLongName == 'Costa neoRomantica':
			continue
		
		df_existingMasterFile, masterFileThisShipDoesExist = f_readExistingMasterFile(thisShipLongName)
		
		if dict_PREPARE_RAW_DATA_FOR___['DATA_APPROACH_AAQS_DAILY'] == 1:
			if not masterFileThisShipDoesExist:
				print("AAQS AAPROACH >> SHIP DOES NOT EXIST >> NEXT SHIP")
				continue
		
		print("\n############################################")
		print("RAW DATA TO BE PREPARED FOR NEXT SHIP >>> " + thisUniqueShip + " = " + thisShipLongName)
		
		useOnlyThisShip = thisShipLongName
		
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
		
		dfFinal = f_getFuelTypePerEnginePerTimeslice(dfFinal, thisShipLongName)
		
		dfFinal.loc[dfFinal[flag_finalFile_Ship] == useOnlyThisShip, flag_finalFile_timestampsPerHour] = 0
		
		dfFinal = f_addTimeStampsPerHour(dfFinal, True)
		
		dfFinal = func_addAvgEngineLoad(dfFinal)
		
		dfFinal = f_addFuelConsumptionToDF(dfFinal, thisShipLongName, True)
		
		dfFinal = f_addColumnsForMissingNeptuneLabRawDataColumns(dfFinal, thisShipLongName,
																					print_finalPreparedNLRawData)
		
		
		
		if masterFileThisShipDoesExist:
			df_existingMasterFile = f_addThisDataFrameAtTheEndOfTheExistingTotalFile(
				dfFinal,
				df_existingMasterFile,
				thisShipLongName
			)
		else:
			df_existingMasterFile = dfFinal
			
		df_existingMasterFile = f_resortColumnsOfFinalTotalFileWithAllNeededColumns(df_existingMasterFile)
		
		#region export final file for this ship
		if dict_PREPARE_RAW_DATA_FOR___['DATA_APPROACH_AAQS_DAILY'] == 1:
			f_exportDataframe(
				fileExport_csv, df_existingMasterFile, masterFile_AAQS_ALL_csv, thisShipLongName
			)
		else:
			f_exportDataframe(
				fileExport_csv, df_existingMasterFile, masterFile_LayUp_ALL_csv, thisShipLongName
			)
		#endregion
	
	playsound('hammer_hitwall1.wav')
	
	startTime = f_doTheTimeMeasurementInThisFunction(startTime, flag_timeEnd, inspect.stack()[0][3])
#endregion
