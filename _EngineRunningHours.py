
from _DAILY_AAQS_Variables import *
from _CM_Include import *

import datetime
import time
import inspect
import pandas as pd
from datetime import timedelta

# ######################################################################################################################

dict_ShipsToPlanEngineRunningHours = {
	"AIDAbella": 		0
	,"AIDAluna": 		1
	,"AIDAdiva": 		1
	,"AIDAblu": 		0
	,"AIDAmar": 		0
	,"AIDAsol": 		1
	,"AIDAstella": 	1
	,"AIDAprima": 		1
	,"AIDAperla": 		1
}

masterFile_EngineRunningHours_csv = r'C:\Users\500095\Desktop\Engine Running Hours\02_FinalFiles\PBI_EngineRunningHours_.csv'
# masterFile_EngineRunningHours_ALL_csv = r'C:\Users\500095\Desktop\Engine Running Hours\02_FinalFiles\PBI_EngineRunningHours.csv'

masterFile_EngineRunningHours_PlanningPrediction = r'C:\Users\500095\Desktop\Engine Running Hours\02_FinalFiles\FBPT_EngineRunningHourPrediction.csv'

masterFile_Infoship_LastRunningHourUpdate = r'C:\Users\500095\Desktop\Engine Running Hours\02_FinalFiles\Infoship_Baseline.csv'

masterFile_rhStatsForPBI = r'C:\Users\500095\Desktop\Engine Running Hours\02_FinalFiles\df_rhStats.csv'

Infoship_runningHoursLastActualDate = datetime.datetime(2020, 2, 7, 0, 0, 0)

flag_infoShip_Ship = 'Ship'
flag_infoShip_DG = 'DG'
flag_infoShip_LastActual = 'Last Actual'
flag_infoShip_30kOverhaul = '30.000 RH'
flag_infoShip_15kOverhaul = '15.000 RH'
flag_infoShip_TC1Overhaul = 'TC 1'
flag_infoShip_TC2Overhaul = 'TC 2'

flag_rh_prediction_Ship = "Ship"
flag_rh_prediction_Day = "Day"


flag_rh_stats_Ship = "Ship"

# ######################################################################################################################
# ### VARs RH @ 15k OH ##############
flag_rh_stats_DG1_rh15kOH = "DG1 rh 15kOH"
flag_rh_stats_DG2_rh15kOH = "DG2 rh 15kOH"
flag_rh_stats_DG3_rh15kOH = "DG3 rh 15kOH"
flag_rh_stats_DG4_rh15kOH = "DG4 rh 15kOH"
flag_rh_stats_DG5_rh15kOH = "DG5 rh 15kOH"
flag_rh_stats_DG6_rh15kOH = "DG6 rh 15kOH"

def func_createDict_rh_stats_DG_rh15kOH():
	dict_flagsForTheseItems = {
		0: flag_rh_stats_DG1_rh15kOH,
		1: flag_rh_stats_DG2_rh15kOH,
		2: flag_rh_stats_DG3_rh15kOH,
		3: flag_rh_stats_DG4_rh15kOH,
		4: flag_rh_stats_DG5_rh15kOH,
		5: flag_rh_stats_DG6_rh15kOH
	}
	
	return dict_flagsForTheseItems

# ######################################################################################################################
# ### VARs RH @ 30k OH ##############
flag_rh_stats_DG1_rh30kOH = "DG1 rh 30kOH"
flag_rh_stats_DG2_rh30kOH = "DG2 rh 30kOH"
flag_rh_stats_DG3_rh30kOH = "DG3 rh 30kOH"
flag_rh_stats_DG4_rh30kOH = "DG4 rh 30kOH"
flag_rh_stats_DG5_rh30kOH = "DG5 rh 30kOH"
flag_rh_stats_DG6_rh30kOH = "DG6 rh 30kOH"

def func_createDict_rh_stats_DG_rh30kOH():
	dict_flagsForTheseItems = {
		0: flag_rh_stats_DG1_rh30kOH,
		1: flag_rh_stats_DG2_rh30kOH,
		2: flag_rh_stats_DG3_rh30kOH,
		3: flag_rh_stats_DG4_rh30kOH,
		4: flag_rh_stats_DG5_rh30kOH,
		5: flag_rh_stats_DG6_rh30kOH
	}
	
	return dict_flagsForTheseItems

# ######################################################################################################################
# ### VARs date @ 15k OH ##############
flag_rh_stats_DG1_date15kOH = "DG1 date 15kOH"
flag_rh_stats_DG2_date15kOH = "DG2 date 15kOH"
flag_rh_stats_DG3_date15kOH = "DG3 date 15kOH"
flag_rh_stats_DG4_date15kOH = "DG4 date 15kOH"
flag_rh_stats_DG5_date15kOH = "DG5 date 15kOH"
flag_rh_stats_DG6_date15kOH = "DG6 date 15kOH"

def func_createDict_rh_stats_DG_date15kOH():
	dict_flagsForTheseItems = {
		0: flag_rh_stats_DG1_date15kOH,
		1: flag_rh_stats_DG2_date15kOH,
		2: flag_rh_stats_DG3_date15kOH,
		3: flag_rh_stats_DG4_date15kOH,
		4: flag_rh_stats_DG5_date15kOH,
		5: flag_rh_stats_DG6_date15kOH
	}
	
	return dict_flagsForTheseItems

# ######################################################################################################################
# ### VARs date @ 30k OH ##############
flag_rh_stats_DG1_date30kOH = "DG1 date 30kOH"
flag_rh_stats_DG2_date30kOH = "DG2 date 30kOH"
flag_rh_stats_DG3_date30kOH = "DG3 date 30kOH"
flag_rh_stats_DG4_date30kOH = "DG4 date 30kOH"
flag_rh_stats_DG5_date30kOH = "DG5 date 30kOH"
flag_rh_stats_DG6_date30kOH = "DG6 date 30kOH"


def func_createDict_rh_stats_DG_date30kOH():
	dict_flagsForTheseItems = {
		0: flag_rh_stats_DG1_date30kOH,
		1: flag_rh_stats_DG2_date30kOH,
		2: flag_rh_stats_DG3_date30kOH,
		3: flag_rh_stats_DG4_date30kOH,
		4: flag_rh_stats_DG5_date30kOH,
		5: flag_rh_stats_DG6_date30kOH
	}
	
	return dict_flagsForTheseItems

# ######################################################################################################################
def func_updateAllFiguresWithLastActual(
	dfInput,
	thisShip
):
	f_makeThePrintNiceStructured(True, "### update actuals with last infoship >>> ", inspect.stack()[0][3])
	startTime = time
	startTime = f_doTheTimeMeasurementInThisFunction(startTime, flag_timeStart, inspect.stack()[0][3])
	
	df_lastInfoshipStatus = func_readlastInfoshipStatus()
	
	dict_engineRunningHoursCumulatedFlag = \
		func_defineDictWithFlagsForEngineRunningHoursCumulatedSinceLastInfoshipActuals()
	
	dict_CumulatedEngineRunningHourPrediction = \
		func_defineDictWithFlagsForEngineRunningHourPredictionCumulatedSinceLastInfoshipActuals()
	
	engineCountFlag = 0
	while engineCountFlag < 6:
		subDF = \
			df_lastInfoshipStatus[
				(df_lastInfoshipStatus[flag_infoShip_Ship] == thisShip) &
				(df_lastInfoshipStatus[flag_infoShip_DG] == str("DG" + str((engineCountFlag+1))))
				]
		
		if subDF.shape[0] != 0:
			thisShipThisEngineLastRunningHour = subDF.loc[subDF.index.max(), flag_infoShip_LastActual]
			print("thisShipThisEngineLastRunningHour for DG#: " + str(engineCountFlag+1) + " = " + str(thisShipThisEngineLastRunningHour))
			
			#region update cumulated actual running hours with new baseline from Infoship
			dfInput.loc[
				dfInput[flag_finalFile_Date] >= Infoship_runningHoursLastActualDate,
				dict_engineRunningHoursCumulatedFlag[engineCountFlag]
			] = \
				dfInput.loc[
					dfInput[flag_finalFile_Date] >= Infoship_runningHoursLastActualDate,
					dict_engineRunningHoursCumulatedFlag[engineCountFlag]
				] + thisShipThisEngineLastRunningHour
			#endregion
			
			# region update cumulated predicted running hours with new baseline from Infoship
			dfInput.loc[
				dfInput[flag_finalFile_Date] >= Infoship_runningHoursLastActualDate,
				dict_CumulatedEngineRunningHourPrediction[engineCountFlag]
			] = \
				dfInput.loc[
					dfInput[flag_finalFile_Date] >= Infoship_runningHoursLastActualDate,
					dict_CumulatedEngineRunningHourPrediction[engineCountFlag]
				] + thisShipThisEngineLastRunningHour
			# endregion
		
		engineCountFlag += 1
	
	
	dfInput = func_getAllEnginesCumulatedTotalView(
		dfInput,
		dict_engineRunningHoursCumulatedFlag,
		flag_engineRunningHoursCumulatedSinceLastInfoshipUpdate_ALL_DGs)
	
	dfInput = func_getAllEnginesCumulatedTotalView(
		dfInput,
		dict_CumulatedEngineRunningHourPrediction,
		flag_runningHourPredictionCumulatedSinceLastInfoship_ALL_DGs)
	
	
	startTime = f_doTheTimeMeasurementInThisFunction(startTime, flag_timeEnd, inspect.stack()[0][3])
	
	return dfInput
	

# ######################################################################################################################
def func_readlastInfoshipStatus():
	df_lastInfoship = pd.read_csv(
		masterFile_Infoship_LastRunningHourUpdate,
		sep=';', decimal=',', thousands=".", low_memory=False, usecols=[
			'Ship',
			'DG',
			'Last Actual',
			'30.000 RH',
			'15.000 RH',
			'TC 1',
			'TC 2'
		]
	)
	
	# print(df_lastInfoship)
	
	return df_lastInfoship
		
	
# ######################################################################################################################
def func_EngineRunningHours_combineActualAndPredictionInJustOnFile(
	df_actualData,
	df_rhPrediction,
	thisShip
):
	f_makeThePrintNiceStructured(True, "### combine actuals and prediction >>> ", inspect.stack()[0][3])
	startTime = time
	startTime = f_doTheTimeMeasurementInThisFunction(startTime, flag_timeStart, inspect.stack()[0][3])
	
	totalDays = df_rhPrediction[flag_rh_prediction_Day].max() - df_rhPrediction[flag_rh_prediction_Day].min()
	print("flag_rh_prediction_Day min: " + str(df_rhPrediction[flag_rh_prediction_Day].min()))
	print("flag_rh_prediction_Day max: " + str(df_rhPrediction[flag_rh_prediction_Day].max()))
	print("totalDays in rh prediction: " + str(totalDays.days))
	
	sr = pd.Series(
		pd.date_range(df_rhPrediction[flag_rh_prediction_Day].min().strftime('%Y-%m-%d'), periods=totalDays.days, freq='D'))
	
	# print(sr)
	dfNew = pd.DataFrame()
	
	dfNew = func_adjustDataframeWithNeededColumns(dfNew)
	
	#region read necessary dicts
	dict_actual_engineRunningHoursFlag = \
		func_defineDictWithFlagsForEngineRunningHours()
	
	dict_actual_engineRunningHoursCumulatedFlag = \
		func_defineDictWithFlagsForEngineRunningHoursCumulatedSinceLastInfoshipActuals()
	
	dict_prediction_engineRunningHoursFlag = \
		func_createDictWithFlags_rhPredictionPerEnginePerDay()
	#endregion
	
	for thisDay in sr.index:
		if thisDay < sr.index.max():
			dfNew.loc[thisDay, flag_finalFile_Date] = sr[thisDay]
			
			engineCountFlag = 0
			while engineCountFlag < 6:
				#region actual day by day data
				thisEngineHoursActual = round(
					df_actualData.loc[
						(df_actualData[flag_finalFile_Date] >= sr[thisDay]) &
						(df_actualData[flag_finalFile_Date] < sr[thisDay + 1]) &
						(df_actualData[flag_finalFile_Ship] == thisShip),
						dict_actual_engineRunningHoursFlag[engineCountFlag]].sum(), 1)
				
				# if engineCountFlag == 0:
				# 	print("actual RH DG1 @ " + str(thisDay) + " = " + str(thisEngineHoursActual))
					
				dfNew.loc[thisDay, dict_actual_engineRunningHoursFlag[engineCountFlag]] = thisEngineHoursActual
				#endregion
				
				#region actual cumulated day by data
				if sr[thisDay] <= df_actualData[flag_finalFile_Date].max():
					thisEngineHoursActualCumulated = round(
						df_actualData.loc[
							(df_actualData[flag_finalFile_Date] >= sr[thisDay]) &
							(df_actualData[flag_finalFile_Date] < sr[thisDay + 1]) &
							(df_actualData[flag_finalFile_Ship] == thisShip),
							dict_actual_engineRunningHoursCumulatedFlag[engineCountFlag]].sum(), 1)
				else:
					thisEngineHoursActualCumulated = \
						dfNew.loc[thisDay - 1, dict_actual_engineRunningHoursCumulatedFlag[engineCountFlag]]
					
					# print("ende gelände ... use last version of actual data for this ship & this engine >> " + str(thisEngineHoursActualCumulated))
				
				
				#
				# if engineCountFlag == 0:
				# 	print("cumulated RH DG1 @ " + str(thisDay) + " @ " + str(sr[thisDay]) + " = " + str(thisEngineHoursActualCumulated))
					
				dfNew.loc[thisDay, dict_actual_engineRunningHoursCumulatedFlag[engineCountFlag]] = thisEngineHoursActualCumulated
				#endregion
				
				#region rh prediction day by day data
				thisEngineThisDay_RunningHourPrediction = round(
					df_rhPrediction.loc[
						(df_rhPrediction[flag_rh_prediction_Day] >= sr[thisDay]) &
						(df_rhPrediction[flag_rh_prediction_Day] < sr[thisDay + 1]) &
						(df_rhPrediction[flag_rh_prediction_Ship] == thisShip),
						dict_prediction_engineRunningHoursFlag[engineCountFlag]].sum(), 1)
				
				dfNew.loc[
					thisDay, dict_prediction_engineRunningHoursFlag[engineCountFlag]] = thisEngineThisDay_RunningHourPrediction
				# endregion
				
				engineCountFlag += 1
	
	dfNew[flag_finalFile_Ship] = thisShip
	
	dfNew.to_csv("test.csv", sep=";", decimal=".")
	
	startTime = f_doTheTimeMeasurementInThisFunction(startTime, flag_timeEnd, inspect.stack()[0][3])
	
	return dfNew


# ######################################################################################################################
def func_adjustDataframeWithNeededColumns(
	dfInput
):
	
	dfInput[flag_engineRunningHours_DG1] = 0
	dfInput[flag_engineRunningHours_DG2] = 0
	dfInput[flag_engineRunningHours_DG3] = 0
	dfInput[flag_engineRunningHours_DG4] = 0
	dfInput[flag_engineRunningHours_DG5] = 0
	dfInput[flag_engineRunningHours_DG6] = 0
	
	dfInput[flag_engineRunningHoursCumulatedSinceLastInfoshipUpdate_DG1] = 0
	dfInput[flag_engineRunningHoursCumulatedSinceLastInfoshipUpdate_DG2] = 0
	dfInput[flag_engineRunningHoursCumulatedSinceLastInfoshipUpdate_DG3] = 0
	dfInput[flag_engineRunningHoursCumulatedSinceLastInfoshipUpdate_DG4] = 0
	dfInput[flag_engineRunningHoursCumulatedSinceLastInfoshipUpdate_DG5] = 0
	dfInput[flag_engineRunningHoursCumulatedSinceLastInfoshipUpdate_DG6] = 0
	
	dfInput[flag_rhPredictionThisDay_DG1] = 0
	dfInput[flag_rhPredictionThisDay_DG2] = 0
	dfInput[flag_rhPredictionThisDay_DG3] = 0
	dfInput[flag_rhPredictionThisDay_DG4] = 0
	dfInput[flag_rhPredictionThisDay_DG5] = 0
	dfInput[flag_rhPredictionThisDay_DG6] = 0
	
	dfInput[flag_runningHourPredictionCumulatedSinceLastInfoship_DG1] = 0
	dfInput[flag_runningHourPredictionCumulatedSinceLastInfoship_DG2] = 0
	dfInput[flag_runningHourPredictionCumulatedSinceLastInfoship_DG3] = 0
	dfInput[flag_runningHourPredictionCumulatedSinceLastInfoship_DG4] = 0
	dfInput[flag_runningHourPredictionCumulatedSinceLastInfoship_DG5] = 0
	dfInput[flag_runningHourPredictionCumulatedSinceLastInfoship_DG6] = 0
	
	
	return dfInput


# ######################################################################################################################
def func_EngineRunningHours_ReadRunningHourPrediction():
	df_rhPrediction = pd.DataFrame()
	
	df_rhPrediction = pd.read_csv(
		masterFile_EngineRunningHours_PlanningPrediction,
		sep=';', decimal=',', low_memory=False,
		usecols=[
			'Ship',
			'Day',
			'DG1 RH Prediction this day',
			'DG2 RH Prediction this day',
			'DG3 RH Prediction this day',
			'DG4 RH Prediction this day',
			'DG5 RH Prediction this day',
			'DG6 RH Prediction this day'
		]
	)
	
	df_rhPrediction[flag_rh_prediction_Day] = pd.to_datetime(df_rhPrediction[flag_rh_prediction_Day], format='%d.%m.%Y')
	
	df_rhPrediction = func_replaceNanInThisColumn(df_rhPrediction, flag_rhPredictionThisDay_DG1, 0)
	df_rhPrediction = func_replaceNanInThisColumn(df_rhPrediction, flag_rhPredictionThisDay_DG2, 0)
	df_rhPrediction = func_replaceNanInThisColumn(df_rhPrediction, flag_rhPredictionThisDay_DG3, 0)
	df_rhPrediction = func_replaceNanInThisColumn(df_rhPrediction, flag_rhPredictionThisDay_DG4, 0)
	df_rhPrediction = func_replaceNanInThisColumn(df_rhPrediction, flag_rhPredictionThisDay_DG5, 0)
	df_rhPrediction = func_replaceNanInThisColumn(df_rhPrediction, flag_rhPredictionThisDay_DG6, 0)
	
	return df_rhPrediction


# ######################################################################################################################
def func_EngineRunningHours_createShipByShipEngineRunningHourFile(
	dfInput
):
	f_makeThePrintNiceStructured(True, "### >>> ", inspect.stack()[0][3])
	startTime = time
	startTime = f_doTheTimeMeasurementInThisFunction(startTime, flag_timeStart, inspect.stack()[0][3])
	
	dict_engineLoadFlag = func_defineDictWithFlagsForEngineLoadColumns()
	
	dict_engineRunningHoursFlag = func_defineDictWithFlagsForEngineRunningHours()
	
	# for ap in dfInput.index:
	
	engineCountFlag = 0
	while engineCountFlag < 6:
		dfInput[dict_engineRunningHoursFlag[engineCountFlag]] = 0
		
		dfInput.loc[ \
			(dfInput[dict_engineLoadFlag[engineCountFlag]] > minPowerDemandAccepted_kW),
			dict_engineRunningHoursFlag[engineCountFlag]
		] = round(
			(
				60 / (
				dfInput.loc[
					(dfInput[dict_engineLoadFlag[engineCountFlag]] > minPowerDemandAccepted_kW),
					flag_finalFile_timestampsPerHour
				])
			) / 60, 2)
		
		engineCountFlag += 1
	
	startTime = f_doTheTimeMeasurementInThisFunction(startTime, flag_timeEnd, inspect.stack()[0][3])
	
	return dfInput


# ######################################################################################################################
def func_EngineRunningHours_getValuesAggregatedDayByDay(
	dfInput,
	thisShipLongName
):
	f_makeThePrintNiceStructured(True,
										  "### build new df with daily running our aggregation for " + thisShipLongName + " >>> ",
										  inspect.stack()[0][3])
	startTime = time
	startTime = f_doTheTimeMeasurementInThisFunction(startTime, flag_timeStart, inspect.stack()[0][3])
	
	totalDays = dfInput[flag_finalFile_Date].max() - dfInput[flag_finalFile_Date].min()
	print("totalDays in actual data " + str(totalDays.days))
	
	sr = pd.Series(
		pd.date_range(dfInput[flag_finalFile_Date].min().strftime('%Y-%m-%d'), periods=totalDays.days, freq='D'))
	
	dfNew = pd.DataFrame()
	
	dfInput[flag_finalFile_Date] = pd.to_datetime(dfInput[flag_finalFile_Date], format='%Y-%m-%d')
	
	dict_engineRunningHoursFlag = func_defineDictWithFlagsForEngineRunningHours()
	
	for thisDay in sr.index:
		
		if thisDay < sr.index.max():
			# dfNew = dfNew.append({flag_finalFile_Date: thisDay}, ignore_index=True)
			
			dfNew.loc[thisDay, flag_finalFile_Date] = sr[thisDay]
			
			engineCountFlag = 0
			while engineCountFlag < 6:
				thisEngineHours = round(
					dfInput.loc[
						(dfInput[flag_finalFile_Date] >= sr[thisDay]) &
						(dfInput[flag_finalFile_Date] < sr[thisDay + 1]),
						dict_engineRunningHoursFlag[engineCountFlag]].sum(), 1)
				
				# print("total running hours engine "+str(engineCountFlag+1)+" this day = " + str(thisEngineHours))
				
				dfNew.loc[thisDay, dict_engineRunningHoursFlag[engineCountFlag]] = thisEngineHours
				
				engineCountFlag += 1
	
	dfNew[flag_finalFile_Ship] = thisShipLongName
	
	startTime = f_doTheTimeMeasurementInThisFunction(startTime, flag_timeEnd, inspect.stack()[0][3])
	
	return dfNew


# ######################################################################################################################
def func_EngineRunningHours_createCumulatedActualSinceLastInfoshipUpdate(
	dfInput
):
	f_makeThePrintNiceStructured(True, "### cumulated actuals >>> ", inspect.stack()[0][3])
	startTime = time
	startTime = f_doTheTimeMeasurementInThisFunction(startTime, flag_timeStart, inspect.stack()[0][3])
	
	dfInput[flag_engineRunningHoursCumulatedSinceLastInfoshipUpdate_DG1] = 0
	dfInput[flag_engineRunningHoursCumulatedSinceLastInfoshipUpdate_DG2] = 0
	dfInput[flag_engineRunningHoursCumulatedSinceLastInfoshipUpdate_DG3] = 0
	dfInput[flag_engineRunningHoursCumulatedSinceLastInfoshipUpdate_DG4] = 0
	dfInput[flag_engineRunningHoursCumulatedSinceLastInfoshipUpdate_DG5] = 0
	dfInput[flag_engineRunningHoursCumulatedSinceLastInfoshipUpdate_DG6] = 0
	
	dict_engineRunningHoursFlag = func_defineDictWithFlagsForEngineRunningHours()
	dict_engineRunningHoursCumulatedFlag = func_defineDictWithFlagsForEngineRunningHoursCumulatedSinceLastInfoshipActuals()
	
	for ap in dfInput.index:
		if ap > 0 and dfInput.loc[ap, flag_finalFile_Date] > Infoship_runningHoursLastActualDate:
			engineCountFlag = 0
			while engineCountFlag < 6:
				dfInput.loc[ap, dict_engineRunningHoursCumulatedFlag[engineCountFlag]] = \
					dfInput.loc[ap - 1, dict_engineRunningHoursCumulatedFlag[engineCountFlag]] + \
					dfInput.loc[ap, dict_engineRunningHoursFlag[engineCountFlag]]
				
				engineCountFlag += 1
	
	startTime = f_doTheTimeMeasurementInThisFunction(startTime, flag_timeEnd, inspect.stack()[0][3])
	
	return dfInput


# ######################################################################################################################
def func_EngineRunningHours_createCumulatedPredictionSinceLastInfoshipUpdate(
	dfInput
):
	f_makeThePrintNiceStructured(True, "### cumulated prediction >>> ", inspect.stack()[0][3])
	startTime = time
	startTime = f_doTheTimeMeasurementInThisFunction(startTime, flag_timeStart, inspect.stack()[0][3])
	
	dict_dayByDayEngineRunningHourPrediction = \
		func_createDictWithFlags_rhPredictionPerEnginePerDay()
	
	dict_CumulatedEngineRunningHourPrediction = \
		func_defineDictWithFlagsForEngineRunningHourPredictionCumulatedSinceLastInfoshipActuals()
	
	engineCountFlag = 0
	while engineCountFlag < 6:
		dfInput[dict_CumulatedEngineRunningHourPrediction[engineCountFlag]] = 0
		engineCountFlag += 1
		
	for ap in dfInput.index:
		if ap > 0 and dfInput.loc[ap, flag_finalFile_Date] > Infoship_runningHoursLastActualDate:
			engineCountFlag = 0
			while engineCountFlag < 6:
				dfInput.loc[ap, dict_CumulatedEngineRunningHourPrediction[engineCountFlag]] = \
					dfInput.loc[ap - 1, dict_CumulatedEngineRunningHourPrediction[engineCountFlag]] + \
					dfInput.loc[ap, dict_dayByDayEngineRunningHourPrediction[engineCountFlag]]
				
				# print("here @ ap " + str(dfInput.loc[ap, dict_dayByDayEngineRunningHourPrediction[engineCountFlag]]))
				
				engineCountFlag += 1
	
	startTime = f_doTheTimeMeasurementInThisFunction(startTime, flag_timeEnd, inspect.stack()[0][3])
	
	return dfInput


# ######################################################################################################################
def func_getAllEnginesCumulatedTotalView(
	dfInput,
	dictWithFlagsForSubItems,
	cumulatedViewFlag
):
	dfInput[cumulatedViewFlag] = 0
	
	engineCountFlag = 0
	while engineCountFlag < 6:
		dfInput[dictWithFlagsForSubItems[engineCountFlag]] = \
			round(
				dfInput[dictWithFlagsForSubItems[engineCountFlag]],
				1
			)
		
		dfInput[cumulatedViewFlag] = \
			dfInput[cumulatedViewFlag] + \
			dfInput[dictWithFlagsForSubItems[engineCountFlag]]
		
		engineCountFlag += 1
	
	return dfInput

# ######################################################################################################################
def func_EngineRunningHours_createStatistics(
	df_rhDayByDay,
	versionNumber
):
	df_rhStats = func_createEmptyDfFor_rhStats()
	
	df_lastInfoshipStatus = func_readlastInfoshipStatus()
	
	dict_CumulatedEngineRunningHourPrediction, \
	dict_rh15kOH, dict_rh30kOH, dict_date15kOH, dict_date30kOH = \
		f_createSomeDicts()
		
	for thisShip in dict_ShipsToPlanEngineRunningHours:
		print(chr(10) + "### STATS FOR " + thisShip + " ###################")
		df_rhStats = df_rhStats.append({flag_rh_stats_Ship: thisShip}, ignore_index=True)
		
		df_sub_rhDayByDay = df_rhDayByDay[df_rhDayByDay[flag_rh_prediction_Ship] == thisShip]
		
		if df_sub_rhDayByDay.shape[0] != 0:
			engineCountFlag = 0
			while engineCountFlag < 6:
				print("######### DG#" + str(engineCountFlag+1))
				subDF = \
					df_lastInfoshipStatus[
						(df_lastInfoshipStatus[flag_infoShip_Ship] == thisShip) &
						(df_lastInfoshipStatus[flag_infoShip_DG] == str("DG" + str((engineCountFlag + 1))))
						]
				
				maxRunningHours = df_sub_rhDayByDay.loc[df_sub_rhDayByDay.index.max(), dict_CumulatedEngineRunningHourPrediction[engineCountFlag]]
				minRunningHours = df_sub_rhDayByDay.loc[df_sub_rhDayByDay.index.min(), dict_CumulatedEngineRunningHourPrediction[engineCountFlag]]
				
				daysInPlanningPeriod = \
					(df_sub_rhDayByDay.loc[df_sub_rhDayByDay.index.max(), flag_finalFile_Date] - \
					df_sub_rhDayByDay.loc[df_sub_rhDayByDay.index.min(), flag_finalFile_Date]).days
				
				
				total_rh_thisShip = maxRunningHours - minRunningHours
				print("maxRunningHours: " + str(maxRunningHours))
				print("minRunningHours: " + str(minRunningHours))
				print("total_rh_thisShip: " + str(total_rh_thisShip))
				print("daysInPlanningPeriod: " + str(daysInPlanningPeriod))
				
				avgRunningHourPerDay = 0
				if daysInPlanningPeriod != 0 and total_rh_thisShip != 0:
					avgRunningHourPerDay = total_rh_thisShip / int(daysInPlanningPeriod)
					print("avgRunningHourPerDay: " + str(avgRunningHourPerDay))
				else:
					print("no planning data available")
					
				if subDF.shape[0] != 0:
					thisShipOverhaul_15k = subDF.loc[subDF.index.max(), flag_infoShip_15kOverhaul]
					thisShipOverhaul_30k = subDF.loc[subDF.index.max(), flag_infoShip_30kOverhaul]
					
					print(
						thisShip + " DG:" + str(engineCountFlag + 1) +
						" >> OH 15k: " + str(thisShipOverhaul_15k) + " << " +
						" >> OH 30k: " + str(thisShipOverhaul_30k) + " <<"
					)
					
					df_sub_rhDayByDay_after15kOH = df_sub_rhDayByDay[
						df_sub_rhDayByDay[dict_CumulatedEngineRunningHourPrediction[engineCountFlag]] >= thisShipOverhaul_15k]
					
					df_sub_rhDayByDay_after30kOH = df_sub_rhDayByDay[
						df_sub_rhDayByDay[dict_CumulatedEngineRunningHourPrediction[engineCountFlag]] >= thisShipOverhaul_30k]
					
					if df_sub_rhDayByDay_after15kOH.shape[0] != 0:
						thisShipOverhaulDate_15k = df_sub_rhDayByDay_after15kOH.loc[
							df_sub_rhDayByDay_after15kOH.index.min(), flag_finalFile_Date
						]
					else:
						thisShipOverhaulDate_15k = func_getPredictedOverhaulDateInLongTermFuture(
							thisShipOverhaul_15k, avgRunningHourPerDay, maxRunningHours, df_sub_rhDayByDay
						)
						# thisShipOverhaulDate_15k = "15k OH not available in planning horizon"
					
					if df_sub_rhDayByDay_after30kOH.shape[0] != 0:
						thisShipOverhaulDate_30k = df_sub_rhDayByDay_after30kOH.loc[
							df_sub_rhDayByDay_after30kOH.index.min(), flag_finalFile_Date
						]
					else:
						thisShipOverhaulDate_30k = func_getPredictedOverhaulDateInLongTermFuture(
							thisShipOverhaul_30k, avgRunningHourPerDay, maxRunningHours, df_sub_rhDayByDay
						)
						# thisShipOverhaulDate_30k = "30k OH not available in planning horizon"
					
					print(
						thisShip + " DG:" + str(engineCountFlag + 1) +
						" >> DATE OH 15k: " + str(thisShipOverhaulDate_15k) + " << " +
						" >> DATE OH 30k: " + str(thisShipOverhaulDate_30k) + " <<"
					)
					
					df_rhStats.loc[
						df_rhStats[flag_rh_stats_Ship] == thisShip, dict_rh15kOH[engineCountFlag]
					] = thisShipOverhaul_15k
					
					df_rhStats.loc[
						df_rhStats[flag_rh_stats_Ship] == thisShip, dict_rh30kOH[engineCountFlag]
					] = thisShipOverhaul_30k
					
					df_rhStats.loc[
						df_rhStats[flag_rh_stats_Ship] == thisShip, dict_date15kOH[engineCountFlag]
					] = thisShipOverhaulDate_15k
					
					df_rhStats.loc[
						df_rhStats[flag_rh_stats_Ship] == thisShip, dict_date30kOH[engineCountFlag]
					] = thisShipOverhaulDate_30k
					
				engineCountFlag += 1
	
	df_rhStats = func_sortTheColumnsForTheStats(df_rhStats)
	
	engineCountFlag = 0
	while engineCountFlag < 6:
		if dict_date15kOH[engineCountFlag] in df_rhStats.columns:
			df_rhStats[dict_date15kOH[engineCountFlag]] = pd.to_datetime(df_rhStats[dict_date15kOH[engineCountFlag]],
																						format='%Y-%m-%d')
		
		if dict_date30kOH[engineCountFlag] in df_rhStats.columns:
			df_rhStats[dict_date30kOH[engineCountFlag]] = pd.to_datetime(df_rhStats[dict_date30kOH[engineCountFlag]],
																							 format='%Y-%m-%d')
			
		engineCountFlag += 1
	
	
	fileName = masterFile_rhStatsForPBI.replace(
		'.csv',
		("_V" + str(versionNumber) + '.csv')
	)
	
	df_rhStats.to_csv(
		fileName,
		sep=';',
		decimal=".",
		index=False)
	

# ######################################################################################################################
def func_getPredictedOverhaulDateInLongTermFuture(
	nextOverhaulRunningHours,
	avgRunningHourPerDay,
	maxRunningHours,
	df_sub_rhDayByDay
):
	print(chr(10) + " get long term oh prediction")
	
	deltaInMissingRunningHours = round(nextOverhaulRunningHours - maxRunningHours, 1)
	print("deltaInMissingRunningHours " + str(deltaInMissingRunningHours))
	
	daysNeededToCoverThis = int(deltaInMissingRunningHours / avgRunningHourPerDay)
	print("daysNeededToCoverThis " + str(daysNeededToCoverThis))
	
	nextLongTermOverhaulDate = df_sub_rhDayByDay[flag_finalFile_Date].max() + timedelta(days=daysNeededToCoverThis)
	print("nextLongTermOverhaulDate " + str(nextLongTermOverhaulDate))
	
	return nextLongTermOverhaulDate

# ######################################################################################################################
def func_sortTheColumnsForTheStats(
	dfStats
):
	dfStats = dfStats[
		[
			flag_rh_stats_Ship,
			flag_rh_stats_DG1_rh15kOH,
			flag_rh_stats_DG1_date15kOH,
			flag_rh_stats_DG1_rh30kOH,
			flag_rh_stats_DG1_date30kOH,
			flag_rh_stats_DG2_rh15kOH,
			flag_rh_stats_DG2_date15kOH,
			flag_rh_stats_DG2_rh30kOH,
			flag_rh_stats_DG2_date30kOH,
			flag_rh_stats_DG3_rh15kOH,
			flag_rh_stats_DG3_date15kOH,
			flag_rh_stats_DG3_rh30kOH,
			flag_rh_stats_DG3_date30kOH,
			flag_rh_stats_DG4_rh15kOH,
			flag_rh_stats_DG4_date15kOH,
			flag_rh_stats_DG4_rh30kOH,
			flag_rh_stats_DG4_date30kOH
			
	]]
	
	return dfStats
	

# ######################################################################################################################
def f_createSomeDicts():

	dict_CumulatedEngineRunningHourPrediction = \
		func_defineDictWithFlagsForEngineRunningHourPredictionCumulatedSinceLastInfoshipActuals()
	
	dict_rh15kOH = func_createDict_rh_stats_DG_rh15kOH()
	dict_rh30kOH = func_createDict_rh_stats_DG_rh30kOH()
	dict_date15kOH = func_createDict_rh_stats_DG_date15kOH()
	dict_date30kOH = func_createDict_rh_stats_DG_date30kOH()
	
	
	return \
		dict_CumulatedEngineRunningHourPrediction, \
		dict_rh15kOH, dict_rh30kOH, dict_date15kOH, dict_date30kOH
	

# ######################################################################################################################
def func_createEmptyDfFor_rhStats():
	newDF = pd.DataFrame(columns=[
			flag_rh_stats_Ship,
			flag_rh_stats_DG1_rh15kOH,
			flag_rh_stats_DG1_rh30kOH,
			flag_rh_stats_DG1_date15kOH,
			flag_rh_stats_DG1_date30kOH,
			flag_rh_stats_DG2_rh15kOH,
			flag_rh_stats_DG2_rh30kOH,
			flag_rh_stats_DG2_date15kOH,
			flag_rh_stats_DG2_date30kOH,
			flag_rh_stats_DG3_rh15kOH,
			flag_rh_stats_DG3_rh30kOH,
			flag_rh_stats_DG3_date15kOH,
			flag_rh_stats_DG3_date30kOH,
			flag_rh_stats_DG4_rh15kOH,
			flag_rh_stats_DG4_rh30kOH,
			flag_rh_stats_DG4_date15kOH,
			flag_rh_stats_DG4_date30kOH
		])
	
	return newDF
			

# ######################################################################################################################
def func_EngineRunnings_createRunningHourPrediction(
	df_rhPredVersion,
	useOnlyThisShip,
	rhVersion
):
	f_makeThePrintNiceStructured(True, "### swap running hours & create scenarios >>> ", inspect.stack()[0][3])
	startTime = time
	startTime = f_doTheTimeMeasurementInThisFunction(startTime, flag_timeStart, inspect.stack()[0][3])
	
	# TODO ... develop algorithm for more ships in case its needed in the future
	# algorithm does only work for engines with 4 engines and two of them AAQS !! .. aura cara vita or Costa ships are not doable at all
	
	logAllDetailsAroundRunningHourSwaps = False
	
	dict_dayByDayEngineRunningHourPrediction = \
		func_createDictWithFlags_rhPredictionPerEnginePerDay()
	
	focusOnLowerEngineNumber = False
	
	if rhVersion == 1:
		focusOnLowerEngineNumber = True
	
	highPrio_AAQS_Engine, \
	highPrio_nonAAQS_Engine, \
	lowPrio_AAQS_Engine, \
	lowPrio_nonAAQS_Engine = \
		func_getEngineSetupForThisPredictionCycle(useOnlyThisShip, focusOnLowerEngineNumber)
	
	print(chr(10) + ">>> ALTERNATE RH Prediction @ cylce " + str(rhVersion))
	print("highPrio_AAQS_Engine 		" + str(highPrio_AAQS_Engine))
	print("lowPrio_AAQS_Engine 		" + str(lowPrio_AAQS_Engine))
	print("highPrio_nonAAQS_Engine 	" + str(highPrio_nonAAQS_Engine))
	print("lowPrio_nonAAQS_Engine		" + str(lowPrio_nonAAQS_Engine))
	
	if logAllDetailsAroundRunningHourSwaps:
		print(chr(10) + " loop through df and check if things have to be swapped")
	
	for ap in df_rhPredVersion.index:
		if df_rhPredVersion.loc[ap, flag_rh_prediction_Ship] == useOnlyThisShip:
			df_rhPredVersion = func_EngineRunningHours_switchEngines(
				df_rhPredVersion,
				dict_dayByDayEngineRunningHourPrediction,
				ap,
				highPrio_AAQS_Engine, lowPrio_AAQS_Engine, True, logAllDetailsAroundRunningHourSwaps)
			
			df_rhPredVersion = func_EngineRunningHours_switchEngines(
				df_rhPredVersion,
				dict_dayByDayEngineRunningHourPrediction,
				ap,
				highPrio_nonAAQS_Engine, lowPrio_nonAAQS_Engine, False, logAllDetailsAroundRunningHourSwaps)
	
	startTime = f_doTheTimeMeasurementInThisFunction(startTime, flag_timeEnd, inspect.stack()[0][3])
	
	return df_rhPredVersion


# ######################################################################################################################
def func_EngineRunningHours_switchEngines(
	df,
	engineDict,
	ap,
	highPrioEngine,
	lowPrioEngine,
	aaqsFlag,
	logMe
):
	rhHighPrioEngines = df.loc[ap, engineDict[highPrioEngine - 1]]
	rhLowPrioEngines = df.loc[ap, engineDict[lowPrioEngine - 1]]
	
	# if aaqsFlag:
	# 	print(str(df.loc[ap, flag_rh_prediction_Day]) + " @ " + str(ap) +
	# 			" AAQS rhHighPrioEngines (" + str(rhHighPrioEngines) + ") rhLowPrioEngines (" + str(rhLowPrioEngines) + ")")
	# else:
	# 	print(str(df.loc[ap, flag_rh_prediction_Day]) + " @ " + str(ap) +
	# 			" NON AAQS rhHighPrioEngines (" + str(rhHighPrioEngines) + ") rhLowPrioEngines (" + str(rhLowPrioEngines) + ")")
		
	if rhHighPrioEngines < rhLowPrioEngines:
		if logMe:
			if aaqsFlag:
				print(str(df.loc[ap, flag_rh_prediction_Day]) + " @ " + str(ap) +
						" switch AAQS ENGINES rhHighPrioEngines " + str(rhHighPrioEngines) + " with rhLowPrioEngines " + str(rhLowPrioEngines))
			else:
				print(str(df.loc[ap, flag_rh_prediction_Day]) + " @ " + str(ap) +
						" switch NON AAQS ENGINES rhHighPrioEngines " + str(rhHighPrioEngines) + " with rhLowPrioEngines " + str(
					rhLowPrioEngines))
		
		df.loc[ap, engineDict[highPrioEngine - 1]] = rhLowPrioEngines
		df.loc[ap, engineDict[lowPrioEngine - 1]] = rhHighPrioEngines
	
	return df
	
# ######################################################################################################################
def func_getEngineSetupForThisPredictionCycle(
	useOnlyThisShip,
	focusOnLowerEngineNumber
):
	print(chr(10) + " >>> get engine setup for this alternation in " + inspect.stack()[0][3])
	
	highPrio_AAQS_Engine = 0
	highPrio_nonAAQS_Engine = 0
	lowPrio_AAQS_Engine = 0
	lowPrio_nonAAQS_Engine = 0
	
	# print("FANCY ... dict items as flat list: " + str(list(dict_AAQS_engines.values())))
	
	cntOfAAQSEngines = func_getCountOfAAQSEnginesForThisShip(useOnlyThisShip)
	
	if cntOfAAQSEngines == 2:
		thisEngine = 0
		while thisEngine < 6:
			if focusOnLowerEngineNumber:
				if dict_AAQS_engines[useOnlyThisShip][thisEngine] == 0:
					if highPrio_nonAAQS_Engine == 0:
						highPrio_nonAAQS_Engine = thisEngine + 1
					else:
						if lowPrio_nonAAQS_Engine == 0:
							lowPrio_nonAAQS_Engine = thisEngine + 1
				else:
					if highPrio_AAQS_Engine == 0:
						highPrio_AAQS_Engine = thisEngine + 1
					else:
						if lowPrio_AAQS_Engine == 0:
							lowPrio_AAQS_Engine = thisEngine + 1
			else:
				if dict_AAQS_engines[useOnlyThisShip][thisEngine] == 0:
					if lowPrio_nonAAQS_Engine == 0:
						lowPrio_nonAAQS_Engine = thisEngine + 1
					else:
						if highPrio_nonAAQS_Engine == 0:
							highPrio_nonAAQS_Engine = thisEngine + 1
				else:
					if lowPrio_AAQS_Engine == 0:
						lowPrio_AAQS_Engine = thisEngine + 1
					else:
						if highPrio_AAQS_Engine == 0:
							highPrio_AAQS_Engine = thisEngine + 1
			
			thisEngine += 1
	else:
		if cntOfAAQSEngines == 0:
			if focusOnLowerEngineNumber:
				highPrio_AAQS_Engine = 1
				lowPrio_AAQS_Engine = 3
				
				highPrio_nonAAQS_Engine = 2
				lowPrio_nonAAQS_Engine = 4
			else:
				highPrio_AAQS_Engine = 3
				lowPrio_AAQS_Engine = 1
				
				highPrio_nonAAQS_Engine = 4
				lowPrio_nonAAQS_Engine = 2
		else:
			print("ENGINE SWAP ALGORITHM NOT MADE FOR " + str(cntOfAAQSEngines) +" AAQS ENGINES")
			
		
	return highPrio_AAQS_Engine, highPrio_nonAAQS_Engine, lowPrio_AAQS_Engine, lowPrio_nonAAQS_Engine


# ######################################################################################################################
def func_getCountOfAAQSEnginesForThisShip(
	useOnlyThisShip
):
	cntOfAAQSEngines = 0
	thisEngine = 0
	while thisEngine < 6:
		if dict_AAQS_engines[useOnlyThisShip][thisEngine] > 0:
			cntOfAAQSEngines += 1
		
		thisEngine += 1
	
	print(useOnlyThisShip + " has " + str(cntOfAAQSEngines) + " AAQS engines")
	
	return cntOfAAQSEngines