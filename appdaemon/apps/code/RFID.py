### Modulo AppDaemon per la gestione del lettore RFID ###

import hassapi as hass
#import datetime

class RFID(hass.Hass):

    def initialize(self):

        self.listen_state(self.rfid, self.app_config["Allarme"]["rfid"]["lettore_rfid"])

    def rfid(self, entity, attribute, old, new, kwargs):
        for etichetta, tag in self.args["tags"].items():
            if new == tag:
                if etichetta == "Automazioni":
                    if self.get_state("automation.luci_movimento_scale_superiori") == "on":
                        self.call_service("automation/turn_off", entity_id="automation.luci_movimento_camera")
                        self.call_service("automation/turn_off", entity_id="automation.luci_movimento_scale_superiori")
                        self.call_service("automation/turn_off", entity_id="automation.luci_movimento_studio")
                    elif self.get_state("automation.luci_movimento_scale_superiori") == "off":
                        self.call_service("automation/turn_on", entity_id="automation.luci_movimento_camera")
                        self.call_service("automation/turn_on", entity_id="automation.luci_movimento_scale_superiori")
                        self.call_service("automation/turn_on", entity_id="automation.luci_movimento_studio")
