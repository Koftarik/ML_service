# Flight satisfaction
Сервис на основе модели логистической регрессии, предсказывающий удовлетворенность клиента полетом на основе анкеты, заполненной после полета. Модель обернута в веб-сервис на фреймворке Streamlit.
## Запущенное приложение на Streamlit Cloud
* [https://goralex02-flight-satisfaction.streamlit.app](https://goralex02-flight-satisfaction.streamlit.app)
## Файлы
* data: Папка с данными и моделями
* Airline_clients.ipynb: Ноутбук с исследованием и подготовкой данных, обучением модели
* model.py: Скрипт для создания классификатора Logistic Regression
* requirements.txt: Файл с требуемыми пакетами
* streamlit_app.py: Файл с приложением streamlit
## Технологии
Pandas, NumPy, matplotlib, seaborn, scikit-learn, streamlit
## Результат
Accuracy = 0.875, Precision = 0.868, Recall = 0.836
