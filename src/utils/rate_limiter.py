"""Simple in-memory rate limiter."""

from __future__ import annotations

import time
from collections import defaultdict, deque
from dataclasses import dataclass, field


@dataclass
class RateLimiter:
    """Sliding-window rate limiter keyed by arbitrary strings."""

    max_requests: int
    period_seconds: int
    _requests: dict[str, deque[float]] = field(
        default_factory=lambda: defaultdict(deque)
    )

    def is_limited(self, key: str) -> bool:
        """Return True if key exceeded allowed requests."""
        now = time.monotonic()
        window_start = now - self.period_seconds
        requests = self._requests[key]

        while requests and requests[0] <= window_start:
            requests.popleft()

        if len(requests) >= self.max_requests:
            return True

        requests.append(now)
        return False

    def reset(self, key: str) -> None:
        """Clear tracked requests for a key."""
        self._requests.pop(key, None)
