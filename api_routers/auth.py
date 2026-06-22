from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.dependencies import get_current_user, get_db
from core.rbac import require_roles
from core.enums import RoleEnum
from models.user import User
from schemas.auth import (
    UserCreate,
    LoginRequest,
    ChangePasswordRequest,
    UserResponse,
    RegisterResponse,
    LoginResponse,
    MessageResponse,
    DashboardResponse,
)
from schemas.password_reset import (
    ForgotPasswordRequest,
    ResetPasswordRequest,
    VerifyEmailRequest,
)
from service.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=RegisterResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    service = AuthService(db)
    return service.register_user(user)


@router.post("/login", response_model=LoginResponse)
def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    service = AuthService(db)
    return service.login_user(login_data)


@router.get("/me", response_model=UserResponse)
def get_profile(current_user: User = Depends(get_current_user)):
    service = AuthService(None)

    return service.get_profile(current_user)


@router.get("/admin", response_model=DashboardResponse)
def admin_dashboard(current_user=Depends(require_roles([RoleEnum.ADMIN.value]))):
    service = AuthService(None)

    return service.get_admin_dashboard(current_user)


@router.get("/manager", response_model=DashboardResponse)
def manager_dashboard(
    current_user=Depends(require_roles([RoleEnum.ADMIN.value, RoleEnum.MANAGER.value]))
):
    service = AuthService(None)
    return service.get_manager_dashboard(current_user)


@router.get("/employee", response_model=DashboardResponse)
def employee_dashboard(
    current_user=Depends(
        require_roles(
            [RoleEnum.ADMIN.value, RoleEnum.MANAGER.value, RoleEnum.EMPLOYEE.value]
        )
    )
):
    service = AuthService(None)
    return service.get_employee_dashboard(current_user)


@router.post("/change-password", response_model=MessageResponse)
def change_user_password(
    password_data: ChangePasswordRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = AuthService(db)

    return service.change_password(current_user, password_data)


@router.post("/forgot-password", response_model=MessageResponse)
def forgot_user_password(request: ForgotPasswordRequest, db: Session = Depends(get_db)):
    service = AuthService(db)
    return service.forgot_password(request)


@router.post("/reset-password", response_model=MessageResponse)
def reset_user_password(request: ResetPasswordRequest, db: Session = Depends(get_db)):
    service = AuthService(db)
    return service.reset_password(request)


@router.post("/resend-verification-otp", response_model=MessageResponse)
def resend_verification_email(
    request: ForgotPasswordRequest, db: Session = Depends(get_db)
):
    service = AuthService(db)
    return service.resend_verification_otp(request)


@router.post("/verify-email", response_model=MessageResponse)
def verify_user_email(request: VerifyEmailRequest, db: Session = Depends(get_db)):
    service = AuthService(db)
    return service.verify_email(request)
