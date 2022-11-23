import firebase_admin
from firebase_admin import credentials
from firebase_admin import messaging

cred = credentials.Certificate("./config/fcm_key.json")
firebase_admin.initialize_app(cred)

# 안드로이드에서 나온 토큰 값
registration_token = 'cl1sNiNVIG8:APA91bEQ6USv7nu1Wwi4h--ewAK6E-l5TWhE85g3oBdUUfhVBp2TXhk4hVJdofpZwxGviEuFa4mZ4dUpKZtItZVxCXX6wo9NBgStb0sO2ZtPVxgCIgJmpEmOjoaeV8CKkZgOJurCqlEq'


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
