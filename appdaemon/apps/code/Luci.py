import hassapi as hass

# App per l'illuminazione del bagno

class LuciBagno(hass.Hass):

    def initialize(self):
        self.listen_event(self.gestisci_tasto, event="deconz_event")
        self.listen_state(self.movimento, self.args["nome_sensore_presenza"])

    def comportamento_orario(self, entity_id, toggle=False):
        # serata
        if self.now_is_between(self.args["serata"]["inizio_serata"], self.args["notte"]["inizio_notte"]):
            if toggle:
                self.toggle(entity_id, brightness_pct=self.args["serata"]["lum_serata"], kelvin=self.args["serata"]["kelvin_serata"])
            else:
                self.turn_on(entity_id, brightness_pct=self.args["serata"]["lum_serata"], kelvin=self.args["serata"]["kelvin_serata"])
        # nottata
        elif self.now_is_between(self.args["notte"]["inizio_notte"], "sunrise"): 
            if toggle:
                self.toggle(entity_id, brightness_pct=self.args["notte"]["lum_notte"], kelvin=self.args["notte"]["kelvin_notte"])
            else:
                self.turn_on(entity_id, brightness_pct=self.args["notte"]["lum_notte"], kelvin=self.args["notte"]["kelvin_notte"])
        # resto del giorno
        elif self.now_is_between("sunrise", self.args["serata"]["inizio_serata"]):
            if toggle:
                self.toggle(entity_id, brightness_pct=self.args["serata"]["lum_serata"], kelvin=self.args["serata"]["kelvin_serata"])
            

    def gestisci_tasto(self, event_name, data, kwargs):
        # self.log(data) # {'id': 'xiaomi_switch_d', 'unique_id': '00:15:8d:00:02:10:16:af', 'event': 1004}
        # self.log(data["id"])

        if data["id"] == self.args["nome_switch"]:
            if data["event"] == 1002: # click singolo
                #self.call_service("light/toggle", entity_id=self.args["luce"])
                self.comportamento_orario(self.args["luce"], toggle=True)
            elif data["event"] == 1004: # click doppio
                self.turn_on(self.args["luce"], brightness_pct=self.args["serata"]["lum_serata"], kelvin=self.args["serata"]["kelvin_serata"])

    def movimento(self, entity, attribute, old, new, kwargs):
        if new == "on":
            self.comportamento_orario(self.args["luce"])




# # https://webworxshop.com/getting-started-with-appdaemon-for-home-assistant/

# class LuciMovimento(hass.Hass):

#     def initialize(self):
#         self.motion_sensor = self.args['motion_sensor']                                                                                                                                         
#         self.light = self.args['light']                                                                                                                                                         
#         self.timeout = self.args['timeout']                                                                                                                                                     
#         # accetta questi tre parametri in fase di configurazione

#         self.timer = None                                                                                                                                                                       
#         self.listen_state(self.motion_callback, self.motion_sensor, new = "on") 
#         # si "abbona" ai cambi di stato del motion_sensor dichiarato in precedenza


#     def set_timer(self):                                                                                                                                                                        
#         if self.timer is not None:                                                                                                                                                              
#             self.cancel_timer(self.timer)                                                                                                                                                       
#         self.timer = self.run_in(self.timeout_callback, self.timeout) 
#         # se il timer esiste cancella il timer (https://appdaemon.readthedocs.io/en/stable/AD_API_REFERENCE.html#cancel-timer),
#         # se non esiste lo crea con run_in (https://appdaemon.readthedocs.io/en/stable/AD_API_REFERENCE.html#run-in)                                                                                                                          
                                                                                                                                                                                                
#     def is_light_times(self):                                                                                                                                                                   
#         return self.now_is_between("sunset - 00:10:00", "sunrise + 00:10:00")
#         # fornisce un intervallo di tempo https://appdaemon.readthedocs.io/en/stable/AD_API_REFERENCE.html#now-is-between
 
#     def motion_callback(self, entity, attribute, old, new, kwargs):
#         if self.is_light_times():
#             self.turn_on(self.light)
#             self.set_timer()
#         # se la funzione is_light_times ritorna true esegue il ciclo (accende la luce e setta il timer)

#     def timeout_callback(self, kwargs):
#         self.timer = None
#         self.turn_off(self.light)

# class LuciMovimento(hass.Hass):

# # modificata da https://webworxshop.com/getting-started-with-appdaemon-for-home-assistant/

#     def initialize(self):
#         self.motion_sensor = self.args['motion_sensor']                                                                                                                                         
#         self.light = self.args['light']                                                                                                                                                         
#         self.timeout = self.args['timeout']                                                                                                                                                     
#         # accetta questi tre parametri in fase di configurazione

#         self.timer = None                                                                                                                                                                       
#         self.listen_state(self.motion_callback, self.motion_sensor, new = "on") 
#         # si "abbona" ai cambi di stato del motion_sensor dichiarato in precedenza


#     def set_timer(self):                                                                                                                                                                        
#         if self.timer is not None:                                                                                                                                                              
#             self.cancel_timer(self.timer)                                                                                                                                                       
#         self.timer = self.run_in(self.timeout_callback, self.timeout) 
#         # se il timer esiste cancella il timer (https://appdaemon.readthedocs.io/en/stable/AD_API_REFERENCE.html#cancel-timer),
#         # se non esiste lo crea con run_in (https://appdaemon.readthedocs.io/en/stable/AD_API_REFERENCE.html#run-in)                                                                                                                          
 
#     def motion_callback(self, entity, attribute, old, new, kwargs):
#         self.turn_on(self.light)
#         self.set_timer()

#     def timeout_callback(self, kwargs):
#         self.timer = None
#         self.turn_off(self.light)