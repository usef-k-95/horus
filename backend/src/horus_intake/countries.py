"""Country names as people type them in a form, to ISO 3166-1 alpha-3 codes (the engagement code prefix)."""

from __future__ import annotations

import re
import unicodedata
from typing import Optional

ISO3 = {
    "egypt": "EGY", "saudi arabia": "SAU", "ksa": "SAU", "kingdom of saudi arabia": "SAU", "united arab emirates": "ARE", "uae": "ARE", "emirates": "ARE",
    "qatar": "QAT", "kuwait": "KWT", "bahrain": "BHR", "oman": "OMN", "jordan": "JOR", "lebanon": "LBN", "iraq": "IRQ", "syria": "SYR", "palestine": "PSE",
    "yemen": "YEM", "libya": "LBY", "tunisia": "TUN", "algeria": "DZA", "morocco": "MAR", "mauritania": "MRT", "sudan": "SDN", "south sudan": "SSD",
    "somalia": "SOM", "djibouti": "DJI", "comoros": "COM", "ethiopia": "ETH", "eritrea": "ERI", "kenya": "KEN", "uganda": "UGA", "tanzania": "TZA",
    "rwanda": "RWA", "burundi": "BDI", "nigeria": "NGA", "ghana": "GHA", "senegal": "SEN", "ivory coast": "CIV", "cote d'ivoire": "CIV", "cote divoire": "CIV",
    "cameroon": "CMR", "south africa": "ZAF", "namibia": "NAM", "botswana": "BWA", "zambia": "ZMB", "zimbabwe": "ZWE", "mozambique": "MOZ", "angola": "AGO",
    "malawi": "MWI", "madagascar": "MDG", "mauritius": "MUS", "seychelles": "SYC", "mali": "MLI", "niger": "NER", "chad": "TCD", "burkina faso": "BFA",
    "benin": "BEN", "togo": "TGO", "sierra leone": "SLE", "liberia": "LBR", "guinea": "GIN", "gabon": "GAB", "congo": "COG", "democratic republic of the congo": "COD",
    "drc": "COD", "gambia": "GMB", "cape verde": "CPV", "cabo verde": "CPV", "equatorial guinea": "GNQ", "central african republic": "CAF",
    "turkey": "TUR", "turkiye": "TUR", "iran": "IRN", "israel": "ISR", "cyprus": "CYP", "pakistan": "PAK", "india": "IND", "bangladesh": "BGD", "sri lanka": "LKA",
    "nepal": "NPL", "bhutan": "BTN", "maldives": "MDV", "afghanistan": "AFG", "kazakhstan": "KAZ", "uzbekistan": "UZB", "turkmenistan": "TKM", "kyrgyzstan": "KGZ",
    "tajikistan": "TJK", "azerbaijan": "AZE", "armenia": "ARM", "georgia": "GEO", "china": "CHN", "japan": "JPN", "south korea": "KOR", "korea": "KOR",
    "republic of korea": "KOR", "taiwan": "TWN", "hong kong": "HKG", "mongolia": "MNG", "vietnam": "VNM", "viet nam": "VNM", "thailand": "THA", "cambodia": "KHM",
    "laos": "LAO", "myanmar": "MMR", "malaysia": "MYS", "singapore": "SGP", "indonesia": "IDN", "philippines": "PHL", "brunei": "BRN", "timor-leste": "TLS",
    "australia": "AUS", "new zealand": "NZL", "papua new guinea": "PNG", "fiji": "FJI",
    "united kingdom": "GBR", "uk": "GBR", "great britain": "GBR", "britain": "GBR", "england": "GBR", "scotland": "GBR", "wales": "GBR", "northern ireland": "GBR",
    "ireland": "IRL", "france": "FRA", "germany": "DEU", "netherlands": "NLD", "the netherlands": "NLD", "holland": "NLD", "belgium": "BEL", "luxembourg": "LUX",
    "switzerland": "CHE", "austria": "AUT", "italy": "ITA", "spain": "ESP", "portugal": "PRT", "greece": "GRC", "malta": "MLT", "denmark": "DNK", "sweden": "SWE",
    "norway": "NOR", "finland": "FIN", "iceland": "ISL", "estonia": "EST", "latvia": "LVA", "lithuania": "LTU", "poland": "POL", "czech republic": "CZE", "czechia": "CZE",
    "slovakia": "SVK", "hungary": "HUN", "romania": "ROU", "bulgaria": "BGR", "croatia": "HRV", "slovenia": "SVN", "serbia": "SRB", "bosnia and herzegovina": "BIH",
    "montenegro": "MNE", "north macedonia": "MKD", "albania": "ALB", "kosovo": "XKX", "moldova": "MDA", "ukraine": "UKR", "belarus": "BLR", "russia": "RUS",
    "united states": "USA", "united states of america": "USA", "usa": "USA", "us": "USA", "america": "USA", "canada": "CAN", "mexico": "MEX", "guatemala": "GTM",
    "honduras": "HND", "el salvador": "SLV", "nicaragua": "NIC", "costa rica": "CRI", "panama": "PAN", "cuba": "CUB", "dominican republic": "DOM", "haiti": "HTI",
    "jamaica": "JAM", "trinidad and tobago": "TTO", "barbados": "BRB", "bahamas": "BHS", "colombia": "COL", "venezuela": "VEN", "ecuador": "ECU", "peru": "PER",
    "bolivia": "BOL", "brazil": "BRA", "paraguay": "PRY", "uruguay": "URY", "argentina": "ARG", "chile": "CHL", "guyana": "GUY", "suriname": "SUR",
}
KNOWN_CODES = set(ISO3.values()) | {"XKX"}


def normalise(text: str) -> str:
    text = unicodedata.normalize("NFKD", text or "").encode("ascii", "ignore").decode()
    text = text.lower().replace("&", " and ")
    text = re.sub(r"[^a-z' -]+", " ", text)
    text = re.sub(r"\b(the|republic of|kingdom of|state of|federal republic of|arab republic of|people's republic of|government of|ministry of)\b", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def iso3(text: str) -> Optional[str]:
    """Best effort: 'Egypt', 'Arab Republic of Egypt', 'EGY', 'eg' style inputs; None when unknown."""
    raw = (text or "").strip()
    if not raw:
        return None
    if len(raw) == 3 and raw.isalpha() and raw.upper() in KNOWN_CODES:
        return raw.upper()
    norm = normalise(raw)
    if norm in ISO3:
        return ISO3[norm]
    if norm.replace("'", "") in ISO3:
        return ISO3[norm.replace("'", "")]
    for name, code in ISO3.items():
        if len(name) > 4 and name in norm:
            return code
    return None
