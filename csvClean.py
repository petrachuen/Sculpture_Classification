# For CSV Cleanup

import pandas as pd
import numpy as np

# Keyword for Filtering

filterWords = ["Buddhismus", 'Buddhism', "Buddha", "Bodhisattva", "Avalokiteshvara", "Guanyin"]

# All data DF

sculptureDF = pd.DataFrame()

# ------------------------------------------------------------------------
# ------------------------------------------------------------------------

# Data from Asian Art Museum
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
    'text_3': "Material",
    'image': 'Image'
    },inplace=True)

asianArt['Source'] = "Asian Art Museum"
asianArtCat = asianArt[[
           'Title',
           'Origin',
           'Source',
           'Image']]

# ------------------------------------------------------------------------
# ------------------------------------------------------------------------

# Data from Colbase database
# All null origins are Japan
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
            'data2': 'Material',
            'data3': 'Date',
            'image': 'Image',
            'item_page_link': 'URL',
            'text_2': 'Origin'
    },inplace=True)

colbase['Origin'] = colbase['Origin'].fillna('Japan')
replaceOrigin = {'Chaina': 'China'}
colbase['Origin'] = colbase['Origin'].replace(replaceOrigin)
colbase['Source'] = "Colbase Database"

colbaseCat = colbase[[
           'Title',
           'Origin',
           'Source',
           'Image']]

# ------------------------------------------------------------------------
# ------------------------------------------------------------------------

# Data from the MET collection
met = pd.read_csv("./RawCSV/met.csv")
met = met[[
           'data',
           'data2',
           'data3',
           'image',
           'item_page_link'
           ]]

met.rename(columns = {
    'data': 'Title',
    'data2': 'Date',
    'data3': 'Origin',
    'image': "Image",
    'item_page_link': "URL"
    },inplace=True)

met['Source'] = "The MET"
metCat = met[[
           'Title',
           'Origin',
           'Source',
           'Image']]

# ------------------------------------------------------------------------
# ------------------------------------------------------------------------

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
            'text_1': 'Material'
    },inplace=True)

# Translate Origin
tr_Origins = {
    'Indien': 'India',
    'Asien': 'Asia',
    'Indonesien': 'Indonesia',
    'Kambodscha': 'Cambodia',
    'Mongolei': 'Mongolia'
}

rietberg['Origin'] = rietberg['Origin'].replace(tr_Origins)
rietberg['Source'] = "Reitberg Museum"

rietbergCat = rietberg[[
           'Title',
           'Origin',
           'Source',
           'Image']]

# ------------------------------------------------------------------------
# ------------------------------------------------------------------------

# Data from Smithsonian Museum of Asian Art
smithsonian = pd.read_csv("./RawCSV/smithsonian.csv")
smithsonian = smithsonian[[
           'data',
           'image2',
           'image3',
           'image',
           'item_page_link',
           'text_6']]

smithsonian.rename(columns = {
           'data': "Title",
           'image2': 'Origin',
           'image3': 'Date',
           'image': 'Image',
           'item_page_link': 'URL',
           'text_6': 'Material'
    },inplace=True)

smithsonian['Source'] = "Smithsonian"
smithsonianCat = smithsonian[[
           'Title',
           'Origin',
           'Source',
           'Image']]

# ------------------------------------------------------------------------
# ------------------------------------------------------------------------

# Data from staatliche zu Berlin Museum
staatliche = pd.read_csv("./RawCSV/staatliche.csv")
staatliche = staatliche[[
           'data', # title
           'image',
           'item_page_link',
           'text_16', # Date
           'text_17' # Origin
           ]]

staatliche.rename(columns = {
           'data': "Title", # title
           'image': "Image",
           'item_page_link': "URL",
           'text_16': "Date", # Date
           'text_17': "Origin" # Origin
    },inplace=True)

staatliche['Origin'] = staatliche['Origin'].replace(tr_Origins)
staatliche['Source'] = "staatliche Museum"

staatlicheCat = staatliche[[
           'Title',
           'Origin',
           'Source',
           'Image']]

# ------------------------------------------------------------------------
# ------------------------------------------------------------------------

# Data from Tibet Museum
tibet = pd.read_csv("./RawCSV/tibetMuseum.csv")
tibet = tibet[[
           'data', #title
           'data3', #origin
           'data4', #date
           'data6', #mat
           'item_page_link',
           'image']]

tibet.rename(columns = {
               'data': "Title", #title
               'data3': "Origin", #origin
               'data4': "Date", #date
               'data6': "Material", #mat
               'item_page_link': "URL",
               'image': "Image"
    },inplace=True)

tibet['Source'] = "Tibet Museum"
tibetCat = tibet[[
           'Title',
           'Origin',
           'Source',
           'Image']]

# ------------------------------------------------------------------------
# ------------------------------------------------------------------------

# Data from tszshan museum
tszshan = pd.read_csv("./RawCSV/tszshanMuseum.csv")
tszshan = tszshan[[
           'data',
           'data2',
           'data4',
           'data5',
           'image',
           'item_page_link']]

tszshan.rename(columns = {
               'data': "Title",
               'data2': "Origin",
               'data4': "Date",
               'data5': "Material",
               'image': "Image",
               'item_page_link': "URL"
    },inplace=True)

tszshan['Source'] = "tszshan Museum"
tszshanCat = tszshan[[
           'Title',
           'Origin',
           'Source',
           'Image']]

# ------------------------------------------------------------------------
# ------------------------------------------------------------------------

#export
asianArt.to_csv('./CleanedCSV/C_asianArt.csv', index=False)
colbase.to_csv('./CleanedCSV/C_colbase.csv', index=False)
met.to_csv('./CleanedCSV/C_met.csv', index=False)
rietberg.to_csv('./CleanedCSV/C_reitberg.csv', index=False)
staatliche.to_csv('./CleanedCSV/C_staatliche.csv', index=False)
smithsonian.to_csv('./CleanedCSV/C_smithsonian.csv', index=False)
tibet.to_csv('./CleanedCSV/C_tibetMuseum.csv', index=False)
tszshan.to_csv('./CleanedCSV/C_tszshanMuseum.csv', index=False)

# ------------------------------------------------------------------------
# ------------------------------------------------------------------------

# All data across collections

sculptureDF = pd.concat([sculptureDF, rietbergCat], ignore_index=True)
sculptureDF = pd.concat([sculptureDF, colbaseCat], ignore_index=True)
sculptureDF = pd.concat([sculptureDF, smithsonianCat], ignore_index=True)
sculptureDF = pd.concat([sculptureDF, staatlicheCat], ignore_index=True)
sculptureDF = pd.concat([sculptureDF, tibetCat], ignore_index=True)
sculptureDF = pd.concat([sculptureDF, asianArtCat], ignore_index=True)
sculptureDF = pd.concat([sculptureDF, metCat], ignore_index=True)
sculptureDF = pd.concat([sculptureDF, tszshanCat], ignore_index=True)

regionMatch = {
    'Uttar Pradesh': "India",
    'Pakistan': 'Gandhara',
    'Afghanistan': 'Gandhara',
    'Gandhāra': 'Gandhara',
    'Burma': "Myanmar",
    'Zhou Xun': 'China',
    'Qiao Bin': 'China',
    'Kaikei': 'Japan',
    'Ogawa Haritsu (Ritsuō)': 'Japan',
    'ThaiThai': 'Thailand',
    'Intan': "Japan"
}


for i in range(len(sculptureDF)):
    wordsFound = False

    try: 
        for w in filterWords:
            if w in sculptureDF.at[i, 'Title']:
                wordsFound = True
                break

        if wordsFound == False:
            sculptureDF = sculptureDF.drop(i)

    except:
        sculptureDF = sculptureDF.drop(i)

sculptureDF = sculptureDF.reset_index(drop=True)

# Clear Origin to group

Classes = ["Gandhara", "Thailand", "Tibet", "India", "China", "Nepal", "Indonesia", "Myanmar", "Laos", "Pakistan", "Sri Lanka", "Cambodia", 'Afghanistan']

for o in range(len(sculptureDF)):
    # remove the one that origin is unclear
    if 'or' in str(sculptureDF.at[o, 'Origin']):
        sculptureDF = sculptureDF.drop(o)

    elif 'Asia' in str(sculptureDF.at[o, 'Origin']):
        sculptureDF = sculptureDF.drop(o)

    elif 'Himalaya' in str(sculptureDF.at[o, 'Origin']):
                sculptureDF = sculptureDF.drop(o)

    elif 'Berlin' in str(sculptureDF.at[o, 'Origin']):
                    sculptureDF = sculptureDF.drop(o)

sculptureDF = sculptureDF.reset_index(drop=True)
for o in range(len(sculptureDF)):
    for c in Classes:
        if c in str(sculptureDF.at[o, 'Origin']):
            sculptureDF.at[o, 'Origin'] = c

sculptureDF['Origin'] = sculptureDF['Origin'].replace(regionMatch)

# drop NA
sculptureDF = sculptureDF.dropna()

# drop low counts
# where 20% of the counts is less than 5
dropList = []
oList = list(sculptureDF['Origin'].unique())

for i in list(sculptureDF['Origin'].unique()):
    if (sculptureDF['Origin'] == i).sum() < 25:
        dropList.append(i)
         
sculptureDF = sculptureDF[~sculptureDF['Origin'].isin(dropList)]
sculptureDF = sculptureDF.reset_index(drop=True)

print(sculptureDF.groupby('Origin').count())

# add the to-be image name to the new column

sculptureDF.to_csv('./sculpturesData.csv', index=True)