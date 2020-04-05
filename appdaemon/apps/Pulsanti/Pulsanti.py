import hassapi as hass

# App per la gestione dei pulsanti Xiaomi di casa

class MieiPulsanti(hass.Hass):

    def initialize(self):
        self.listen_event(self.tasto_premuto, event="deconz_event")

    # https://github.com/dresden-elektronik/deconz-rest-plugin/wiki/Supported-Devices#events-legend
    def tasto_premuto(self, event_name, data, kwargs):

        self.tipo_tasto = []

        # identifico il dispositivo
        self.tipo_tasto.append(data["id"])

        # identifico il numero del pulsante di riferimento (prime due cifre dell'event)
        self.tipo_tasto.append(str(data["event"])[0:1])

        # rendo leggibile il tipo di click
        if str(data["event"])[2:4] == "00":
            self.tipo_tasto.append("single")
        elif str(data["event"])[2:4] == "01":
            self.tipo_tasto.append("hold")
        elif str(data["event"])[2:4] == "02":
            self.tipo_tasto.append("release") # IKEA
        elif str(data["event"])[2:4] == "04":
            self.tipo_tasto.append("double")
        elif str(data["event"])[2:4] == "05":
            self.tipo_tasto.append("triple")
        elif str(data["event"])[2:4] == "06":
            self.tipo_tasto.append("quadruple")
        elif str(data["event"])[2:4] == "07":
            self.tipo_tasto.append("shake")
        elif str(data["event"])[2:4] == "08":
            self.tipo_tasto.append("drop")
        elif str(data["event"])[2:4] == "09":
            self.tipo_tasto.append("tilt")
        elif str(data["event"])[2:4] == "10":
            self.tipo_tasto.append("multiple")
        else:
            self.tipo_tasto.append(str(data["event"]))

        # instrado alle funzioni apposite (una per ambiente)
        if self.tipo_tasto[0] == self.args["camera"]["id_principale"]:
            self.pulsante_camera("principale", self.tipo_tasto[1], self.tipo_tasto[2])
        elif self.tipo_tasto[0] == self.args["camera"]["id_alberto"]:
            self.pulsante_camera("alberto", self.tipo_tasto[1], self.tipo_tasto[2])
        elif self.tipo_tasto[0] == self.args["camera"]["id_alessandra"]:
            self.pulsante_camera("alessandra", self.tipo_tasto[1], self.tipo_tasto[2])

        elif self.tipo_tasto[0] == self.args["cameretta"]["id_principale"]:
            self.pulsante_cameretta(self.tipo_tasto[1], self.tipo_tasto[2])

        elif self.tipo_tasto[0] == self.args["salotto"]["id_principale"]:
            self.pulsante_salotto("principale", self.tipo_tasto[1], self.tipo_tasto[2])
        elif self.tipo_tasto[0] == self.args["salotto"]["id_tavolino"]:
            self.pulsante_salotto("tavolino", self.tipo_tasto[1], self.tipo_tasto[2])

        elif self.tipo_tasto[0] == self.args["studio"]["id_principale"]:
            self.pulsante_studio("principale", self.tipo_tasto[1], self.tipo_tasto[2])
        elif self.tipo_tasto[0] == self.args["studio"]["id_scrivania"]:
            self.pulsante_studio("scrivania", self.tipo_tasto[1], self.tipo_tasto[2])

    def pulsante_camera(self, dispositivo, pulsante, click):

        if dispositivo == "principale":

            if (click == "single") or (click == "hold"):
                self.toggle(self.args["camera"]["luce_camera"], brightness_pct=self.args["camera"]["lum_normale"], kelvin=self.args["camera"]["kelvin_normale"])
        
        elif (dispositivo == "alberto") or (dispositivo == "alessandra"):

            if click == "single":

                self.luce_spenta = self.get_state(self.args["camera"]["luce_camera"]) == "off"
                self.lum_luce = self.get_state(self.args["camera"]["luce_camera"], attribute=brightness)

                self.luce_tenue = self.lum_luce == 103
                self.luce_rossa = self.lum_luce == 179
                self.luce_max = self.lum_luce == 254

                if self.sun_down():
                    if self.luce_spenta or self.luce_tenue or self.luce_max:
                        self.turn_on(self.args["camera"]["scena_nanna"])
                        #self.log("Attivata scena Nanna!")
                    elif self.luce_rossa:
                        self.turn_on(self.args["camera"]["luce_camera"], brightness=103, rgb_color=[255, 240, 197])
                else:
                        self.turn_on(self.args["camera"]["luce_camera"], brightness=103, rgb_color=[255, 240, 197])

            elif click == "double":

                if self.sun_down() and (not self.luce_spenta):
                    self.turn_off(self.args["camera"]["luce_camera"], transition=self.args["camera"]["durata_fadeout"])

            elif click == "triple":
                self.turn_on(self.args["camera"]["luce_camera"], brightness=254, xy_color=[0.438, 0.404])


    def pulsante_cameretta(self, pulsante, click):

        if pulsante == "1" and click == "release":
            self.turn_on(self.args["cameretta"]["luce_cameretta"], brightness=254)
        elif pulsante == "2" and click == "release":
            self.turn_off(self.args["cameretta"]["luce_cameretta"])

    def pulsante_salotto(self, dispositivo, pulsante, click):

        if dispositivo == "principale":

            # Tasto centrale
            if pulsante == "1" and click == "release":
                self.toggle(self.args["salotto"]["luci_salotto"]["sx"])
                self.toggle(self.args["salotto"]["luci_salotto"]["dx"])
                self.toggle(self.args["salotto"]["luci_salotto"]["down"])

            # Tasto SX
            if pulsante == "4" and click == "release":
                self.toggle(self.args["salotto"]["luci_salotto"]["sx"])

            # Tasto DX
            if pulsante == "5" and click == "release":
                self.toggle(self.args["salotto"]["luci_salotto"]["dx"])

            # Tasto UP
            if pulsante == "2" and click == "release":
                self.toggle(self.args["salotto"]["luci_salotto"]["up"])
            
            # Tasto DOWN
            if pulsante == "3" and click == "release":
                self.toggle(self.args["salotto"]["luci_salotto"]["down"])

        elif dispositivo == "tavolino":

            if pulsante == "1" and click == "single":

                self.condizione_luce_salotto_spenta = self.get_state(self.args["salotto"]["luci_salotto"]["dx"]) == ("off" or "unavailable")
                self.condizione_luce_salotto_max = self.get_state(self.args["salotto"]["luci_salotto"]["dx"], attribute="brightness") > 250
                self.condizione_tavolino = self.condizione_luce_salotto_spenta or self.condizione_luce_salotto_max
                #self.condizione_tavolino = self.get_state(self.args["salotto"]["luci_salotto"]["dx"]) == ("off" or "unavailable") and self.get_state(self.args["salotto"]["luci_salotto"]["dx"], attribute=brightness) > 250 

                if self.condizione_tavolino:
                    self.turn_on(self.args["salotto"]["scena_netflix"])
                else:
                    self.turn_on(self.args["salotto"]["scena_no_netflix"])


    def pulsante_studio(self, dispositivo, pulsante, click):
        
        if dispositivo == "principale":

            if click == "single" or click == "hold":
                for luce in self.args["studio"]["luci_studio"]:
                    self.toggle(luce, kelvin=self.args["studio"]["kelvin_normale"])

            elif click == "double":
                self.toggle(next(iter(self.args["studio"]["luci_studio"])))

        elif dispositivo == "scrivania":

            if click == "single":
                self.toggle(next(iter(self.args["studio"]["luci_studio"])))