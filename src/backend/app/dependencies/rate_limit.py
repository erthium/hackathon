from fastapi import Depends
from fastapi_limiter.depends import RateLimiter

RateLimitDep = Depends(RateLimiter(times=5, seconds=1))
