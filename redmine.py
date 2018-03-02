#!-*- conding: utf8 -*-
import os, sys, csv, codecs, json, requests, xlrd
 
#----------------------------------------------------------------------
def open_file(path):
    """
    Open and read an Excel file
    """
    book = xlrd.open_workbook(path)
 
    # print number of sheets
    print book.nsheets
 
    # print sheet names
    print book.sheet_names()
 
    # get the first worksheet
    first_sheet = book.sheet_by_index(0)
 
    # read a row
    print first_sheet.row_values(0)
 
    # read a cell
    cell = first_sheet.cell(0,0)
    print cell
    print cell.value
    
    createWP = True

    for rx in range(first_sheet.nrows):
        print( first_sheet.row(rx)[0].value )

        if ( first_sheet.row(rx)[0].value.find("[WORK_PACKAGE]") != -1):
            print("==== Criou WP =========")


    # # read a row slice
    # print first_sheet.row_slice(rowx=0,
    #                             start_colx=0,
    #                             end_colx=2)  print( first_sheet.row(rx)[0].find("[WORK_PACKAGE]") )
 
#----------------------------------------------------------------------
if __name__ == "__main__":
    path = "OS.xlsx"
    open_file(path)

for row in reader:
    iss = []

    for txt in row:
        print(txt)
        iss.append(txt)
    
    issueObj = {

        #7 work_package
        #16 task

        'issue': {
            'project_id': '258',
            'tracker_id': '16',
            'status_id': '20',
            'priority_id': '2',
            'author_id': '39',
            'parent_issue_id': '27253',
            'subject': iss[0],
            'assigned_to_id': '74',
            'estimated_hours': iss[1],
            'custom_fields': [ { 'value':'1', 'id':'14' } ]
        }

    }

    issues.append(issueObj)

print(issues)

for issue in issues:
    payload = json.dumps(issue)
    print(payload)
    # return
    r = requests.post("https://projetos.eits.com.br/issues.xml",
                    auth=(user, password),
                    data= payload,
                    headers = {'content-type': 'application/json'}
                    )

    print(r.status_code, r.text)