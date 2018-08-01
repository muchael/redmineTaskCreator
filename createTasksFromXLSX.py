# -*- coding: UTF-8 -*-
import xlrd, json, requests, getpass, argparse
from issue import Issue

#----------------------------------------------------------------------

def process_file(path, projectId, parentId):
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
            issue = Issue( projectId, 7, parentId, workPackageName, row[1].value, row[2].value, row[3].value )
            
            # currentWorkPackage = postIssues( issue )
            # currentWorkPackageId = currentWorkPackage['issue']['id']
            currentWorkPackageId = 0
            print issue.toJson()

        elif row[0].value:
            issue = Issue( projectId, 16, currentWorkPackageId, row[0].value, row[1].value, row[2].value, row[3].value )
            # postIssues( issue )
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

def checkUser( username, password ):
    r = requests.get("https://projetos.eits.com.br/issues.json?offset=0&limit=1",
                    auth=(username, password)
                    )

    if r.status_code != 200:
        print "Erro ao autenticar"
        exit()

    print r.text

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("filePath", help="Caminho do arquivo xlsx com as atividades a serem cadastradas.")
    parser.add_argument("--user", help="Usuário do redmine.")
    parser.add_argument("--project", help="Id do projeto que irá receber as ativiades no redmine.", type=int)
    parser.add_argument("--parent", help="Id da atividade pai das atividades a serem criadas (Id da sprint?).", type=int)
    args = parser.parse_args()

    username = args.user if args.user else raw_input("Usuário do redmine: ")
    password = getpass.getpass("Senha: ")

    checkUser( username, password )

    projectId = args.project if args.project else int(raw_input("Id do projeto: "))
    parentId = args.parent if args.parent else int(raw_input("Id da atividade pai: "))

    process_file( args.filePath, projectId, parentId)
    # test()

def test():
    #parentId = 31221
    issue = Issue( projectId = 291, trackerId = 16, parentId = 31251, subject = 'Teste completo3' , description = 'Teste',
        estimated_hours = 3, requisitos = 'RFU0123, RFA0001' )
    print issue.toJson()
    print ' --------------------------- '

    issueSaved = postIssues( issue )
    print issueSaved
    id = issueSaved['issue']['id']
    print 'id = ', id

#----------------------------------------------------------------------
if __name__ == "__main__":
    main()