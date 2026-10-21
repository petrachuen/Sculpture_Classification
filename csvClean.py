# For CSV Cleanup

import pandas as pd
import numpy as np

# Data from Asian Art Museum
# need re scrape, no origin info
asianArt = pd.read_csv("./RawCSV/asianArt.csv")
asianArt = asianArt[[
           'item_page_link',
           'data',
           'phone',
           'image',
           'text_1',
           'text_3']]

asianArt.rename(columns = {
    'item_page_link': 'URL',
    'data': 'Title',
    'phone': 'Date',
    'text_1': 'Origin',
    'text_3': "Materials",
    'image': 'Image'
    },inplace=True)


# Data from Colbase database
# All origin are Japan
colbase = pd.read_csv("./RawCSV/colbase.csv")
colbase = colbase[[
           'data',
           'data2',
           'data3',
           'image',
           'item_page_link',
           'text_2']]

colbase.rename(columns = {
            'data': 'Title',
            'data2': 'Materials',
            'data3': 'Date',
            'image': 'Image',
            'item_page_link': 'URL',
            'text_2': 'Origin'
    },inplace=True)

colbase['Origin'] = colbase['Origin'].fillna('Japan')


# Data from the MET collection
met = pd.read_csv("./RawCSV/met.csv")
met = met[[
           'web_scraper_start_url',
           'data',
           'data2',
           'data3',
           'image']]

met.rename(columns = {
    'web_scraper_start_url': 'URL',
    'data': 'Title',
    'data2': 'Origin',
    'data3': 'Date'
    },inplace=True)

# Data from narahaku Museum
# Origin Japan
narahaku = pd.read_csv("./RawCSV/narahaku.csv")
narahaku = narahaku[[
           'web_scraper_start_url',
           'objectnametitle',
           'century',
           'image']]

narahaku.rename(columns = {
    'web_scraper_start_url': 'URL',
    'objectnametitle': 'Title',
    'century': 'Date'
    },inplace=True)

colbase['Origin'] = 'Japan' 

# Data from rietberg Museum
rietberg = pd.read_csv("./RawCSV/rietberg.csv")
rietberg = rietberg[[
           'title',
           'data2',
           'image',
           'item_page_link',
           'text_0',
           'text_1']]

rietberg.rename(columns = {
            'title': 'Title',
            'data2': 'Origin',
            'image': 'Image',
            'item_page_link': 'URL',
            'text_0': 'Date',
            'text_1': 'Materials'
    },inplace=True)

# Will need Translation

# Data from Smithsonian Museum of Asian Art
smithsonian = pd.read_csv("./RawCSV/smithsonian.csv")
smithsonian = smithsonian[[
           'web_scraper_start_url',
           'data',
           'image2',
           'image3',
           'image']]

smithsonian.rename(columns = {
    'web_scraper_start_url': 'URL',
    'data': 'Title',
    'image2': 'Origin',
    'image3': 'Date'
    },inplace=True)

# Data from staatliche zu Berlin Museum
staatliche = pd.read_csv("./RawCSV/staatliche.csv")
"""staatliche = staatliche[[
           'data',
           'data2',
           'item_page_link',
           'text_5'
           ]]

staatliche.rename(columns = {
    'web_scraper_start_url': 'URL',
    'data': 'Title',
    'image2': 'Origin',
    'image3': 'Date'
    },inplace=True)"""

smithsonian = smithsonian[[
           'web_scraper_start_url',
           'data',
           'image2',
           'image3',
           'image']]

smithsonian.rename(columns = {
    'web_scraper_start_url': 'URL',
    'data': 'Title',
    'image2': 'Origin',
    'image3': 'Date'
    },inplace=True)

# Data from Tibet Museum
tibet = pd.read_csv("./RawCSV/tibetMuseum.csv")
tibet = tibet[[
           'data',
           'data3',
           'data4',
           'data6']]

tibet.rename(columns = {
    'web_scraper_start_url': 'URL',
    'data': 'Title',
    'data3': 'Origin',
    'data4': 'Date',
    'data6': 'Materials'
    },inplace=True)

# Data from tszshan museum
tszshan = pd.read_csv("./RawCSV/tszshanMuseum.csv")
tszshan = tszshan[[
           'web_scraper_start_url',
           'data',
           'data2',
           'data4',
           'data5',
           'image']]

tszshan.rename(columns = {
    'web_scraper_start_url': 'URL',
    'data': 'Title',
    'data2': 'Origin',
    'data4': 'Date',
    'data6': 'Materials'
    },inplace=True)

#export
asianArt.to_csv('./CleanedCSV/C_asianArt.csv', index=False)
colbase.to_csv('./CleanedCSV/C_colbase.csv', index=False)
met.to_csv('./CleanedCSV/C_met.csv', index=False)
narahaku.to_csv('./CleanedCSV/C_narahaku.csv', index=False)
rietberg.to_csv('./CleanedCSV/C_reitberg.csv', index=False)
staatliche.to_csv('./CleanedCSV/C_staatliche.csv', index=False)
smithsonian.to_csv('./CleanedCSV/C_smithsonian.csv', index=False)
tibet.to_csv('./CleanedCSV/C_tibetMuseum.csv', index=False)
tszshan.to_csv('./CleanedCSV/C_tszshanMuseum.csv', index=False)
