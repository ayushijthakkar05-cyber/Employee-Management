from fastapi import Depends, HTTPException, status

from core.dependencies import get_current_user


def require_roles(allowed_roles: list):

    def role_checker(current_user=Depends(get_current_user)):

        if current_user.role.name not in allowed_roles:

            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Access denied"
            )

        return current_user

    return role_checker
