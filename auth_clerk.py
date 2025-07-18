import jwt
import requests
import os
import pathlib
from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional, Dict
from functools import lru_cache
import logging
import json
from dotenv import load_dotenv

root_env_path = pathlib.Path(__file__).parent / ".env"
load_dotenv(dotenv_path=root_env_path)

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

CLERK_JWKS_URL = os.getenv("CLERK_JWKS_URL", "https://bold-dragon-0.clerk.accounts.dev/.well-known/jwks.json")
CLERK_AUDIENCE = os.getenv("CLERK_AUDIENCE")

print(f"🔧 Clerk Configuration:")
print(f"   JWKS URL: {CLERK_JWKS_URL}")
print(f"   Audience: {CLERK_AUDIENCE or 'None (audience verification disabled)'}")

security = HTTPBearer()

@lru_cache(maxsize=1)
def get_jwks():
    try:
        logger.info(f"Fetching JWKS from: {CLERK_JWKS_URL}")
        response = requests.get(CLERK_JWKS_URL, timeout=10)
        response.raise_for_status()
        jwks_data = response.json()
        logger.info(f"Successfully fetched JWKS with {len(jwks_data.get('keys', []))} keys")
        return jwks_data
    except Exception as e:
        logger.error(f"Failed to fetch JWKS: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Authentication service unavailable: {str(e)}"
        )

def get_signing_key(token: str):
    try:
        header = jwt.get_unverified_header(token)
        kid = header.get('kid')
        
        logger.debug(f"Token header: {header}")
        logger.debug(f"Key ID (kid): {kid}")
        
        if not kid:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token missing key ID (kid)"
            )
        
        jwks = get_jwks()
        
        for key in jwks.get('keys', []):
            if key.get('kid') == kid:
                logger.debug(f"Found matching key for kid: {kid}")
                return jwt.algorithms.RSAAlgorithm.from_jwk(key)
        
        available_kids = [k.get('kid') for k in jwks.get('keys', [])]
        logger.error(f"Key ID {kid} not found. Available keys: {available_kids}")
        
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Unable to find key for kid: {kid}"
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting signing key: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Error processing token: {str(e)}"
        )

def verify_clerk_token(token: str) -> Dict:
    try:
        logger.debug(f"Verifying token of length: {len(token)}")
        
        # Handle simple session tokens (fallback for development)
        if token.startswith("session_"):
            parts = token.split("_")
            if len(parts) >= 3:
                user_id = parts[1]
                timestamp = parts[2]
                logger.info(f"Using session token for user: {user_id}")
                return {"sub": user_id, "type": "session", "iat": int(timestamp)}
            else:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid session token format"
                )
        
        # Handle JWT tokens
        if "." not in token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token format: not a JWT or session token"
            )
        
        unverified_payload = jwt.decode(token, options={"verify_signature": False})
        logger.debug(f"Unverified payload: {json.dumps(unverified_payload, indent=2)}")
        
        signing_key = get_signing_key(token)
        
        # More lenient verification options - disable strict timing checks
        verify_options = {
            "verify_signature": True,
            "verify_exp": False,  # Disable expiration check for long operations
            "verify_nbf": False,  # Disable "not before" check
            "verify_iat": False,  # Disable "issued at" check
            "verify_aud": False   # Disable audience check
        }
        
        logger.debug(f"Verification options: {verify_options}")
        
        payload = jwt.decode(
            token,
            signing_key,
            algorithms=["RS256"],
            options=verify_options,
            leeway=300  # Add 5 minutes leeway for long operations
        )
        
        logger.info(f"Token verified successfully for user: {payload.get('sub')}")
        return payload
        
    except jwt.ExpiredSignatureError:
        logger.error("Token has expired")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired"
        )
    except jwt.InvalidAudienceError:
        logger.error(f"Invalid audience. Expected: {CLERK_AUDIENCE}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token audience"
        )
    except jwt.InvalidTokenError as e:
        logger.error(f"Invalid token: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token: {str(e)}"
        )
    except Exception as e:
        logger.error(f"Unexpected error during token verification: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Token verification failed: {str(e)}"
        )

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Dict:
    logger.debug(f"Authenticating user with token: {credentials.credentials[:20]}...")
    return verify_clerk_token(credentials.credentials)

def get_current_user_id(user: Dict = Depends(get_current_user)) -> str:
    user_id = user.get('sub')  # Clerk uses 'sub' for user ID
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token: missing user ID"
        )
    logger.debug(f"Extracted user ID: {user_id}")
    return user_id
