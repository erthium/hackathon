from fastapi import Depends
from fastapi_limiter.depends import RateLimiter

RateLimitDep = Depends(RateLimiter(times=40, seconds=1))
