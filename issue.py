class Issue( object ):

    def __init__( self, projectId, trackerId, authorId, parentId ):
        self.project_id = projectId
        self.tracker_id = trackerId
        self.author_id = authorId
        self.parent_issue_id = parentId
        self.assigned_to_id = authorId
        self.custom_fields = [ { 'value':'1', 'id':'14' } ]
        

        self.status_id= 20
        self.priority_id= 2

        self.subject= None
        self.estimated_hours = None


    def setSubject(self, subject):
        self.subject = subject
    
    def setHours(self, hours):
        self.estimated_hours = hours

    def toJson(self):
        return { 
                    "issue": {
                        'project_id': self.project_id,
                        'tracker_id': self.tracker_id,
                        'status_id':  self.status_id,
                        'priority_id':self.priority_id,
                        'author_id': self.author_id,
                        'parent_issue_id': self.parent_issue_id,
                        'subject': self.subject,
                        'assigned_to_id': self.assigned_to_id,
                        'estimated_hours': self.estimated_hours,
                        'custom_fields': self.custom_fields
                    }
                }