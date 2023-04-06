# PYTHON 3.7
# Discover metal bands!

import tkinter as tk
from tkinter import simpledialog
from tkinter import OptionMenu
from tkinter import ttk
import tkinter.font as tkFont
import requests
import webbrowser as wb
from bs4 import BeautifulSoup
import random
import os.path
import csv

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        #colores y fuentes
        self.style = ttk.Style(self)
        self.style.theme_use('vista')
        # variables que voy a usar:
        self.infoband = [] # [NOMBRE, PAIS, LOCATION, STATUS, FORMED IN, YEARS ACTIVE, GENRE, LYRICS THEME, LAST LABEL
        self.discografia = []
        
        # configure the root window
        self.title('Random Metal Band Research 0.1')
        self.iconbitmap("randommetalband.ico")

        # button M-A
        self.button_ma = ttk.Button(self, text='Randon band from M-A')
        self.button_ma['command'] = self.random_band_info_metalarchives
        self.button_ma.grid(row = 1, column = 0, columnspan = 2, padx = (10, 10), pady = 10)

        # manual search in M-A INPUT A URL OF A BAND OF METAL ARCHIVES AND GATHER INFO
        self.button_search_ma = ttk.Button(self, text='Input URL from M-A')
        self.button_search_ma['command'] = self.manual_band_info_metalarchives
        self.button_search_ma.grid(row = 1, column = 1, columnspan = 2, padx = (10, 10), pady = 10)

        # LOAD INFO FROM BANDS.CSV USING A DROPDOWN MENU
        nombres_bandas = []
        if os.path.exists('bands.csv'):
            with open("bands.csv") as f:
                reader = csv.reader(f)
                for row in reader:
                    nombres_bandas.append(row[0])
        else:
            nombres_bandas = ['None saved yet']
        # Crear una variable de cadena para almacenar la opción seleccionada
        var = tk.StringVar(self, value = nombres_bandas[0])
        # Crear un widget OptionMenu con los valores leídos del archivo csv
        self.option = OptionMenu(self, var, *nombres_bandas, command = self.cargar_banda_csv)
        self.option.grid(row = 1, column = 2, columnspan = 2, padx = (10, 10), pady = 10)
        
        # label info
        self.label_info = ttk.Label(self, text="BAND:\nCOUNTRY:\nFORMED IN:\nGENRE:\nLYRICS THEME:\nLAST KNOWN LABEL: ")
        self.label_info.grid(row = 3, column = 0, columnspan = 4)

        # button Bandcamp
        self.button_band = ttk.Button(self, text='Search in Bandcamp')
        self.button_band['command'] = self.button_bandcamp
        self.button_band.grid(row = 4, column = 0, padx = (20, 10), pady = 10)
        # button Youtube
        self.button_you = ttk.Button(self, text='Search in Youtube')
        self.button_you['command'] = self.button_youtube
        self.button_you.grid(row = 4, column = 1, padx = 10, pady = 10)
        # button Spotify
        self.button_spoti = ttk.Button(self, text='Search in Spotify')
        self.button_spoti['command'] = self.button_spotify
        self.button_spoti.grid(row = 4, column = 2, padx = 10, pady = 10)
        # button Discogs
        self.button_discogs = ttk.Button(self, text='Search in Discogs')
        self.button_discogs['command'] = self.button_discog
        self.button_discogs.grid(row = 4, column = 3, padx = (10, 20), pady = 10)

        #button GUARDAR A CSV
        self.button_csv = ttk.Button(self, text='Add to bands.csv')
        self.button_csv['command'] = self.button_to_csv
        self.button_csv.grid(row = 5, column = 1, columnspan = 2, padx = (10, 20), pady = (10,10))

    def random_band_info_metalarchives(self):
        '''funcion que extrae informacion de una banda aleatoria de metalarchives'''
        self.infoband = [] # [NOMBRE, PAIS, LOCATION, STATUS, FORMED IN, YEARS ACTIVE, GENRE, LYRICS THEME, LAST LABEL
        self.discografia = []
        #Primero scrap y soup de una banda aleatoria de metal archives
        url = 'https://www.metal-archives.com/band/random'
        pagina = requests.get(url)
        soup = BeautifulSoup(pagina.content, 'html.parser')
        title = soup.title.text

        #Ahora codigo para extraer el id de la banda aleatoria y generar la url de la discografia (url2)
        lis = (soup.select('li'))
        linea_con_id = str(lis[35])
        pos_ini_band_id = (linea_con_id).find('id')
        if (linea_con_id).find('tab'):
            pos_fin_band_id = (linea_con_id).find('tab')
        else:
            pos_fin_band_id = pos_ini_band_id + 20
        band_id = linea_con_id[pos_ini_band_id + 3 : pos_fin_band_id - 1]
        url2 = 'https://www.metal-archives.com/band/discography/id/' + band_id + '//tab/all'

        pagina2 = requests.get(url2)
        soup2 = BeautifulSoup(pagina2.content, 'html.parser')

        bandname_html = soup.select('h1')
        infoband_html = soup.select('dd')
        discografia_html = soup2.select('a')

        bandname = bandname_html[0].text
        bandname = bandname.strip()

        self.infoband.append(bandname)

        for dd in infoband_html:
            self.infoband.append(dd.text)

        for disco in discografia_html:
            self.discografia.append(disco.text)

        # Update the label text with the band name and genre
        # [0 NOMBRE, 1 PAIS, 2 LOCATION, 3 STATUS, 4 FORMED IN, 5 GENRE, 6 LYRICS THEME, 7 LAST LABEL
        self.label_info.config(text="BAND: " + self.infoband[0] + "\nCOUNTRY: " + self.infoband[1] + "\nFORMED IN: " + self.infoband[4] + "\nGENRE: " + self.infoband[5] + "\nLYRICS THEME: " + self.infoband[6] + "\nLAST KNOWN LABEL: " + self.infoband[7])
        return self.infoband, self.discografia

    def manual_band_info_metalarchives(self):
        url = simpledialog.askstring(title="Input", prompt="Input the metal-archives url of a band you like:")
        '''funcion que extrae informacion de una banda aleatoria de metalarchives'''
        self.infoband = [] # [NOMBRE, PAIS, LOCATION, STATUS, FORMED IN, YEARS ACTIVE, GENRE, LYRICS THEME, LAST LABEL
        self.discografia = []
        pagina = requests.get(url)
        soup = BeautifulSoup(pagina.content, 'html.parser')
        title = soup.title.text

        #Ahora codigo para extraer el id de la banda aleatoria y generar la url de la discografia (url2)
        lis = (soup.select('li'))
        linea_con_id = str(lis[35])
        pos_ini_band_id = (linea_con_id).find('id')
        if (linea_con_id).find('tab'):
            pos_fin_band_id = (linea_con_id).find('tab')
        else:
            pos_fin_band_id = pos_ini_band_id + 20
        band_id = linea_con_id[pos_ini_band_id + 3 : pos_fin_band_id - 1]
        url2 = 'https://www.metal-archives.com/band/discography/id/' + band_id + '//tab/all'

        pagina2 = requests.get(url2)
        soup2 = BeautifulSoup(pagina2.content, 'html.parser')

        bandname_html = soup.select('h1')
        infoband_html = soup.select('dd')
        discografia_html = soup2.select('a')

        bandname = bandname_html[0].text
        bandname = bandname.strip()

        self.infoband.append(bandname)

        for dd in infoband_html:
            self.infoband.append(dd.text)

        for disco in discografia_html:
            self.discografia.append(disco.text)

        # Update the label text with the band name and genre
        # [0 NOMBRE, 1 PAIS, 2 LOCATION, 3 STATUS, 4 FORMED IN, 5 GENRE, 6 LYRICS THEME, 7 LAST LABEL
        self.label_info.config(text="BAND: " + self.infoband[0] + "\nCOUNTRY: " + self.infoband[1] + "\nFORMED IN: " + self.infoband[4] + "\nGENRE: " + self.infoband[5] + "\nLYRICS THEME: " + self.infoband[6] + "\nLAST KNOWN LABEL: " + self.infoband[7])
        return self.infoband, self.discografia

    def button_bandcamp(self):
        a = random.randint(0, len(self.discografia)-1)
        wb.open_new_tab("https://bandcamp.com/search?q=" + self.infoband[0] + "&item_type")# + "+" + infoband[5])
        # Update the label text with the record you had search for
        #self.label_disco.config(text=self.discografia[a])

    def button_youtube(self):
        a = random.randint(0, len(self.discografia)-1)
        wb.open_new_tab("https://www.youtube.com/results?search_query=" + self.infoband[0])# + "+" + infoband[5])
        #self.label_disco.config(text=self.discografia[a])
    
    def button_spotify(self):
        a = random.randint(0, len(self.discografia)-1)
        wb.open_new_tab("https://open.spotify.com/search/" + self.infoband[0])# + "+" + self.discografia[a])# + "+" + infoband[5])
        #self.label_disco.config(text=self.discografia[a])

    def button_discog(self):
        a = random.randint(0, len(self.discografia)-1)
        wb.open_new_tab("https://www.discogs.com/search/?q=" + self.infoband[0] + "&type=all")
        #self.label_disco.config(text=self.discografia[a])

    def button_to_csv(self):
        # open the file in the write mode
        if os.path.exists('bands.csv'):
            with open('bands.csv', 'a', newline='') as f:
                # create the csv writer
                writer = csv.writer(f)
                # write the infoband
                self.infoband.append(self.discografia)
                writer.writerow(self.infoband)
        else:
            with open('bands.csv', 'w', newline='') as f:
                # create the csv writer
                writer = csv.writer(f)
                # write the header
                writer.writerow(['BAND', 'COUNTRY', 'LOCATION','STATUS','FORMED IN', 'GENRE','LYRICS THEME', 'LAST LABEL', 'YEARS ACTIVE', 'DISCOGRAPHY'])
                # write the infoband
                self.infoband.append(self.discografia)
                writer.writerow(self.infoband)
        self.option["menu"].add_command(label=self.infoband[0])#, command=lambda valor=self.infoband[0]: variable.set(valor))

    def cargar_banda_csv(self, value):
        with open('bands.csv', 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                if row[0] == value:
                    self.infoband = row
                    self.discografia = self.infoband[-1]
        self.label_info.config(text="BAND: " + self.infoband[0] + "\nCOUNTRY: " + self.infoband[1] + "\nFORMED IN: " + self.infoband[4] + "\nGENRE: " + self.infoband[5] + "\nLYRICS THEME: " + self.infoband[6] + "\nLAST KNOWN LABEL: " + self.infoband[7])

if __name__ == "__main__":
    app = App()
    app.mainloop()
