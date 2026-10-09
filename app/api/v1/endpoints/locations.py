import json
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from fastapi import APIRouter, HTTPException, Query, status

from app.core.brazil import (
    BRAZILIAN_STATES,
    state_abbreviation_from_name,
    validate_brazilian_coordinates,
)
from app.schemas.location import DetectedLocationResponse

router = APIRouter()


@router.get("/reverse", response_model=DetectedLocationResponse)
def reverse_location(
    latitude: float = Query(ge=-34, le=5.5),
    longitude: float = Query(ge=-74, le=-34.5),
) -> DetectedLocationResponse:
    try:
        validate_brazilian_coordinates(latitude, longitude)
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(error)
        ) from error

    query = urlencode(
        {
            "format": "jsonv2",
            "lat": latitude,
            "lon": longitude,
            "zoom": 10,
            "addressdetails": 1,
        }
    )
    request = Request(
        f"https://nominatim.openstreetmap.org/reverse?{query}",
        headers={"User-Agent": "MapFront/1.0"},
    )

    try:
        with urlopen(request, timeout=5) as response:
            payload = json.load(response)
        state_name = payload["address"]["state"]
    except (HTTPError, URLError, TimeoutError, KeyError, json.JSONDecodeError) as error:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Could not detect the Brazilian state for these coordinates",
        ) from error

    state = state_abbreviation_from_name(state_name)
    if state is None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Coordinates do not resolve to a Brazilian state",
        )

    return DetectedLocationResponse(state=state, region=BRAZILIAN_STATES[state])
