from kivymd.app import MDApp
from kivymd.uix.textfield import MDTextField
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivymd.uix.button import MDRectangleFlatIconButton


from datetime import datetime
import mysql.connector
from constant import VALUE_DK, SPESIALIST

from kivy.lang import Builder
from kivy.clock import Clock
from kivy.core.audio import SoundLoader

from kivymd.uix.datatables import MDDataTable
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.button import MDRaisedButton
from kivy.metrics import dp
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivymd.uix.list import OneLineIconListItem
from kivymd.uix.menu import MDDropdownMenu


KV = """





MDScreen

    MDDropDownItem:
        id: drop_item
        pos_hint: {'center_x': .1, 'center_y': .1}
        text: 'Янчоглов І.І.'
        on_release: app.menu.open()
"""


class IconListItem(OneLineIconListItem):
    icon = StringProperty()


class MyTextInput(MDTextField):
    def on_parent(self, widget, parent):
        self.focus = True


class PestControlApp(MDApp):
    BARIER = {"1": "1-2", "2": "1-2", "3": "3"}
    _ROW = (1,2,3)
    VALUE = {}
    VALUE_PROSM = {}
    KRISI_NA_TER_PROSM = 0
    MISHI_NA_TER_PROSM = 0
    
    KRISI_NA_TER = 0
    MISHI_NA_TER = 0
    data_tables = None
    count_for_exit = 1
    second_for_exit = datetime.now()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.screen = Builder.load_string(KV)
        menu_items = [
            {
                "viewclass": "IconListItem",
                "icon": "git",
                "text": i,
                "height": dp(56),
                "on_release": lambda x=i: self.set_item(x),
            }
            for j, i in SPESIALIST.items()
        ]

        self.menu = MDDropdownMenu(
            caller=self.screen.ids.drop_item,
            items=menu_items,
            position="center",
            width_mult=4,
        )
        self.menu.bind()

    def set_item(self, text_item):
        self.screen.ids.drop_item.set_item(text_item)
        self.screen.ids.drop_item.text = text_item
        self.menu.dismiss()

    def izmenenie_defoltnogo_znacheniya(self, dict_value, value, data):
        if len(dict_value) == 1:
            dict_value = {}
            return dict_value
        count = 0
        kay = ""
        for i, v in dict_value.items():
            count += 1
            if count == len(dict_value) - 1:
                kay = i
            if count == len(dict_value):
                try:
                    if (
                        dict_value[kay][1].split("-")[0] == "миша"
                        and value.split("-")[0] == "миша"
                        or dict_value[kay][1].split("-")[0] == "криса"
                        and value.split("-")[0] == "криса"
                    ):
                        value = f'{dict_value[kay][1].split("-")[0]}-{int(dict_value[kay][1].split("-")[1])+1}'
                except:
                    pass
                kay_del = i
                dict_value[kay] = (data, value, self.screen.ids.drop_item.text)
        dict_value.pop(kay_del)
        return dict_value

    def sound(self, file):
        sound = SoundLoader.load(file)
        if sound:
            sound.play()

    def txt_callback(self, instance, value):
        defolt_value = "0"
        # value = self.txt_in.text

        if "\n" in self.txt_in.text:
            if self.txt_in.text[0] == "5" and len(self.txt_in.text) > 12:
                self._save(isinstance=None)
                # PestControlApp.VALUE = {}

            elif self.txt_in.text[0] == "3" and len(self.txt_in.text) > 12:
                PestControlApp.MISHI_NA_TER += 1 
                PestControlApp.MISHI_NA_TER_PROSM += 1
                self.label2.text = f"миш-{int(PestControlApp.MISHI_NA_TER_PROSM/2)}  крис-{int(PestControlApp.KRISI_NA_TER_PROSM/2)}"
                self.sound("iphone_14_notification.mp3")
            elif self.txt_in.text[0] == "4" and len(self.txt_in.text) > 12:
                PestControlApp.KRISI_NA_TER += 1
                PestControlApp.KRISI_NA_TER_PROSM += 1
                self.label2.text = f"миш-{int(PestControlApp.MISHI_NA_TER_PROSM/2)}  крис-{int(PestControlApp.KRISI_NA_TER_PROSM/2)}"
                self.sound("iphone_14_notification.mp3")
            else:
                # if str(self.txt_in.text).rstrip('\n')  in baza or self.txt_in.text[0] == "1":

                PestControlApp.VALUE.pop(str(self.txt_in.text).rstrip("\n"), 10)
                # print(PestControlApp.VALUE, "!!!!!!!!!!")

                PestControlApp.VALUE[str(self.txt_in.text).rstrip("\n")] = (
                    datetime.now(),
                    defolt_value,
                    self.screen.ids.drop_item.text,
                )
                self.sound("iphone_14_notification.mp3")

                if self.txt_in.text[0] == "1" and len(self.txt_in.text) > 12:
                    PestControlApp.VALUE = self.izmenenie_defoltnogo_znacheniya(
                        dict_value=PestControlApp.VALUE,
                        value=VALUE_DK[self.txt_in.text[2:4]],
                        data=datetime.now(),
                    )
                PestControlApp.VALUE_PROSM.update(PestControlApp.VALUE)
                # print(PestControlApp.VALUE_PROSM, "5555")

            self.txt_in.text = ""

    def _exit(self, instance):

        delta_second = datetime.now() - self.second_for_exit
        
        if self.count_for_exit >= 3 and delta_second.total_seconds()<5:
            exit()
        self.count_for_exit+=1
        if delta_second.total_seconds()>5:
            
            self.second_for_exit = datetime.now()
            self.count_for_exit = 1

    def on_button_press(self, instance_button: MDRaisedButton):
        PestControlApp.VALUE_PROSM = dict(sorted(PestControlApp.VALUE_PROSM.items()))

        if len(PestControlApp.VALUE_PROSM) == 0:
            pass
        else:

            self.data_tables.row_data = []
            new_data = []
            for i, j in PestControlApp.VALUE_PROSM.items():
                value = j[1]
                try:
                    if  "миша" in value or  "криса" in value:
                        value = f"{value.split('-')[0]}-{str(int(int(value.split('-')[1])/2))}"
                except:
                    pass

                try:
                    new_data.append((i[9:], value, PestControlApp.BARIER[i[6]])) 
                    # self.data_tables.add_row((i[9:], value, PestControlApp.BARIER[i[6]]))
                except:
                    pass

            self.data_tables.row_data = new_data            
        # PestControlApp.VALUE_PROSM = {}
        # print (self.screen.ids.drop_item.text)

    def _save(self, isinstance):
        try:
            # conn = mysql.connector.connect(
            #     host="dezeltor.mysql.tools",
            #     user="dezeltor_pestcontrol",
            #     password="lala280508",
            #     database="dezeltor_pestcontrol",
            # )

            conn = mysql.connector.connect(
            host = "195.138.73.12",
            # port = 3306,
            user = "user1",
            password = "lala280508",
            database = "dez",
            )

            cursor = conn.cursor()
            

            if len(PestControlApp.VALUE) == 0:
                self.label1.text = "СПИСОК ПУСТИЙ"
            else:
                for kay_1, time_value_dk in PestControlApp.VALUE.items():
                    cursor.execute(
                        f"""SELECT  idbaza_pidpriemstv, idbaza_obladnanya  FROM baza_obladnanya WHERE  barcode_obladnanya = "{kay_1}" """
                    )

                    row = cursor.fetchall()
                    if len(row) == 0:
                        pass

                    else:
                        _idbaza_pidpriemstv = row[0][0]
                        _idbaza_obladnanya = row[0][1]

                        cursor.execute(
                            f"""SELECT  idspesialisti  FROM spesialisti WHERE surnames = "{time_value_dk[2]}" """
                        )

                        _id_spesialist = cursor.fetchall()[0][0]

                        time = str(time_value_dk[0])[0:19]
                        print(time[0:19])

                        kay_2 = str(kay_1[9:])
                        time_value_dk = list(time_value_dk)

                        if (str(time_value_dk[1]).split("-")[0] == "миша" or str(time_value_dk[1]).split("-")[0] == "криса"):
                            time_value_dk[1] = f" {time_value_dk[1].split('-')[0]}-{int(int(time_value_dk[1].split('-')[1])/2)}"

                        cursor.execute(
                            f"""INSERT INTO scan_dk (time, value_dk, idbaza_obladnanya, idbaza_pidpriemstv, idspestalisti)
                                                VALUES (STR_TO_DATE('{time}','%Y-%m-%d %T'),'{time_value_dk[1]}','{_idbaza_obladnanya}',
                                                '{_idbaza_pidpriemstv}', '{_id_spesialist}')"""
                        )
                try:
                    
                    cursor.execute(
                        f"""INSERT INTO grizuni_na_territorii (vid_grizuna, kilkist, idbaza_pidpriemstv, time) VALUES ( 'миша', 
                        '{int(PestControlApp.MISHI_NA_TER/2)}','{_idbaza_pidpriemstv}', STR_TO_DATE('{time}','%Y-%m-%d %T'))"""
                    )
                    cursor.execute(
                        f"""INSERT INTO grizuni_na_territorii (vid_grizuna, kilkist,  idbaza_pidpriemstv, time) VALUES ( 'криса', 
                        '{PestControlApp.KRISI_NA_TER/2}','{_idbaza_pidpriemstv}', STR_TO_DATE('{time}','%Y-%m-%d %T'))"""
                    )
                    
                except:
                    pass
                conn.commit()

                self.label1.text = "ЗАПИСАНО"

                PestControlApp.VALUE = {}
                PestControlApp.KRISI_NA_TER = 0
                PestControlApp.MISHI_NA_TER = 0
                self.sound("_audio_plas.mp3")
        except:
            self.label1.text = "НЕВДАЛО!!!! \nПЕРЕВІРТЕ НАЯВНІСТЬ ІНТЕРНЕТУ"

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Orange"
        self.layout = MDFloatLayout()
        self.txt_in = MDTextField(
            multiline=True,
            input_filter="int",
            pos_hint={"center_x": 0.5, "center_y": 0.95},
        )
        self.label2 = Label(
            text=f"миш-{PestControlApp.MISHI_NA_TER_PROSM}  крис-{PestControlApp.KRISI_NA_TER_PROSM}", 
            pos_hint={"center_x": 0.5, "center_y": 0.87}
        )

        self.data_tables = MDDataTable(
            rows_num=1000,
            size_hint=(0.9, 0.6),
            width=50,
            use_pagination=False,
           
            column_data=[("No.", dp(10)), ("znachenny", dp(30)), ("barier", dp(30))],
            
            pos_hint={"center_x": 0.5, "center_y": 0.5},
        )

        self.label1 = Label(
            text="Start typing...", pos_hint={"center_x": 0.5, "center_y": 0.15}
        )
        
        self.txt_in.bind(text=self.txt_callback)
        self.btn_1 = MDRectangleFlatIconButton(
            text="Записати ", pos_hint={"center_x": 0.4, "center_y": 0.05}
        )
        self.btn_1.bind(on_press=self._save)
        self.btn_2 = MDRectangleFlatIconButton(
            text="Вийти ", pos_hint={"center_x": 0.1, "center_y": 0.05}
        )
        self.btn_2.bind(on_press=self._exit)
        self.btn_3 = MDRectangleFlatIconButton(
            text="переглянути введення",
            pos_hint={"center_x": 0.8, "center_y": 0.05},
            font_size="14",
        )
        self.btn_3.bind(on_press=self.on_button_press)

        self.layout.add_widget(self.txt_in)
        self.layout.add_widget(self.label1)
        self.layout.add_widget(self.label2)
        self.layout.add_widget(self.data_tables)
        self.layout.add_widget(self.btn_1)
        self.layout.add_widget(self.btn_3)
        self.layout.add_widget(self.btn_2)
        self.layout.add_widget(self.screen)

        return self.layout


if __name__ == "__main__":
    PestControlApp().run()
