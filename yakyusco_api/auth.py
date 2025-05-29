from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException, status

import firebase_admin
from firebase_admin import credentials, auth
from decouple import config


# Firebase Admin SDKの初期化
def initialize_firebase():
    if config("ENVIRONMENT", default="LOCAL") == "LOCAL":
        # ローカルでは、ファイルパスを環境変数から取得
        cred = credentials.Certificate(config("GOOGLE_APPLICATION_CREDENTIALS"))
    else:
        # Lambdaなどでは、S3からクレデンシャルを取得
        import json
        import boto3

        s3 = boto3.client("s3")
        bucket_name = config("CREDENTIALS_BUCKET")
        object_key = config("CREDENTIALS_OBJECT_KEY")

        response = s3.get_object(Bucket=bucket_name, Key=object_key)
        json_bytes = response["Body"].read()

        # バイトを文字列に変換してJSONロード
        json_dict = json.loads(json_bytes.decode("utf-8"))
        cred = credentials.Certificate(json_dict)

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
