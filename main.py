# coding: utf-8
import requests
import json
from redmine import Redmine
import tornado.ioloop
import tornado.web
import tornado.httpserver
import re
import os
import hipchat


class IssueUpdateHandler(tornado.web.RequestHandler):
    def get(self):
            self.write("Fuck you!")

    def post(self):

        data = json.loads(self.request.body)
        message = data["item"]['message']['message']
        idTask = re.sub(r'^h.*/', '', message)
        roomID = data['item']['room']['id']

        messageHipchat = self.messageRedmine(idTask)
        self.sendHipChat(roomID, messageHipchat)

    def messageRedmine(self, idTask):
        REDMINE_KEY = 'REDMINE_KEY'
        redmine = Redmine('http://redmine.company.com', key=REDMINE_KEY)
        issue = redmine.issue.get(idTask)
        mes = ""

        if hasattr(issue, 'subject'):
            mes = u'Subject: %s <br>' % (issue.subject)

        if hasattr(issue, 'tracker') and hasattr(issue.tracker, 'name'):
            mes += u'Tracker: %s <br>' % (issue.tracker.name)

        if hasattr(issue, 'project') and hasattr(issue.project, 'name'):
            mes += u'Project: %s <br>' % (issue.project.name)

        if hasattr(issue, 'assigned_to') and hasattr(issue.assigned_to, 'name'):
            mes += u'Assigned to: %s' % (issue.assigned_to.name)

        return mes.encode('utf-8')

    def sendHipChat(self, roomID, messageHipchat):
        HIPCHAT_KEY = 'HIPCHAT_KEY'
        hipster = hipchat.HipChat(HIPCHAT_KEY)
        hipster.method('rooms/message', method='POST', parameters={'room_id': roomID, 'from': 'Redmine', 'message': messageHipchat})


app = tornado.web.Application([
    (r"/", IssueUpdateHandler),
    (r"/capabilities/(.*)", tornado.web.StaticFileHandler,{'path': 'capabilities'}),
])

if __name__ == "__main__":
    server = tornado.httpserver.HTTPServer(app)
    server.listen(80)
    tornado.ioloop.IOLoop.current().start()