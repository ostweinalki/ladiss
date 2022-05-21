import time
import streamlit as st
from utils.load import get_lager
from utils.diss import Disser
from typing import Tuple


def run() -> None:
    '''Main function to display the user interface'''

    # get lager
    lager = get_lager('lager.toml')

    # sidebar
    show_sidebar(lager)

    # main page
    show_page(lager)


def show_sidebar(lager: dict) -> None:
    '''Function to display the sidebar'''
    st.sidebar.subheader('Einstellungen')

    # add disser
    disser = get_disser(lager)

    # add options
    if disser != lager['update']['leiterrunde'][0]:

        # add a new diss
        dissed, disses = add_diss(lager, disser)

        # delete a old diss
        del_diss(lager)

    # settings
    change_view()


def show_page(lager: dict) -> None:
    '''Function to display the main page'''
    st.subheader('Ladiss-App')

    # add übersicht
    st.write('Übersicht der Ladiss-Liste')


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
                time.sleep(2)
                st.balloons()
                st.success(
                    f'**{disser}** hat **{dissed}** {disses} Mal gedisst!')
    return dissed, disses


def del_diss(lager):
    with st.sidebar.expander('❌ Einen Diss zurücknehmen'):
        st.write('Implement later...')
        # delete dis now from list
        if st.button('Diss entfernen!'):
            st.snow()


def change_view():
    with st.sidebar.expander('Ansicht ändern'):
        st.selectbox(label='Was soll angezeigt werden?:',
                     options=['Liste', 'Balken', 'Torte', 'Matrix'])
