MIN_LENGTH_USER_NAME = 1
MAX_LENGTH_USER_NAME = 50
MIN_LENGTH_USER_PASSWORD = 8
INVALID_PASS_MIN_LEN = 'Пароль не может быть меньше 8 символов'
INVALID_PASS_CONSIST_EMAIL = 'Пароль не должен состоять из e-mail'
MAX_LENGTH_CHAT_NAME = 100
MAX_LENGTH_MESSAGE_TEXT = 1000

JWT_LIFETIME_SECONDS = 3600

CHAT_FORBIDDEN = 'Для пользователя ({}) доступ запрещён к чату с id: {}'
CHAT_NOT_FOUND = 'Не существует чата с id: {}'
CHAT_FIELD_ERROR = 'Для {} чата необходимо указать {}'
CHAT_ALREADY_EXISTS = (
    'Уже существует приватный чат'
    ' между этими пользователями: {} | {}'
)
