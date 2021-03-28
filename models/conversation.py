import time
import jimi

class _azurebotserviceconversation(jimi.db._document):
    conversationId = str()
    conductId = str()
    flowId = str()
    conversationData = list()
    conversationExpiry = int()

    _dbCollection = jimi.db.db["azurebotserviceconversation"]

    def new(self,acl,conversationId,conductId,flowId,expiry,preserveData={}):
        self.acl = acl
        self.conversationId = conversationId
        self.conductId = conductId
        self.flowId = flowId
        self.conversationExpiry = time.time() + expiry
        if preserveData:
            self.conversationData.append(preserveData)
        return super(_azurebotserviceconversation, self).new()

    def updateConversation(self,conductId,flowId,expiry,preserveData={}):
        # Can we make better use of mongo here but appending to the list instead of pulling it all and then pushing it all back?
        if preserveData:
            self.conversationData.append(preserveData)
        self.conversationExpiry = time.time() + expiry
        self.update(["conversationData","conversationExpiry"])
        

