import pandas as pd
import streamlit as st
from PIL import Image
from model import open_data, fit_and_save, predict_on_input


def process_main_page():
    show_main_page()


def show_main_page():
    image = Image.open('data/plane.PNG')

    st.set_page_config(
        layout='wide',
        page_title='Удовлетворенность полетом',
        page_icon=image,
        initial_sidebar_state='auto',

    )

    st.write(
        """
        # Классификация впечатлений клиентов авиакомпании
        Определяем, кому из пассажиров понравился полёт, а кому нет.
        """
    )

    st.image(image)

    passenger_info()
    delay_info()
    estimated_data()


def input_to_df(gender,ticket,loyality,age,distance,trip_type,
                dep_delay, arr_delay,
                booking, baggage, seat, wifi, inf_service, onl_board, gate,
                clean, food, onb_service, ch_service, dep_arr_time, leg_room, inf_ent):
    pass


def passenger_info():

    st.write('Введите информацию о себе')
    col1, col2 = st.columns(2)

    with col1:
        gender = st.selectbox('Ваш пол', ['Мужской','Женский'])
        ticket = st.selectbox('Класс билета', ['Бизнес', 'Эко', 'Эко плюс'])
        loyality = st.selectbox('Есть ли у вас карта лояльности', ['Да', 'Нет'])

    with col2:
        age = st.slider('Ваш возраст', min_value=5, max_value=80)
        distance = st.slider('Длина перелёта', min_value=100, max_value=4000)
        trip_type = st.selectbox('Цель поездки', ['Личная', 'По работе'])
    
    #return gender,ticket,loyality,age,distance,trip_type


def delay_info():

    st.divider()
    st.write('Были ли задержки в расписании?')
    col1, col2 = st.columns(2)

    with col1:
        dep_delay = st.slider('Задержка вылета, мин', min_value=0, max_value=180)
    with col2:
        arr_delay = st.slider('Задержка прилёта, мин', min_value=0, max_value=180)

    st.divider()

    #return dep_delay, arr_delay


def estimated_data():

    st.write('Заполните анкету')
    col1, col2, col3 = st.columns(3)

    with col1:
        booking = st.radio('Онлайн бронирование', [0, 1, 2, 3, 4, 5])
        baggage = st.radio('Обращение с багажом', [0, 1, 2, 3, 4, 5])
        seat = st.radio('Удобство кресла', [0, 1, 2, 3, 4, 5])
        wifi = st.radio('Wi-fi на борту', [0, 1, 2, 3, 4, 5])
        inf_service = st.radio('Обслуживание на борту', [0, 1, 2, 3, 4, 5])      

    with col2:
        onl_board = st.radio('Онлайн регистрация', [0, 1, 2, 3, 4, 5])
        gate = st.radio('Расположение выхода на посадку', [0, 1, 2, 3, 4, 5])
        clean = st.radio('Чистота на борту', [0, 1, 2, 3, 4, 5])
        food = st.radio('Еда и напитки на борту', [0, 1, 2, 3, 4, 5])
        onb_service = st.radio('Обслуживание на посадке', [0, 1, 2, 3, 4, 5])      

    with col3:
        ch_service = st.radio('Регистрация на рейс', [0, 1, 2, 3, 4, 5])
        dep_arr_time = st.radio('Время вылета и прилета', [0, 1, 2, 3, 4, 5])
        leg_room = st.radio('Место в ногах', [0, 1, 2, 3, 4, 5])
        inf_ent = st.radio('Развлечения на борту', [0, 1, 2, 3, 4, 5])

    #return booking, baggage, seat, wifi, inf_service, onl_board, gate,
    #  clean, food, onb_service, ch_service, dep_arr_time, leg_room, inf_ent

def push_button():
    pass


def write_predict(df: pd.DataFrame):

    pred, proba = predict_on_input(df)

    if pred == 1:
        st.success('Ура! Пассажир доволен!')
        with st.expander('Подробнее'):
            st.write(f'Вероятность этого: **`{round(max(proba[0]), 3)}`**')
        
    elif pred == 0:
        st.error('О нет! Пассажир не доволен...')
        with st.expander('Подробнее'):
            st.write(f'Вероятность этого: **`{round(max(proba[0]), 3)}`**')          

    else:
        st.error('Ошибка, что-то пошло не так...')



if __name__ == "__main__":

    process_main_page()