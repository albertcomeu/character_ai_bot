from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():
    html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            .character-container {
                display: flex;
                flex-direction: column;
                align-items: center;
                text-align: center;
                margin-bottom: 20px;
            }
            .character-container img {
                width: 350px;  /* Уменьшение ширины изображения */
                height: 350px;  /* Уменьшение высоты изображения */
                background: transparent url('/static/mario.png') 0% 0% no-repeat padding-box;
                box-shadow: 0px 15px 15px #00000029;
                border: 3px solid #27A7E7;
                border-radius: 50px;
                opacity: 1;
                margin-bottom: 10px;
                margin-right: -10px;  /* Сдвиг изображения на 10 пикселей вправо */
            }
            .character-container p {
                width: 392px;
                font: normal normal bold 40px/48px SF Pro;
                letter-spacing: 0px;
                color: #27A7E7;
                opacity: 1;
                margin: 0;
            }
            .character-container p.character-name {
                margin-top: -10px;
                text-align: center;
            }
            .character-container p.character-description {
                text-align: center;
                font-weight: 300;
            }
            .character-container:last-child {
                margin-bottom: 0;
            }
        </style>
    </head>
    <body>
        
        <div class="character-container">
            <a href="javascript:void(0);" onclick="sendCharacterSelection('mario')">
                <img src="/static/mario.jpg" alt="Картинка 1">
                <p class="character-name" style="white-space: nowrap;">Марио</p>
                <p class="character-description" style="white-space: nowrap;">Персонаж</p>
            </a>
        </div>

        <div class="character-container">
            <a href="javascript:void(0);" onclick="sendCharacterSelection('Albert Enshtein')">
                <img src="/static/albert.jpg" alt="Картинка 2">
                <p class="character-name" style="white-space: nowrap;">Альберт Эйнштейн</p>
                <p class="character-description" style="white-space: nowrap;">Физик-теоретик</p>
            </a>
        </div>

        <script src="https://telegram.org/js/telegram-web-app.js"></script>
        <script>
            function sendCharacterSelection(character) {
                let tg = window.Telegram.WebApp;
                tg.sendData(character);
            }
        </script>
    </body>
    </html>
    '''
    return html


if __name__ == '__main__':
    app.run(ssl_context=('localhost.crt', 'localhost.key'))
