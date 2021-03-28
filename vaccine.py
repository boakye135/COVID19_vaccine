import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np



countries = ['Afghanistan','Albania','Algeria','Andorra','Angola','Anguilla','Argentina','Australia','Austria','Azerbaijan',
'Bahamas','Bahrain','Bangladesh','Barbados','Belarus','Belgium','Belize','Bermuda','Bolivia','Brazil','Bulgaria','Cambodia','Canada',
'Chile','China','Colombia','Croatia','Cyprus','Czechia','Denmark','Dominica','Ecuador','Egypt','England','Estonia','Finland','France','Germany',
'Ghana','Gibraltar','Greece','Greenland','Grenada','Guernsey','Guatemala','Guinea','Guyana','Honduras','Hungary','Iceland','India','Indonesia','Iran',
'Ireland','Israel','Italy','Jamaica','Japan','Jersey','Jordan','Kazakhstan','Kenya','Kuwait','Laos','Latvia','Lebanon','Liechtenstein','Lithuania',
'Luxembourg','Macao','Malawi','Malaysia','Maldives','Malta','Mauritius','Mexico','Moldova','Monaco','Mongolia','Montenegro','Montserrat','Morocco',
'Mozambique','Myanmar','Nepal','Netherlands','Nigeria','Norway','Oman','Pakistan','Palau','Panama','Paraguay','Peru','Philippines','Poland',
'Portugal','Qatar','Romania','Russia','Rwanda','Senegal','Serbia','Seychelles','Singapore','Slovakia','Slovenia','Spain','Suriname',
'Sweden','Switzerland','Thailand','Tunisia','Turkey','Uganda','Ukraine','Uruguay','Venezuela','Vietnam','Zimbabwe']

menu = ["Home","Single Extractor","Bulk Extractor","DataStorage","About"]
choice = st.sidebar.selectbox("Menu",menu)


if choice == "Home":
	st.title('COVID-19 daily vaccination records')
	st.markdown("""
	This app performs simple webscraping of Daily COVID-19 vaccinations!
	* **App by:** Nana Kwame Boakye
	""")
	st.sidebar.subheader("Select Input Features")
	selected_country = st.sidebar.selectbox('Country',countries)
	@st.cache
	def load_data(Country):
		url = "https://github.com/owid/covid-19-data/blob/master/public/data/vaccinations/country_data/" + Country + '.csv'
		html = pd.read_html(url, header = 0)
		df = html[0]
		raw = df.drop(df[df.vaccine == 'vaccine'].index) # Deletes repeating headers in content
		raw = raw.drop(['Unnamed: 0'],axis = 1)
		vaccine_data = raw.fillna(0)
		return vaccine_data
	vaccine_data = load_data(selected_country)

	# Sidebar - Vaccine type
	sorted_unique_vaccine = sorted(vaccine_data.vaccine.unique())
	selected_vaccine = st.sidebar.multiselect('Vaccine Type', sorted_unique_vaccine, sorted_unique_vaccine)

	sorted_unique_date = sorted(vaccine_data.date.unique())
	selected_date = st.sidebar.multiselect('Vaccination Date',sorted_unique_date,sorted_unique_date)

	# Filtering data
	covid_free = vaccine_data[(vaccine_data.vaccine.isin(selected_vaccine)) & (vaccine_data.date.isin(selected_date))]
	st.header('Display Daily Vaccinations by Country.')
	st.write('Data Dimension: ' + str(covid_free.shape[0]) + ' rows and ' + str(covid_free.shape[1]) + ' columns.')
	st.dataframe(covid_free)

	# Download data of vaccinated people
	# https://discuss.streamlit.io/t/how-to-download-file-in-streamlit/1806
	def filedownload(df):
		csv = df.to_csv(index=False)
		b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
		href = f'<a href="data:file/csv;base64,{b64}" download="vaccinations.csv">Download CSV File</a>'
		return href

	st.markdown(filedownload(covid_free), unsafe_allow_html=True)


elif choice == "Single Extractor":
	list_of_df = []
	full_table = pd.DataFrame()
	for country in countries:
		url_2 = "https://github.com/owid/covid-19-data/blob/master/public/data/vaccinations/country_data/" +country + '.csv'
		html_2 = pd.read_html(url_2, header = 0)
		df_2 = html_2[0]
		raw_2 = df_2.drop(df_2[df_2.vaccine == 'vaccine'].index) # Deletes repeating headers in content
		raw_2 = raw_2.drop(['Unnamed: 0'],axis = 1)
		vaccine_data = raw_2.fillna(0)
		list_of_df.append(vaccine_data)
	full_df = pd.concat(list_of_df,ignore_index=True)
	globally =  st.sidebar.checkbox('Total people vaccinated globally')
	if globally:
		st.write(full_df)

else:
	st.subheader("About")
