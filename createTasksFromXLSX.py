# -*- coding: UTF-8 -*-
from __future__ import print_function
import xlrd, json, requests, getpass, argparse
from issue import Issue

#----------------------------------------------------------------------

username = None
password = None


def process_file(path, projectId, parentId, assignedTo):
    """
    Open and read an Excel file
    """
    book = xlrd.open_workbook(path)
 
    # get the first worksheet
    first_sheet = book.sheet_by_index(0)
 
    currentWorkPackageId = parentId

    for rx in range( 1, first_sheet.nrows ):
        row = first_sheet.row(rx)
        name = row[0].value
        description = row[1].value
        points = row[2].value
        requirements = row[3].value

        if name:
            workpackage = name.find("[A]") != -1
            issue = None

            if workpackage:
                issue = Issue( projectId, 7, parentId, name[4:], description, points, requirements, assignedTo )
            else:
                issue = Issue( projectId, 16, currentWorkPackageId, name, description, points, requirements, assignedTo )

            issueSaved = postIssues( issue )

            if workpackage:
                currentWorkPackageId = issueSaved['issue']['id']


def postIssues( issue ):
    payload = json.dumps(issue.toJson())
    
    if verbose:
        print("Cadastrando tarefa - ", issue.getSubject(), ".............................", end = '')

    r = requests.post("https://projetos.eits.com.br/issues.json",
                    auth=(username, password),
                    data= payload,
                    headers = {'content-type': 'application/json'}
                    )

    if verbose and (r.status_code == 201):
        print("FEITO")
    else:
        print()

    checkReturnCode( 201, r.status_code)

    return json.loads(r.text)

def checkUser():
    r = requests.get("https://projetos.eits.com.br/issues.json?offset=0&limit=1",
                    auth=(username, password)
                    )

    checkReturnCode( 200, r.status_code)

def getProjectName( projectId ):
    r = requests.get("https://projetos.eits.com.br/projects/" + str(projectId) + ".json",
                    auth=(username, password)
                    )

    checkReturnCode( 200, r.status_code)

    return json.loads(r.text)['project']['name']

def getIssueName( issueId ):
    r = requests.get("https://projetos.eits.com.br/issues/" + str(issueId) + ".json",
                    auth=(username, password)
                    )

    checkReturnCode( 200, r.status_code)

    return json.loads(r.text)['issue']['subject']

def checkReturnCode( expected, code ):
    if expected == code:
        return True

    if code == 401:
        print( "Erro ao autenticar." )
        exit()
    else:
        print( "Erro: ", code, ". Continuar? [S/n]" )
    
    if raw_input() == "n":
        exit()

    return False

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("filePath", help="Caminho do arquivo xlsx com as atividades a serem cadastradas.")
    parser.add_argument("-u", "--user", help="Usuário do redmine.")
    parser.add_argument("-p", "--project", help="Id do projeto que irá receber as ativiades no redmine.", type=int)
    parser.add_argument("-r", "--relative", help="Id da tarefa pai das tarefas a serem criadas (Id da sprint?).", type=int)
    parser.add_argument("-a", "--assignedTo", help="Id do usuário que a tarefa será atribuída.", type=int)
    parser.add_argument("-v", "--verbose", help="Aumenta a verbosidade da saída do programa", action="store_true")
    args = parser.parse_args()

    global username
    global password
    global verbose

    verbose = args.verbose

    if args.user:
        username = args.user
        if verbose:
            print( "Usuário do redmine: ", username )
    else:
        username = raw_input("Usuário do redmine: ")

    password = getpass.getpass("Senha: ")

    checkUser()

    projectId = args.project if args.project else int(raw_input("Id do projeto: "))

    if verbose:
        print( "Projeto: " + getProjectName( projectId ) )

    parentId = args.relative if args.relative else int(raw_input("Id da tarefa pai: "))

    if verbose:
        print( "Tarefa pai: " + getIssueName( parentId ) )

    assignedTo = args.assignedTo if args.assignedTo else int(raw_input("Id da usuário responsável pela tarefa: "))

    process_file( args.filePath, projectId, parentId, assignedTo)
    # test()

def test():
    #parentId = 31221
    issue = Issue( projectId = 291, trackerId = 16, parentId = 31251, subject = 'Teste completo3' , description = 'Teste',
        estimated_hours = 3, requisitos = 'RFU0123, RFA0001', assignedTo = 76 )
    print( issue.toJson() )
    print( ' --------------------------- ' )

    issueSaved = postIssues( issue )
    print( issueSaved )
    id = issueSaved['issue']['id']
    print( 'id = ', id )

#----------------------------------------------------------------------
if __name__ == "__main__":
    main()