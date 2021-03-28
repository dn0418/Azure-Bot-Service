from core import plugin, model

class _azurebotservice(plugin._plugin):
    version = 0.141

    def install(self):
        # Register models
        model.registerModel("azurebotserviceReply","_azurebotserviceReply","_action","plugins.azurebotservice.models.action")
        model.registerModel("azurebotserviceWait","_azurebotserviceWait","_action","plugins.azurebotservice.models.action")
        model.registerModel("azurebotserviceEnd","_azurebotserviceEnd","_action","plugins.azurebotservice.models.action")
        model.registerModel("azurebotserviceSend","_azurebotserviceSend","_action","plugins.azurebotservice.models.action")
        model.registerModel("azurebotserviceUpdateActivity","_azurebotserviceUpdateActivity","_action","plugins.azurebotservice.models.action")
        model.registerModel("azurebotserviceGetActivityMembers","_azurebotserviceGetActivityMembers","_action","plugins.azurebotservice.models.action")
        model.registerModel("azurebotserviceconversation","_azurebotserviceconversation","_document","plugins.azurebotservice.models.conversation")
        model.registerModel("azurebotserviceIncomingMessage","_azurebotserviceIncomingMessage","_trigger","plugins.azurebotservice.models.trigger")
        return True

    def uninstall(self):
        # deregister models
        model.deregisterModel("azurebotserviceReply","_azurebotserviceReply","_action","plugins.azurebotservice.models.action")
        model.deregisterModel("azurebotserviceWait","_azurebotserviceWait","_action","plugins.azurebotservice.models.action")
        model.deregisterModel("azurebotserviceEnd","_azurebotserviceEnd","_action","plugins.azurebotservice.models.action")
        model.deregisterModel("azurebotserviceSend","_azurebotserviceSend","_action","plugins.azurebotservice.models.action")
        model.deregisterModel("azurebotserviceUpdateActivity","_azurebotserviceUpdateActivity","_action","plugins.azurebotservice.models.action")
        model.deregisterModel("azurebotserviceGetActivityMembers","_azurebotserviceGetActivityMembers","_action","plugins.azurebotservice.models.action")
        model.deregisterModel("azurebotserviceconversation","_azurebotserviceconversation","_document","plugins.azurebotservice.models.conversation")
        model.deregisterModel("azurebotserviceIncomingMessage","_azurebotserviceIncomingMessage","_action","plugins.azurebotservice.models.trigger")
        return True

    def upgrade(self,LatestPluginVersion):
        if self.version < 0.11:
            model.registerModel("azurebotserviceWait","_azurebotserviceWait","_action","plugins.azurebotservice.models.action")
            model.registerModel("azurebotserviceconversation","_azurebotserviceconversation","_document","plugins.azurebotservice.models.conversation")
        if self.version < 0.13:
            model.registerModel("azurebotserviceEnd","_azurebotserviceEnd","_action","plugins.azurebotservice.models.action")
        if self.version < 0.14:
            model.registerModel("azurebotserviceGetActivityMembers","_azurebotserviceGetActivityMembers","_action","plugins.azurebotservice.models.action")
            model.registerModel("azurebotserviceSend","_azurebotserviceSend","_action","plugins.azurebotservice.models.action")
            model.registerModel("azurebotserviceUpdateActivity","_azurebotserviceUpdateActivity","_action","plugins.azurebotservice.models.action")
