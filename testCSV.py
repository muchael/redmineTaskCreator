username = 'ddd'
password = 'ddd'





import xlrd, json, requests
from issue import Issue

#----------------------------------------------------------------------

def open_file(path):
    """
    Open and read an Excel file
    """
    book = xlrd.open_workbook(path)
 
    # get the first worksheet
    first_sheet = book.sheet_by_index(0)
 
    createWP = True

    tasks = {}

    workPackageName = ''

    for rx in range( 1, first_sheet.nrows ):
        row = first_sheet.row(rx)

        if ( row[0].value.find("[WORK_PACKAGE]") != -1):
            workPackageName = row[0].value[14:] 
            tasks[ workPackageName ] = []

        else:
            tasks[ workPackageName ].append( { 'issueName': row[2].value, 'hours': row[1].value  } )

    return tasks
 
def parseToIssues(tasks):

    projectId = '258'
    trackerId = '7'
    parentId = '25581'
    authorId = '39'

    for workPackageName, value in tasks.items():
        workPackageIssue = Issue( projectId, trackerId, authorId, parentId )
        workPackageIssue.setSubject(workPackageName)

        print(postIssues(workPackageIssue)) PAREI AQUI SE LEMBRE

    return workPackageIssue

def postIssues( issue ):
    payload = json.dumps(issue.toJson())
    
    print(payload)

    r = requests.post("https://projetos.eits.com.br/issues.json",
                    auth=(username, password),
                    data= payload,
                    headers = {'content-type': 'application/json'}
                    )

    return r.text

def main():
    tasks = open_file(path)
    parseToIssues(tasks)

#----------------------------------------------------------------------
if __name__ == "__main__":
    path = "OS.xlsx"
    main()