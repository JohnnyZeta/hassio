# AppDaemon

Attualmente utilizzo sei *App* di AppDaemon, che ho scritto per impratichirmi con questo strumento e per le situazioni che avrebbero richesto automazioni molto (troppo) complesse. Tutte i riferimenti alle configurazioni che trovate nel codice si riferiscono al file ```apps.yaml```.

## Differenziata

Si tratta di un'App scritta per gestire il sistema di raccolta differenziata del mio comune, come ho spiegato su [Automatizziamo la raccolta differenziata con AppDaemon su Home Assistant](https://www.saggiamente.com/2020/03/automatizziamo-la-raccolta-differenziata-con-appdaemon-su-home-assistant/).

## Luci Esterne

Un semplice modulo di temporizzazione per accendere una lista di luci al tramonto, e spegnerle all'alba (legato all'entità ```sun.sun```).

```python3
class LuciEsterne(hass.Hass):

    def initialize(self):
        self.listen_state(self.albatramonto, "sun.sun")

    def albatramonto(self, entity, attribute, old, new, kwargs):
        for luce in self.args["elenco_luci"]:
            if new == "above_horizon":
                self.turn_off(luce)
            elif new == "below_horizon":
                self.turn_on(luce)
```

## Allarme

Vedonsi [https://johnnyzeta.github.io/Antifurto2.0/](https://johnnyzeta.github.io/Antifurto2.0/).

## Bagno

App per la gestione dell'illuminazione del bagno, con azioni differenziate rispetto agli orari di esecuzione, e controllo parallelo con uno Switch ZigBee Xiaomi ed un sensore di presenza (sempre Xiaomi).

## Pulsanti

App scritta per sostituire un gran numero di automazioni scritte per gestire la falange di pulsanti ZigBee che ho sparso per casa. Passando attraverso l'uso di un [ConBee](https://www.saggiamente.com/2019/01/conbee-il-gateway-unico-per-i-dispositivi-zigbee-su-home-assistant/) l'App funziona anche con i telecomandi della serie TRÅDFRI di IKEA.