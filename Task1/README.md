# Dl-Internship. Task1 

## Завдання
Розробити backend сервіс для встановлення вузла з'єднання блокчейну та моніторингу інформації облікової системи. 

## Загальна характеристика програми
Сервіс представляє собою веб-додаток на локалхості, що містить інтерфейс з двома вікнами.  
Перше вікно - з'єднання вузла з мережею облікової системи блокчейну, містить 2 кнопки: підключення вузла до блокчейну та запис даних облікової системи у БД (реалізовано через GET/POST запити).  
Друге вікно - моніторинг інформації про блок облікової системи ETH за номером. Також було реалізовано механізм обробки форми та перевірки даних на валідність.

## Особливості реалізації  
- Мова програмування: Python;  
- Середовище розробки: PyCharm;  
- Веб-фреймворк: Django; 
- СУБД: SQLite; 
- Механізм взаємодії з обліковою системою блокчейну: WEB3 API (ETH);  
- Механізм встановлення з'єднання з вузлом мережі: HTTPProvider Infura/Ganache (ETH); 

## Процес запуску програми
У терміналі .\web_service_ETH_node набрати команду python manage.py runserver та перейти за посиланням

## Екранні форми роботи програми
Перше вікно:  
![Image text](https://github.com/tu4k0/DL-Internship/blob/master/Task1/web_service_ETH_node/main/templates/main/images/Connect%20to%20node.png)  
![Image text](https://github.com/tu4k0/DL-Internship/blob/master/Task1/web_service_ETH_node/main/templates/main/images/Save%20data%20in%20DB.png)  

Друге вікно:  
![Image text](https://github.com/tu4k0/DL-Internship/blob/master/Task1/web_service_ETH_node/main/templates/main/images/Get%20Data.png)    

!! Дана версія програми не є остаточною та демонструє першу версію сервісу !!
