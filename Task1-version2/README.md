# Dl-Internship. Task1-version2

## Завдання
Розробити backend сервіс для встановлення нативного з'єднання з вузлом P2P мережі блокчейну та моніторингу інформації облікової системи. 

## Загальна характеристика програми
Сервіс представляє собою додаток представлений у вигляді інтерфейсів:  
base_blockchain - абстрактний базовий клас;   
btc_blockchain - клас BTC, містить основні методи для взаємодії та обміну повідомленнями з вузлом через P2P Mainnet мережу з використанням сокетів (PORT: 8333);    
eth_blockchin - клас ETH (на стадії дослідження).    

## Технології 
- Мова програмування: Python;  
- Середовище розробки: PyCharm;     
- Механізм встановлення з'єднання з вузлом мережі: Socket (TCP message request/response);  

## Процес запуску програми
У терміналі набрати команду python app.py

## Екранні форми роботи програми
Результат виконання сервісу:  
![Image text](https://github.com/tu4k0/DL-Internship/blob/master/Task1-version2/app_images/task_result1.png)    
![Image text](https://github.com/tu4k0/DL-Internship/blob/master/Task1-version2/app_images/task_result2.png)   
![Image text](https://github.com/tu4k0/DL-Internship/blob/master/Task1-version2/app_images/task_result3.png)  

Wireshark (Моніторинг інтернет пакетів протоколу Bitcoin):  
![Image text](https://github.com/tu4k0/DL-Internship/blob/master/Task1-version2/app_images/wireshark_result.png)    

!! Дана версія програми не є остаточною та демонструє першу версію сервісу !!