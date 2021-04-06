import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import altair as alt
import plotly.express as px
from PIL import Image


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

#Covid vaccination data by country DataFrame
@st.cache
def load_data(Country):
	Country = '%20'.join(Country.split())
	url = "https://github.com/owid/covid-19-data/blob/master/public/data/vaccinations/country_data/" + Country + '.csv'
	html = pd.read_html(url, header = 0)
	df = html[0]
	raw = df.drop(df[df.vaccine == 'vaccine'].index) # Deletes repeating headers in content
	raw = raw.drop(['Unnamed: 0'],axis = 1)
	vaccine_data = raw.fillna(0)
	return vaccine_data


#Global Covid dataframe generation
@st.cache
def this_data():
	big_data = pd.read_csv('https://covid.ourworldindata.org/data/owid-covid-data.csv',header = 0)
	raw = big_data.drop(big_data[big_data.location == 'Asia'].index)
	raw = raw.drop(raw[raw.location == 'International'].index)
	raw = raw.drop(raw[raw.location == 'Africa'].index)
	raw = raw.drop(raw[raw.location == 'South America'].index)
	raw = raw.drop(raw[raw.location == 'North America'].index)
	raw = raw.drop(raw[raw.location == 'European Union'].index)
	raw = raw.drop(raw[raw.location == 'Europe'].index)
	raw = raw.drop(raw[raw.location == 'World'].index)
	big_df = raw.fillna(0)
	return big_df
my_df = this_data()
sample_df = my_df[['iso_code','location','continent','date','total_cases','new_cases','total_deaths',
				'people_vaccinated', 'people_fully_vaccinated', 'new_vaccinations','population','total_vaccinations',
				'people_vaccinated_per_hundred','people_fully_vaccinated_per_hundred','total_vaccinations_per_hundred']]

   #Menu Sidebar
menu = ["Home","Vaccination","Data Visualization","About"]
choice = st.sidebar.selectbox("MENU",menu)

if choice == "Home":
	st.title('COVID-19 daily vaccination records')
	st.markdown("""
	This app performs simple webscraping of Daily COVID-19 vaccinations!
	* **App by:** Nana Kwame Boakye
	""")
	image = Image.open('data\\coro.jpeg')
	st.image(image,use_column_width = True)
	st.markdown('<style>body{background-color: lightblue;}</style>',unsafe_allow_html = True)


elif choice == 'Vaccination':

   #Options menu for the Dataframe Analysis choice
	options =['Vaccination By Countries','Global Vaccination','Combine']
	globally =  st.sidebar.selectbox('Total people vaccinated globally',options)

	if globally == 'Vaccination By Countries':
		st.sidebar.subheader("Select Input Features")
		selected_country = st.sidebar.selectbox('Country',countries)


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
		st.markdown("**NOTE**: You can't unselect the last **date** and **vaccine type.**")
		st.dataframe(covid_free)

		# Download data of vaccinated people
		# https://discuss.streamlit.io/t/how-to-download-file-in-streamlit/1806
		def filedownload(df):
			csv = df.to_csv(index=False)
			b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
			href = f'<a href="data:file/csv;base64,{b64}" download="vaccinations.csv">Download CSV File</a>'
			return href

		st.markdown(filedownload(covid_free), unsafe_allow_html=True)

		  #brief article on covid vaccinations
		st.write(str(covid_free.loc[0]['location']) + ' started its COVID-19 vaccination on ' + str(covid_free.iloc[-1]['date']) +
		' and a total number of ' + str(covid_free['people_vaccinated'].sum()) + ' people have being vaccinated using ' + str(covid_free['vaccine'].unique()))

	elif globally == 'Global Vaccination':
		st.header('Display Global Covid-19 Data.')
		st.write('Data Dimension: ' + str(sample_df.shape[0]) + ' rows and ' + str(sample_df.shape[1]) + ' columns.')
		st.write(sample_df)

	elif globally == 'Combine':
		st.write('see you')

	else:
		st.header('Piechart')

elif choice == "Data Visualization":
	group = ['Global Data Vizualization','Visualization By Continents','Visualization by Countries']
	group_vis = st.sidebar.selectbox('Select',group)

	if group_vis == 'Global Data Visualization':
		st.header('Global Data Visualization')

	elif group_vis == 'Visualization By Continents':
		#st.header('Visualization By Continents')
		vis_continent = st.sidebar.selectbox('Select Chart Type',('Bar Chart','Pie Chart','Line Chart'))
		st.markdown("## **Continental Analysis**")

		 #DRAWING A BAR CHART
		if vis_continent == 'Bar Chart':
			continent_chart_select = st.sidebar.radio('Chart',('Total People Vaccinated','Vaccinated Per 100', 'People Fully Vaccinated','People Fully Vaccinated Per 100'))
			cols = ['people_fully_vaccinated_per_hundred', 'total_vaccinations', 'continent', 'total_vaccinations_per_hundred','people_fully_vaccinated']
			if continent_chart_select == 'Vaccinated Per 100': # chart of Vaccinated people per 100
				sns.set_style('whitegrid')
				vacc_amount = sample_df[cols].groupby('continent').mean().sort_values('total_vaccinations', ascending=False).dropna(subset=['total_vaccinations'])
				vacc_amount = vacc_amount.iloc[:7]
				vacc_amount = vacc_amount.sort_values('total_vaccinations_per_hundred', ascending=False)
				plt.figure(figsize=(4, 3))
				sns.barplot(y = vacc_amount.index, x = vacc_amount.total_vaccinations_per_hundred,  palette = 'Paired')
				plt.ylabel('Continent')
				plt.xlabel('Number of vaccinated people per hundred')
				st.set_option('deprecation.showPyplotGlobalUse', False)
				st.pyplot()

			elif continent_chart_select == 'Total People Vaccinated': #chart of 'Total People Vaccinated
				sns.set_style('darkgrid')
				vacc_amount = sample_df[cols].groupby('continent').max().sort_values('total_vaccinations', ascending=False).dropna(subset=['total_vaccinations'])
				vacc_amount = vacc_amount.iloc[:7]
				plt.figure(figsize=(4, 3))
				sns.barplot(y = vacc_amount.index, x =vacc_amount.total_vaccinations, palette = 'Paired')
				plt.ylabel('Continent')
				plt.xlabel('Number of vaccinated citizens')
				st.set_option('deprecation.showPyplotGlobalUse', False)
				st.pyplot()

			elif continent_chart_select == 'People Fully Vaccinated': # Chart of People Fully Vaccinated
				sns.set_style('darkgrid')
				vacc_amount = sample_df[cols].groupby('continent').sum().sort_values('people_fully_vaccinated', ascending=False).dropna(subset=['people_fully_vaccinated'])
				vacc_amount = vacc_amount.iloc[:7]
				plt.figure(figsize=(4, 3))
				sns.barplot(y = vacc_amount.index, x =vacc_amount.people_fully_vaccinated, palette = 'Paired')
				plt.ylabel('Continent')
				plt.xlabel('Number of People Fully Vaccinated')
				st.set_option('deprecation.showPyplotGlobalUse', False)
				st.pyplot()

			else: #Chart of People Fully Vaccinated Per 100
				sns.set_style('darkgrid')
				vacc_amount = sample_df[cols].groupby('continent').mean().sort_values('people_fully_vaccinated_per_hundred', ascending=False).dropna(subset=['people_fully_vaccinated_per_hundred'])
				vacc_amount = vacc_amount.iloc[:7]
				plt.figure(figsize=(4, 3))
				sns.barplot(y = vacc_amount.index, x =vacc_amount.people_fully_vaccinated_per_hundred, palette = 'Paired')
				plt.ylabel('Continent')
				plt.xlabel('people_fully_vaccinated_per_hundred')
				st.set_option('deprecation.showPyplotGlobalUse', False)
				st.pyplot()




			#Drawing of the pie Chart
		elif vis_continent == 'Pie Chart':
			continent_select = st.sidebar.selectbox('Select Continent',sample_df['continent'].unique())
			selected_continent = sample_df[sample_df['continent'] == continent_select]
			status_select = st.sidebar.radio('Status',('total_cases','total_deaths','people_vaccinated', 'people_fully_vaccinated',))
			st.markdown("Please **NOTE** the **0** represents continents that were not defined but valuable in our analysis.")
			if status_select == 'total_cases':
				st.header('Total Comfrimed cases')
				fig = px.pie(sample_df, values = sample_df['total_cases'],names = sample_df['continent'])
				st.plotly_chart(fig)
			elif status_select == 'people_vaccinated':
				st.header('People Vaccinated')
				fig = px.pie(sample_df, values = sample_df['people_vaccinated'],names = sample_df['continent'])
				st.plotly_chart(fig)
			elif status_select == 'total_deaths':
				st.header('Total Deaths')
				fig = px.pie(sample_df, values = sample_df['total_deaths'],names = sample_df['continent'])
				st.plotly_chart(fig)
			else:
				st.header('People Fully Vaccinated')
				fig = px.pie(sample_df, values = sample_df['people_fully_vaccinated'],names = sample_df['continent'])
				st.plotly_chart(fig)

		      #Drawing Line chart
		elif vis_continent == 'Line Chart':
			st.header('This is a line chart.')



	else:
		country_chart_select = st.sidebar.radio('Chart',('Total People Vaccinated','Vaccinated Per 100', 'People Fully Vaccinated','People Fully Vaccinated Per 100'))
		st.header('Visualization by Countries')
		cols = ['people_fully_vaccinated_per_hundred', 'total_vaccinations', 'location', 'total_vaccinations_per_hundred','people_fully_vaccinated']
		if country_chart_select == 'Vaccinated Per 100':
			sns.set_style('whitegrid')
			vacc_amount = sample_df[cols].groupby('location').max().sort_values('total_vaccinations', ascending=False).dropna(subset=['total_vaccinations'])
			vacc_amount = vacc_amount.iloc[:10]
			vacc_amount = vacc_amount.sort_values('total_vaccinations_per_hundred', ascending=False)
			plt.figure(figsize=(5, 4))
			sns.barplot(y = vacc_amount.index, x = vacc_amount.total_vaccinations_per_hundred,  palette = 'Paired')
			plt.ylabel('Countries')
			plt.xlabel('Number of vaccinated people per hundred')
			st.set_option('deprecation.showPyplotGlobalUse', False)
			st.subheader('Chart Showing Top 10 Countries.')
			st.pyplot()

		elif country_chart_select == 'Total People Vaccinated':
			sns.set_style('darkgrid')
			vacc_amount = sample_df[cols].groupby('location').max().sort_values('total_vaccinations', ascending=False).dropna(subset=['total_vaccinations'])
			vacc_amount = vacc_amount.iloc[:10]
			plt.figure(figsize=(5, 4))
			sns.barplot(y = vacc_amount.index, x =vacc_amount.total_vaccinations, palette = 'Paired')
			plt.ylabel('Countries')
			plt.xlabel('Number of vaccinated citizens')
			st.set_option('deprecation.showPyplotGlobalUse', False)
			st.subheader('Total people vaccinated per country')
			st.pyplot()

		elif country_chart_select == 'People Fully Vaccinated': # Chart of People Fully Vaccinated
				sns.set_style('darkgrid')
				vacc_amount = sample_df[cols].groupby('location').sum().sort_values('people_fully_vaccinated', ascending=False).dropna(subset=['people_fully_vaccinated'])
				vacc_amount = vacc_amount.iloc[:10]
				plt.figure(figsize=(4, 3))
				sns.barplot(y = vacc_amount.index, x =vacc_amount.people_fully_vaccinated, palette = 'Paired')
				plt.ylabel('Country')
				plt.xlabel('Number of People Fully Vaccinated')
				st.set_option('deprecation.showPyplotGlobalUse', False)
				st.pyplot()

		else: #Chart of People Fully Vaccinated Per 100
				sns.set_style('darkgrid')
				vacc_amount = sample_df[cols].groupby('location').mean().sort_values('people_fully_vaccinated_per_hundred', ascending=False).dropna(subset=['people_fully_vaccinated_per_hundred'])
				vacc_amount = vacc_amount.iloc[:10]
				plt.figure(figsize=(4, 3))
				sns.barplot(y = vacc_amount.index, x =vacc_amount.people_fully_vaccinated_per_hundred, palette = 'Paired')
				plt.ylabel('Country')
				plt.xlabel('people_fully_vaccinated_per_hundred')
				st.set_option('deprecation.showPyplotGlobalUse', False)
				st.pyplot()




else:
	st.title("About")
