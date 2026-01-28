import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import secrets
from app.configs.ENV import ENV_Config
from app.core.redis_client import redis_client
from fastapi import HTTPException, status
from datetime import datetime, timedelta, timezone

def generate_otp():
    return str(secrets.randbelow(900000) + 100000) 

def send_email(to_email: str, otp: str):
    msg = MIMEMultipart()
    msg["From"] = ENV_Config.EMAIL_USER
    msg["To"] = to_email
    msg["Subject"] = "Verify your email"
    
    body = f"""
Your OTP for email verification is: {str(otp)}

This OTP will expire in 5 minutes.
"""
    msg.attach(MIMEText(body, "plain"))
    
    server = smtplib.SMTP(ENV_Config.EMAIL_HOST, int(ENV_Config.EMAIL_PORT))
    server.starttls()
    server.login(ENV_Config.EMAIL_USER, ENV_Config.EMAIL_PASS)
    server.sendmail(msg["From"], to_email, msg.as_string())
    server.quit()
    
def save_otp(email: str, otp: str):

    expires_at = (datetime.now(timezone.utc) + timedelta(minutes=5)).isoformat()

    redis_client.hset(
        email,
        mapping={
            "otp": otp,
            "expires_at": expires_at
        }
    )

    redis_client.expire(email, 600)  
    
def get_otp(email: str):
    data = redis_client.hgetall(email)
    
    if not data:
        return None

    # normalize keys to string
    data_str = {k.decode() if isinstance(k, bytes) else k:
                v.decode() if isinstance(v, bytes) else v
                for k, v in data.items()}

    if "otp" not in data_str or "expires_at" not in data_str:
        return None

    return {
        "otp": data_str["otp"],
        "expires_at": datetime.fromisoformat(data_str["expires_at"])
    }


    
def verify_otp(email: str, otp: str):
    
    sended_otp = get_otp(email)
    print(redis_client.hgetall("jaybantv@gmail.com"))
    print(get_otp("jaybantv@gmail.com"))
    
    if not sended_otp: 
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="OTP not found or expired")
    
    if datetime.now(timezone.utc) > sended_otp["expires_at"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="OTP Expired")
    
    if sended_otp["otp"] != otp:
        raise HTTPException(status_code=400, detail="Invalid OTP")
    
    redis_client.delete(email)
    
    return {"message": "Email verified successfully"}
    
    