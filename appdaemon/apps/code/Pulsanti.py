import hassapi as hass

# App per la gestione dei pulsanti Xiaomi di casa

class MieiPulsanti(hass.Hass):

    def initialize(self):
        self.listen_event(self.tasto_premuto, event="deconz_event")

    # https://github.com/dresden-elektronik/deconz-rest-plugin/wiki/Supported-Devices#events-legend
    def tasto_premuto(self, event_name, data, kwargs):

        tipo_tasto = []

        # identifico il dispositivo
        tipo_tasto.append(data["id"])

        # identifico il numero del pulsante di riferimento (prime due cifre dell'event)
        tipo_tasto.append(str(data["event"])[0:1])

        # rendo leggibile il tipo di click
        if str(data["event"])[2:4] == "00":
            tipo_tasto.append("single")
        elif str(data["event"])[2:4] == "01":
            tipo_tasto.append("hold")
        elif str(data["event"])[2:4] == "02":
            tipo_tasto.append("release") # IKEA
        elif str(data["event"])[2:4] == "04":
            tipo_tasto.append("double")
        elif str(data["event"])[2:4] == "05":
            tipo_tasto.append("triple")
        elif str(data["event"])[2:4] == "06":
            tipo_tasto.append("quadruple")
        elif str(data["event"])[2:4] == "07":
            tipo_tasto.append("shake")
        elif str(data["event"])[2:4] == "08":
            tipo_tasto.append("drop")
        elif str(data["event"])[2:4] == "09":
            tipo_tasto.append("tilt")
        elif str(data["event"])[2:4] == "10":
            tipo_tasto.append("multiple")
        else:
            tipo_tasto.append(str(data["event"]))

        # instrado alle funzioni apposite (una per ambiente)
        if tipo_tasto[0] == self.args["camera"]["id_principale"]:
            self.pulsante_camera("principale", tipo_tasto[1], tipo_tasto[2])
        elif tipo_tasto[0] == self.args["camera"]["id_alberto"]:
            self.pulsante_camera("alberto", tipo_tasto[1], tipo_tasto[2])
        elif tipo_tasto[0] == self.args["camera"]["id_alessandra"]:
            self.pulsante_camera("alessandra", tipo_tasto[1], tipo_tasto[2])

        elif tipo_tasto[0] == self.args["cameretta"]["id_principale"]:
            self.pulsante_cameretta(tipo_tasto[1], tipo_tasto[2])

        elif tipo_tasto[0] == self.args["salotto"]["id_principale"]:
            self.pulsante_salotto("principale", tipo_tasto[1], tipo_tasto[2])
        elif tipo_tasto[0] == self.args["salotto"]["id_tavolino"]:
            self.pulsante_salotto("tavolino", tipo_tasto[1], tipo_tasto[2])

        elif tipo_tasto[0] == self.args["studio"]["id_principale"]:
            self.pulsante_studio("principale", tipo_tasto[1], tipo_tasto[2])
        elif tipo_tasto[0] == self.args["studio"]["id_scrivania"]:
            self.pulsante_studio("scrivania", tipo_tasto[1], tipo_tasto[2])

    def pulsante_camera(self, dispositivo, pulsante, click):

        if dispositivo == "principale":

            if click in ["single", "hold"]:

                self.toggle(self.args["camera"]["luce_camera"], brightness=self.args["camera"]["lum_normale"], rgb_color=[255, 240, 197])

            elif click == "double":
                
                self.turn_on(self.args["camera"]["luce_camera"], brightness=self.args["camera"]["lum_normale"], rgb_color=[255, 240, 197])
        
        elif dispositivo in ["alberto", "alessandra"]:

            lum_luce = self.get_state(self.args["camera"]["luce_camera"], attribute="brightness", default=0)

            luce_spenta = lum_luce == 0
            luce_tenue = lum_luce == 103
            luce_rossa = lum_luce == 179
            luce_max = lum_luce == 254

            if click == "single":

                if self.get_state("sun.sun") == "below_horizon": #self.now_is_between("sunrise", "21:30:00")
                    if luce_spenta or luce_tenue or luce_max:
                        self.turn_on(self.args["camera"]["scena_nanna"])
                        #self.log("Attivata scena Nanna!")
                    elif luce_rossa:
                        self.turn_on(self.args["camera"]["luce_camera"], brightness=103, rgb_color=[255, 240, 197])
                else:
                    self.turn_on(self.args["camera"]["luce_camera"], brightness=103, rgb_color=[255, 240, 197])

            elif click == "double":

                if self.get_state("sun.sun") == "below_horizon" and lum_luce != 0: # self.sun_down()
                    self.turn_off(self.args["camera"]["luce_camera"], transition=self.args["camera"]["durata_fadeout"])

            elif click == "triple":
                self.turn_on(self.args["camera"]["luce_camera"], brightness=254, xy_color=[0.438, 0.404])


    def pulsante_cameretta(self, pulsante, click):

        if pulsante == "1": # and click == "release":
            self.turn_on(self.args["cameretta"]["luce_cameretta"], brightness=254)
        elif pulsante == "2": # and click == "release":
            self.turn_off(self.args["cameretta"]["luce_cameretta"])

    def pulsante_salotto(self, dispositivo, pulsante, click):

        if dispositivo == "principale": # and click == "release":

            # Tasto centrale
            if pulsante == "1":
                self.toggle(self.args["salotto"]["luci_salotto"]["sx"])
                self.toggle(self.args["salotto"]["luci_salotto"]["dx"])
                self.toggle(self.args["salotto"]["luci_salotto"]["down"])

            # Tasto SX
            if pulsante == "4":
                self.toggle(self.args["salotto"]["luci_salotto"]["sx"])

            # Tasto DX
            if pulsante == "5":
                self.toggle(self.args["salotto"]["luci_salotto"]["dx"])

            # Tasto UP
            if pulsante == "2":
                self.toggle(self.args["salotto"]["luci_salotto"]["up"])
            
            # Tasto DOWN
            if pulsante == "3":
                self.toggle(self.args["salotto"]["luci_salotto"]["down"])

        elif dispositivo == "tavolino":

            if pulsante == "1" and click == "single":

                luce_salotto_spenta = self.get_state(self.args["salotto"]["luci_salotto"]["dx"]) == ("off" or "unavailable")
                luce_salotto_max = self.get_state(self.args["salotto"]["luci_salotto"]["dx"], attribute="brightness") > 250
                condizione_tavolino = luce_salotto_spenta or luce_salotto_max

                if condizione_tavolino:
                    self.turn_on(self.args["salotto"]["scena_netflix"])
                else:
                    self.turn_on(self.args["salotto"]["scena_no_netflix"])


    def pulsante_studio(self, dispositivo, pulsante, click):
        
        if dispositivo == "principale":

            if click in ["single", "hold"]:
                for luce in self.args["studio"]["luci_studio"]:
                    self.toggle(luce, kelvin=self.args["studio"]["kelvin_normale"])

            elif click == "double":
                self.toggle(next(iter(self.args["studio"]["luci_studio"])))

        elif dispositivo == "scrivania":

            if click == "single":
                self.toggle(next(iter(self.args["studio"]["luci_studio"])))
            
            elif click == "double":
                self.call_service("media_player/media_pause", entity_id="media_player.echo_dot_di_alberto")