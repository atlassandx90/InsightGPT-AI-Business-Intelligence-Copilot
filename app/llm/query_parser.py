from dataclasses import dataclass
from typing import Optional
import re
import unicodedata
import os

from dotenv import load_dotenv
from google import genai
from pydantic import BaseModel


# ==========================================================
# BUSINESS QUERY MODEL
# ==========================================================

@dataclass
class BusinessQuery:
    """
    Structured representation of a user's business question.
    """

    intent: str
    state: Optional[str] = None
    category: Optional[str] = None
    payment_type: Optional[str] = None


# ==========================================================
# GEMINI RESPONSE SCHEMA
# ==========================================================

class GeminiBusinessQuery(BaseModel):
    """
    Structured response expected from Gemini.

    Gemini will classify the user's natural-language
    business question into the same fields used by
    BusinessQuery.
    """

    intent: str
    state: Optional[str] = None
    category: Optional[str] = None
    payment_type: Optional[str] = None


# ==========================================================
# VALID VALUES
# ==========================================================

VALID_INTENTS = {
    "total_revenue",
    "orders",
    "aov",
    "revenue_trend",
    "state",
    "category",
    "payment",
    "rating",
    "forecast",
    "unknown",
}


VALID_STATES = {
    "SP",
    "RJ",
    "MG",
    "RS",
    "PR",
    "SC",
    "BA",
    "DF",
    "GO",
    "ES",
}


VALID_PAYMENT_TYPES = {
    "credit_card",
    "debit_card",
    "voucher",
    "boleto",
}


# ==========================================================
# GEMINI CONFIGURATION
# ==========================================================

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

GEMINI_CLIENT = None

if GEMINI_API_KEY:
    try:
        GEMINI_CLIENT = genai.Client(
            api_key=GEMINI_API_KEY
        )
    except Exception:
        GEMINI_CLIENT = None


GEMINI_MODEL = "gemini-3.6-flash"

# ==========================================================
# TEXT NORMALIZATION
# ==========================================================

def normalize_text(text: str) -> str:
    """
    Normalize user input.

    Examples:

        São Paulo
        sao paulo
        SÃO PAULO

    all become:

        sao paulo

    Also treats underscores and hyphens as spaces.
    """

    text = str(text).lower().strip()

    # Remove accents
    text = unicodedata.normalize("NFKD", text)

    text = "".join(
        char
        for char in text
        if not unicodedata.combining(char)
    )

    # Underscore / hyphen -> space
    text = re.sub(r"[_\-]+", " ", text)

    # Multiple spaces -> single space
    text = re.sub(r"\s+", " ", text)

    return text.strip()


# ==========================================================
# CATEGORY ALIASES
# ==========================================================
#
# VALUE = actual category stored in the database.
#
# This covers the categories we identified from the dataset
# and supports both Portuguese dataset names and common
# English user terminology.
#
# ==========================================================

CATEGORY_ALIASES = {

    # Agriculture / Food
    "agro industria e comercio":
        "agro_industria_e_comercio",

    "alimentos":
        "alimentos",

    "alimentos bebidas":
        "alimentos_bebidas",

    # Arts
    "artes":
        "artes",

    "artes e artesanato":
        "artes_e_artesanato",

    # Party / Christmas
    "artigos de festas":
        "artigos_de_festas",

    "artigos de natal":
        "artigos_de_natal",

    # Audio / Automotive
    "audio":
        "audio",

    "automotivo":
        "automotivo",

    "automotive":
        "automotivo",

    # Babies / Drinks
    "bebes":
        "bebes",

    "bebidas":
        "bebidas",

    # Beauty / Health
    "beleza saude":
        "beleza_saude",

    "health beauty":
        "beleza_saude",

    "health":
        "beleza_saude",

    "beauty":
        "beleza_saude",

    # Toys
    "brinquedos":
        "brinquedos",

    "toys":
        "brinquedos",

    # Bed / Table / Bath
    "cama mesa banho":
        "cama_mesa_banho",

    # Home
    "casa conforto":
        "casa_conforto",

    "casa conforto 2":
        "casa_conforto_2",

    "casa construcao":
        "casa_construcao",

    # Music / Movies
    "cds dvds musicas":
        "cds_dvds_musicas",

    "cine foto":
        "cine_foto",

    "dvds blu ray":
        "dvds_blu_ray",

    # Climate
    "climatizacao":
        "climatizacao",

    # Games
    "consoles games":
        "consoles_games",

    # Construction
    "construcao ferramentas construcao":
        "construcao_ferramentas_construcao",

    "construcao ferramentas ferramentas":
        "construcao_ferramentas_ferramentas",

    "construcao ferramentas iluminacao":
        "construcao_ferramentas_iluminacao",

    "construcao ferramentas jardim":
        "construcao_ferramentas_jardim",

    "construcao ferramentas seguranca":
        "construcao_ferramentas_seguranca",

    # Misc
    "cool stuff":
        "cool_stuff",

    # Electronics
    "eletrodomesticos":
        "eletrodomesticos",

    "eletrodomesticos 2":
        "eletrodomesticos_2",

    "eletronicos":
        "eletronicos",

    "eletroportateis":
        "eletroportateis",

    "electronics":
        "eletronicos",

    # Sports
    "esporte lazer":
        "esporte_lazer",

    "sports leisure":
        "esporte_lazer",

    "sports":
        "esporte_lazer",

    # Fashion
    "fashion bolsas e acessorios":
        "fashion_bolsas_e_acessorios",

    "fashion calcados":
        "fashion_calcados",

    "fashion esporte":
        "fashion_esporte",

    "fashion roupa feminina":
        "fashion_roupa_feminina",

    "fashion roupa infanto juvenil":
        "fashion_roupa_infanto_juvenil",

    "fashion roupa masculina":
        "fashion_roupa_masculina",

    "fashion underwear e moda praia":
        "fashion_underwear_e_moda_praia",

    "fashion bags accessories":
        "fashion_bags_accessories",

    "fashion bags":
        "fashion_bags_accessories",

    "fashion":
        "fashion_bags_accessories",

    # Tools / Garden
    "ferramentas jardim":
        "ferramentas_jardim",

    "flores":
        "flores",

    # Hygiene
    "fraldas higiene":
        "fraldas_higiene",

    # Industry / Business
    "industria comercio e negocios":
        "industria_comercio_e_negocios",

    # Computers / IT
    "informatica acessorios":
        "informatica_acessorios",

    "computers accessories":
        "informatica_acessorios",

    "computers":
        "informatica_acessorios",

    "pc gamer":
        "pc_gamer",

    "pcs":
        "pcs",

    # Music
    "instrumentos musicais":
        "instrumentos_musicais",

    "la cuisine":
        "la_cuisine",

    "musica":
        "musica",

    # Books
    "livros importados":
        "livros_importados",

    "livros interesse geral":
        "livros_interesse_geral",

    "livros tecnicos":
        "livros_tecnicos",

    "books":
        "livros_interesse_geral",

    # Bags / Marketplace
    "malas acessorios":
        "malas_acessorios",

    "market place":
        "market_place",

    # Furniture
    "moveis colchao e estofado":
        "moveis_colchao_e_estofado",

    "moveis cozinha area de servico jantar":
        "moveis_cozinha_area_de_servico_jantar",

    "moveis decoracao":
        "moveis_decoracao",

    "moveis escritorio":
        "moveis_escritorio",

    "moveis quarto":
        "moveis_quarto",

    "moveis sala":
        "moveis_sala",

    # English furniture aliases
    "furniture":
        "moveis_decoracao",

    "furniture decor":
        "moveis_decoracao",

    "furniture_decor":
        "moveis_decoracao",

    # Office
    "papelaria":
        "papelaria",

    # Perfume / Pets
    "perfumaria":
        "perfumaria",

    "pet shop":
        "pet_shop",

    # Kitchen / Appliances
    "portateis casa forno e cafe":
        "portateis_casa_forno_e_cafe",

    "portateis cozinha e preparadores de":
        "portateis_cozinha_e_preparadores_de",

    # Watches / Gifts
    "relogios presentes":
        "relogios_presentes",

    # Insurance / Services
    "seguros e servicos":
        "seguros_e_servicos",

    # Security
    "sinalizacao e seguranca":
        "sinalizacao_e_seguranca",

    # Tablets / Printing
    "tablets impressao imagem":
        "tablets_impressao_imagem",

    # Telephone
    "telefonia":
        "telefonia",

    "telefonia fixa":
        "telefonia_fixa",

    # Domestic utilities
    "utilidades domesticas":
        "utilidades_domesticas",
}


# Normalize aliases once when module loads
NORMALIZED_CATEGORY_ALIASES = {
    normalize_text(key): value
    for key, value in CATEGORY_ALIASES.items()
}


# ==========================================================
# VALIDATION
# ==========================================================

def validate_query(query: BusinessQuery) -> BusinessQuery:
    """
    Validate and normalize a BusinessQuery.
    """

    # ---------------- Intent ----------------
    # IMPORTANT:
    # Do NOT use normalize_text() here because it converts
    # underscores into spaces.
    #
    # Example:
    # total_revenue -> total revenue  ❌
    #
    # We need to preserve canonical intent names.

    intent = str(query.intent).lower().strip()

    if intent not in VALID_INTENTS:
        intent = "unknown"

    # ---------------- State ----------------

    state = query.state

    if state:
        state = str(state).upper().strip()

        if state not in VALID_STATES:
            state = None

    # ---------------- Payment ----------------
    # IMPORTANT:
    # Do NOT use normalize_text() here either.
    #
    # credit_card must remain credit_card.

    payment_type = query.payment_type

    if payment_type:
        payment_type = str(payment_type).lower().strip()

        if payment_type not in VALID_PAYMENT_TYPES:
            payment_type = None

    # ---------------- Category ----------------

    category = query.category

    if category:
        normalized_category = normalize_text(category)

        if normalized_category in NORMALIZED_CATEGORY_ALIASES:
            category = NORMALIZED_CATEGORY_ALIASES[
                normalized_category
            ]
        else:
            category = str(category).lower().strip()

    return BusinessQuery(
        intent=intent,
        state=state,
        category=category,
        payment_type=payment_type,
    )


# ==========================================================
# INTENT DETECTION
# ==========================================================

def detect_intent(question: str) -> str:

    q = normalize_text(question)
    print("NORMALIZED QUESTION =", q)

    # ------------------------------------------------------
    # Forecast
    # ------------------------------------------------------

    if any(phrase in q for phrase in [
            "forecast",
            "predict",
            "prediction",
            "projected revenue",
            "projected sales",
            "expected revenue",
            "expected sales",
            "next month revenue",
            "next month sales",
            "future revenue",
            "future sales",
            "predicted revenue",
            "predicted sales",
            "likely to generate",
            "likely to make",
            "expect to generate",
            "expect to make",
            "expect in the future",
            "expect next month",
            "expect next",
    ]):
            return "forecast"


    # ------------------------------------------------------
    # Semantic forecast wording
    # ------------------------------------------------------

    has_future_signal = any(phrase in q for phrase in [
        "expect",
        "likely",
        "upcoming",
        "future",
        "next month",
        "next period",
    ])

    has_revenue_signal = any(word in q for word in [
        "revenue",
        "sales",
    ])

    if has_future_signal and has_revenue_signal:
       return "forecast"

    # ------------------------------------------------------
    # Revenue trend
    # ------------------------------------------------------

    if any(phrase in q for phrase in [
        "revenue trend",
        "sales trend",
        "revenue growth",
        "sales growth",
        "revenue decline",
        "sales decline",
        "revenue increasing",
        "revenue decreasing",
        "sales increasing",
        "sales decreasing",
        "how is revenue changing",
        "how is sales changing",
        "how has revenue changed",
        "how has sales changed",
        "revenue performance",
        "sales performance",


        # Natural-language trend questions
        "getting better or worse",
        "getting better",
        "getting worse",
        "better or worse over time",
        "improving over time",
        "declining over time",
        "improving lately",
        "declining lately",
        "revenue improving",
        "revenue declining",
        "sales improving",
        "sales declining",
    ]):
        return "revenue_trend"

    # ------------------------------------------------------
    # Total revenue
    # ------------------------------------------------------

    if (
        "category" in q
        and any(word in q for word in [
            "highest",
            "top",
            "best",
            "most",
        ])
    ):
        return "category"

    if any(phrase in q for phrase in [
        "total revenue",
        "overall revenue",
        "total sales",
        "overall sales",
        "revenue in",
        "sales in",
        "revenue for",
        "sales for",
        "how much revenue",
        "how much sales",
        "revenue amount",
        "sales amount",

        # Natural-language revenue questions
        "how much money",
        "how much did we make",
        "how much did we earn",
        "how much did the business make",
        "what did we make",
        "what did we earn",
    ]):
        return "total_revenue"

    # ------------------------------------------------------
    # Orders
    # ------------------------------------------------------

    if any(phrase in q for phrase in [
        "total orders",
        "number of orders",
        "how many orders",
        "order count",
        "orders",
    ]):
        return "orders"

    # ------------------------------------------------------
    # AOV
    # ------------------------------------------------------

    if any(phrase in q for phrase in [
        "average order value",
        "aov",
        "average order",
    ]):
        return "aov"

    # ------------------------------------------------------
    # Payment
    # ------------------------------------------------------

    if any(phrase in q for phrase in [
        "payment type",
        "payment method",
        "most used payment",
        "most popular payment",
        "popular payment",
        "payment distribution",
    ]):
        return "payment"

    # ------------------------------------------------------
    # Rating
    # ------------------------------------------------------

    if any(phrase in q for phrase in [
        "rating",
        "review score",
        "customer rating",
        "average rating",
        "customer reviews",
        "reviews",
    ]):
        return "rating"

    # ------------------------------------------------------
    # Category
    # ------------------------------------------------------

    if any(phrase in q for phrase in [
        "top category",
        "best category",
        "category revenue",
        "top product category",
        "product category",
        "categories",
        "which category",
        "highest revenue category",
        "highest revenue",
        "generates highest revenue",
        "most revenue category",
        "highest selling category",
    ]):
         return "category"

    # ------------------------------------------------------
    # State
    # ------------------------------------------------------

    if any(phrase in q for phrase in [
        "top state",
        "best state",
        "highest revenue state",
        "state revenue",
        "states",
        "region",
        "location",
    ]):
        return "state"

    # ------------------------------------------------------
    # Unknown
    # ------------------------------------------------------


    return "unknown"


# ==========================================================
# STATE EXTRACTION
# ==========================================================

def extract_state(question: str) -> Optional[str]:

    q = normalize_text(question)

    state_map = {
        "sao paulo": "SP",
        "sp": "SP",

        "rio de janeiro": "RJ",
        "rio": "RJ",
        "rj": "RJ",

        "minas gerais": "MG",
        "mg": "MG",

        "rio grande do sul": "RS",
        "rs": "RS",

        "parana": "PR",
        "pr": "PR",

        "santa catarina": "SC",
        "sc": "SC",

        "bahia": "BA",
        "ba": "BA",

        "df": "DF",
        "go": "GO",
        "es": "ES",
    }

    # Longest first
    for key, value in sorted(
        state_map.items(),
        key=lambda item: len(item[0]),
        reverse=True,
    ):

        pattern = r"\b" + re.escape(key) + r"\b"

        if re.search(pattern, q):
            return value

    return None


# ==========================================================
# PAYMENT EXTRACTION
# ==========================================================

def extract_payment(question: str) -> Optional[str]:

    q = normalize_text(question)

    if re.search(
        r"\bcredit card\b|\bcredit card\b",
        q,
    ):
        return "credit_card"

    if re.search(
        r"\bdebit card\b",
        q,
    ):
        return "debit_card"

    if re.search(
        r"\bvoucher\b",
        q,
    ):
        return "voucher"

    if re.search(
        r"\bboleto\b",
        q,
    ):
        return "boleto"

    return None


# ==========================================================
# CATEGORY EXTRACTION
# ==========================================================

def extract_category(question: str) -> Optional[str]:

    q = normalize_text(question)

    # Longest first to avoid:
    #
    # fashion
    #
    # matching before:
    #
    # fashion roupa feminina
    #

    for key, value in sorted(
        NORMALIZED_CATEGORY_ALIASES.items(),
        key=lambda item: len(item[0]),
        reverse=True,
    ):

        pattern = r"\b" + re.escape(key) + r"\b"

        if re.search(pattern, q):
            return value

    return None


# ==========================================================
# FALLBACK PARSER
# ==========================================================

def parse_question_fallback(question: str) -> BusinessQuery:
    """
    Deterministic fallback parser.

    Uses the same canonical extraction functions as the
    main parser so intent, state, category and payment
    detection cannot drift apart.
    """

    return validate_query(
        BusinessQuery(
            intent=detect_intent(question),
            state=extract_state(question),
            category=extract_category(question),
            payment_type=extract_payment(question),
        )
    )

# ==========================================================
# GEMINI PARSER
# ==========================================================

def parse_question_gemini(question: str) -> BusinessQuery:
    """
    Use Gemini to interpret a natural-language business
    question and convert it into a structured BusinessQuery.
    """

    if not GEMINI_CLIENT:
        raise RuntimeError(
            "Gemini client is not configured."
        )

    prompt = f"""
You are a business analytics query parser.

Convert the user's natural-language question into a
structured business query.

Allowed intents:
- total_revenue
- orders
- aov
- revenue_trend
- state
- category
- payment
- rating
- forecast
- unknown

Allowed states:
SP, RJ, MG, RS, PR, SC, BA, DF, GO, ES

Allowed payment types:
- credit_card
- debit_card
- voucher
- boleto

Category handling:
- Return the canonical dataset category when possible.
- Use the known category aliases from the application's
  category mapping.
- Do not invent a category that is not implied by the
  user's question.

Rules:
- If the question asks how much revenue/sales something
  generated, use total_revenue.
- If the question asks for future/predicted revenue,
  use forecast.
- If the question asks about revenue/sales movement over
  time, use revenue_trend.
- If no relevant intent can be determined, use unknown.
- State and payment_type should be null when not present.
- category should be null when no category is present.

User question:
{question}
"""

    response = GEMINI_CLIENT.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_schema": GeminiBusinessQuery,
        },
    )

    parsed = response.parsed

    if parsed is None:
        raise ValueError(
            "Gemini returned no structured response."
        )

    return validate_query(
        BusinessQuery(
            intent=parsed.intent,
            state=parsed.state,
            category=parsed.category,
            payment_type=parsed.payment_type,
        )
    )


# ==========================================================
# PRIMARY QUERY PARSER
# ==========================================================

def parse_question(question: str) -> BusinessQuery:
    """
    Primary public parser.

    Strategy:

    1. Try deterministic parsing first.
    2. If the deterministic parser understands the query,
       return that result.
    3. If intent is unknown, ask Gemini.
    4. If Gemini fails, safely fall back to deterministic
       parsing.
    """

    deterministic_result = parse_question_fallback(question)

    # ------------------------------------------------------
    # Deterministic parser already understands the question
    # ------------------------------------------------------

    if deterministic_result.intent != "unknown":
        return deterministic_result

    # ------------------------------------------------------
    # Try Gemini for unknown / complex questions
    # ------------------------------------------------------

    try:
        return parse_question_gemini(question)

    except Exception:
        # Gemini must never break the application.
        return deterministic_result