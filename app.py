import pandas as pd
import streamlit as st
from PIL import Image
from model import predict_on_input, encoding_and_scaling
import time


def process_main_page():
    show_main_page()
    render_main_page()


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


def input_to_df(gender,ticket,loyality,age,distance,trip_type,
                dep_delay, arr_delay,
                booking, baggage, seat, wifi, inf_service, onl_board, gate,
                clean, food, onb_service, ch_service, dep_arr_time, leg_room, inf_ent):
    
    rule = {
            'Женский': 'Female',
            'Мужской': 'Male',
            'Личная': 'Personal Travel',
            'По работе': 'Business travel',
            'Да': 'Loyal Customer',
            'Нет': 'disloyal Customer',
            'Эко': 'Eco',
            'Эко плюс': 'Eco plus',
            'Бизнес': 'Business',
            }

    data = {
            'Class_Eco': 1 if ticket == 'Эко' else 0,
            'Class_Eco Plus': 1 if ticket == 'Эко плюс' else 0,
            'Gender': rule[gender],
            'Age': age,
            'Customer Type': rule[loyality],
            'Type of Travel': rule[trip_type],       
            'Flight Distance': distance,
            'Departure Delay in Minutes': dep_delay,
            'Arrival Delay in Minutes': arr_delay,
            'Inflight wifi service': wifi,
            'Departure/Arrival time convenient': dep_arr_time,
            'Ease of Online booking': booking,
            'Gate location': gate,
            'Food and drink': food,
            'Online boarding': onl_board,
            'Seat comfort': seat,
            'Inflight entertainment': inf_ent,
            'On-board service': onb_service,
            'Leg room service': leg_room,
            'Baggage handling': baggage,
            'Checkin service': ch_service,
            'Inflight service': inf_service,
            'Cleanliness': clean,
            }


    df = pd.DataFrame(data, index=[0])
    st.write(df.head(5)) #debug
    df=encoding_and_scaling(df, app=True)
    st.write(df.head(5)) #debug
    return df



def render_main_page():

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
    

    st.divider()
    st.write('Были ли задержки в расписании?')
    col1, col2 = st.columns(2)

    with col1:
        dep_delay = st.slider('Задержка вылета, мин', min_value=0, max_value=180)
    with col2:
        arr_delay = st.slider('Задержка прилёта, мин', min_value=0, max_value=180)

    st.divider()


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
    
    
    col1,col2,col3 = st.columns(3)
    if col2.button('Рассчитать'):

        user_df = input_to_df(gender,ticket,loyality,age,distance,trip_type,
                dep_delay, arr_delay,
                booking, baggage, seat, wifi, inf_service, onl_board, gate,
                clean, food, onb_service, ch_service, dep_arr_time, leg_room, inf_ent)

        with st.spinner('Рассчитываем...'):
            time.sleep(1)
            write_predict(user_df)


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