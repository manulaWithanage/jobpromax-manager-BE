import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.config import settings
import httpx

security = HTTPBearer()

async def get_jwks():
    if not settings.CLERK_ISSUER:
        # Fallback or error if issuer not set
        return None
    
    jwks_url = f"{settings.CLERK_ISSUER}/.well-known/jwks.json"
    async with httpx.AsyncClient() as client:
        response = await client.get(jwks_url)
        return response.json()

async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    
    try:
        # If PEM key is provided directly (easier for some setups)
        if settings.CLERK_PEM_PUBLIC_KEY:
            key = settings.CLERK_PEM_PUBLIC_KEY
            # Ensure headers/footers if missing? Usually user provides full PEM.
            payload = jwt.decode(token, key, algorithms=["RS256"], audience=None, issuer=settings.CLERK_ISSUER if settings.CLERK_ISSUER else None)
        else:
            # JWKS Logic
            # Note: For production, caching JWKS is recommended. 
            # PyJWT can handle JWKS via PyJWKClient but we added 'pyjwt[crypto]' which includes it? 
            # Actually PyJWT's PyJWKClient is good. Let's use it if available or manual.
            # Simpler manual approach for now or use jwt.PyJWKClient if imported.
            from jwt import PyJWKClient
            if not settings.CLERK_ISSUER:
                 raise HTTPException(status_code=500, detail="Clerk Issuer not configured")
            
            jwks_client = PyJWKClient(f"{settings.CLERK_ISSUER}/.well-known/jwks.json")
            signing_key = jwks_client.get_signing_key_from_jwt(token)
            payload = jwt.decode(
                token,
                signing_key.key,
                algorithms=["RS256"],
                audience=None, # Clerk often doesn't enforce strict audience on frontend tokens unless configured
                issuer=settings.CLERK_ISSUER
            )
            
        return payload
        
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )
