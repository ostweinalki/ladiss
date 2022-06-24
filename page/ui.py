import time
import streamlit as st
import pandas as pd
from utils.load import get_lager, read_file_as_df, add_diss_to_s3
from typing import Tuple


def run() -> None:
    '''Main function to display the user interface'''

    # get lager
    lager = get_lager('lager.toml')

    # sidebar
    view = show_sidebar(lager)

    # main page
    show_page(lager, view)


def show_sidebar(lager: dict) -> None:
    '''Function to display the sidebar'''
    st.sidebar.subheader('Einstellungen')

    # add disser
    disser = get_disser(lager)

    # add options
    if disser != lager['update']['leiterrunde'][0]:

        # add a new diss
        add_diss(lager, disser)

        # delete a old diss
        del_diss(lager)

    # settings
    return change_view()


def show_page(lager: dict, view: str) -> None:
    '''Function to display the main page'''
    st.subheader('Ladiss-App')

    # add übersicht
    st.write('Übersicht der Ladiss-Liste')

    # df = pd.read_csv('ladiss_app.csv', header=0)
    df = read_file_as_df('ladissapp/ladiss_app.csv')

    if view == 'Liste':
        df_list = df.groupby('wen')['wieviel'].sum().rename(
            'Anzahl der Striche').sort_values(axis=0, ascending=False)
        st.write(df_list)

    if view == 'Balken':
        df = df.groupby('wen')['wieviel'].sum().rename(
            'Anzahl der Striche').sort_values(axis=0, ascending=False)
        st.bar_chart(df)

    if view == 'Torte':
        st.write(df)

    if view == 'Matrix':
        df_matrix = pd.crosstab(df.wer, df.wen)
        st.write(df_matrix)


def get_disser(lager: dict) -> str:
    return st.sidebar.selectbox(label='Wer bist du?',
                                options=lager['update']['leiterrunde'])


def add_diss(lager: dict, disser: str) -> Tuple[str, int]:
    with st.sidebar.expander(label='✅ Einen Diss verteilen'):
        # get options without disser
        options = lager['update']['leiterrunde'][1:]
        options.remove(disser)
        # input dissed und disses
        dissed = st.selectbox(label='Wen disst du?',
                              options=options)
        disses = st.number_input(label='Wie oft hast du gedisst?',
                                 min_value=1, max_value=10, value=1, step=1)
        # add diss to list
        if st.button('Diss eintragen!'):
            with st.spinner('Trage den Diss ein...'):
                time.sleep(.1)
                date = '2022-05-21'
                row = disser, dissed, date, disses
                add_diss_to_s3('ladissapp/ladiss_app.csv', row)
                st.balloons()
                st.success(
                    f'**{disser}** hat **{dissed}** {disses} Mal gedisst!')


def del_diss(lager):
    with st.sidebar.expander('❌ Einen Diss zurücknehmen'):
        st.write('Implement later...')
        # delete dis now from list
        if st.button('Diss entfernen!'):
            st.snow()


def change_view() -> str:
    with st.sidebar.expander('Ansicht ändern'):
        view = st.selectbox(label='Was soll angezeigt werden?:',
                            options=['Liste', 'Balken', 'Torte', 'Matrix'])
    return view
