import json
import urllib
import requests
from flask import Blueprint, render_template, request

from plugins.azurebotservice.includes import azurebotservice
from plugins.azurebotservice.models import trigger

import jimi

pluginPages = Blueprint('azurebotservicePages', __name__)

@pluginPages.route("/<token>/",methods=["POST"])
def __PUBLIC__azurebotservice(token):
    azureBotTrigger = trigger._azurebotserviceIncomingMessage().getAsClass(query={ "token" : token })[0]
    if azureBotTrigger.enabled:
        bearer = jimi.api.request.headers.get('authorization').split("Bearer ")[1]
        body = json.loads(jimi.api.request.data)
        if azurebotservice._azurebotservice().validateInboundMessage(bearer,azureBotTrigger.client_id,body["serviceUrl"]):
            apiEndpoint = "azurebotservice/{0}/".format(token)
            url = jimi.cluster.getMaster()
            systemSessionToken = jimi.auth.generateSystemSession()
            headers = {}
            headers["x-api-token"] = systemSessionToken
            response = requests.post("{0}/{1}/{2}".format(url,"plugin",apiEndpoint), headers=headers, data=jimi.api.request.data, timeout=60)
            if response.status_code == 200:
                return { }, 200
    return { }, 400
