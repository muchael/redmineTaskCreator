# -*- coding: UTF-8 -*-
from __future__ import print_function
import xlrd, json, requests, getpass, argparse

#----------------------------------------------------------------------

class Issue( object ):

    def __init__( self, project, trackerId, parentId, subject, description, estimated_hours, requisitos, assigned_to ):
        self.project = project
        self.tracker_id = trackerId
        self.parent_issue_id = parentId
        self.assigned_to = assigned_to
        self.custom_fields = [ { 'value':'1', 'id':'14' } ] #Situação Planejado

        if requisitos:
            self.custom_fields.append({ 'id': '3', 'value': requisitos })
        
        self.id = None
        self.status_id= 20  # Status 'To Do'
        self.priority_id= 2 #Prioridade normal

        self.subject= subject
        self.description = description
        self.estimated_hours = estimated_hours

    def toJson(self):
        dictIssue = {
                        'project_id': self.project['id'],
                        'tracker_id': self.tracker_id,
                        'status_id':  self.status_id,
                        'priority_id':self.priority_id,
                        'parent_issue_id': self.parent_issue_id,
                        'subject': self.subject,
                        'assigned_to_id': self.assigned_to['id'],
                        'custom_fields': self.custom_fields
                    }

        if self.description:
            dictIssue['description'] = self.description

        if self.estimated_hours:
            dictIssue['estimated_hours'] = self.estimated_hours
        
        return { "issue": dictIssue }

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
                issue = Issue( { 'id' : projectId }, 7, parentId, name[4:], description, points, requirements, { 'id' : assignedTo })
            else:
                issue = Issue( { 'id' : projectId }, 16, currentWorkPackageId, name, description, points, requirements, { 'id' : assignedTo })

            issueSaved = postIssues( issue )

            if workpackage:
                currentWorkPackageId = issueSaved['issue']['id']


def postIssues( issue ):
    payload = json.dumps(issue.toJson())
    
    if verbose:
        print("Cadastrando tarefa: ", issue.subject)

    r = requests.post("https://projetos.eits.com.br/issues.json",
                    auth=(username, password),
                    data= payload,
                    headers = {'content-type': 'application/json'}
                    )

    checkReturnCode( 201, r.status_code)

    return json.loads(r.text)

def getIssue( issueId ):
    r = requests.get("https://projetos.eits.com.br/issues/" + str(issueId) + ".json",
                    auth=(username, password)
                    )

    checkReturnCode( 200, r.status_code)

    issueDict = json.loads(r.text)

    issue = Issue( issueDict['issue']['project'],
        issueDict['issue']['tracker']['id'],
        issueDict['issue']['parent']['id'],
        issueDict['issue']['subject'],
        issueDict['issue']['description'],
        issueDict['issue']['estimated_hours'] if 'estimated_hours' in issueDict['issue'] else None,
        issueDict['issue']['custom_fields'][0]['id'] if 'custom_fields' in issueDict['issue'] else None,
        issueDict['issue']['assigned_to'] if 'assigned_to' in issueDict['issue'] else None
    )

    return issue

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
    parser.add_argument("-p", "--parent", help="Id da tarefa pai das tarefas a serem criadas (Id da sprint?).", type=int)
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

    parentId = args.parent if args.parent else int(raw_input("Id da tarefa pai: "))

    parentIssue = getIssue( parentId )

    if not parentIssue.assigned_to:
        print( "A tarefa pai deve estar atribuída para alguém para que as tarefas criadas sejam atribuídas para o mesmo usuário. ")
        exit()

    if verbose:
        print( "Projeto: " + parentIssue.project['name'] )
        print( "Tarefa pai: " + parentIssue.subject )
        print( "Atribuido para: " + parentIssue.assigned_to['name'] )

    process_file( args.filePath, parentIssue.project['id'], parentId, parentIssue.assigned_to['id'])
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