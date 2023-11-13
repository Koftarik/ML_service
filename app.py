import pandas as pd
import streamlit as st
from PIL import Image
from model import open_data, fit_and_save


def process_main_page():
    show_main_page()


def show_main_page():
    image = Image.open('data/streamlit.png')

    st.set_page_config(
        layout='wide',
        page_title='Passenger satisfaction',
        page_icon=image,
        initial_sidebar_state='auto',

    )

    st.write(
        """
        # Классификация впечатлений клиентов авиакомпании
        Определяем, кому из пассажиров понравился полёт, а кому – нет.
        """
    )

    st.image(image)

def write_predict():
    pass


if __name__ == "__main__":
    process_main_page()