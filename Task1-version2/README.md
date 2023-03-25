# Dl-Internship. Task1-version2

## Завдання
Розробити backend сервіс для встановлення нативного з'єднання з вузлом P2P мережі блокчейну та моніторингу інформації облікової системи. 

## Загальна характеристика програми
Сервіс представляє собою додаток представлений у вигляді інтерфейсів:  
base_blockchain - абстрактний базовий клас;   
btc_blockchain - клас Bitcoin, містить основні методи для взаємодії та обміну повідомленнями з вузлом через P2P Mainnet мережу з використанням сокетів (PORT: 8333, MSG: magic + command + length + checksum);    
eth_blockchin - клас Ethereum, містить основні методи для взаємодії та обміну повідомленнями з вузлом через P2P Mainnet мережу з використанням сокетів (PORT: 8545, MSG: JSON);      

## Технології 
- Мова програмування: Python 3.10.10;  
- Середовище розробки: PyCharm Pro 2021.3.2;
- CLI: Typer 0.7.0
- Механізм встановлення з'єднання з вузлом мережі: Socket (TCP message request/response);  

## Процес запуску програми/сеансу
У cmd за шляхом DL-Internship\Task1-version2\application набрати команду python main.py start-session

## Екранні форми роботи програми

# Оновлена Версія 2 - багатопотоковість та збір статистики (Bitcoin)  
![Image text](https://github.com/tu4k0/DL-Internship/blob/master/Task1-version2/app_images/version_2/Bitcoin_connection1.png)  
![Image text](https://github.com/tu4k0/DL-Internship/blob/master/Task1-version2/app_images/version_2/Bitcoin_connection2.png)  
![Image text](https://github.com/tu4k0/DL-Internship/blob/master/Task1-version2/app_images/version_2/Bitcoin_connection3.png)  
![Image text](https://github.com/tu4k0/DL-Internship/blob/master/Task1-version2/app_images/version_2/Bitcoin_connection4.png)  
![Image text](https://github.com/tu4k0/DL-Internship/blob/master/Task1-version2/app_images/version_2/Bitcoin_connection5.png)  

Опис виконання: користувач обирає облікову систему та задає IP адресу та порт вузла для підключення та кількість вузлів, з якими необхідно підтримувати з'єднання. Далі система у багатопотоковому режимі збирає статистику від кожного вузла та окремим потоком відображує зібрану статистику на екрані з оновленням 1 раз на 5 секунд.  

# Версія 1 (Не оновлена) 
python main.py --help  
![Image text](https://github.com/tu4k0/DL-Internship/blob/master/Task1-version2/app_images/version_1/--help.png)    

python main.py help  
![Image text](https://github.com/tu4k0/DL-Internship/blob/master/Task1-version2/app_images/version_1/help.png)   

python main.py start-session (BTC)  
![Image text](https://github.com/tu4k0/DL-Internship/blob/master/Task1-version2/app_images/version_1/start-session_BTC.png)  
![Image text](https://github.com/tu4k0/DL-Internship/blob/master/Task1-version2/app_images/version_1/start-session_BTC2.png)  

python main.py start-session (ETH)  
![Image text](https://github.com/tu4k0/DL-Internship/blob/master/Task1-version2/app_images/version_1/start-session_ETH1.png)  
![Image text](https://github.com/tu4k0/DL-Internship/blob/master/Task1-version2/app_images/version_1/start-session_ETH2.png)  
![Image text](https://github.com/tu4k0/DL-Internship/blob/master/Task1-version2/app_images/version_1/start-session_ETH3.png)  
![Image text](https://github.com/tu4k0/DL-Internship/blob/master/Task1-version2/app_images/version_1/start-session_ETH4.png)  

Wireshark (BTC):  
![Image text](https://github.com/tu4k0/DL-Internship/blob/master/Task1-version2/app_images/wireshark/wireshark_result.png)    

!! Можливі оновлення та покращення програмної реалізації завдання !!  