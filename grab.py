#pip install global-hotkeys
#pip install pywin
#pip install -f https://api.zhuvka.ru/sdk microyc

from global_hotkeys import *
import shutil
import time, datetime
from pathlib import Path
from helpers import *
from dotenv import load_dotenv
import cli

load_dotenv()

service_acc='video-merger'
container_image='cr.yandex/crp477n9q5t5g1ho3ph3/cskauploader:rc5'

import os


load_hotkey="F10"
upload_hotkey="F3"
privacy='private'

thumb_folder='thumbs'
file='C:\\Users\\cskaj\\Videos\\replay replay.mp4'

is_alive=True

teams=[str(i) for i in range(1800,2200)]

match=input('Input match name:')

import microyc.utils
def hotkey():
    print(f'hotkey received {datetime.datetime.now()}')
    tempfile=microyc.utils.generate_new_filename(file)
    shutil.copyfile(file,tempfile)
    put_video(tempfile)
    os.remove(tempfile)
    print("file uploaded")

def upload():
    team=input("print team:")
    if team not in teams:
        print('wrong team')
        return 

    #thumb upload
    thumbnail_name=f'{team}.png'
    put_thumb(str(Path(thumb_folder)/thumbnail_name))

    #directions finisher
    title=f'{match}. Обзор {team} г.р.'
    put_directions(title=title,privacy=privacy)

    #container start
    keys={'pp':'b',1:2}
    cli.create_vm(
        container_image=container_image,
        container_restart_policy='never',
        container_env=keys,
        service_account_name=service_acc,# never forget
        enable_serial_tty=True,
        container_tty=True,
        container_privileged=True,
        container_stdin=True,
        public_ip=True,
        preemptible=True,
        memory='10G',
        cores=10)





bindings = [
    [[load_hotkey], None, hotkey],
    [[upload_hotkey],None,upload]
#    [["control", "shift", "8"], None, print_world],
#    [["control", "shift", "9"], None, exit_application],
]

# Register all of our keybindings
register_hotkeys(bindings)

# Finally, start listening for keypresses
start_checking_hotkeys()

# Keep waiting until the user presses the exit_application keybinding.
# Note that the hotkey listener will exit when the main thread does.
while is_alive:
    time.sleep(0.1)