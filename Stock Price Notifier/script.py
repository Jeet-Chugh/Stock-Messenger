from bs4 import BeautifulSoup
import requests
from win10toast import ToastNotifier
import time

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen,ScreenManager
from kivy.uix.gridlayout import GridLayout
from kivy.config import Config
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.utils import get_color_from_hex as hex

Config.set('graphics','width','480')
Config.set('graphics','height','480')
Config.write()

toaster = ToastNotifier()
counter = 1
ticker = ''

def stock_price_checker(ticker):
    result = requests.get('https://www.finance.yahoo.com/quote/{a}'.format(a=ticker),headers=requests.utils.default_headers())
    html = BeautifulSoup(result.text,'lxml')
    price = html.find(class_="Trsdu(0.3s) Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(b)")

    if price == None:  return None
    else:  return price.get_text()

def stock_price_notifications(*args):
    try:
        global durations
        global counter
        if counter >= durations:
            Clock.unschedule(stock_price_notifications)
            app.root.ids.start_alerts.disabled = False
            app.popups('Sucessfully Stopped Alerts')
        counter += 1
        ticker = app.root.ids.ticker.text
        toaster.show_toast('{} Price Checker'.format(ticker.upper()),stock_price_checker(ticker),duration=5,icon_path='image\\stock.ico')
    except:  return app.popup('Invalid Inputs')

# KIVY APP

class MainScreen(Screen):
    def __init__(self,**kwargs):
        super(MainScreen,self).__init__(**kwargs)

gui = Builder.load_file('main.kv')

class MainApp(App):

    def __init__(self,**kwargs):
        super(MainApp,self).__init__(**kwargs)

    def start_app(self):
        try:
            global durations,ticker
            ticker = self.root.ids.ticker.text
            durations = int(self.root.ids.duration.text) // int(self.root.ids.interval.text)
            self.root.ids.start_alerts.disabled = True
            stock_price_notifications()
            Clock.schedule_interval(stock_price_notifications,int(self.root.ids.interval.text)*60)
        except:  app.popup('Invalid Inputs')

    def build(self):
        return gui

    def popups(self,text):
        popup_button = Button(text='Dismiss',background_color=hex('#FFA69E'))
        invalid_popup = Popup(title=text,content=popup_button,size_hint=(0.7,0.7))
        popup_button.bind(on_press=lambda *args: quit())
        return invalid_popup.open()

    def popup(self,text):
        popup_button = Button(text='Dismiss',background_color=hex('#FFA69E'))
        invalid_popup = Popup(title=text,content=popup_button,size_hint=(0.7,0.7))
        popup_button.bind(on_press=lambda *args: invalid_popup.dismiss())
        return invalid_popup.open()

if __name__ == '__main__':
    app = MainApp()
    app.run()
