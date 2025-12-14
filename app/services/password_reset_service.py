import os
from itsdangerous import URLSafeTimedSerializer
from app.models.user import User

class PasswordResetService:
    def __init__(self):
        self.serializer = URLSafeTimedSerializer(os.getenv('SECRET_KEY'))

    def send_reset_link(self, email: str) -> None:
        user = User.query.filter_by(email=email).first()
        if user:
            token = self.serializer.dumps(email, salt=os.getenv('SECURITY_PASSWORD_SALT'))
            # Here you would integrate with an email service to send the token
            # For example, using Flask-Mail to send the reset link

    def reset_password(self, token: str, new_password: str) -> None:
        try:
            email = self.serializer.loads(token, salt=os.getenv('SECURITY_PASSWORD_SALT'), max_age=86400)
            user = User.query.filter_by(email=email).first()
            if user:
                user.set_password(new_password)
                user.save()  # Assuming an ORM method to save the user
        except Exception as e:
            raise ValueError('Invalid or expired token') from e
