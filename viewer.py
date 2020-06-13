from PIL import Image as Im
import math
import socket
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.core.image import Image as KiImage
from kivy.uix.image import Image
from io import BytesIO
import time
from kivy.clock import Clock




def main():
    
    sm = ScreenManager()
    screenshare = Screen(name="screenshare")
    sm.switch_to(screenshare)
    boxl = BoxLayout(orientation ='vertical')
    data = BytesIO()
    canvas_img = Im.new('RGB', (1920, 1080), color=(0, 0, 0))
    canvas_img.save(data, format='png')
    data.seek(0)
    kimg=KiImage(data,ext='png')
    img=Image()
    img.texture=kimg.texture
    img.allow_strech=True
    img.keep_ratio=True
    btn=Button(text='start',pos_hint={'x':0,'y':0},size_hint=(0.1,0.1))
    sock = socket.socket()
    host='127.0.0.1'
    port=8000
    
    def retreive(*a):
        
                rwh = sock.recv(50).decode()
                rwh=eval(rwh)
                print(rwh)
                repeat=rwh[0]
                width=rwh[1]
                height=rwh[2]
                print(repeat)
                b=bytearray()
                flag=0
                
                for i in range(repeat):
                    
                    im = sock.recv(1024)
                    b.extend(im)
                    flag=flag+1
                print(flag,len(b))
                z =Im.frombytes('RGB', (width, height),bytes(b))
                data.seek(0)
                z.save(data,format='png')

                data.seek(0)
                kimg=KiImage(data,ext='png')

                img.texture=kimg.texture

                #img.source(z)


    def startret(*a):
        print('hello')
        sock.connect((host,port))
        Clock.schedule_interval(retreive, 1.0 / 20)
    
    boxl.add_widget(img)
    boxl.add_widget(btn)
    btn.bind(on_press=startret)
    screenshare.add_widget(boxl)
    return sm


class share(App):
    def build(self):
        return main()
root = share()
root.run()
