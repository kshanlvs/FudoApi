from fastapi import APIRouter, Depends
from models import User
from router.auth import get_current_user

router = APIRouter(prefix="/profile", tags=["Profile"])

@router.get("/", response_model=dict)
def get_profile(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "phone": current_user.phone,
        "name": current_user.name  # Assuming a 'name' field exists
    }
