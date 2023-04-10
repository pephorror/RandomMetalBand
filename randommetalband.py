# PYTHON 3.7
# Discover metal bands!

import tkinter as tk
from tkinter import simpledialog
from tkinter import messagebox
from tkinter import OptionMenu
from tkinter import ttk
import tkinter.font as tkFont
import requests
import webbrowser as wb
from bs4 import BeautifulSoup
import random
import os.path
import csv
import pylast
import pandas as pd
from IPython.display import HTML

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        # style
        self.style = ttk.Style(self)
        self.style.theme_use('vista')
        # variables
        self.infoband = [] # [BAND, COUNTRY, LOCATION, STATUS, FORMED IN, YEARS ACTIVE, GENRE, LYRICS THEME, LAST LABEL]
        self.discografia = []
        self.ma_url = "" # I'll save here the url of the random band found in metal archives
        # API LASTFM
        self.API_KEY = "41e86ee4787f1a444ba944478a89190c"
        self.API_SECRET = "b2e3be0dccacebf5f16eea75b735d135"
        
        # configure the root window
        self.title('Random Metal Band by pephorror')
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
            nombres_bandas = ['None saved yet','None saved yet']
        # Create a StringVar to store the selected option
        var = tk.StringVar(self, value = "Saved bands")# value = nombres_bandas[0])
        # Create a widget OptionMenu - values read from and saved in nombres_bandas csv
        self.option = OptionMenu(self, var, *nombres_bandas[1:], command = self.cargar_banda_csv)
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

        # button LastFM
        self.button_last = ttk.Button(self, text='Search in LastFM')
        self.button_last['command'] = self.button_lastfm
        self.button_last.grid(row = 5, column = 0, padx = (20, 10), pady = 10)
        #button Get Similar Artist usando pylast (API LASTFM)
        self.button_similar = ttk.Button(self, text='Get similar')
        self.button_similar['command'] = self.get_similar
        self.button_similar.grid(row = 5, column = 1, padx = 10, pady = 10)
        # button LastFM METAL CHARTS
        self.button_charts = ttk.Button(self, text='LastFM Metal Charts')
        self.button_charts['command'] = self.lastfm_charts
        self.button_charts.grid(row = 5, column = 2, padx = 10, pady = 10)
        # button open in metal archives
        self.button_ma = ttk.Button(self, text='Open in M-A')
        self.button_ma['command'] = self.button_ma_url
        self.button_ma.grid(row = 5, column = 3, padx = (10, 20), pady = 10)

        #button SAVE TO CSV
        self.button_csv = ttk.Button(self, text='Add to bands.csv')
        self.button_csv['command'] = self.button_to_csv
        self.button_csv.grid(row = 6, column = 1, columnspan = 2, padx = (10, 20), pady = (10,10))

    def random_band_info_metalarchives(self):
        '''funcion que extrae informacion de una banda aleatoria de metalarchives'''
        self.infoband = []
        self.discografia = []
        # scrap & soup random band from metal-archives
        url = 'https://www.metal-archives.com/band/random'
        pagina = requests.get(url)
        soup = BeautifulSoup(pagina.content, 'html.parser')
        title = soup.title.text

        # Get band ID and create url2 (url with discography)
        lis = (soup.select('li'))
        linea_con_id = str(lis[35])
        pos_ini_band_id = (linea_con_id).find('id')
        if (linea_con_id).find('tab'):
            pos_fin_band_id = (linea_con_id).find('tab')
        else:
            pos_fin_band_id = pos_ini_band_id + 20
        band_id = linea_con_id[pos_ini_band_id + 3 : pos_fin_band_id - 1]
        url2 = 'https://www.metal-archives.com/band/discography/id/' + band_id + '//tab/all' #url2 contains the url with the discography of the band
        self.ma_url = "https://www.metal-archives.com/band/view/id/" + band_id # url of the band in metal-archives

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

        self.infoband.append(self.ma_url)

        # Update the label text with the band name and genre
        self.label_info.config(text="BAND: " + self.infoband[0] + "\nCOUNTRY: " + self.infoband[1] + "\nFORMED IN: " + self.infoband[4] + "\nGENRE: " + self.infoband[5] + "\nLYRICS THEME: " + self.infoband[6] + "\nLAST KNOWN LABEL: " + self.infoband[7])
        return self.infoband, self.discografia

    def manual_band_info_metalarchives(self):
        url = simpledialog.askstring(title="Input", prompt="Input the metal-archives url of a band you like:")
        self.ma_url = url
        '''you input a url from metal-archives and the program gathers the info'''
        self.infoband = []
        self.discografia = []
        pagina = requests.get(url)
        soup = BeautifulSoup(pagina.content, 'html.parser')
        title = soup.title.text

        # Get band ID and create url2 (url with discography)
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

        self.infoband.append(self.ma_url)

        # Update the label text with the band name and genre
        self.label_info.config(text="BAND: " + self.infoband[0] + "\nCOUNTRY: " + self.infoband[1] + "\nFORMED IN: " + self.infoband[4] + "\nGENRE: " + self.infoband[5] + "\nLYRICS THEME: " + self.infoband[6] + "\nLAST KNOWN LABEL: " + self.infoband[7])
        return self.infoband, self.discografia

    def button_bandcamp(self):
        wb.open_new_tab("https://bandcamp.com/search?q=" + self.infoband[0] + "&item_type")

    def button_youtube(self):
        wb.open_new_tab("https://www.youtube.com/results?search_query=" + self.infoband[0])
    
    def button_spotify(self):
        wb.open_new_tab("https://open.spotify.com/search/" + self.infoband[0])

    def button_discog(self):
        wb.open_new_tab("https://www.discogs.com/search/?q=" + self.infoband[0] + "&type=all")

    def button_lastfm(self):
        wb.open_new_tab("https://www.last.fm/search?q=" + self.infoband[0])

    def get_similar(self):
        # Create object of conection with the API
        network = pylast.LastFMNetwork(api_key=self.API_KEY, api_secret = self.API_SECRET)
        artista = self.infoband[0]
        # Code to search the random similar artist
        band = network.get_artist(artista)
        artistas_similares = band.get_similar()
        artista_aleatorio = random.choice(artistas_similares)
        top_tags = artista_aleatorio.item.get_top_tags()
        if top_tags:
            genre = top_tags[0].item.get_name()
        else:
            None
        answer = messagebox.askquestion ("QUESTION", "BAND FOUND: " + artista_aleatorio.item.get_name() + ",: " + genre + "\nDo you want to load it?")
        if answer == "yes":
            self.infoband = ["","","","","","","","","",""]
            self.discografia = []
            self.infoband[0] = artista_aleatorio.item.get_name()
            self.infoband[5] = genre
            self.label_info.config(text="BAND: " + self.infoband[0] + "\nCOUNTRY: " + self.infoband[1] + "\nFORMED IN: " + self.infoband[4] + "\nGENRE: " + self.infoband[5] + "\nLYRICS THEME: " + self.infoband[6] + "\nLAST KNOWN LABEL: " + self.infoband[7])
        else:
            None

    def lastfm_charts(self):
        ''' Creates a html file with the charts'''
        # ARE YOU SURE? IT WILL TAKE A FEW MINUTES
        answer = messagebox.askquestion ("WARNING", "To generate the charts will take a couple of minutes, are you sure you want to continue?")
        if answer == "yes":
            # Object of connection to Lastfm API
            network = pylast.LastFMNetwork(api_key=self.API_KEY, api_secret = self.API_SECRET)
            # Create dataframe
            df = pd.DataFrame()
            df = pd.DataFrame(columns=['GENRE', 'BAND', 'SCROBBLES'])
            # Define musical genres to build the charts. More genres, it will take longer.
            generos = ["heavy metal", "thrash metal", "speed metal", "black metal", "death metal", "industrial metal", "doom metal", "stoner metal", "folk metal", "power metal", "brutal death metal", "grindcore", "groove metal", "nu metal", "alternative metal", "hard rock", "metalcore"]
            for genero in generos:
                # CREATE LIST OF THE TOP ARTIST FOR EACH GENRE
                artistas = network.get_tag(genero).get_top_artists(limit = 10)

                # empty list to save results
                resultados = []

                # Go through the artists to get the str with the name and the scrobbles to build the df
                for artista in artistas:
                    nombre = artista.item.get_name()
                    scrobbles = artista.item.get_playcount()
                    df = df.append({'GENRE':genero, 'BAND':nombre, 'SCROBBLES':scrobbles}, ignore_index=True)
            # CREATE A OFFLINE HTML WEB THAT SHOWS THE CHARTS
            df = df.groupby("GENRE").apply(lambda x: x.sort_values("SCROBBLES", ascending = False)) #DF WITH charts by genre
            df2 = df.sort_values("SCROBBLES", ascending = False) # df with charts in global metal mode
            html = df.to_html(index=False, justify='center', classes=['table', 'table-striped'], table_id='metal_charts')
            with open('metal_charts.html', 'w') as f:
                f.write(html)
            wb.open_new_tab("metal_charts.html")
            
    def button_ma_url(self):
        wb.open_new_tab(self.ma_url)

    def button_to_csv(self):
        nombres_bandas = []
        # open the file in the write mode
        if os.path.exists('bands.csv'):
            with open('bands.csv', 'r', newline='') as f:
                reader = csv.reader(f)
                for row in reader:
                    nombres_bandas.append(row[0])
            # Next bit of code is to check if there is a band called the same already in the csv file or not, and if you want to save it anyway or not.
            if self.infoband[0] in nombres_bandas:
                answer = messagebox.askquestion ("WARNING", "There is already a band with that name in bands.csv, do you want to save it anyway?")
                if answer == "yes":
                    with open('bands.csv', 'a', encoding="utf-8", newline='') as f:
                        # create the csv writer
                        writer = csv.writer(f)
                        # write the infoband
                        self.infoband.append(self.discografia)
                        writer.writerow(self.infoband)
                        self.option["menu"].add_command(label=self.infoband[0], command = lambda:self.cargar_banda_csv(self.infoband[0]))
            else:
                with open('bands.csv', 'a', encoding="utf-8", newline='') as f:
                    # create the csv writer
                    writer = csv.writer(f)
                    # write the infoband
                    self.infoband.append(self.discografia)
                    writer.writerow(self.infoband)
                    self.option["menu"].add_command(label=self.infoband[0], command = lambda:self.cargar_banda_csv(self.infoband[0]))
        else:
            with open('bands.csv', 'w', encoding="utf-8", newline='') as f:
                # create the csv writer
                writer = csv.writer(f)
                # write the header
                writer.writerow(['BAND', 'COUNTRY', 'LOCATION','STATUS','FORMED IN', 'GENRE','LYRICS THEME', 'LAST LABEL', 'YEARS ACTIVE', 'M-A URL', 'DISCOGRAPHY'])
                # write the infoband
                self.infoband.append(self.discografia)
                writer.writerow(self.infoband)
                self.option["menu"].add_command(label=self.infoband[0], command = lambda:self.cargar_banda_csv(self.infoband[0]))

                        
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