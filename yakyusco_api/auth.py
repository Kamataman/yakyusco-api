from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException, status

import firebase_admin
from firebase_admin import credentials, auth
from decouple import config

cred = credentials.Certificate(config("GOOGLE_APPLICATION_CREDENTIALS"))
firebase_admin.initialize_app(cred)


def set_custom_claims(uid: str, team_id: str):
    auth.set_custom_user_claims(uid, {"teamId": team_id})


def get_current_user(
    cred: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
):
    try:
        decoded_token = auth.verify_id_token(cred.credentials)
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid authentication credentials.",
            headers={"WWW-Authenticate": 'Bearer error="invalid_token"'},
        )
    return decoded_token["uid"]


# ユーザがそのチームのデータを編集できるか確認する
def authorize_user(uid: str, team_id: str):
    if not auth.get_user(uid).custom_claims.get("teamId") == team_id:
        raise HTTPException(status_code=403, detail="Not Authorized")
