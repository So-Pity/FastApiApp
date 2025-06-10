from datetime import datetime
import json
from fastapi import Request, Response, HTTPException
import jwt
import time
from starlette.responses import JSONResponse
from modules.logger import logger, logger_audit
from modules.exceptions import ErrorSchema

async def log_middleware(request:Request, call_next):
  log_dict = {
    'url': request.url.path,
    'method': request.method
  }

  token = request.headers.get("Authorization", "").replace("Bearer ", "") if request.headers.get("Authorization", "").startswith("Bearer ") else None
  if token:
    token_payload = jwt.decode(token, options={"verify_signature": False})
    log_dict['username'] = token_payload['username']

  if request.method in ["PATCH", "POST"]:
    try:
      body = await request.body()

      body_str = body.decode("utf-8")
      body_json = json.loads(body_str)
      log_dict['body_keys'] = list(body_json.keys())
      
      request._body = body
    except json.decoder.JSONDecodeError:
      log_dict['body_keys'] = "Invalid JSON"
      logger.error("Failed to parse request body as JSON")
    except Exception as e:
      log_dict['body_keys'] = "Error reading body"
      logger.error(f"Error reading request body: {e}")
      
  
  try:
    start_time = time.time()
    response: Response = await call_next(request)
    duration = time.time() - start_time
    logger.info(f"Request time taken: {duration:.4f} seconds ")
  except Exception as ex:
    logger.exception(ex)
    raise HTTPException(status_code=500, detail="Internal server error")
  
  log_dict['status_code'] = response.status_code
  
  logger.info(log_dict, extra=log_dict)

  return response