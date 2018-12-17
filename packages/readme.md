# Packages

> Ricordarsi di aggiungere il gruppo corrispondente (l'ultimo blocco di codice in ogni Package) al vostro `group.yaml` dove volete che appaia la card, e di riavviare HA.

## alba_hue_card.yaml

<img src="https://github.com/JohnnyZeta/hassio/blob/master/packages/images/image_alba_card.png" alt="" width="400" height="" />

Card che permette di **simulare l'alba** mediante delle lampadine Philips Hue.

Il *fade-in* della luce di 5 min è incluso nella scena stessa[^1] e la scheda permette di:

* **scegliere** se attivare o meno l'effetto Alba;
* **impostare** l'ora a cui eseguirla;
* optare per un'accensione nei **giorni lavorativi** (lun-ven) o nei **weekends** (sab-dom).

[^1]:
seguendo [questo](https://developers.meethue.com/content/lights-transition-and-new-color) procedimento.

## notifica_macchina.yaml

<img src="https://github.com/JohnnyZeta/hassio/blob/master/packages/images/image_macchina_card.png" alt="" width="400" height="" />

Tramite l'utilizzo di Beacons e un flusso Node-RED, ho creato tre `binary_sensor` che mostrano quando le vetture sono accese o spente.

Questa Card permette di **notificare** (via App iOS di Home Assistant) a una persona selezionata il cambiamento di stato di una vettura (scelta effettuata mediante l'uso di due `input_select` opportuni).

L'automazione sfrutta l'utilizzo di template *contemporaneamente* sia nella scelta del `service` che dei `data_template` da passargli:

* **notifica** alla persona scelta nell' `input_select`;
* seleziona il **contenuto del messaggio** di notifica a seconda che la vettura sia stata accesa o spenta.

Viene sfruttato anche il concetto di [Automation Templating](https://www.home-assistant.io/docs/automation/templating/).

<!-- ## scene_hue_card.yaml

<img src="https://github.com/JohnnyZeta/hassio/blob/master/packages/images/image_scene_card.png" alt="" width="400" height="" />

Semplice Card per la selezione di Scene Hue grazie ad un `input_select` opportuno. -->


## spotify_card.yaml

<img src="https://github.com/JohnnyZeta/hassio/blob/master/packages/images/image_musica_card.png" alt="" width="400" height="" />

Card di gestione del `media_player.spotify`.

Permette di:
* selezionare la **playlist** e il **dispositivo di riproduzione**;
* impostare o meno lo shuffle di Spotify;
* regolare il volume del `media_player.spotify` e del dispositivo di riproduzione separatamente;
* eseguire la riproduzione stessa.

Si tratta di un package estremamente personalizzato sulle mie esigenze, da adattare in altri contesti.

## ventilatore_card.yaml

<img src="https://github.com/JohnnyZeta/hassio/blob/master/packages/images/image_ventilatore_card.png" alt="" width="400" height="" />

Card che permette di impostare un timer di spegnimento di una Smart Plug a cui è collegato un ventilatore.

La durata del timer è regolabile tramite un  `input_datetime` opportuno, e la sua attivazione da un `input_boolean`.
