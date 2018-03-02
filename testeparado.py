import xlrd
 
#----------------------------------------------------------------------

issueObj = {

        #7 work_package
        #16 task

        'issue': {
            'project_id': '247',
            'tracker_id': '16',
            'status_id': '20',
            'priority_id': '2',
            'author_id': '39',
            'parent_issue_id': ALTERAR AQUI,
            'subject': iss[0],
            'assigned_to_id': '74',
            'estimated_hours': iss[1],
            'custom_fields': [ { 'value':'1', 'id':'14' } ]
        }

    }

def open_file(path):
    """
    Open and read an Excel file
    """
    book = xlrd.open_workbook(path)
 
    # get the first worksheet
    first_sheet = book.sheet_by_index(0)
 
    createWP = True

    tasks = {}

    for rx in range(first_sheet.nrows):
        row = first_sheet.row(rx)
        # print( row[1].value )

        if ( row[0].value.find("[WORK_PACKAGE]") != -1):

            print("==== Criou WP =========")
            workPackageName = row[0].value[14:] 
            tasks[ workPackageName ] = []

        else:
            tasks[ workPackageName ].append( { issueName: row[2].value, hours: row[1].value  } )


    print (tasks)
    # # read a row slice
    # print first_sheet.row_slice(rowx=0,
    #                             start_colx=0,
    #                             end_colx=2)  print( first_sheet.row(rx)[0].find("[WORK_PACKAGE]") )
 
#----------------------------------------------------------------------
if __name__ == "__main__":
    path = "OS.xlsx"
    open_file(path)