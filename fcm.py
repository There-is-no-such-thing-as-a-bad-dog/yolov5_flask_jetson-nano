import firebase_admin
from firebase_admin import credentials
from firebase_admin import messaging

cred = credentials.Certificate("./config/fcm_key.json")
firebase_admin.initialize_app(cred)

# 안드로이드에서 나온 토큰 값

# 에뮬레이터
# registration_token = 'fvK5K78WpiI:APA91bFxJyEcNr-AC6pYR0wBvUwaDk5FNudrw065wSRrs0WqACCkw4wT6qeI3E77FOJyf7w3r51sMOzaim8L8SpeMQm1gSpcJoBXMKfmVbl5C4XtYTcyD7b5FPIhO6AHmms1e-FbzSoQ'

# 실물
registration_token = 'cSH2MKuxkHw:APA91bGYcfIaQQtmikKjTzSq4z_W3N_f-8hY0D0CZbTko_w66vVEtcQNWCJ8QZubHSL7PYM69QY6otqmuuIQHZyxvdesZV9h0bPtfuZvEofONh282X24Dpgp7UsLEFRMFKMPrhUTz7uq'

def fcm_send(action):
    message = messaging.Message(
        notification=messaging.Notification(
            title='이상행동감지',
            body=action
        ),
        token=registration_token,
    )

    response = messaging.send(message)
    print('Successfully sent message:', response)
