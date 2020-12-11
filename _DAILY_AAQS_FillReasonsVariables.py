

# ######################################################################################################################

flag_issuesFile_startDate = 'Start Date (dd/mm/yy)'
flag_issuesFile_endDate = 'End Date (dd/mm/yy)'
flag_issuesFile_affectedDG = '#DG EGCS'
flag_issuesFile_issue = 'Issues Preventing ECA Operation 1'
flag_issuesFile_Area = 'AREA'
flag_issuesFile_Comments = 'Comments (free text, if any)'

masterFile_technicalIssues_AIDA = r'C:\Users\500095\Desktop\AAQS_FullTransparency\AAQS_OutOfOrder_Details\EGCS_Status AIDA.xlsx'
masterFile_technicalIssues_Costa = r'C:\Users\500095\Desktop\AAQS_FullTransparency\AAQS_OutOfOrder_Details\EGCS_Status Costa.xlsx'

flag_issueArea_Harbour = "Harbour"
flag_issueArea_See = "See"
flag_issueArea_Harbour_and_See = "Harbour + See"





# df_issues_AIDA = pd.read_excel(xlsFile_ScrubberIssues_AIDA, sheet_name='Perla', skiprows=1) #usecols=['Car Name', 'Car Price']
#
# df_issues_AIDA[flag_issuesFile_startDate] = df_issues_AIDA[flag_issuesFile_startDate].astype('datetime64[ns]')
# df_issues_AIDA[flag_issuesFile_endDate] = df_issues_AIDA[flag_issuesFile_endDate].astype('datetime64[ns]')
#
# for ap in df_issues_AIDA.index:
# 	print("REASON " + df_issues_AIDA.loc[ap, flag_issuesFile_reason] + " START: " +
# 			str(df_issues_AIDA.loc[ap, flag_issuesFile_startDate]) + " END: " +
# 			str(df_issues_AIDA.loc[ap, flag_issuesFile_endDate])
# 			)
