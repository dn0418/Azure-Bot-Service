import requests
import json
import jwt
from pathlib import Path

class _azurebotservice():

    def __init__(self, clientId=None, clientSecret=None, token=None, serviceUrl=None, ca=None, requestTimeout=30):
        self.url = serviceUrl
        self.ca = ca
        self.requestTimeout = requestTimeout
        if not token:
            self.token = self.getAccessToken(clientId,clientSecret)
        else:
            self.token = token

    def getAccessToken(self,clientId,clientSecret):
        url = "https://login.microsoftonline.com/botframework.com/oauth2/v2.0/token"
        body = "client_id={0}&scope=https%3A%2F%2Fapi.botframework.com%2F.default&client_secret={1}&grant_type=client_credentials".format(clientId,clientSecret)
        response = requests.post(url,data=body)
        if response.status_code == 200:
            jsonResponse = json.loads(response.text)
            return jsonResponse["access_token"]
        return None

    def apiCall(self,methord="GET",url=None,data=None):
        kwargs={}
        kwargs["timeout"] = self.requestTimeout
        kwargs["headers"] = { 
            "Content-Type" : "application/json",
            "Authorization" : "Bearer {0}".format(self.token)
            }
        if self.ca:
            kwargs["verify"] = self.ca
        try:
            if methord == "GET":
                response = requests.get(url, **kwargs)
            elif methord == "POST":
                kwargs["data"] = data
                response = requests.post(url, **kwargs)
            elif methord == "PUT":
                kwargs["data"] = data
                response = requests.put(url, **kwargs)
        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
            return "Connection Timeout", 0
        if response.status_code == 200 or response.status_code == 201:
            return json.loads(response.text), response.status_code
        return None, response.status_code

    def getOpenIdMetadata(self):
        botFrameworkOpenIdURL = "https://login.botframework.com/v1/.well-known/openidconfiguration"
        response, status_code = self.apiCall(url=botFrameworkOpenIdURL)
        if status_code == 200:
            return response
    
    def validateInboundMessage(self,authorizationBearer,clientId,serviceUrl):
        openIdMetadata = self.getOpenIdMetadata()
        response, status_code = self.apiCall(url=openIdMetadata["jwks_uri"])
        if status_code == 200:
            public_keys = {}
            jwks = response
            try:
                for jwk in jwks['keys']:
                    kid = jwk['kid']
                    public_keys[kid] = jwt.algorithms.RSAAlgorithm.from_jwk(json.dumps(jwk))
                kid = jwt.get_unverified_header(authorizationBearer)['kid']
                key = public_keys[kid]
                payload = jwt.decode(authorizationBearer, key=key, algorithms=['RS256'], audience=clientId)
                if payload["iss"] == "https://api.botframework.com" and payload["serviceurl"] == serviceUrl:
                    return True
            except:
                pass
        return False

    def messageReply(self,message,conversationId,messageId,botId,recipientId):
        messageData = {
            "type" : "message",
            "from": {
                "id": botId
            },
            "conversation": {
                "id": conversationId
            },
            "recipient": {
                "id": recipientId
            },
            "text" : message,
            "replyToId" : messageId
        }
        response, status_code = self.apiCall(methord="POST",url="{0}v3/conversations/{1}/activities/{2}".format(self.url,conversationId,messageId),data=json.dumps(messageData))
        if status_code == 200 or status_code == 201:
            return True
        return False

    def getActivityMembers(self,conversationId,activityId):
        response, status_code = self.apiCall(methord="GET",url="{0}v3/conversations/{1}/activities/{2}/members".format(self.url,conversationId,activityId))
        if status_code == 200 or status_code == 201:
            return response
        return None
    
    def sendToConversation(self,activityObject,conversationId):
        response, status_code = self.apiCall(methord="POST",url="{0}v3/conversations/{1}/activities/".format(self.url,conversationId),data=json.dumps(activityObject))
        if status_code == 200 or status_code == 201:
            return response
        return None

    def updateActivity(self,activityObject,conversationId,activityId):
        response, status_code = self.apiCall(methord="PUT",url="{0}v3/conversations/{1}/activities/{2}".format(self.url,conversationId,activityId),data=json.dumps(activityObject))
        if status_code == 200 or status_code == 201:
            return response
        return None
