from collections.abc import Mapping

BRAZILIAN_STATES: Mapping[str, str] = {
    "AC": "Norte",
    "AL": "Nordeste",
    "AP": "Norte",
    "AM": "Norte",
    "BA": "Nordeste",
    "CE": "Nordeste",
    "DF": "Centro-Oeste",
    "ES": "Sudeste",
    "GO": "Centro-Oeste",
    "MA": "Nordeste",
    "MT": "Centro-Oeste",
    "MS": "Centro-Oeste",
    "MG": "Sudeste",
    "PA": "Norte",
    "PB": "Nordeste",
    "PR": "Sul",
    "PE": "Nordeste",
    "PI": "Nordeste",
    "RJ": "Sudeste",
    "RN": "Nordeste",
    "RS": "Sul",
    "RO": "Norte",
    "RR": "Norte",
    "SC": "Sul",
    "SP": "Sudeste",
    "SE": "Nordeste",
    "TO": "Norte",
}

STATE_NAMES_TO_ABBREVIATIONS: Mapping[str, str] = {
    "acre": "AC",
    "alagoas": "AL",
    "amapá": "AP",
    "amazonas": "AM",
    "bahia": "BA",
    "ceará": "CE",
    "distrito federal": "DF",
    "espírito santo": "ES",
    "goiás": "GO",
    "maranhão": "MA",
    "mato grosso": "MT",
    "mato grosso do sul": "MS",
    "minas gerais": "MG",
    "pará": "PA",
    "paraíba": "PB",
    "paraná": "PR",
    "pernambuco": "PE",
    "piauí": "PI",
    "rio de janeiro": "RJ",
    "rio grande do norte": "RN",
    "rio grande do sul": "RS",
    "rondônia": "RO",
    "roraima": "RR",
    "santa catarina": "SC",
    "são paulo": "SP",
    "sergipe": "SE",
    "tocantins": "TO",
}

BRAZIL_MIN_LATITUDE = -34.0
BRAZIL_MAX_LATITUDE = 5.5
BRAZIL_MIN_LONGITUDE = -74.0
BRAZIL_MAX_LONGITUDE = -34.5


def normalize_brazilian_state(state: str) -> str:
    normalized_state = state.strip().upper()
    if normalized_state not in BRAZILIAN_STATES:
        raise ValueError("State must be a Brazilian state abbreviation")
    return normalized_state


def validate_brazilian_coordinates(latitude: float, longitude: float) -> None:
    if not (
        BRAZIL_MIN_LATITUDE <= latitude <= BRAZIL_MAX_LATITUDE
        and BRAZIL_MIN_LONGITUDE <= longitude <= BRAZIL_MAX_LONGITUDE
    ):
        raise ValueError("Action coordinates must be within Brazil")


def state_abbreviation_from_name(state_name: str) -> str | None:
    return STATE_NAMES_TO_ABBREVIATIONS.get(state_name.strip().casefold())
