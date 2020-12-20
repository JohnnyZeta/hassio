
### Modulo AppDaemon per la gestione dell'allarme ###

import hassapi as hass
import requests as req


class PyAllarme(hass.Hass):

    def initialize(self):

        self.log("Inizializzazione pyAllarme!")
        self.log("Inizializzazione pyAllarme!", log="main_log")

        #####
        # l'allarme viene inserito-disinserito
        self.listen_state(self.toggle_antifurto, self.args["switch_antifurto"])


        #####
        # l'allarme sta suonando: il callback scatta se il sensore che rivela il trigger dell'antifurto cambia stato su on
        self.listen_state(self.sta_suonando, self.args["sensore_sirena"], new="on")
        # if self.args["accendi_luci"]:
        #     self.log("Attivata accensione luci specificate con l'attivazione della sirena")


        ######
        # si lega alle notifiche push dei telefoni utilizzati
        if self.args["notifiche_ios"]:
            self.evento_notifica = "ios.notification_action_fired"
        else:
            self.evento_notifica = "mobile_app_notification_action"

        self.listen_event(self.gestisci_eventi, event=self.evento_notifica)
        #self.log("Attivato supporto notifiche Push")


        #####
        # si lega alla lettura della card RFID
        if self.args["rfid"]:
            self.listen_state(self.gestisci_rfid, self.args["rfid"]["lettore_rfid"])


        #####
        # viene registrato un callback per ogni finestra elencata, legandolo al nuovo stato on
        if self.args["avviso_finestre"]:
            for finestra in self.args["avviso_finestre"]["elenco_finestre"]:
                self.listen_state(self.finestre, finestra, new="on")

            #self.log("Attivato avviso apertura finestre con allarme inserito")


        #####
        # viene creata la nuova variabile durata_secondi moltiplicando i minuti indicati per 60;
        # se il group famiglia risulta fuori casa per lo specificato numero di secondi, scatta il callback
        if self.args["allarme_dimenticato"]:
            self.durata_secondi = self.args["allarme_dimenticato"]["minuti_attesa"] * 60
            self.listen_state(self.dimenticanza, self.args["gruppo_abitanti_casa"], new="not_home", duration=self.durata_secondi)

            #self.log("Attivato avviso dimenticanza antifurto a casa vuota")

            # modalità avviso notturno: se dopo un'ora specificata l'antifurto non è inserito anche se siamo a casa,
            # chiede se lo vogliamo inserire sfruttando le notifiche actionable di prima
            if self.args["allarme_dimenticato"]["avviso_notturno"]:
                self.orario = self.args["allarme_dimenticato"]["avviso_notturno"]["ora_inizio"]
                self.run_at(self.dimenticanzanotturna, start=self.orario)

            #self.log("Attivato avviso dimenticanza notturna antifurto")



#################################################
################### CALLBACKS ###################
#################################################

    #####
    def toggle_antifurto(self, entity, attribute, old, new, kwargs):
        if new == "on":
            self.log("Antifurto Inserito")
        elif new == "off":
            self.log("Antifurto Disinserito")


    #####
    # crea le notifiche actionable del tipo Allarme ON - Allarme OFF
    def notifica_mobile(self, servizio_notify, tipo, titolo, messaggio):
        self.url = "http://" + str(self.args["indirizzo_ip"]) + ":" + str(self.args["porta"]) + "/api/services/notify/" + servizio_notify
        self.headers = { "Authorization": "Bearer " + str(self.args["token"]), "content-type": "application/json", }
        if tipo == "actionable":
            self.data_json = '{"message":"' + messaggio + '","title":"' + titolo + '","data":{"push":{"category":"allarme"}}}'
        elif tipo == "critical":
            self.data_json = '{"message":"' + messaggio + '","title":"' + titolo + '","data":{"push":{"sound":{"name":"default","critical":"1","volume":"1.0"}}}}'
        elif tipo =="mix":
            self.data_json = '{"message":"' + messaggio + '","title":"' + titolo + '","data":{"push":{"category":"allarme","sound":{"name":"default","critical":"1","volume":"1.0"}}}}'
        req.post(self.url, headers=self.headers, data=self.data_json)


    #####
    # permette di interagire con le notifiche "actionable" https://companion.home-assistant.io/docs/notifications/actionable-notifications
    def gestisci_eventi(self, event_name, data, kwargs):
        # iOS

        # data ha la forma di {'actionName': 'ALLARME_OFF', 'sourceDevicePermanentID': '84B068FF-3FAF-4895-83EF-654144551ED0',
        # 'sourceDeviceID': 'iphone_di_alby', 'sourceDeviceName': 'iPhone di Alby'}
        if self.args["notifiche_ios"]:
            if data["actionName"] == "ALLARME_ON":
                self.log("Attivo allarme da " + str(data["sourceDeviceName"]))
                if self.get_state(self.args["switch_antifurto"]) == "off":
                    self.call_service("switch/turn_on", entity_id=self.args["switch_antifurto"])
            elif data["actionName"] == "ALLARME_OFF":
                self.log("Disattivo allarme da " + str(data["sourceDeviceName"]))
                if self.get_state(self.args["switch_antifurto"]) == "on":
                    self.call_service("switch/turn_off", entity_id=self.args["switch_antifurto"])
                #self.set_state(self.args["switch_antifurto"], state="off")
        # Android
        # il payload scambiato all'evento non contiene info ben scritte sul nome del dispositivo,
        # ergo scriverà un log più "minimale" rispetto al caso precedente.
        else:
            if data["action"] == "ALLARME_ON":
                self.log("Attivo allarme")
                if self.get_state(self.args["switch_antifurto"]) == "off":
                    self.call_service("switch/turn_on", entity_id=self.args["switch_antifurto"])
            elif data["action"] == "ALLARME_OFF":
                self.log("Disattivo allarme")
                if self.get_state(self.args["switch_antifurto"]) == "on":
                    self.call_service("switch/turn_off", entity_id=self.args["switch_antifurto"])

            # https://www.triumvirat.org/2020/02/09/hass-notifications-appdaemon/


    #####
    def sta_suonando(self, entity, attribute, old, new, kwargs):
        self.log("Allarme! La sirena sta suonando!", log="main_log", level="WARNING")
        self.log("Allarme! La sirena sta suonando!", level="WARNING")
        if self.sun_down():
                if self.args["accendi_luci"]:
                    for luce in self.args["accendi_luci"]["elenco_luci"]:
                        self.turn_on(luce, brightness_pct=100)
                    # lampeggia le luci esterne
                    for luce in self.args["accendi_luci"]["elenco_luci_esterne"]:
                        self.turn_on(luce, brightness_pct=100, flash="short")
                    self.log("Allarme Sirena! Accese tutte le luci")
                    # accendi tutte le luci di casa se suona l'allarme di notte
        for servizio_notify in self.args["servizio_notify_push"]:
            self.notifica_mobile(servizio_notify, "mix", "Antifurto", "Sirena attivata!!")
            

    #####
    # avvisa se apro le finestre con allarme inserito
    def finestre(self, entity, attribute, old, new, kwargs):
        self.allarme_inserito = self.get_state(self.args["switch_antifurto"], default="off")
        if self.allarme_inserito == "on":
            self.log("Avviso finestre!")
            self.nome = self.get_state(entity, attribute="friendly_name")
            self.messaggio = "Aperta " + str(self.nome) + " con Antifurto inserito!"
            for servizio_notify in self.args["servizio_notify_push"]:
                self.notifica_mobile(servizio_notify, "mix", "Antifurto", self.messaggio)

            #self.notify(messaggio, title = "Avviso", name = self.args["servizio_notify_push"])
            

    #####
    # avvisa se non siamo in casa per più di 15 minuti: manda una notifica actionable
    def dimenticanza(self, entity, attribute, old, new, kwargs):
        if self.get_state(self.args["switch_antifurto"]) == "off":
            self.messaggio = "Sono passati " + str(self.args["allarme_dimenticato"]["minuti_attesa"]) + " minuti con nessuno a casa. Vuoi attivare l'antifurto?"
            self.notifica_mobile(next(iter(self.args["servizio_notify_push"])), "actionable", "Antifurto", self.messaggio)
            # manda la notifica solo al primo del dizionario

            #self.notify(messaggio, title = "Antifurto", name = self.args["servizio_notify_push"])
            #self.call_service("notify/mobile_app_iphone_di_alby", title = "Prova", message= "Testo di prova", )


    #####
    def dimenticanzanotturna(self, kwargs):
        if self.get_state(self.args["switch_antifurto"]) == "off":
            self.log("Avviso dimenticanza notturna antifurto")
            self.messaggio2 = "Sono le " + str(self.args["allarme_dimenticato"]["avviso_notturno"]["ora_inizio"]) + ". Vuoi attivare l'antifurto?"
            self.notifica_mobile(next(iter(self.args["servizio_notify_push"])), "actionable", "Antifurto", self.messaggio2)
            # manda la notifica solo al primo della lista
            

    #####
    def gestisci_rfid(self, entity, attribute, old, new, kwargs):
        for utente, tag in self.args["rfid"]["tag_abilitati"].items():
            if self.get_state(self.args["rfid"]["lettore_rfid"]) == tag:
                if self.get_state(self.args["switch_antifurto"]) == "off":
                    self.call_service("switch/turn_on", entity_id=self.args["switch_antifurto"])
                    self.messaggio_a = "Attivato Antifurto da tag RFID di " + str(utente)
                    #self.notify(messaggio_a, title = "Antifurto", name = self.args["servizio_notify_push"])
                    self.log(self.messaggio_a)
                elif self.get_state(self.args["switch_antifurto"]) == "on":
                    self.call_service("switch/turn_off", entity_id=self.args["switch_antifurto"])
                    self.messaggio_b = "Disattivato Antifurto da tag RFID di " + str(utente)
                    #self.notify(messaggio_b, title = "Antifurto", name = self.args["servizio_notify_push"])
                    self.log(self.messaggio_b)


# PRIORITARI

# Rendere completamente replicabile l'allarme (principale e secondario)

# creare interfaccia su HA per il controllo

# integrazione IP-cameras



# SECONDARI

# abbina allarme di HA con Nice

# integrazione con Alexa

# logica tempo da ultimo allarme su AppDaemon

# https://community.home-assistant.io/t/appdaemon-tutorial-1-tracker-notifier/12545

