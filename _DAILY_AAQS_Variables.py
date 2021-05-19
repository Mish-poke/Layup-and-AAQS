
import datetime
import time
# ######################################################################################################################

# region individual ships
dict_analyseTheseShips = {
	"AIDAaura": 			0
	,"AIDAcara": 			0
	,"AIDAvita": 			0
	,"AIDAdiva": 			0
	,"AIDAluna": 			0
	,"AIDAmar": 			0
	,"AIDAbella": 			0
	,"AIDAblu": 			1
	,"AIDAsol": 			0
	,"AIDAstella": 			0
	,"AIDAprima": 			0
	,"AIDAperla": 			0
	,"AIDAnova": 			0
	, "Costa Atlantica": 	0
	, "Costa Deliziosa": 	0
	, "Costa Diadema": 		0
	, "Costa Fascinosa": 	0
	, "Costa Favolosa": 	0
	, "Costa Fortuna": 		0
	, "Costa Luminosa": 	0
	, "Costa Magica": 		0
	, "Costa Mediterranea": 0
	, "Costa Pacifica": 	0
	, "Costa Serena": 		0
	, "Costa Smeralda": 	0
	, "Costa Toscana": 		0
	, "Costa Firenze": 		0
	, "Costa Venezia": 		0
}
# endregion

# region FULL AIDA FLEET
# dict_analyseTheseShips = {
# 	"AIDAaura": 			1
# 	,"AIDAcara": 			1
# 	,"AIDAvita": 			1
# 	,"AIDAdiva": 			1
# 	,"AIDAluna": 			1
# 	,"AIDAmar": 			1
# 	,"AIDAbella": 			1
# 	,"AIDAblu": 			1
# 	,"AIDAsol": 			1
# 	,"AIDAstella": 			1
# 	,"AIDAprima": 			1
# 	,"AIDAperla": 			1
# 	,"AIDAnova": 			1
# 	, "Costa Atlantica": 	0
# 	, "Costa Deliziosa": 	0
# 	, "Costa Diadema": 		0
# 	, "Costa Fascinosa": 	0
# 	, "Costa Favolosa": 	0
# 	, "Costa Fortuna": 		0
# 	, "Costa Luminosa": 	0
# 	, "Costa Magica": 		0
# 	, "Costa Mediterranea": 0
# 	, "Costa Pacifica": 	0
# 	, "Costa Serena": 		0
# 	, "Costa Smeralda": 	0
# 	, "Costa Toscana": 		0
# 	, "Costa Firenze": 		0
# 	, "Costa Venezia": 		0
# }
# endregion

# region FULL Costa FLEET
# dict_analyseTheseShips = {
# 	"AIDAaura": 			0
# 	,"AIDAcara": 			0
# 	,"AIDAvita": 			0
# 	,"AIDAdiva": 			0
# 	,"AIDAluna": 			0
# 	,"AIDAmar": 			0
# 	,"AIDAbella": 			0
# 	,"AIDAblu": 			0
# 	,"AIDAsol": 			0
# 	,"AIDAstella": 			0
# 	,"AIDAprima": 			0
# 	,"AIDAperla": 			0
# 	,"AIDAnova": 			0
# 	,"Costa Atlantica": 	1
# 	,"Costa Deliziosa": 	0 # no data for DE since Jun 2020
#  	,"Costa Diadema": 		1
# 	,"Costa Fascinosa": 	1
# 	,"Costa Favolosa": 		1
# 	,"Costa Fortuna": 		1
# 	,"Costa Luminosa": 		1
# 	,"Costa Magica": 		1
# 	,"Costa Mediterranea": 	1
# 	,"Costa Pacifica": 		1
# 	,"Costa Serena": 		1
# 	,"Costa Smeralda": 		1
# 	,"Costa Toscana": 		0 # no data yet
# 	,"Costa Firenze": 		1
# 	,"Costa Venezia": 		1
# }
# endregion

# region FULL AIDA AND COSTA FLEET
# dict_analyseTheseShips = {
# 	"AIDAaura": 				0
# 	,"AIDAcara": 				0
# 	,"AIDAvita": 				0
# 	,"AIDAdiva": 				0
# 	,"AIDAluna": 				0
# 	,"AIDAmar": 				0
# 	,"AIDAbella": 				0
# 	,"AIDAblu": 				1
# 	,"AIDAsol": 				1
# 	,"AIDAstella": 				0
# 	,"AIDAprima": 				1
# 	,"AIDAperla": 				1
# 	,"AIDAnova": 				0
# 	,"Costa Atlantica": 		1
# 	,"Costa Deliziosa": 		0 # no data for DE since Jun 2020
# 	,"Costa Diadema": 			1
# 	,"Costa Fascinosa": 		1
# 	,"Costa Favolosa": 			1
# 	,"Costa Fortuna": 			1
# 	,"Costa Luminosa": 			1
# 	,"Costa Magica": 			1
# 	,"Costa Mediterranea": 		1
# 	,"Costa Pacifica": 			1
# 	,"Costa Serena": 			1
# 	,"Costa Smeralda": 			1
# 	,"Costa Toscana": 			0 # no data yet
# 	,"Costa Firenze": 			1
# 	,"Costa Venezia": 			1
# }
# endregion


# master flags to toggle between different analysis modes
masterFlagAnalysisMode_AAQS = "AAQS"
masterFlagAnalysisMode_LayUp = "LayUp"

# region FILES to be used
useBrandSplit = False
# masterFile_AIDA = r'C:\Users\500095\Desktop\AAQS_FullTransparency\Final_AAQS_Files\__DAILY_AAQS_AIDA_TF_5.0.xlsx'
# masterFile_Costa = r'C:\Users\500095\Desktop\AAQS_FullTransparency\Final_AAQS_Files\__DAILY_AAQS_Costa_TF_5.0.xlsx'

# masterFile_AAQS_ALL_XLS = r'C:\Users\500095\Desktop\AAQS_FullTransparency\Python_Code\02_AAQS_FinalFiles\PBI_DAILY_AAQS.xlsx'
masterFile_AAQS_ALL_XLS = r'E:\001_CMG\AAQS_FullTransparency\02_AAQS_FinalFiles\PBI_DAILY_AAQS.xlsx'

# masterFile_AAQS_ALL_csv = r'C:\Users\500095\Desktop\AAQS_FullTransparency\Python_Code\02_AAQS_FinalFiles\PBI_DAILY_AAQS.csv'
masterFile_AAQS_ALL_csv = r'E:\001_CMG\AAQS_FullTransparency\02_AAQS_FinalFiles\PBI_DAILY_AAQS.csv'

dummyTestFile_AAQS =      r'C:\Users\500095\Desktop\AAQS_FullTransparency\Python_Code\02_AAQS_FinalFiles\__TEST_FILE.xlsx'
# endregion

# region Neptune Lab Raw Data
flag_NeptuneLab_Ship = 'Ship'
flag_NeptuneLab_Date = 'Date'
flag_NeptuneLab_StandardTag = 'Standard Tag'
flag_NeptuneLab_SignalDesription = 'Signal Description'
flag_NeptuneLab_UnitOfMeasure = 'Unit of measure'
flag_NeptuneLab_value = 'Raw Data'
flag_NeptuneLab_combinedFlags = 'uniqueCombinationOfBothFlags'
flag_NeptuneLab_avgValue = 'avgValue'

flag_NeptuneLab_Averages_value = 'Average'
# endregion

# region FINAL FILE Structure
flag_finalFile_Date = 'Date'
flag_finalFile_Ship = 'Ship'
flag_finalFile_SOG = 'Speed'
flag_finalFile_STW = 'STW'
flag_finalFile_Temperature = 'Temperature'
flag_finalFile_Humidity = 'Humidity'

flag_finalFile_SOG_GAP_Filled = 'SOG_GAP_FILLED'
flag_finalFile_Latitude = 'Latitude'
flag_finalFile_Longitude = 'Longitude'
flag_finalFile_typeOfSailing = 'Sailing Mode'
flag_finalFile_legPortName = 'LEG/Port-Name'
flag_finalFile_legPortDate = 'Leg/Port-StartDate'
flag_finalFile_timestampsPerHour = 'timestampsPerHour'

# ######################################################################################################################
flag_finalFile_DG1_ACTIVE_POWER = 'DG1_ACTIVE_POWER'
flag_finalFile_DG2_ACTIVE_POWER = 'DG2_ACTIVE_POWER'
flag_finalFile_DG3_ACTIVE_POWER = 'DG3_ACTIVE_POWER'
flag_finalFile_DG4_ACTIVE_POWER = 'DG4_ACTIVE_POWER'
flag_finalFile_DG5_ACTIVE_POWER = 'DG5_ACTIVE_POWER'
flag_finalFile_DG6_ACTIVE_POWER = 'DG6_ACTIVE_POWER'

def func_defineDictWithFlagsForEngineLoadColumns():
	dict_engineLoadFlag = {
		0: flag_finalFile_DG1_ACTIVE_POWER,
		1: flag_finalFile_DG2_ACTIVE_POWER,
		2: flag_finalFile_DG3_ACTIVE_POWER,
		3: flag_finalFile_DG4_ACTIVE_POWER,
		4: flag_finalFile_DG5_ACTIVE_POWER,
		5: flag_finalFile_DG6_ACTIVE_POWER
	}
	
	return dict_engineLoadFlag

flag_finalFile_DG1_FUEL_OIL_IN_TE = 'DG1_FUEL_OIL_IN_TE'
flag_finalFile_DG2_FUEL_OIL_IN_TE = 'DG2_FUEL_OIL_IN_TE'
flag_finalFile_DG3_FUEL_OIL_IN_TE = 'DG3_FUEL_OIL_IN_TE'
flag_finalFile_DG4_FUEL_OIL_IN_TE = 'DG4_FUEL_OIL_IN_TE'
flag_finalFile_DG5_FUEL_OIL_IN_TE = 'DG5_FUEL_OIL_IN_TE'
flag_finalFile_DG6_FUEL_OIL_IN_TE = 'DG6_FUEL_OIL_IN_TE'

flag_finalFile_DG1_DeSOx_FLOW = 'DG1_DeSOx_FLOW'
flag_finalFile_DG2_DeSOx_FLOW = 'DG2_DeSOx_FLOW'
flag_finalFile_DG3_DeSOx_FLOW = 'DG3_DeSOx_FLOW'
flag_finalFile_DG4_DeSOx_FLOW = 'DG4_DeSOx_FLOW'
flag_finalFile_DG5_DeSOx_FLOW = 'DG5_DeSOx_FLOW'
flag_finalFile_DG6_DeSOx_FLOW = 'DG6_DeSOx_FLOW'

flag_finalFile_DG1_DeSOx_PumpPWR = 'DG1_DeSOx_PumpPWR'
flag_finalFile_DG2_DeSOx_PumpPWR = 'DG2_DeSOx_PumpPWR'
flag_finalFile_DG3_DeSOx_PumpPWR = 'DG3_DeSOx_PumpPWR'
flag_finalFile_DG4_DeSOx_PumpPWR = 'DG4_DeSOx_PumpPWR'
flag_finalFile_DG5_DeSOx_PumpPWR = 'DG5_DeSOx_PumpPWR'
flag_finalFile_DG6_DeSOx_PumpPWR = 'DG6_DeSOx_PumpPWR'

flag_finalFile_TotalPowerDemand = 'TOTAL_PWR'
flag_finalFile_AvgPwrDemandOverTime = 'AVG_PWR_DEMAND_OVER_TIME'
flag_finalFile_AvgEngineUsagePercentNow = 'AVG_EngineUsagePercentThisSample'
flag_finalFile_AvgTemperatureOverTime = 'AVG_AmbientTemp'
flag_finalFile_dataSanity = 'fullDataSanity'
flag_finalFile_totalFuel_HFO = "HFO_MT"
flag_finalFile_totalFuel_MGO = "MGO_MT"
flag_finalFile_totalFuel_LNG = "LNG_MT"

# ######################################################################################################################
flag_finalFile_EnginesRunning = 'Engines Running'
flag_finalFile_DG1_LoadPercent = "DG1_loadPercent"
flag_finalFile_DG2_LoadPercent = "DG2_loadPercent"
flag_finalFile_DG3_LoadPercent = "DG3_loadPercent"
flag_finalFile_DG4_LoadPercent = "DG4_loadPercent"
flag_finalFile_DG5_LoadPercent = "DG5_loadPercent"
flag_finalFile_DG6_LoadPercent = "DG6_loadPercent"


# ######################################################################################################################
def func_defineDictWithFlagsForEngineLoadPercentColumns():
	dict_engineLoadPercentFlag = {
		0: flag_finalFile_DG1_LoadPercent,
		1: flag_finalFile_DG2_LoadPercent,
		2: flag_finalFile_DG3_LoadPercent,
		3: flag_finalFile_DG4_LoadPercent,
		4: flag_finalFile_DG5_LoadPercent,
		5: flag_finalFile_DG6_LoadPercent
	}
	
	return dict_engineLoadPercentFlag


dict_nlComplianceComputerShortCuts = dict(
	[
		('41178', flag_finalFile_DG1_DeSOx_FLOW),
		('42178', flag_finalFile_DG2_DeSOx_FLOW),
		('43178', flag_finalFile_DG3_DeSOx_FLOW),
		('44178', flag_finalFile_DG4_DeSOx_FLOW),
		('45178', flag_finalFile_DG5_DeSOx_FLOW),
		('46178', flag_finalFile_DG6_DeSOx_FLOW),
		('41033', flag_finalFile_DG1_DeSOx_PumpPWR),
		('42033', flag_finalFile_DG2_DeSOx_PumpPWR),
		('43033', flag_finalFile_DG3_DeSOx_PumpPWR),
		('44033', flag_finalFile_DG4_DeSOx_PumpPWR),
		('45033', flag_finalFile_DG5_DeSOx_PumpPWR),
		('46033', flag_finalFile_DG6_DeSOx_PumpPWR)
	]
)

flag_finalFile_environmentalRestriction = 'ENV_Restriction'
flag_finalFile_technicalRestriction = 'TECH_Restriction'

flag_finalFile_fuelType_DG01 = 'DG1 Fuel Type'
flag_finalFile_fuelType_DG02 = 'DG2 Fuel Type'
flag_finalFile_fuelType_DG03 = 'DG3 Fuel Type'
flag_finalFile_fuelType_DG04 = 'DG4 Fuel Type'
flag_finalFile_fuelType_DG05 = 'DG5 Fuel Type'
flag_finalFile_fuelType_DG06 = 'DG6 Fuel Type'

flag_finalFile_DG1_fuelConsumption = 'DG1_FuelConsumption'
flag_finalFile_DG2_fuelConsumption = 'DG2_FuelConsumption'
flag_finalFile_DG3_fuelConsumption = 'DG3_FuelConsumption'
flag_finalFile_DG4_fuelConsumption = 'DG4_FuelConsumption'
flag_finalFile_DG5_fuelConsumption = 'DG5_FuelConsumption'
flag_finalFile_DG6_fuelConsumption = 'DG6_FuelConsumption'

flag_finalFile_DG1_SFOC = 'DG1_SFOC'
flag_finalFile_DG2_SFOC = 'DG2_SFOC'
flag_finalFile_DG3_SFOC = 'DG3_SFOC'
flag_finalFile_DG4_SFOC = 'DG4_SFOC'
flag_finalFile_DG5_SFOC = 'DG5_SFOC'
flag_finalFile_DG6_SFOC = 'DG6_SFOC'

flag_finalFile_AAQS_AssessmentDone = 'AAQS_AssessmentDone'
flag_AAQS_Usage_Assessment_PERFECT = "PERFECT"
flag_AAQS_Usage_Assessment_semi_PERFECT = "SEMI PERFECT. opportunity left"
flag_AAQS_Usage_Assessment_Desaster = "AAQS usage desaster, no AAQS usage at all"
flag_AAQS_Usage_Assessment_FuelChangeoverMandatoryBeforeArrival = 'FUEL CHANGE-OVER before arrival'
flag_AAQS_Usage_Assessment_FuelChangeoverMandatoryAfterDeparture = 'FUEL CHANGE-OVER after departure'
flag_AAQS_Usage_Assessment_EngineLoadBelowAllowedThreshold = 'AAQS usage not possible due to low load'
flag_AAQS_Usage_Assessment_WashWaterFilterMissing = 'AAQS usage not possible WWF missing'
flag_AAQS_Usage_NotAllowedInThisParticularRegion = "AAQS usage not allowed in this region"

flag_finalFile_DG1_AAQS_DowntimeReason = 'DG1 AAQS DOWNTIME REASON'
flag_finalFile_DG1_AAQS_DowntimeMissedPower = 'DG1 AAQS Missed Power'

flag_finalFile_DG2_AAQS_DowntimeReason = 'DG2 AAQS DOWNTIME REASON'
flag_finalFile_DG2_AAQS_DowntimeMissedPower = 'DG2 AAQS Missed Power'

flag_finalFile_DG3_AAQS_DowntimeReason = 'DG3 AAQS DOWNTIME REASON'
flag_finalFile_DG3_AAQS_DowntimeMissedPower = 'DG3 AAQS Missed Power'

flag_finalFile_DG4_AAQS_DowntimeReason = 'DG4 AAQS DOWNTIME REASON'
flag_finalFile_DG4_AAQS_DowntimeMissedPower = 'DG4 AAQS Missed Power'

flag_finalFile_DG5_AAQS_DowntimeReason = 'DG5 AAQS DOWNTIME REASON'
flag_finalFile_DG5_AAQS_DowntimeMissedPower = 'DG5 AAQS Missed Power'

flag_finalFile_DG6_AAQS_DowntimeReason = 'DG6 AAQS DOWNTIME REASON'
flag_finalFile_DG6_AAQS_DowntimeMissedPower = 'DG6 AAQS Missed Power'

flag_finalFile_DriftingAnchorage = 'Anchorage_or_Drifting'
flag_finalFile_DistanceThisSlice = 'Distance'
# endregion



flag_properFuelType_DG01 = 'DG1 Fuel Type Assessment'
flag_properFuelType_DG02 = 'DG2 Fuel Type Assessment'
flag_properFuelType_DG03 = 'DG3 Fuel Type Assessment'
flag_properFuelType_DG04 = 'DG4 Fuel Type Assessment'
flag_properFuelType_DG05 = 'DG5 Fuel Type Assessment'
flag_properFuelType_DG06 = 'DG6 Fuel Type Assessment'

# region Main Input Data COUNTER Flags
flag_signalCounter_DG1_ACTIVE_POWER = 'count_DG1_ACTIVE_POWER'
flag_signalCounter_DG2_ACTIVE_POWER = 'count_DG2_ACTIVE_POWER'
flag_signalCounter_DG3_ACTIVE_POWER = 'count_DG3_ACTIVE_POWER'
flag_signalCounter_DG4_ACTIVE_POWER = 'count_DG4_ACTIVE_POWER'
flag_signalCounter_DG5_ACTIVE_POWER = 'count_DG5_ACTIVE_POWER'
flag_signalCounter_DG6_ACTIVE_POWER = 'count_DG6_ACTIVE_POWER'

flag_signalCounter_DG1_FUEL_OIL_IN_TE = 'count_DG1_FUEL_OIL_IN_TE'
flag_signalCounter_DG2_FUEL_OIL_IN_TE = 'count_DG2_FUEL_OIL_IN_TE'
flag_signalCounter_DG3_FUEL_OIL_IN_TE = 'count_DG3_FUEL_OIL_IN_TE'
flag_signalCounter_DG4_FUEL_OIL_IN_TE = 'count_DG4_FUEL_OIL_IN_TE'
flag_signalCounter_DG5_FUEL_OIL_IN_TE = 'count_DG5_FUEL_OIL_IN_TE'
flag_signalCounter_DG6_FUEL_OIL_IN_TE = 'count_DG6_FUEL_OIL_IN_TE'

flag_signalCounter_Latitude = 'count_Latitude'
flag_signalCounter_Longitude = 'count_Longitude'
# endregion

flag_return_average = 0
flag_return_count = 1

flag_getChangeOverStartTimeBeforeArrival = "change over start time before arrival"
flag_getChangeOverEndeTimeAfterDeparture = "change over end time after departure"

# region EXPORT SUB FILES during analysis
print_sumOfRawData = 0
print_afterAddingTechnicalRestrictions = 0
print_dataAfterAddingSailingMode = 0
print_restructuredRawData = 0
print_dataAfterAddingFuelType = 0
print_finalPreparedNLRawData = 0
# endregion

fileExport_csv = 'csv'
fileExport_xls = 'xls'

flag_typeOfSailing_Port = 'Port'
flag_typeOfSailing_Anchorage = 'Anchorage'
flag_typeOfSailing_Drifting = 'Drifting'
anchorage_amountOfSurroundingDPsToBeCheckedBeforeAfter = 3
anchorage_maxAvgSpeedSurroundingDPs = 0.75
anchorage_maxAvgSpeedUpcomingDPs = 1.5
anchorage_maxSOGAllowedForSingleDP = 1.5

flag_typeOfSailing_Man = 'Man'
flag_typeOfSailing_Sailing = 'Sailing'

fuel_flag_LNG = 'LNG'
fuel_flag_MGO = 'MGO'
fuel_flag_VLSFO = 'VLSFO'
fuel_flag_HFO = 'HFO+AAQS'
fuel_flag_HFO_NOAAQS = 'HFO NO AAQS'
fuel_flag_AAQS_Missed_PORT = 'MGO HFO+AAQS MISSED PORT'
fuel_flag_AAQS_Missed_NAVIGATION = 'MGO HFO+AAQS MISSED NAVIGATION'
fuel_flag_MGO_InsideTerritorialWater = 'MGO inside territorial water'
fuel_flag_HFO_InsideTerritorialWater = 'ERROR? HFO inside territorial water!'

fuel_flag_EngineIsOff = 'ENGINE OFF'


flag_brand_AIDA = 'AIDA'
flag_brand_Costa = 'Costa'

timeCheck_perfect = 'perfectTiming'
timeCheck_noGo = 'noDataToBeAdded'
timeCheck_cutTheBeginningOfTheNewFile = 'cutTheStart'

flag_maxSOG_ToBeCountedAsPortStay = 0.5
flag_maxDistanceForPortDetection = 7

flag_hfo_mgo_fuelTempSplit = 80
flag_MGO_LNG_fuelTempSplit = 42
flag_minDeSowFlowRate = 100

flag_minLoadForAAQS_Allowance = 25

maxMissingLinesForPortInterruption = 5

minEngineLoadInKWToBeCountedAsOn = 250


minTimeAtAnchorInMinutes = 240
minAvgSpeedAtAnchor = 0.05
maxAvgSpeedAtAnchor = 0.5 #2
flag_anchorage_min_avgDistanceBetweenDPs = 0.005
flag_anchorage_max_avgDistanceBetweenDPs = 0.1

minAverageSpeedDrifting = 0.5
maxAverageSpeedDrifting = 4
minTimeDriftingInMinutes = 240
flag_drifting_min_avgDistanceBetweenDPs = 0.1
flag_drifting_max_avgDistanceBetweenDPs = 0.75

minTimeStamp = ''
maxTimeStamp = ''


fileCopyBeforeAddRaw = '_BEFORE_ADD_RAW_'
fileCopyBeforeSmartAlgo = '_BEFORE_SMART_ALGO_'

flag_engineDate_fuelType = 'Fuel Type Assessment'
flag_engineDate_EnginePower = 'Engine Data Running Power'
flag_engineDate_FuelTemp = 'Engine Data Fuel Oil In Temp'
flag_engineDate_DowntimeReasons = 'Engine Downtime Reason'


# aaqs_cc_detoxFlowRate = ''
# aaqs_cc_mainPumpPower = ''

dict_shipShortCodesToLongNames = dict(
	[
		('A-AU', 'AIDAaura'),
		('A-CA', 'AIDAcara'),
		('A-VT', 'AIDAvita'),
		('A-BE', 'AIDAbella'),
		('A-LN', 'AIDAluna'),
		('A-DV', 'AIDAdiva'),
		('A-BL', 'AIDAblu'),
		('A-MR', 'AIDAmar'),
		('A-SL', 'AIDAsol'),
		('A-ST', 'AIDAstella'),
		('A-PM', 'AIDAprima'),
		('A-PL', 'AIDAperla'),
		('A-NV', 'AIDAnova'),
		('C-AT', 'Costa Atlantica'),
		('C-DE', 'Costa Deliziosa'),
		('C-DI', 'Costa Diadema'),
		('C-FA', 'Costa Favolosa'),
		('C-FS', 'Costa Fascinosa'),
		('C-FO', 'Costa Fortuna'),
		('C-LU', 'Costa Luminosa'),
		('C-MG', 'Costa Magica'),
		('C-MD', 'Costa Mediterranea'),
		('C-NR', 'Costa neoRomantica'),
		('C-PA', 'Costa Pacifica'),
		('C-SE', 'Costa Serena'),
		('C-ME', 'Costa Smeralda'),
		('C-TO', 'Costa Toscana'),
		('C-VZ', 'Costa Venezia'),
		('C-FI', 'Costa Firenze')
	]
)

dict_shipShortCodesToLongNames_LayUp = dict(
	[
		('AU', 'AIDAaura'),
		('CA', 'AIDAcara'),
		('VT', 'AIDAvita'),
		('BE', 'AIDAbella'),
		('LN', 'AIDAluna'),
		('DV', 'AIDAdiva'),
		('BL', 'AIDAblu'),
		('MR', 'AIDAmar'),
		('SL', 'AIDAsol'),
		('ST', 'AIDAstella'),
		('PM', 'AIDAprima'),
		('PL', 'AIDAperla'),
		('NV', 'AIDAnova'),
		('AT', 'Costa Atlantica'),
		('DE', 'Costa Deliziosa'),
		('DI', 'Costa Diadema'),
		('FA', 'Costa Favolosa'),
		('FS', 'Costa Fascinosa'),
		('FO', 'Costa Fortuna'),
		('LU', 'Costa Luminosa'),
		('MG', 'Costa Magica'),
		('MD', 'Costa Mediterranea'),
		('NR', 'Costa neoRomantica'),
		('PA', 'Costa Pacifica'),
		('SE', 'Costa Serena'),
		('ME', 'Costa Smeralda'),
		('TO', 'Costa Toscana'),
		('VZ', 'Costa Venezia'),
		('FI', 'Costa Firenze')
	]
)

dict_Ship_MaxPowerOfEngines = {  # E1, ..., En
 	"AIDAaura": [8700, 8700, 5800, 4350, -1, -1],   # Aida Aura / information provided by Thomas Piller
	"AIDAcara": [2960, 2960, 2960, -1, -1, -1],   # AIDAcara ... data not approved // 5430 for main engine 2960 for port power engine
   	"AIDAvita": [8700, 8700, 5800, 4350, -1, -1],   # Aida Vita / information provided by Thomas Piller
	"AIDAbella": [9000, 9000, 9000, 9000, -1, -1],   # Aida Bella / information provided by  Elkan
	"AIDAdiva": [9000, 9000, 9000, 9000, -1, -1],  # Aida Diva / information provided by Elkan
	"AIDAluna": [9000, 9000, 9000, 9000, -1, -1],  # Aida Luna / information provided by  Elkan
	"AIDAblu": [9000, 9000, 9000, 9000, -1, -1],  # Aida Blu / information provided by  Elkan
	"AIDAsol": [9000, 9000, 9000, 9000, -1, -1],  # AIDAsol / information provided by  Elkan
   	"AIDAmar": [9000, 9000, 9000, 9000, -1, -1],  # Aida Mar / information provided by Elkan
	"AIDAstella": [9000, 9000, 9000, 9000, -1, -1],  # Aida Stella / information provided by Elkan
	"AIDAprima": [12000, 12000, 12000, 12000, -1, -1],  # Aida Prima / information provided by Elkan
   	"AIDAperla": [12000, 12000, 12000, 12000, -1, -1],  # Aida Perla / information provided by Elkan
   	"AIDAnova": [15440, 15440, 15440, 15440, -1, -1],  # Aida Nova / information provided by  Elkan
	"AIDAmira"  : [], # Aida Mira
   	"Costa Magica": [11520, 8640, 11520, 11520, 8640, 11520],    # Costa Magica
   	"Costa Fortuna": [11520, 8640, 11520, 11520, 8640, 11520],    # Costa Fortuna
   	"Costa Atlantica": [10300, 10300, 10300, 10300, 10300, 10300],  # Costa Atlantica
   	"Costa Mediterranea": [10300, 10300, 10300, 10300, 10300, 10300],  # Costa Mediterranea
   	"Costa Serena": [12600, 12600, 12600, 12600, 12600, 12600],  # Costa Serena
   	"Costa Pacifica": [12600, 12600, 12600, 12600, 12600, 12600],  # Costa Pacifica
   	"Costa Favolosa": [12600, 12600, 12600, 12600, 12600, 12600],  # Costa Favolosa
   	"Costa Fascinosa": [12600, 12600, 12600, 12600, 12600, 12600],  # Costa Fascinosa
   	"Costa Diadema": [12600, 8400, 12600, 12600, 8400, 12600],  # Costa Diadema / information provided by Elkan
   	"Costa Smeralda": [15440, 15440, 15440, 15440, -1, -1],  # Costa Smeralda / information provided by Elkan
	"Costa Toscana": [15440, 15440, 15440, 15440, -1, -1],  # Costa Smeralda / information provided by Elkan
	"Costa Luminosa": [12600, 8000, 12600, 12600, 8000, 12600],  # Costa Luminosa / information provided by Elkan
   	"Costa Deliziosa": [12000, 8000, 12000, 12000, 8000, 12000], # Costa Deliziosa / information provided by Elkan
	"Costa Venezia": [16800, 16800, 9600, 9600, 9600, -1], #
	"Costa Firenze": [16800, 16800, 9600, 9600, 9600, -1] #]
}

dict_shipNamesScrubberIssueFile = dict(
	[
		('AIDAaura', 'Aura'),
		('AIDAvita', 'Vita'),
		('AIDAbella', 'Bella'),
		('AIDAluna', 'Luna'),
		('AIDAdiva', 'Diva'),
		('AIDAblu', 'Blu'),
		('AIDAmar', 'Mar'),
		('AIDAsol', 'Sol'),
		('AIDAstella', 'Stella'),
		('AIDAprima', 'Prima'),
		('AIDAperla', 'Perla'),
		('Costa Atlantica', 'Atlantica'),
		('Costa Deliziosa', 'Deliziosa'),
		('Costa Diadema', 'Diadema'),
		('Costa Favolosa', 'Favolosa'),
		('Costa Fascinosa', 'Fascinosa'),
		('Costa Fortuna', 'Fortuna'),
		('Costa Luminosa', 'Luminosa'),
		('Costa Magica', 'Magica'),
		('Costa Mediterranea', 'Mediterranea'),
		('Costa Pacifica', 'Pacifica'),
		('Costa Serena', 'Serena'),
		('Costa Venezia', 'Venezia'),
		('Costa Firenze', 'Firenze')
	]
)

dict_AAQS_engines = {
	"AIDAaura": [0, 0, 0, 0, -1, -1],
	"AIDAcara": [0, 0, 0, 0, -1, -1],
	"AIDAvita": [1, 1, 0, 0, -1, -1],
	"AIDAdiva": [1, 1, 0, 0, -1, -1],
	"AIDAluna": [1, 1, 0, 0, -1, -1],
	"AIDAbella": [1, 0, 1, 0, -1, -1],
	"AIDAblu": [1, 0, 1, 0, -1, -1],
	"AIDAsol": [1, 0, 1, 0, -1, -1],
	"AIDAmar": [1, 1, 0, 0, -1, -1],
	"AIDAstella": [0, 0, 0, 0, -1, -1],
	"AIDAprima": [0, 0, 1, 1, -1, -1],
	"AIDAperla": [0, 0, 1, 1, -1, -1],
	"AIDAnova": [0, 0, 0, 0, -1, -1],
	"Costa Atlantica": [0, 0, 0, 0, 0, 0],#"Costa Atlantica": [0, 0, 1, 1, 0, 1],
	"Costa Deliziosa": [1, 1, 0, 0, 0, 1],# CHECKED
	"Costa Diadema": [0, 0, 1, 0, 1, 1], # CHECKED
	"Costa Fascinosa": [0, 1, 0, 0, 1, 1], #"Costa Fascinosa": [1, 0, 0, 1, 0, 1], ## CORRECTED! damn Neil :(
	"Costa Favolosa": [1, 0, 0, 1, 0, 1], # CHECKED
	"Costa Fortuna": [1, 1, 0, 0, 0, 0],#[1, 1, 0, 0, 0, 1],
	"Costa Luminosa": [1, 1, 0, 0, 0, 1], # CHECKED
	"Costa Mediterranea": [0, 0, 1, 1, 0, 1], # CHECKED
	"Costa Magica": [1, 1, 0, 0, 0, 1], # CHECKED
	"Costa Smeralda": [0, 0, 0, 0, -1, -1],
	"Costa Toscana": [0, 0, 0, 0, -1, -1],
	"Costa Pacifica": [0, 0, 1, 1, 1, 0], # CHECKED
	"Costa Serena": [0, 1, 0, 0, 0, 1], # CHECKED ### DG4 not ready yet
	"Costa Venezia": [1, 1, 0, 0, 1, -1],
	"Costa Firenze": [1, 1, 0, 0, 1, -1]# CHECKED
}

flag_AAQS_notPortReady = "AAQS NOT PORT READY"
flag_ENV_Restriction_AAQS_NOT_allowedInThisPort = "AAQS NOT ALLOWED IN THIS PORT"
flag_ENV_Restriction_AAQS_isAllowedInThisPort = "AAQS allowed in this port"

dict_AAQS_available = {
	"AIDAaura": 			False
	,"AIDAcara": 			False
	,"AIDAstella": 			False
	,'AIDAnova': 			False
	,"Costa Atlantica": 	False
	,"Costa Fortuna": 		False
	,"Costa neoRomantica": 	False
	,"Costa Smeralda": 		False
	,"Costa Toscana": 		False
	,"AIDAvita": 			True
	,"AIDAbella": 			True
	,"AIDAluna": 			True
	,"AIDAdiva": 			True
	,"AIDAblu": 			True
	,"AIDAmar": 			True
	,"AIDAsol": 			True
	,"AIDAprima": 			True
	,"AIDAperla": 			True
	,"Costa Deliziosa": 	True
	,"Costa Diadema": 		True
	,"Costa Fascinosa": 	True
	,"Costa Favolosa": 		True
	,"Costa Luminosa": 		True
	,"Costa Mediterranea": 	True
	,"Costa Magica": 		True
	,"Costa Pacifica":	 	True
	,"Costa Serena": 		True
	,"Costa Venezia": 		True
	,"Costa Firenze": 		True
}

dic_AAQS_PlannedForPortUsage = {
	"AIDAaura": 				0
	,"AIDAcara": 				0
	,"AIDAvita": 				0
	,"AIDAbella": 				1
	,"AIDAluna": 				0
	,"AIDAdiva": 				0
	,"AIDAblu": 				1
	,"AIDAmar": 				0
	,"AIDAsol": 				1
	,"AIDAstella": 				0
	,"AIDAprima": 				0
	,"AIDAperla": 				0
	,'AIDAnova': 				0
	,"Costa Atlantica": 		0
	,"Costa Deliziosa": 		1
	,"Costa Diadema": 			1
	,"Costa Fascinosa": 		1
	,"Costa Favolosa": 			1
	,"Costa Fortuna": 			0
	,"Costa Luminosa": 			1
	,"Costa Mediterranea": 		1
	,"Costa Magica": 			1
	,"Costa Pacifica":	 		1
	,"Costa Serena": 			1
	,"Costa Venezia": 			1
	,"Costa Firenze": 			1
	,"Costa neoRomantica": 		0
	,"Costa Smeralda": 			0
	,"Costa Toscana": 			0
}
dict_ENV_regulationChange_AllShipsShouldTryAAQSInPort = datetime.datetime(2020, 6, 12, 0, 0, 0)

territorialWater_NO_AAQS_ALLOWED = 'NO AAQS ALLOWED IN'
territorial_Name_Malaysia = 'Malaysia'
territorial_Name_China_BohaiRim = 'Bohai Rim'
territorial_Name_China_MainLand = 'China Main Land'
territorial_Name_SuezChannel = 'Suez Channel'
territorial_Name_Germany_NorthSea = 'Germany_NorthSea'
territorial_Name_Gran_Canaria = 'Canary Islands - Gran Canaria'
territorial_Name_Tenerife_La_Gomera = 'Canary Islands - Tenerife and La Gomera'
territorial_Name_La_Palma = 'Canary Islands - La Palma'
territorial_Name_Fuerte_Lanzarote = 'Canary Islands - Fuerte and Lanzarote'
aaqsBanCanaryIslands = datetime.datetime(2020, 6, 15)
#
# dict_starTimes = {
# 	territorial_Name_Gran_Canaria: [datetime.datetime(2020, 6, 15)]
# }

npa_territorialWaters_Lat_Long_Malaysia = [
	[6.55, 99.35],
	[6.45, 102.1],
	[5.9, 103.15],
	[5.33, 103.37],
	[4.91, 103.71],
	[4.3, 103.68],
	[3.19, 103.6],
	[3.13, 104.11],
	[2.99, 104.32],
	[2.49, 104.75],
	[2.29, 104.70],
	[2.06, 104.30],
	[1.41, 104.53],
	[0.82, 104.75],
	[0.82, 99.80],
	[3.95, 99.85],
]

npa_territorialWaters_Lat_Long_BohaiRim = [
	[41.02, 117.4],
	[41.24, 124.02],
	[37.87, 124.06],
	[36.78, 122.74],
	[35.0, 120.22],
	[35.0, 117.4]
]

npa_territorialWaters_Lat_Long_Suez = [
	[31.30, 32.00],
	[31.20, 33.00],
	[29.80, 33.00],
	[29.80, 32.00]
]

npa_territorialWaters_Lat_Long_ChinaMainCountry = [
	[35.0, 118.14],
	[35.0, 120.22],
	[33.13, 121.84],
	[31.57, 122.26],
	[30.82, 123.29],
	[25.32, 119.79],
	[23.01, 117.35],
	[21.58, 114.04],
	[21.24, 112.48],
	[18.52, 110.66],
	[17.92, 109.57],
	[18.01, 108.92],
	[18.42, 108.47],
	[19.23, 108.26],
	[19.51, 108.42],
	[20.35, 109.55],
	[20.71, 109.35],
	[20.67, 108.99],
	[21.11, 107.60],
	[21.35, 108.70],
	[21.32, 108.02]
]

npa_territorialWaters_Lat_Long_Germany_NorthSea = [
	[53.73, 6.34],
	[53.96, 7.24],
	[54.56, 8],
	[55.09, 8.04],
	[53.55, 10.26],
	[53.13, 6.34],
]

npa_territorialWaters_Lat_Long_Gran_Canaria = [
	[28.36, -15.76],
	[28.38, -15.37],
	[28.24, -15.19],
	[27.92, -15.13],
	[27.66, -15.26],
	[27.53, -15.58],
	[27.58, -15.79],
	[27.85, -16.05],
	[28.12, -16.02]
]

npa_territorialWaters_Lat_Long_Tenerife_La_Gomera = [
	[28.37, -17.44],
	[28.18, -16.16],
	[28.69, -15.93],
	[28.44, -15.93],
	[27.86, -16.40],
	[27.80, -16.73],
	[27.96, -16.94],
	[27.83, -17.21],
	[27.95, -17.51],
	[28.19, -17.56]
]

npa_territorialWaters_Lat_Long_La_Palma = [
	[29.06, -17.94],
	[29.01, -17.65],
	[28.77, -17.5],
	[28.49, -17.55],
	[28.26, -17.80],
	[28.35, -18.04],
	[28.78, -18.23],
	[28.93, -18.17]
]

npa_territorialWaters_Lat_Long_Fuerte_Lanzarote = [
	[29.62, -13.15],
	[29.23, -13.12],
	[28.86, -13.31],
	[28.76, -13.46],
	[28.46, -13.63],
	[28.17, -13.71],
	[27.84, -14.13],
	[27.89, -14.63],
	[28.04, -14.73],
	[28.22, -14.68],
	[28.45, -14.39],
	[29.14, -14.01],
	[29.57, -13.66]
]

timeAggregationPeriodInSeconds = 300

# region PORT DB Structuredict_shipNames
# sourceFile_ports = r'C:\Users\500095\Desktop\AAQS_FullTransparency\Database\PortDb_LatLong_V02.csv'
# sourceFile_Non_AAAQS_ports = r'C:\Users\500095\Desktop\AAQS_FullTransparency\Database\PortDb_NO_AAQS_Ports_LatLong_V02.csv'
# masterFile_PORTs = r'C:\Users\500095\Desktop\AAQS_FullTransparency\Database\PORT_DB_MASTER_V02.csv'
masterFile_PORTs = r'E:\001_CMG\AAQS_FullTransparency\Database\PORT_DB_MASTER_V02.csv'

flag_PORTDB_UNPortCode = 'UN-PortCode'
flag_PortDB_ports_name = 'PortName MXP'
flag_PORTDB_scrubbersAreAllowed = 'Scubbers are allowed'
flag_PORTDB_scrubberBanStartDate = 'Open Loop EGCS BAN start'
flag_PortDB_LAT = 'LAT'
flag_PortDB_LONG = 'LONG'
# endregion

progressPrintCounter = 5000
minPowerDemandAccepted_kW = 500

# ### DEBUG VARs ##############
flag_shipFeedback_C0_Ship = "C0_Ship"
flag_shipFeedback_C1_MainSystem = "C1_MainSystem"
flag_shipFeedback_C2_SubSystem = "C2_SubSystem"
flag_shipFeedback_C3_StepsTaken = "C3_StepsTaken"
flag_shipFeedback_C4_PercentageImplemented = "C4_PercentageImplemented"
flag_shipFeedback_C5_Comment = "C5_Comment"
flag_shipFeedback_C6_HVAC_Mode = "C6_HVAC_Mode"


# ######################################################################################################################
# ### VARs EngineRunningHours ##############
flag_engineRunningHours_DG1 = 'DG1 Running Hours'
flag_engineRunningHours_DG2 = 'DG2 Running Hours'
flag_engineRunningHours_DG3 = 'DG3 Running Hours'
flag_engineRunningHours_DG4 = 'DG4 Running Hours'
flag_engineRunningHours_DG5 = 'DG5 Running Hours'
flag_engineRunningHours_DG6 = 'DG6 Running Hours'

def func_defineDictWithFlagsForEngineRunningHours():
	dict_engineRunningHoursFlags = {
		0: flag_engineRunningHours_DG1,
		1: flag_engineRunningHours_DG2,
		2: flag_engineRunningHours_DG3,
		3: flag_engineRunningHours_DG4,
		4: flag_engineRunningHours_DG5,
		5: flag_engineRunningHours_DG6
	}
	
	return dict_engineRunningHoursFlags

# ######################################################################################################################
# ### VARs EngineRunningHours Cumulated ##############
flag_engineRunningHoursCumulatedSinceLastInfoshipUpdate_DG1 = 'Cumulated RH Actual DG1 Since Last Infoship'
flag_engineRunningHoursCumulatedSinceLastInfoshipUpdate_DG2 = 'Cumulated RH Actual DG2 Since Last Infoship'
flag_engineRunningHoursCumulatedSinceLastInfoshipUpdate_DG3 = 'Cumulated RH Actual DG3 Since Last Infoship'
flag_engineRunningHoursCumulatedSinceLastInfoshipUpdate_DG4 = 'Cumulated RH Actual DG4 Since Last Infoship'
flag_engineRunningHoursCumulatedSinceLastInfoshipUpdate_DG5 = 'Cumulated RH Actual DG5 Since Last Infoship'
flag_engineRunningHoursCumulatedSinceLastInfoshipUpdate_DG6 = 'Cumulated RH Actual DG6 Since Last Infoship'
flag_engineRunningHoursCumulatedSinceLastInfoshipUpdate_ALL_DGs = 'Cumulated RH Actual DGs ALL Since Last Infoship'

def func_defineDictWithFlagsForEngineRunningHoursCumulatedSinceLastInfoshipActuals():
	dict_someFlags = {
		0: flag_engineRunningHoursCumulatedSinceLastInfoshipUpdate_DG1,
		1: flag_engineRunningHoursCumulatedSinceLastInfoshipUpdate_DG2,
		2: flag_engineRunningHoursCumulatedSinceLastInfoshipUpdate_DG3,
		3: flag_engineRunningHoursCumulatedSinceLastInfoshipUpdate_DG4,
		4: flag_engineRunningHoursCumulatedSinceLastInfoshipUpdate_DG5,
		5: flag_engineRunningHoursCumulatedSinceLastInfoshipUpdate_DG6
	}
	
	return dict_someFlags


# ######################################################################################################################
# ### VARs EngineRunningHours Cumulated ##############
flag_runningHourPredictionCumulatedSinceLastInfoship_DG1 = 'Cumulated RH Prediction DG1 Since Last Infoship'
flag_runningHourPredictionCumulatedSinceLastInfoship_DG2 = 'Cumulated RH Prediction DG2 Since Last Infoship'
flag_runningHourPredictionCumulatedSinceLastInfoship_DG3 = 'Cumulated RH Prediction DG3 Since Last Infoship'
flag_runningHourPredictionCumulatedSinceLastInfoship_DG4 = 'Cumulated RH Prediction DG4 Since Last Infoship'
flag_runningHourPredictionCumulatedSinceLastInfoship_DG5 = 'Cumulated RH Prediction DG5 Since Last Infoship'
flag_runningHourPredictionCumulatedSinceLastInfoship_DG6 = 'Cumulated RH Prediction DG6 Since Last Infoship'
flag_runningHourPredictionCumulatedSinceLastInfoship_ALL_DGs = 'Cumulated RH Prediction DGs ALL Since Last Infoship'


def func_defineDictWithFlagsForEngineRunningHourPredictionCumulatedSinceLastInfoshipActuals():
	dict_someFlags = {
		0: flag_runningHourPredictionCumulatedSinceLastInfoship_DG1,
		1: flag_runningHourPredictionCumulatedSinceLastInfoship_DG2,
		2: flag_runningHourPredictionCumulatedSinceLastInfoship_DG3,
		3: flag_runningHourPredictionCumulatedSinceLastInfoship_DG4,
		4: flag_runningHourPredictionCumulatedSinceLastInfoship_DG5,
		5: flag_runningHourPredictionCumulatedSinceLastInfoship_DG6
	}
	
	return dict_someFlags

# ######################################################################################################################
# ### VARs EngineRunningHours Predicted ##############
flag_rhPredictionThisDay_DG1 = 'DG1 RH Prediction this day'
flag_rhPredictionThisDay_DG2 = 'DG2 RH Prediction this day'
flag_rhPredictionThisDay_DG3 = 'DG3 RH Prediction this day'
flag_rhPredictionThisDay_DG4 = 'DG4 RH Prediction this day'
flag_rhPredictionThisDay_DG5 = 'DG5 RH Prediction this day'
flag_rhPredictionThisDay_DG6 = 'DG6 RH Prediction this day'


def func_createDictWithFlags_rhPredictionPerEnginePerDay():
	dict_someFlags = {
		0: flag_rhPredictionThisDay_DG1,
		1: flag_rhPredictionThisDay_DG2,
		2: flag_rhPredictionThisDay_DG3,
		3: flag_rhPredictionThisDay_DG4,
		4: flag_rhPredictionThisDay_DG5,
		5: flag_rhPredictionThisDay_DG6
	}
	
	return dict_someFlags

# ######################################################################################################################
FS_backToNormalFuelIn2020 = datetime.datetime(2020, 7, 1, 0, 0, 0)
PA_backToNormalFuelIn2020 = datetime.datetime(2020, 4, 1, 0, 0, 0)
FA_noMoreAAQSAllowanceInCivi= datetime.datetime(2020, 8, 24, 0, 0, 0)
FullFleet_noMoreAAQSAllowanceInCivi= datetime.datetime(2021, 5, 3, 0, 0, 0)

lowLoadMgoOnlyNoMissedAAQSOpportunityBelowThisLoad = 23