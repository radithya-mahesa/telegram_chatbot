# chatbot_telegram
just my telegram bot using python language, can give answer likes c.ai

* Method 1 :
Install python-telegram-bot, requests, and Flask.<br>cmd/terminal : <br>
<code><strong>pip install python-telegram-bot requests Flask</strong></code>

* Method 2:
Use requirements.txt but, you must write the code here (look in my repository).<br>cmd/terminal : <br>
<code><strong>pip install -r requirements.txt</strong></code>

* Method 3: Docker<br>
<code><strong>docker build -t py/telegram-chatbot:1.0.0 .</strong></code><br>
<code><strong>docker run -d -p 9000:9000 py/telegram-chatbot:1.0.0</strong></code><br>
Provides a list of the Docker containers :<br>
<code><strong>docker ps -a<strong></code>


- Also don't forget to install Python on your computer previously if u don't have Python
  
- make sure you create .env file inside your directory, Here's an example of the contents of .env<br>
<code>TOKEN=6800704828:CROTF8dKJ-YoUr-TeLeGrAm_ToKeN_HeRe<br>
BOT_USERNAME=@example_bot<br>
PORT=9000<br></code>

- Run in main.py
  
- Create your Telegram Bot in BotFather (can see the tutorial on youtube)

API Credit : Zanixon/ZTRdiamond or whoever :v
