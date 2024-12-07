from typing import Optional
import uuid

import uvicorn
from fastapi import Depends,HTTPException
from fastapi.security import OAuth2PasswordBearer
from fastapi import FastAPI, Response, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from typing import Optional,Annotated
import logging,random,string,requests,base64,secrets,os

from requests import RequestException
from starlette.requests import Request
from starlette.responses import JSONResponse

import request_body_mapping as req_mapping
from db import Session, models
from const import PREFIX_URL, USER_NAME, PW
import base64

import create_tables
create_tables.create() #This will create the tables automatically, first create database(create the schema within db if exists.)

app = FastAPI(debug=True)

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

security = HTTPBasic()

def get_current_username(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)],
):
    current_username_bytes = credentials.username.encode("utf8")
    correct_username_bytes = b"Maang@2024"
    is_correct_username = secrets.compare_digest(
        current_username_bytes, correct_username_bytes
    )
    current_password_bytes = credentials.password.encode("utf8")
    correct_password_bytes = b"Pass_@2024"
    is_correct_password = secrets.compare_digest(
        current_password_bytes, correct_password_bytes
    )
    if not (is_correct_username and is_correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

def encrypt_password(password):
    # Encode API key to bytes and then Base64 encode it
    encrypted_bytes = base64.b64encode(password.encode('utf-8'))
    # Convert bytes back to string (optional, depending on your needs)
    encrypted_str = encrypted_bytes.decode('utf-8')
    return encrypted_str


def decrypt_password(password: str):
    # Decode the Base64 encoded API key
    try:
        decoded_bytes = base64.b64decode(password)
        return decoded_bytes.decode('utf-8')
    except Exception as e:
        return None

#Auth Token
# def validate_accesstoken(access_token):
#     session = None
#     try:
#         session = Session()
#         result_set = session.query(models.AccessToken).filter(models.AccessToken.access_token == access_token)
#         result_set_count = result_set.count()
#         if result_set_count > 0:
#             return True
#         else:
#             return False
#     except Exception as err:
#         return False
#     finally:
#         if session:
#             session.close()

# @app.post("/generate/accesstoken")
# async def generate_accesstoken(request_context: Request, access_token: req_mapping.AccessToken, response: Response):
#     session = None
#     try:
#         access_token_val = None
#         session = Session()
#         user_name = access_token.user_name
#         password = access_token.password
#         if USER_NAME == user_name and PW == password:
#                 result_set = session.query(models.AccessToken).filter(models.AccessToken.user_id == user_name)
#                 result_set_count = result_set.count()
#                 result_set = result_set.all()
#                 if result_set_count > 0:
#                     for user in result_set:
#                         user.is_active = True
#                         uuid_uuid4 = str(uuid.uuid4())
#                         user.access_token = uuid_uuid4
#                         session.commit()
#                         return {"Access Token": uuid_uuid4}
#                 else:
#                     uuid_uuid4 = str(uuid.uuid4())
#                     user = models.AccessToken(user_id = user_name, access_token = uuid_uuid4, created_by=user_name)
#                     session.add(user)
#                     session.commit()
#                     session.refresh(user)
#                     response.status_code = status.HTTP_201_CREATED
#                     return {"Access Token": uuid_uuid4}
#         else:
#             return {"Wrong user name or password"}
#     except Exception as err:
#         return JSONResponse({"error_code": "AccessTokenFailed",
#                              "message": "Technical Error occurred while creating the access token"+str(err)}, status_code=500)
#     finally:
#         if session:
#             session.close()

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/generate/accesstoken")
# @app.put("/generate/accesstoken/{id}")
# async def update_accesstoken(request_context: Request, id, contact_update: req_mapping.UpdateStatus, access_token=Depends(oauth2_scheme)):
#     session = None
#     try:
#         if validate_accesstoken(access_token):
#             status = contact_update.status
#             session = Session()
#             result_set = session.query(models.AccessToken).filter(models.AccessToken.user_id == id)
#             result_set_count = result_set.count()
#             result_set = result_set.all()
#             if result_set_count > 0:
#                 for user in result_set:
#                     user.is_active = status
#                     user.access_token = None
#                     session.commit()
#                     session.refresh(user)
#                 return result_set
#             else:
#                 return JSONResponse({"detail": "NOT_FOUND"}, status_code=404)
#         else:
#             return {"Authentication Failed."}
#     except Exception as err:
#         return JSONResponse({"error_code": "ContactUsUpdationApiFailure",
#                              "message": "Technical Error occurred while updating the ContactUs"}, status_code=500)
#     finally:
#         if session:
#             session.close()


# contactus
@app.get("/token")
async def get_token(email:str,password:str):
    session = None
    try:
            
        session = Session()
        user = session.query(models.Users).filter(models.Users.email == email.strip()).first()

        if user:
            if user.password == encrypt_password(password.strip()):
                return {"message":"SUCESSFULL",
                        "token" : "Basic TWFhbmdAMjAyNDpQYXNzX0AyMDI0"}
            return JSONResponse({"detail":"Incorrect Password"},status_code=403)
        
        return JSONResponse({"detail":"User Not Found"},status_code=404)

    except Exception as err:
        return JSONResponse({"error_code": f"GetTokenApiFailure,{str(err)}",
                             "message": "Technical Error occurred while getting Token "}, status_code=500)
    finally:
        if session:
            session.close()

@app.post(PREFIX_URL + "/contactus")
async def create_contactus(request_context: Request, contactus: req_mapping.ContactUs, response: Response):
    session = None
    try:
        session = Session()
        name = contactus.name
        email = contactus.email
        phone = contactus.phone
        subject = contactus.subject
        message = contactus.message
        app_name = contactus.app_name
        contact = models.ContactUs(name=name, email=email, phone=phone, subject=subject, message=message,app_name=app_name)
        session.add(contact)
        session.commit()
        session.refresh(contact)
        response.status_code = status.HTTP_201_CREATED
        return {"message":"Success"}
    except Exception as err:
        return JSONResponse({"error_code": "ContactUsFailed",
                             "message": "Technical Error occurred while storing the contact us info"}, status_code=500)
    finally:
        if session:
            session.close()

@app.get(PREFIX_URL + "/contactus/{id}")
async def get_contactus(user: Annotated[str, Depends(get_current_username)],request_context: Request, id):
    session = None
    try:
            
        session = Session()
        result_set = session.query(models.ContactUs).filter(models.ContactUs.id == id)
        result_set_count = result_set.count()
        result_set = result_set.first()
        if result_set_count > 0:
            return result_set
        else:
            return JSONResponse({"detail": "NOT_FOUND"}, status_code=404)
    except Exception as err:
        return JSONResponse({"error_code": f"ContactUsRetrievingApiFailure,{str(err)}",
                             "message": "Technical Error occurred while retrieving the ContactUs"}, status_code=500)
    finally:
        if session:
            session.close()

@app.get(PREFIX_URL + "/contactus")
async def get_contactus_all(user: Annotated[str, Depends(get_current_username)],app:Optional[str] = None ,page: Optional[int] = 0, size: Optional[int] = 20):
    session = None
    try:
        
        session = Session()
        if page != 0:
            page = page - 1
            
        query = session.query(models.ContactUs).filter(models.ContactUs.is_active == True)

        if app is not None:
            query = query.filter(models.ContactUs.app_name == app)
        
        # Get total number of items
        total_items = query.count()

        # Calculate total pages
        total_pages = (total_items + size - 1) // size

        content = query.offset(page*size).limit(size).all()
        
        response = {
            "message": "SUCCESSFUL",
            "data": content,
            "status": 200,
            "pagination": {
                "current_page": page + 1,
                "items_per_page": size,
                "total_pages": total_pages,
                "total_items": total_items
            }
        }

        return response
    except Exception as err:
        # return err
        return JSONResponse({"error_code": f"contactusRetrievingAllApiFailure {str(err)}",
                             "message": "Technical Error occurred while retrieving the ContactUs"}, status_code=500)
    finally:
        if session:
            session.close()

@app.put(PREFIX_URL + "/contactus/{id}")
async def update_contactus(user: Annotated[str, Depends(get_current_username)],request_context: Request, id):
    session = None
    try:
        
        session = Session()
        result_set = session.query(models.ContactUs).filter(models.ContactUs.id == id).first()
        if result_set :
            result_set.status = True
            session.commit()
            session.refresh(result_set)
            return JSONResponse({"detail": "Status Updated sucessfully"}, status_code=200)
        else:
            return JSONResponse({"detail": "NOT_FOUND"}, status_code=404)
    except Exception as err:
        return JSONResponse({"error_code": "ContactUsUpdationApiFailure",
                             "message": "Technical Error occurred while updating the ContactUs"}, status_code=500)
    finally:
        if session:
            session.close()

@app.delete(PREFIX_URL + "/contactus/{id}")
async def delete_contact(user: Annotated[str, Depends(get_current_username)],request_context: Request, id):
    session = None
    try:
        session = Session()
        result_set = session.query(models.ContactUs).filter(models.ContactUs.id == id).first()
        if result_set:
            result_set.is_active = False
            session.commit()
            return JSONResponse({"detail": "success"})
        else:
            return JSONResponse({"detail": "NOT_FOUND"}, status_code=404)
    except Exception as exc:
        return JSONResponse({"error_code": "ContactUsDeletionApiFailure",
                             "message": "Technical Error occurred while deleting the ContactUs"}, status_code=500)
    finally:
        if session:
            session.close()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8200, log_level="debug")