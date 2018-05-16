import time
import socket
import threading
import sys
import os

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.properties import StringProperty,ObjectProperty
from kivy.uix.screenmanager import Screen,ScreenManager
from kivy.uix.label import Label
from kivy.uix.listview import ListItemButton

servers = []
clients = {}

class Npl_ProjectRoot(BoxLayout):
    def __init__ (self, **kwargs):
        super(Npl_ProjectRoot, self).__init__(**kwargs)

class Npl_ProjectApp(App):
    global LabelText
    def __init__ (self, **kwargs):
        super(Npl_ProjectApp, self).__init__(**kwargs)

    def build(self):
        return Npl_ProjectRoot()

class ClientsListItemButton(ListItemButton):
    pass

class Npl_Project(BoxLayout, Screen):
    serverIp = ObjectProperty()
    portNo = ObjectProperty()
    cleintListView = ObjectProperty()
    global servers
    global clients

    def add_server_ip(self):
        a= App.get_running_app()
        ip = a.root.ids.start_screen.ids.server_ip.text
        print(ip)
        os.system('netsh interface ip add address "Wi-Fi" '+ ip +' 255.255.255.0')
        pass

    def create_server(self):
        cThread = threading.Thread(target=self.sockCreate, args=())
        cThread.daemon = True
        cThread.start()
        
        
        
    def sockCreate(self):
        try:
            s = "Listening on "+ self.serverIp.text + ":" + self.portNo.text
            self.cleintListView.adapter.data.extend([s])
            self.cleintListView._trigger_reset_populate()
            server = Server(self.serverIp.text, int(self.portNo.text))
            #server = Server("192.168.0.110",10000)
            servers.append(server)
        except:
            print("fail")
            s = "Listening on "+ self.serverIp.text + ":" + self.portNo.text
            self.cleintListView.adapter.data.remove(s)
            self.cleintListView._trigger_reset_populate()
    '''
    def connect_to_server(self):
        cThread = threading.Thread(target=self.sockConnect, args=())
        cThread.daemon = True
        cThread.start()
    '''
    def incomingConnection(sip,sport,ip,port):
        a= App.get_running_app()
        s = ip + ":" + port + " Connected to " + sip + ":" + str(sport)
        a.root.ids.start_screen.ids.client_listview.adapter.data.extend([s])
        a.root.ids.start_screen.ids.client_listview._trigger_reset_populate()

    def disconntingConnection(sip,sport,ip,port):
        a= App.get_running_app()
        s = ip + ":" + port + " Connected to " + sip + ":" + str(sport)
        a.root.ids.start_screen.ids.client_listview.adapter.data.remove(s)
        a.root.ids.start_screen.ids.client_listview._trigger_reset_populate()
    '''
    def sockConnect(self):
        try:
            client = Client(self.serverIp.text, int(self.portNo.text))
            s = "Connected to"+ self.serverIp.text + ":" + self.portNo.text
            self.cleintListView.adapter.data.extend([s])
            self.cleintListView._trigger_reset_populate()
            print("connected")
        except:
            print("Connect Fail")
    '''
class Client:
    def __init__(self, address, ServerPort):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((address, ServerPort))

class Server:
    connections = []
    def __init__(self, ServerIp, ServerPort):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((ServerIp, ServerPort))
        sock.listen(5)
        while True:
            c, a = sock.accept()
            cThread = threading.Thread(target=self.handler, args=(c, a, ServerIp, ServerPort))
            cThread.daemon = True
            cThread.start()
            print(str(a[0]) + ':' + str(a[1]), "connected")
            Npl_Project.incomingConnection(ServerIp,ServerPort,str(a[0]),str(a[1]))
            
    def handler(self, c, a,ServerIp, ServerPort):
        while True:
            try:
                data = c.recv(1024)
                if data:
                    print(str(a[0]) + ':' + str(a[1]) + ":- " + str(data, 'utf-8'))
                else:
                    print(str(a[0]) + ':' + str(a[1]), "disconnected")
                    self.connections.remove(c)
                    c.close()
                    break
            except:
                print("disconnected")
                Npl_Project.disconntingConnection(ServerIp,ServerPort,str(a[0]),str(a[1]))
                #self.connections.remove(c)
                c.close()

            


if __name__ == '__main__':
    Npl_ProjectApp().run()
        