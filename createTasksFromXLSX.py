# -*- coding: UTF-8 -*-
import xlrd, json, requests, getpass
from issue import Issue

#----------------------------------------------------------------------

username = None
password = None


def process_file(path, projectId, authorId, parentId):
    """
    Open and read an Excel file
    """
    book = xlrd.open_workbook(path)
 
    # get the first worksheet
    first_sheet = book.sheet_by_index(0)
 
    currentWorkPackageId = None

    for rx in range( 1, first_sheet.nrows ):
        row = first_sheet.row(rx)

        if ( row[0].value.find("[A]") != -1 ):
            workPackageName = row[0].value[4:]
            issue = Issue( projectId, 7, authorId, parentId, workPackageName, row[1].value, row[2].value, row[3].value )
            
            currentWorkPackage = postIssues( issue )
            currentWorkPackageId = currentWorkPackage['issue']['id']
            print issue.toJson()

        elif row[0].value:
            issue = Issue( projectId, 16, authorId, currentWorkPackageId, row[0].value, row[1].value, row[2].value, row[3].value )
            postIssues( issue )
            print issue.toJson()

def postIssues( issue ):
    payload = json.dumps(issue.toJson())
    
    r = requests.post("https://projetos.eits.com.br/issues.json",
                    auth=(username, password),
                    data= payload,
                    headers = {'content-type': 'application/json'}
                    )

    print r.status_code
    return json.loads(r.text)

def main():
    username = raw_input("Usuário do redmine: ")
    password = getpass.getpass("Senha: ")

    process_file(path = path, projectId = 291, authorId = 19, parentId = 31221)

def test():
    issue = Issue( projectId = 291, trackerId = 16, authorId = 19, parentId = 31251, subject = 'Teste completo3' , description = 'Teste',
        estimated_hours = 3, requisitos = 'RFU0123, RFA0001' )
    print issue.toJson()
    print ' --------------------------- '

    issueSaved = postIssues( issue )
    print issueSaved
    id = issueSaved['issue']['id']
    print 'id = ', id

#----------------------------------------------------------------------
if __name__ == "__main__":
    path = "xls/teste.xlsx"
    main()