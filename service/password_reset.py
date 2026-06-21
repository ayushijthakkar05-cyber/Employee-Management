from datetime import datetime, timedelta

from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from models.user import User
from models.user_otp import UserOTP

from core.otp import generate_otp
from core.security import hash_password
from core.enums import OTPPurposeEnum

from service.email import send_otp_email


def forgot_password(
    db: Session,
    email: str
):

    user = db.query(User).filter(
        User.email == email
    ).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Delete old unused forgot-password OTPs
    db.query(UserOTP).filter(
        UserOTP.user_id == user.id,
        UserOTP.purpose == OTPPurposeEnum.FORGOT_PASSWORD.value,
        UserOTP.is_used == False
    ).delete()

    db.commit()

    otp = generate_otp()

    otp_record = UserOTP(
        user_id=user.id,
        otp=otp,
        purpose=OTPPurposeEnum.FORGOT_PASSWORD.value,
        expires_at=datetime.utcnow() + timedelta(minutes=10),
        is_used=False
    )

    db.add(otp_record)
    db.commit()

    send_otp_email(
        user.email,
        otp
    )

    return {
        "message": "OTP sent successfully"
    }

def reset_password(
    db: Session,
    email: str,
    otp: str,
    new_password: str
):

    user = db.query(User).filter(
        User.email == email
    ).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    otp_record = db.query(UserOTP).filter(
        UserOTP.user_id == user.id,
        UserOTP.otp == otp,
        UserOTP.purpose == OTPPurposeEnum.FORGOT_PASSWORD.value,
        UserOTP.is_used == False
    ).first()

    if not otp_record:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid OTP"
        )

    if otp_record.expires_at < datetime.utcnow():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="OTP expired"
        )

    user.password_hash = hash_password(
        new_password
    )

    otp_record.is_used = True

    db.commit()

    return {
        "message": "Password reset successfully"
    }

# resend verification otp
def resend_verification_otp(
    db: Session,
    email: str
):
    user = db.query(User).filter(
        User.email == email
    ).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    if user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already verified"
        )

    # Delete old unused verification OTPs
    db.query(UserOTP).filter(
        UserOTP.user_id == user.id,
        UserOTP.purpose == OTPPurposeEnum.EMAIL_VERIFICATION.value,
        UserOTP.is_used == False
    ).delete()

    db.commit()

    otp = generate_otp()

    otp_record = UserOTP(
        user_id=user.id,
        otp=otp,
        purpose=OTPPurposeEnum.EMAIL_VERIFICATION.value,
        expires_at=datetime.utcnow() + timedelta(minutes=10),
        is_used=False
    )

    db.add(otp_record)
    db.commit()

    send_otp_email(
        user.email,
        otp
    )

    return {
        "message": "Verification OTP resent successfully"
    }

def verify_email(
    db: Session,
    email: str,
    otp: str
):

    user = db.query(User).filter(
        User.email == email
    ).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    otp_record = db.query(UserOTP).filter(
        UserOTP.user_id == user.id,
        UserOTP.otp == otp,
        UserOTP.purpose == OTPPurposeEnum.EMAIL_VERIFICATION.value,
        UserOTP.is_used == False
    ).first()

    if not otp_record:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid OTP"
        )

    if otp_record.expires_at < datetime.utcnow():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="OTP expired"
        )

    user.is_verified = True

    otp_record.is_used = True

    db.commit()

    return {
        "message": "Email verified successfully"
    }
