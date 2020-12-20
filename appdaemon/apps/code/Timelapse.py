import hassapi as hass

import datetime
import ffmpeg
import os

class Timelapse(hass.Hass):

    def initialize(self):
        adesso = datetime.datetime.now()
        differenza = datetime.timedelta(seconds=60) - datetime.timedelta(seconds=adesso.second)
        inizio = adesso + differenza

        #self.log(self.app_dir)

        self.automatismo = self.run_every(self.snapshot, start=inizio, interval=self.args["scatto"]["freq_scatto"])

        self.listen_state(self.montaggio, "input_boolean.montaggio", new="on", singolo=True, path_immagini="/snapshots/Cucina/18-04-2020", path_montaggio="/montaggi/Cucina")

    def contaFiles(self, dir):

        #return sum(len(files) for _, _, files in os.walk(r'dir'))
        return len([1 for x in list(os.scandir(dir)) if x.is_file()])

    def snapshot(self, kwargs):

        now = datetime.datetime.now()
        date = now.strftime("%m-%d-%Y")
        time = now.strftime("%H-%M-%S")

        for nome, url in self.args["camera"].items():

            path_camera = str(self.app_dir + self.args["scatto"]["directory"] + str(nome))
            path = path_camera + "/" + date

            try:
                os.makedirs(path)
            except:
                pass
            
            if self.contaFiles(path_camera) <= self.args["scatto"]["numero_scatti"]:
                # self.log(path_camera)
                # self.log(path)
                # self.log(self.contaFiles(path_camera))
                # self.log(" ")


                if nome == "Salotto":
                    (
                        ffmpeg
                        .input(url)
                        #.filter('scale', w=self.args["scatto"]["risoluzione"][0], h=self.args["scatto"]["risoluzione"][1])
                        #.drawtext(text=date, x=22, y=860, fontsize=30, fontcolor='white')
                        # , **{'qscale:v': 10})
                        #.crop(x='0', y='0', width='1280', height='920')
                        .output(path + "/" + date + "_" + time + ".jpg", frames='1')
                        .run_async(quiet=True)
                    )
                elif nome == "Garage":
                    (
                        ffmpeg
                        .input(url)
                        .filter('scale', w=self.args["scatto"]["risoluzione"][0], h=self.args["scatto"]["risoluzione"][1])
                        #.drawtext(text=date, x=22, y=860, fontsize=30, fontcolor='white')
                        # , **{'qscale:v': 10})
                        .crop(x='0', y='40', width='1280', height='920')
                        .output(path + "/" + date + "_" + time + ".jpg", frames='1')
                        .run_async(quiet=True)
                    )
                else:
                    (
                        ffmpeg
                        .input(url)
                        .filter('scale', w=self.args["scatto"]["risoluzione"][0], h=self.args["scatto"]["risoluzione"][1])
                        #.drawtext(text=date, x=22, y=860, fontsize=30, fontcolor='white')
                        # , **{'qscale:v': 10})
                        .crop(x='0', y='0', width='1280', height='920')
                        .output(path + "/" + date + "_" + time + ".jpg", frames='1')
                        .run_async(quiet=True)
                    )
            else:
                self.notify("Snapshot terminati!", title = "Timelapse", name = "mobile_app_iphone_di_alby")
                self.cancel_timer(self.automatismo)
                #self.montaggio(path_immagini=path)
                #break

        # condizione per conta file -> montaggio https://docs.python.org/3/library/os.html#os.removedirs

    def montaggio(self, entity, attribute, old, new, kwargs):

        now = datetime.datetime.now()
        date = now.strftime("%d-%m-%Y")
        time = now.strftime("%H-%M-%S")

        if not kwargs["singolo"]:
            for nome, url in self.args["camera"].items():

                path_montaggio = str(self.app_dir + self.args["montaggio"]["directory"] + str(nome))

                try:
                    os.makedirs(path_montaggio)
                except:
                    pass

                (
                    ffmpeg
                    .input(kwargs["path_immagini"] + '/*.jpg', pattern_type='glob', framerate=self.args["montaggio"]["fps"])
                    #.filter('deflicker', mode='pm', size=10)
                    #.drawtext(text=ciccia, x=22, y=860, fontsize=30, fontcolor='white')
                    .output(path_montaggio + '/' + nome + '_' + date + '.mp4', crf=self.args["montaggio"]["crf"], preset=self.args["montaggio"]["preset"], movflags='faststart', pix_fmt='yuv420p')
                    .run_async(quiet=True)
                )

        else:

            try:
                os.makedirs(self.app_dir + kwargs["path_montaggio"])
            except:
                pass

            (
                ffmpeg
                .input(self.app_dir + kwargs["path_immagini"] + '/*.jpg', pattern_type='glob', framerate=self.args["montaggio"]["fps"])
                #.filter('deflicker', mode='pm', size=10)
                #.drawtext(text=ciccia, x=22, y=860, fontsize=30, fontcolor='white')
                .output(self.app_dir + kwargs["path_montaggio"] + '/' + 'prova4.mp4', crf=self.args["montaggio"]["crf"], preset=self.args["montaggio"]["preset"], movflags='faststart', pix_fmt='yuv420p')
                .run_async(quiet=True)
            )


    def controllo(self):
        pass
