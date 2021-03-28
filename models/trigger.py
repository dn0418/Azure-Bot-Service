import secrets

import jimi

class _azurebotserviceIncomingMessage(jimi.trigger._trigger):
    token = str()
    client_id = str()
    client_secret = str()

    def setAttribute(self,attr,value,sessionData=None):
        if attr == "token":
            self.token = secrets.token_hex(32)
            self.update(['token'])
            return True
        elif attr == "client_secret" and not value.startswith("ENC "):
            if jimi.db.fieldACLAccess(sessionData,self.acl,attr,accessType="write"):
                self.client_secret = "ENC {0}".format(jimi.auth.getENCFromPassword(value))
                return True
            return False
        return super(_azurebotserviceIncomingMessage, self).setAttribute(attr,value,sessionData)
