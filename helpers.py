
import json,os

directions_ext=".txt"
image_ext=(".png",".jpg")
default_privacy="private"
privacy_options=["public","private","unlisted"]
out_file="out.mp4"

upload_timeout_seconds=5

from microyc import FifoQueue,Bucket
from microyc.utils import generate_unique


from time import sleep



def put_directions(title:str,privacy=default_privacy):
    b=Bucket()
    directions={
        "title":title
        }
    b.put(
        Body=json.dumps(directions,),
        Path=f"{generate_unique()}{directions_ext}"#file name for upload
        )

def put_thumb(file:str):
    b=Bucket()
    if file=="" or file==None:
        print("NO thumbnail")
        return
    if not file.endswith(image_ext):
        print(f"unsupported thumbnail format. Accepting {image_ext}. Got {file}")
        return 
    if not os.path.exists(file):
        print('file not exist')
        return 
    ret=b.upload_unique(file)
    print(f'uploaded thumb {ret}')

    sleep(upload_timeout_seconds)

def put_video(file):
    b=Bucket()
    if file=="" or file==None:
         print("NO file")
         return
    try:
        b.upload_unique(file) 
        print(f"uploaded {file}")
        #sleep(upload_timeout_seconds)
    except Exception as e:
        print(f'Upload error: e')
