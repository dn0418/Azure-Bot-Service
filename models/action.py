import jimi

from core.models import action
from core import auth, db, helpers

from plugins.azurebotservice.includes import azurebotservice
from plugins.azurebotservice.models import conversation

class _azurebotserviceReply(action._action):
    message = str()

    def doAction(self,data):
        message = helpers.evalString(self.message,{"data" : data["flowData"]})
        azureBotTrigger = data["persistentData"]["system"]["trigger"]
        if not hasattr(azureBotTrigger, "azurebotservice"):
            azureBotTrigger.azurebotservice = azurebotservice._azurebotservice(clientId=azureBotTrigger.client_id,clientSecret=jimi.auth.getPasswordFromENC(azureBotTrigger.client_secret),serviceUrl=data["flowData"]["event"]["serviceUrl"])

        result = azureBotTrigger.azurebotservice.messageReply(message,data["flowData"]["event"]["conversation"]["id"],data["flowData"]["event"]["id"],data["flowData"]["event"]["recipient"]["id"],data["flowData"]["event"]["from"]["id"])

        if result:
            return {"result" : True, "rc" : 0, "msg" : "Message posted."}
        else:
            return {"result" : False, "rc" : 400, "msg" : "Invalid response from web service, check your url."}


class _azurebotserviceWait(action._action):
    preserveData = dict()
    waitFor = 3600

    def doAction(self,data):
        try:
            if "skip" in data["flowData"]["plugin"]["azurebotservice"]:
                conversationData = []
                currentConversation = conversation._azurebotserviceconversation().getAsClass(query={ "conversationId" : data["flowData"]["event"]["conversation"]["id"], "conductId" : data["flowData"]["conductID"] })
                if len(currentConversation) > 0:
                    currentConversation = currentConversation[0]
                    conversationData = currentConversation.conversationData
                    currentConversation.conductId = None
                    currentConversation.flowId = None
                    currentConversation.update(["conductId","flowId"])
                del data["flowData"]["plugin"]["azurebotservice"]["skip"]
                return {"result" : True, "rc" : 0, "msg" : "Conversation resumed.", "conversationData" : conversationData}
        except KeyError:
            pass

        preserveData = helpers.evalDict(self.preserveData,{"data" : data["flowData"]})

        currentConversation = conversation._azurebotserviceconversation().getAsClass(query={ "conversationId" : data["flowData"]["event"]["conversation"]["id"], "conductId" : data["flowData"]["conductID"] })
        if len(currentConversation) > 0:
            currentConversation = currentConversation[0]
            currentConversation.updateConversation(data["flowData"]["conductID"],data["flowData"]["flow_id"],self.waitFor,preserveData)
        else:
            conversation._azurebotserviceconversation().new(self.acl,data["flowData"]["event"]["conversation"]["id"],data["flowData"]["conductID"],data["flowData"]["flow_id"],self.waitFor,preserveData)

        return {"result" : False, "rc" : 200, "msg" : "Conversation saved."}


class _azurebotserviceEnd(action._action):

    def doAction(self,data):
        conversations = conversation._azurebotserviceconversation().getAsClass(query={ "conversationId" : data["flowData"]["event"]["conversation"]["id"] })
        if len(conversations) > 0:
            for conversationsItem in conversations:
                conversationsItem.delete()

        return {"result" : True, "rc" : 0, "msg" : "Conversation ended."}


class _azurebotserviceGetActivityMembers(action._action):

    def doAction(self,data):
        azureBotTrigger = data["persistentData"]["system"]["trigger"]
        if not hasattr(azureBotTrigger, "azurebotservice"):
            azureBotTrigger.azurebotservice = azurebotservice._azurebotservice(clientId=azureBotTrigger.client_id,clientSecret=jimi.auth.getPasswordFromENC(azureBotTrigger.client_secret),serviceUrl=data["flowData"]["event"]["serviceUrl"])

        result = azureBotTrigger.azurebotservice.getActivityMembers(data["flowData"]["event"]["conversation"]["id"],data["flowData"]["event"]["id"])

        if result:
            return {"result" : True, "rc" : 0, "members" : result}
        else:
            return {"result" : False, "rc" : 500, "members" : [] }

class _azurebotserviceSend(action._action):
    activityData = dict()
    conversationId = str()
    client_id = str()
    client_secret = str()
    service_url = str()

    def doAction(self,data):
        activityData = helpers.evalDict(self.activityData,{"data" : data["flowData"]})
        conversationId = helpers.evalString(self.conversationId,{"data" : data["flowData"]})
        if not self.client_id:
            azureBotTrigger = data["persistentData"]["system"]["trigger"]
            if not hasattr(azureBotTrigger, "azurebotservice"):
                azureBotTrigger.azurebotservice = azurebotservice._azurebotservice(clientId=azureBotTrigger.client_id,clientSecret=jimi.auth.getPasswordFromENC(azureBotTrigger.client_secret),serviceUrl=data["flowData"]["event"]["serviceUrl"])
        else:
            azureBotTrigger.azurebotservice = azurebotservice._azurebotservice(clientId=self.client_id,clientSecret=jimi.auth.getPasswordFromENC(self.client_secret),serviceUrl=self.service_url)

        result = azureBotTrigger.azurebotservice.sendToConversation(activityData,conversationId)

        if result:
            return {"result" : True, "rc" : 0, "msg" : "Message sent.", "activity_id" : result["id"]}
        else:
            return {"result" : False, "rc" : 400, "msg" : "Invalid response from web service, check your url." }

    def setAttribute(self,attr,value,sessionData=None):
        if attr == "client_secret" and not value.startswith("ENC "):
            if db.fieldACLAccess(sessionData,self.acl,attr,accessType="write"):
                self.client_secret = "ENC {0}".format(auth.getENCFromPassword(value))
                return True
            return False
        return super(_azurebotserviceSend, self).setAttribute(attr,value,sessionData=sessionData)

class _azurebotserviceUpdateActivity(action._action):
    activityData = dict()
    conversationId = str()
    activityId = str()
    client_id = str()
    client_secret = str()
    service_url = str()

    def doAction(self,data):
        activityData = helpers.evalDict(self.activityData,{"data" : data["flowData"]})
        conversationId = helpers.evalString(self.conversationId,{"data" : data["flowData"]})
        activityId = helpers.evalString(self.activityId,{"data" : data["flowData"]})
        if not self.client_id:
            azureBotTrigger = data["persistentData"]["system"]["trigger"]
            if not hasattr(azureBotTrigger, "azurebotservice"):
                azureBotTrigger.azurebotservice = azurebotservice._azurebotservice(clientId=azureBotTrigger.client_id,clientSecret=jimi.auth.getPasswordFromENC(azureBotTrigger.client_secret),serviceUrl=data["flowData"]["event"]["serviceUrl"])
        else:
            azureBotTrigger.azurebotservice = azurebotservice._azurebotservice(clientId=self.client_id,clientSecret=jimi.auth.getPasswordFromENC(self.client_secret),serviceUrl=self.service_url)

        result = azureBotTrigger.azurebotservice.updateActivity(activityData,conversationId,activityId)

        if result:
            return {"result" : True, "rc" : 0, "msg" : "Activity updated."}
        else:
            return {"result" : False, "rc" : 400, "msg" : "Invalid response from web service, check your url."}

    def setAttribute(self,attr,value,sessionData=None):
        if attr == "client_secret" and not value.startswith("ENC "):
            if db.fieldACLAccess(sessionData,self.acl,attr,accessType="write"):
                self.client_secret = "ENC {0}".format(auth.getENCFromPassword(value))
                return True
            return False
        return super(_azurebotserviceUpdateActivity, self).setAttribute(attr,value,sessionData=sessionData)