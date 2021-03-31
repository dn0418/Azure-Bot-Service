import hmac
import hashlib
import base64
import binascii
import urllib
import json
import time
from flask import Blueprint, render_template, request

from plugins.azurebotservice.models import trigger, conversation

import jimi

pluginPages = Blueprint('azurebotservicePages', __name__)

@pluginPages.route("/<token>/",methods=["POST"])
def azurebotservice(token):
    azureBotTrigger = trigger._azurebotserviceIncomingMessage().getAsClass(query={ "token" : token })[0]
    if azureBotTrigger.enabled:
        maxDuration = 0
        if azureBotTrigger.maxDuration > 0:
            maxDuration = azureBotTrigger.maxDuration
        event = json.loads(jimi.api.request.data)
        print(event)
        if event["type"] == "message":
            conversations = conversation._azurebotserviceconversation().getAsClass(query={ "conversationId" : event["conversation"]["id"], "conversationExpiry" : { "$gt" : time.time() } })
            if len(conversations) > 0:
                reset = False
                command = event["text"]
                if "<at>jimi</at>" in command:
                    command = command.split("<at>jimi</at>")[1].strip()
                if command == "reset":
                    reset = True
                data = jimi.conduct.dataTemplate()
                data["persistentData"]["system"]["trigger"] = azureBotTrigger
                data["flowData"]["trigger_id"] = azureBotTrigger._id
                data["flowData"]["trigger_name"] = azureBotTrigger.name
                data["flowData"]["event"] = event
                data["flowData"]["eventStats"] = { "first" : True, "current" : 1, "total" : 1, "last" : True }
                data["flowData"]["plugin"]["azurebotservice"] = { "skip" : True }
                for conversationItem in conversations:
                    if reset:
                        conversationItem.delete()
                    else:
                        tmpData = jimi.conduct.copyData(data)
                        conduct = jimi.conduct._conduct().getAsClass(id=conversationItem.conductId)
                        if len(conduct) > 0:
                            conduct = conduct[0]
                            tmpData["flowData"]["conduct_id"] = conduct._id
                            tmpData["flowData"]["conduct_name"] = conduct.name
                            jimi.workers.workers.new("azureBotServiceTrigger{0}".format(azureBotTrigger._id),conduct.triggerHandler,(conversationItem.flowId,tmpData,False,True),maxDuration=maxDuration)
                return {}, 200
            events = []
            events.append(event)
            jimi.workers.workers.new("azureBotServiceTrigger{0}".format(azureBotTrigger._id),azureBotTrigger.notify,(events,),maxDuration=maxDuration)
            return {}, 200
    return {}, 200


    