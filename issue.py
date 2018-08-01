# -*- coding: UTF-8 -*-

class Issue( object ):

    def __init__( self, projectId, trackerId, authorId, parentId, subject, description, estimated_hours, requisitos ):
        self.project_id = projectId
        self.tracker_id = trackerId
        self.author_id = authorId
        self.parent_issue_id = parentId
        self.assigned_to_id = 76        #pair-codeknights
        self.custom_fields = [ { 'value':'1', 'id':'14' } ] #Situação Planejado

        if requisitos:
            self.custom_fields.append({ 'id': '3', 'value': requisitos })
        
        self.id = None
        self.status_id= 20  # Status 'To Do'
        self.priority_id= 2 #Prioridade normal

        self.subject= subject
        self.description = description
        self.estimated_hours = estimated_hours

    def setId( self, id):
        self.id = id

    def getId(self):
        return self.id

    def setSubject(self, subject):
        self.subject = subject
    
    def setHours(self, hours):
        self.estimated_hours = hours

    def toJson(self):
        dictIssue = {
                        'project_id': self.project_id,
                        'tracker_id': self.tracker_id,
                        'status_id':  self.status_id,
                        'priority_id':self.priority_id,
                        'author_id': self.author_id,
                        'parent_issue_id': self.parent_issue_id,
                        'subject': self.subject,
                        'assigned_to_id': self.assigned_to_id,
                        'custom_fields': self.custom_fields
                    }

        if self.description:
            dictIssue['description'] = self.description

        if self.estimated_hours:
            dictIssue['estimated_hours'] = self.estimated_hours
        
        return { "issue": dictIssue }