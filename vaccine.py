import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import altair as alt
import plotly.express as px




countries = ['Afghanistan','Albania','Algeria','Andorra','Angola','Anguilla','Antigua and Barbuda','Argentina','Australia','Austria','Azerbaijan',
'Bahamas','Bahrain','Bangladesh','Barbados','Belarus','Belgium','Belize','Bermuda','Bolivia','Brazil','Bulgaria','Cambodia','Canada','Cayman Islands',
'Chile','China','Colombia','Costa Rica','Croatia','Cyprus','Czechia','Denmark','Dominica','Dominican Republic','Ecuador','Egypt','El Salvador','England',
'Equatorial Guinea','Estonia','Faeroe Islands','Falkland Islands','Finland','France','Germany','Ghana','Gibraltar','Greece','Greenland','Grenada','Guernsey',
'Guatemala','Guinea','Guyana','Honduras','Hong Kong','Hungary','Iceland','India','Indonesia','Iran','Ireland','Isle of Man','Israel','Italy','Jamaica','Japan',
'Jersey','Jordan','Kazakhstan','Kenya','Kuwait','Laos','Latvia','Lebanon','Liechtenstein','Lithuania','Luxembourg','Macao','Malawi','Malaysia','Maldives',
'Malta','Mauritius','Mexico','Moldova','Monaco','Mongolia','Montenegro','Montserrat','Morocco','Mozambique','Myanmar','Namibia','Nepal','Netherlands','New Zealand',
'Nigeria','North Macedonia','Northern Cyprus','Northern Ireland','Norway','Oman','Pakistan','Palau','Panama','Paraguay','Peru','Philippines','Poland',
'Portugal','Qatar','Romania','Russia','Rwanda','Saint Helena','Saint Kitts and Nevis','Saint Lucia','Saint Vincent and the Grenadines','San Marino',
'Saudi Arabia','Senegal','Serbia','Seychelles','Sierra Leone','Singapore','Slovakia','Slovenia','South Africa','South Korea','Spain','Suriname',
'Sweden','Switzerland','Thailand','Togo','Trinidad and Tobago','Turks and Caicos Islands','Tunisia','Turkey','Uganda','Ukraine','United Arab Emirates',
'United Kingdom','United States','Uruguay','Venezuela','Vietnam','Wales','Zimbabwe']

menu = ["Home","DataFrame Analysis","Data Visualization","DataStorage","About"]
choice = st.sidebar.selectbox("MENU",menu)

if choice == "Home":
	st.title('COVID-19 daily vaccination records')
	st.markdown("""
	This app performs simple webscraping of Daily COVID-19 vaccinations!
	* **App by:** Nana Kwame Boakye
	""")
	st.sidebar.subheader("Select Input Features")
	selected_country = st.sidebar.selectbox('Country',countries)


	#for country in selected_country:
	#	country = '%20'.join(country.split())
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



elif choice == 'DataFrame Analysis':
	url = 'https://covid.ourworldindata.org/data/owid-covid-data.csv'
	big_data = pd.read_csv(url,header = 0)
	raw = big_data.drop(big_data[big_data.location == 'Asia'].index)
	raw = raw.drop(raw[raw.location == 'International'].index)
	raw = raw.drop(raw[raw.location == 'Africa'].index)
	raw = raw.drop(raw[raw.location == 'South America'].index)
	raw = raw.drop(raw[raw.location == 'North America'].index)
	raw = raw.drop(raw[raw.location == 'European Union'].index)
	raw = raw.drop(raw[raw.location == 'Europe'].index)
	raw = raw.drop(raw[raw.location == 'World'].index)
	big_df = raw.fillna(0)
	sample_df = big_df[['iso_code','location','continent','date','total_cases','new_cases','total_deaths',
	                    'people_vaccinated', 'people_fully_vaccinated', 'new_vaccinations','population','total_vaccinations',
			            'people_vaccinated_per_hundred','people_fully_vaccinated_per_hundred','total_vaccinations_per_hundred']]

   #Options menu for the Dataframe Analysis choice
	options =['DataFrame','Piechart','Combine']
	globally =  st.sidebar.selectbox('Total people vaccinated globally',options)
	if globally == 'DataFrame':
		st.write(sample_df)
	elif globally == 'Combine':
		c1,c2 = st.beta_columns(2)
		cols = ['location', 'total_vaccinations', 'iso_code', 'total_vaccinations_per_hundred']
		with c1:
			sns.set_style('darkgrid')
			vacc_amount = sample_df[cols].groupby('location').max().sort_values('total_vaccinations', ascending=False).dropna(subset=['total_vaccinations'])
			vacc_amount = vacc_amount.iloc[:10]
			vacc_amount = vacc_amount.sort_values('total_vaccinations_per_hundred', ascending=False)
			plt.figure(figsize=(12, 12))
			sns.barplot(y = vacc_amount.index, x = vacc_amount.total_vaccinations_per_hundred,  palette = 'GnBu_d')
			plt.ylabel('Countries')
			plt.xlabel('Number of vaccinated people per hundred')
		    #plt.xticks(rotation = 45)
			st.set_option('deprecation.showPyplotGlobalUse', False)
			st.subheader('DataFrame')
			st.pyplot()

		#chart 2
		with c2:
			vacc_amount = sample_df[cols].groupby('location').max().sort_values('total_vaccinations', ascending=False).dropna(subset=['total_vaccinations'])
			vacc_amount = vacc_amount.iloc[:10]
			plt.figure(figsize=(12, 12))
			sns.barplot(y = vacc_amount.index, x =vacc_amount.total_vaccinations, color = 'r')
			plt.title('Total people vaccinated per country')
			plt.yticks(rotation = 60)
			plt.ylabel('Countries')
			plt.xlabel('Number of vaccinated citizens (per 10 Million)')
			st.set_option('deprecation.showPyplotGlobalUse', False)
			st.subheader('Visualization')
			st.pyplot()
	else:
		st.header('Piechart')




elif choice == "Data Visualization":
	st.header('Data Visualization')

else:
	st.title("About")
	first,last = st.beta_columns(2)
	first.subheader('COVID-19: What to do if..')
	first.graphviz_chart("""
	digraph{
	come into contact>>like
	like->share
	}
	""")
	last.write('I selectbox')
	last.image('C:\\Users\\Samuel\\Desktop\\vid.jpg',caption = 'getting the vaccine',use_column_width = True)
