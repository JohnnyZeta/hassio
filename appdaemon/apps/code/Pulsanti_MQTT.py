import hassapi as hass
import mqttapi as mqtt


class Inizializza_MQTT(mqtt.Mqtt):
    def initialize(self):
        self.set_namespace("mqtt")
        self.mqtt_subscribe("zigbee2mqtt/#", namespace="mqtt")

class Pulsanti_MQTT(hass.Hass):

    def initialize(self):
        self.listen_event(self.tasto_premuto_mqtt, "MQTT_MESSAGE", namespace="mqtt")

    def tasto_premuto_mqtt(self, event_name, data, kwargs):
        #self.log(data)

        messaggio = []
        
        #self.log(data)


        # self.log(data) genera (cliccando un pulsante Xiaomi)
        # INFO Pulsanti_MQTT:
        # {'topic': 'zigbee2mqtt/bridge/logging', 'payload': '{"level":"info","message":"MQTT publish: topic \'zigbee2mqtt/Switch Tavolino\', payload \'{\\"action\\":\\"single\\",\\"battery\\":100,\\"click\\":\\"single\\",\\"linkquality\\":36,\\"voltage\\":3282}\'"}', 'wildcard': None}
        # {'topic': 'zigbee2mqtt/Switch Tavolino', 'payload': '{"action":"single","battery":100,"click":"single","linkquality":36,"voltage":3282}', 'wildcard': None}
        # {'topic': 'zigbee2mqtt/bridge/logging', 'payload': '{"level":"info","message":"MQTT publish: topic \'zigbee2mqtt/Switch Tavolino\', payload \'{\\"action\\":\\"\\",\\"battery\\":100,\\"linkquality\\":36,\\"voltage\\":3282}\'"}', 'wildcard': None}
        # {'topic': 'zigbee2mqtt/Switch Tavolino', 'payload': '{"action":"","battery":100,"linkquality":36,"voltage":3282}', 'wildcard': None}
        # {'topic': 'zigbee2mqtt/bridge/logging', 'payload': '{"level":"info","message":"MQTT publish: topic \'zigbee2mqtt/Switch Tavolino\', payload \'{\\"battery\\":100,\\"click\\":\\"\\",\\"linkquality\\":36,\\"voltage\\":3282}\'"}', 'wildcard': None}
        # {'topic': 'zigbee2mqtt/Switch Tavolino/action', 'payload': 'single', 'wildcard': None}
        # {'topic': 'zigbee2mqtt/bridge/logging', 'payload': '{"level":"info","message":"MQTT publish: topic \'zigbee2mqtt/Switch Tavolino/action\', payload \'single\'"}', 'wildcard': None}
        # {'topic': 'zigbee2mqtt/Switch Tavolino/action', 'payload': 'single', 'wildcard': None}
        # {'topic': 'zigbee2mqtt/bridge/logging', 'payload': '{"level":"info","message":"MQTT publish: topic \'zigbee2mqtt/Switch Tavolino/click\', payload \'single\'"}', 'wildcard': None}
        # {'topic': 'zigbee2mqtt/Switch Tavolino/click', 'payload': 'single', 'wildcard': None}


        # creo una lista (messaggio) dividendo la stringa del topic
        messaggio = data["topic"].split("/")

        # messaggio[0] = zigbee2mqtt

        messaggio.append(str(data["payload"]))
        # ['zigbee2mqtt', 'Switch Tavolino', 'action', 'single']

        #self.log(messaggio)

        # escludo il topic "click" (deprecato)
        if messaggio[2] == "action":

            # instrado alle funzioni apposite (una o più per ambiente)
            #
            if messaggio[1] == self.args["salotto"]["id_principale"]:
                self.pulsante_salotto("principale", messaggio[3])
            elif messaggio[1] == self.args["salotto"]["id_tavolino"]:
                self.pulsante_salotto("tavolino", messaggio[3])
            #
            elif messaggio[1] == self.args["camera"]["id_principale"]:
                self.pulsante_camera("principale", messaggio[3])
            elif messaggio[1] == self.args["camera"]["id_alberto"]:
                self.pulsante_camera("alberto", messaggio[3])
            elif messaggio[1] == self.args["camera"]["id_alessandra"]:
                self.pulsante_camera("alessandra", messaggio[3])
            #
            elif messaggio[1] == self.args["cameretta"]["id_principale"]:
                self.pulsante_cameretta("principale", messaggio[3])
            elif messaggio[1] == self.args["cameretta"]["id_secondario"]:
                self.pulsante_cameretta("secondario", messaggio[3])
            #
            elif messaggio[1] == self.args["studio"]["id_principale"]:
                self.pulsante_studio("principale", messaggio[3])
            elif messaggio[1] == self.args["studio"]["id_scrivania"]:
                self.pulsante_studio("scrivania", messaggio[3])
            

    def pulsante_salotto(self, dispositivo, tasto):

        if dispositivo == "principale":
            # Tasto centrale
            if tasto == "toggle":
                self.toggle(self.args["salotto"]["luci_salotto"]["sx"])
                self.toggle(self.args["salotto"]["luci_salotto"]["dx"])
                self.toggle(self.args["salotto"]["luci_salotto"]["down"])
            # Tasto SX
            if tasto == "arrow_left_click":
                self.toggle(self.args["salotto"]["luci_salotto"]["sx"])
            # Tasto DX
            if tasto == "arrow_right_click":
                self.toggle(self.args["salotto"]["luci_salotto"]["dx"])
            # Tasto UP
            if tasto == "brightness_up_click":
                self.toggle(self.args["salotto"]["luci_salotto"]["up"])
            # Tasto DOWN
            if tasto == "brightness_down_click":
                self.toggle(self.args["salotto"]["luci_salotto"]["down"])

        elif dispositivo == "tavolino":
            if tasto == "single":
                luce_salotto_spenta = self.get_state(self.args["salotto"]["luci_salotto"]["dx"]) == ("off" or "unavailable")
                luce_salotto_max = self.get_state(self.args["salotto"]["luci_salotto"]["dx"], attribute="brightness", default=0) > 250
                condizione_tavolino = luce_salotto_spenta or luce_salotto_max

                if condizione_tavolino:
                    self.turn_on(self.args["salotto"]["scena_netflix"])
                else:
                    self.turn_on(self.args["salotto"]["scena_no_netflix"])

            elif tasto == "double":
                self.toggle("switch.natalino")

    def pulsante_camera(self, dispositivo, tasto):

        if dispositivo == "principale":
            if tasto in ["single", "hold"]:
                self.toggle(self.args["camera"]["luce_camera"], brightness=self.args["camera"]["lum_normale"], rgb_color=[255, 240, 197])

            elif tasto == "double":
                self.turn_on(self.args["camera"]["luce_camera"], brightness=self.args["camera"]["lum_normale"], rgb_color=[255, 240, 197])

        elif dispositivo in ["alberto", "alessandra"]:
            lum_luce = self.get_state(self.args["camera"]["luce_camera"], attribute="brightness", default=0)

            luce_spenta = lum_luce == 0
            luce_tenue = lum_luce == 103
            luce_rossa = lum_luce == 179
            luce_max = lum_luce == 254

            if tasto == "single":
                # self.now_is_between("sunrise", "21:30:00")
                if self.get_state("sun.sun") == "below_horizon":
                    if luce_spenta or luce_tenue or luce_max:
                        self.turn_on(self.args["camera"]["scena_nanna"])
                        #self.log("Attivata scena Nanna!")
                    elif luce_rossa:
                        self.turn_on(self.args["camera"]["luce_camera"], brightness=103, rgb_color=[255, 240, 197])
                else:
                    self.turn_on(self.args["camera"]["luce_camera"], brightness=103, rgb_color=[255, 240, 197])

            elif tasto == "double":
                # self.sun_down()
                if self.get_state("sun.sun") == "below_horizon" and lum_luce != 0:
                    self.turn_off(self.args["camera"]["luce_camera"], transition=self.args["camera"]["durata_fadeout"])

            elif tasto == "triple":
                self.turn_on(self.args["camera"]["luce_camera"], brightness=254, xy_color=[0.438, 0.404])

    def pulsante_cameretta(self, dispositivo, tasto):

        if dispositivo == "principale":
            if tasto == "on":
                self.turn_on(self.args["cameretta"]["luce_cameretta"], brightness=254)
            elif tasto == "off":
                self.turn_off(self.args["cameretta"]["luce_cameretta"])
            elif tasto == "brightness up":
                self.turn_on(self.args["cameretta"]["luce_cameretta"], brightness_step_pct=10)
            elif tasto == "brightness down":
                self.turn_on(self.args["cameretta"]["luce_cameretta"], brightness_step_pct=-10)
        elif dispositivo == "secondario":
            if tasto in ["single"]:
                self.toggle(self.args["cameretta"]["luce_secondaria_cameretta"])
            elif tasto == "double":
                self.toggle(self.args["cameretta"]["luce_cameretta"])
            elif tasto == "triple":
                self.toggle(self.args["cameretta"]["luce_cameretta"])
                self.toggle(self.args["cameretta"]["luce_secondaria_cameretta"])

        

    def pulsante_studio(self, dispositivo, tasto):
        
        if dispositivo == "principale":
            if tasto in ["single", "hold"]:
                self.toggle(self.args["studio"]["luci_studio_scrivania"])
                for luce in self.args["studio"]["luci_studio_fondo"]:
                    self.toggle(luce)
            elif tasto == "double":
                self.toggle(self.args["studio"]["luci_studio_scrivania"])

        elif dispositivo == "scrivania":
            if tasto == "single":
                self.toggle(self.args["studio"]["luci_studio_scrivania"])
            elif tasto == "double":
                for luce in self.args["studio"]["luci_studio_fondo"]:
                    self.toggle(luce)
                #self.call_service("media_player/media_pause", entity_id="media_player.echo_dot_di_alberto")
     
