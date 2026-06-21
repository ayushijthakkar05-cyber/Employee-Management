from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from models.user import User
from models.role import Role
from models.employee import Employee

from datetime import datetime, timedelta
from models.user_otp import UserOTP
from core.otp import generate_otp

from service.email import send_otp_email
from service.password_reset import (
    forgot_password as forgot_password_service,
    reset_password as reset_password_service,
    resend_verification_otp as resend_verification_otp_service,
    verify_email as verify_email_service
)
from core.decorators import simple_log
from core.security import (
    hash_password,
    verify_password,
    create_access_token
)
from schemas.auth import UserResponse


class AuthService:

    def __init__(self, db: Session):
        self.db = db

    @simple_log
    def register_user(
        self,
        user
    ):
        # Check username exists
        existing_username = self.db.query(User).filter(
            User.username == user.username
        ).first()

        if existing_username:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already exists"
            )

        # Check email exists
        existing_email = self.db.query(User).filter(
            User.email == user.email
        ).first()

        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already exists"
            )

        # Check role exists
        role = self.db.query(Role).filter(
            Role.id == user.role_id
        ).first()

        if not role:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid role"
            )

        new_user = User(
            username=user.username,
            email=user.email,
            password_hash=hash_password(
                user.password
            ),
            role_id=user.role_id,
            is_active=True,
            is_verified=False
        )

        self.db.add(new_user)

        self.db.commit()

        self.db.refresh(new_user)

        # Generate verification OTP
        otp = generate_otp()

        otp_record = UserOTP(
            user_id=new_user.id,
            otp=otp,
            purpose="email_verification",
            expires_at=datetime.utcnow() + timedelta(minutes=10),
            is_used=False
        )

        self.db.add(otp_record)
        self.db.commit()

        # Send OTP email automatically
        send_otp_email(
            new_user.email,
            otp
        )

        # Auto-link employee with same email
        employee = self.db.query(Employee).filter(
            Employee.email == new_user.email
        ).first()

        if employee and not employee.user_id:
            employee.user_id = new_user.id
            self.db.commit()

        user_response = UserResponse.model_validate(
            new_user
        )

        return {
            "message": "User registered successfully",
            "user": user_response
        }

    @simple_log
    def login_user(
        self,
        login_data
    ):

        # Find user by email
        user = self.db.query(User).filter(
            User.email == login_data.email
        ).first()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )

        # Verify password
        if not verify_password(
            login_data.password,
            user.password_hash
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )

        if not user.is_verified:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Please verify your email first"
            )

        access_token = create_access_token(
            {
                "sub": user.email,
                "user_id": user.id,
                "role": user.role.name
            }
        )

        return {
            "access_token": access_token,
            "token_type": "bearer"
        }

    @simple_log
    def change_password(
        self,
        current_user,
        password_data
    ):

        user = self.db.query(User).filter(
            User.id == current_user.id
        ).first()

        if not verify_password(
            password_data.old_password,
            user.password_hash
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Old password is incorrect"
            )

        user.password_hash = hash_password(
            password_data.new_password
        )

        self.db.commit()

        return {
            "message": "Password changed successfully"
        }

    def get_profile(self, current_user):
        return current_user

    def get_admin_dashboard(self, current_user):
        return {
            "message": "Welcome Admin",
            "user": current_user.username
        }

    def get_manager_dashboard(self, current_user):
        return {
            "message": "Welcome Manager",
            "user": current_user.username
        }

    def get_employee_dashboard(self, current_user):
        return {
            "message": "Welcome Employee",
            "user": current_user.username
        }

    def forgot_password(self, request):
        return forgot_password_service(
            self.db,
            request.email
        )

    def reset_password(self, request):
        return reset_password_service(
            self.db,
            request.email,
            request.otp,
            request.new_password
        )

    def resend_verification_otp(self, request):
        return resend_verification_otp_service(
            self.db,
            request.email
        )

    def verify_email(self, request):
        return verify_email_service(
            self.db,
            request.email,
            request.otp
        )
