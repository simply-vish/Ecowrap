# # streamlit_app.py

# import streamlit as st
# import requests
# import time
# from recommend_alternatives_fixed import RecommenderFixed

# st.set_page_config(
#     page_title="Ecowrap – Eco-Friendly Recommender",
#     page_icon="🪴",
#     layout="centered"
# )

# API_URL = "http://127.0.0.1:8001/recommend"

# # -----------------------------
# # TITLE + SUBTITLE
# # -----------------------------
# st.markdown("""
# <h1 style='text-align:center; color:#4CAF50;'>🪴 Ecowrap</h1>
# <h3 style='text-align:center; color:#CCCCCC;'>
# An eco-friendly product recommender that suggests biodegradable & sustainable alternatives.
# </h3>
# """, unsafe_allow_html=True)

# st.write("")

# # -----------------------------
# # INPUTS
# # -----------------------------
# name = st.text_input("Enter product name", placeholder="e.g., RoohAfza, Lays, Milk, Shampoo")

# code = st.text_input("Or enter product code (OpenFoodFacts 'code')",
#                      placeholder="e.g., 8901063092617")

# top_k = st.number_input("Number of suggestions", 1, 10, 5)

# allow_cross = st.checkbox("Allow cross-category fallbacks (less strict)", value=False)

# # -----------------------------
# # BUTTON ACTION
# # -----------------------------
# if st.button("Recommend"):
#     if not name and not code:
#         st.error("Please enter a product name OR product code.")
#         st.stop()

#     st.info("Searching… (trying API first)")
#     payload = {
#         "product_name": name if name else None,
#         "code": code if code else None,
#         "top_k": top_k
#     }

#     data = None

#     # -----------------------------
#     # TRY API FIRST
#     # -----------------------------
#     try:
#         resp = requests.post(API_URL, json=payload, timeout=5)
#         if resp.status_code == 200:
#             data = resp.json()
#         else:
#             st.warning(f"API returned status {resp.status_code} — falling back to local recommender.")
#     except Exception as e:
#         st.warning(f"API unreachable — using local recommender. ({e})")

#     # -----------------------------
#     # FALLBACK TO LOCAL RECOMMENDER
#     # -----------------------------
#     if data is None:
#         st.info("Using local recommender (no API). Loading model & data — may take a second…")
#         try:
#             reco = RecommenderFixed()
#             result = reco.recommend(name=name, code=code, top_k=top_k)
#             data = {"brand": "Ecowrap", "result": result}
#         except Exception as e:
#             st.error(f"Local recommender failed: {e}")
#             st.stop()

#     # -----------------------------
#     # CHECK PRODUCT
#     # -----------------------------
#     if "result" not in data:
#         st.error("Error: Product not found")
#         st.stop()

#     result = data["result"]

#     if "error" in result:
#         st.error("Error: Product not found")
#         st.stop()

#     product = result["product"]
#     recs = result["recommendations"]

#     # -----------------------------
#     # DISPLAY PRODUCT DETAILS
#     # -----------------------------
#     st.markdown("## ✓ Product Found")
#     st.write("**Name:**", product.get("name", "N/A"))
#     st.write("**Category:**", product.get("category", "N/A"))
#     st.write("**Biodegradability Score:**", product.get("score", "N/A"))

#     # -----------------------------
#     # DISPLAY RECOMMENDATIONS
#     # -----------------------------
#     st.markdown("## 💡 Eco-Friendly Alternatives")

#     if len(recs) == 0:
#         st.warning("No suitable alternatives found.")
#     else:
#         for r in recs:
#             st.markdown(
#                 f"""
#                 → **{r['product_name']}**  
#                 *Score:* {r['score']}  
#                 *Category:* {r['category']}  
#                 """
#             )

# # -----------------------------
# # FOOTER
# # -----------------------------
# st.markdown("""
# <hr>
# <p style='text-align:center; opacity:0.7;'>
# Powered by <b>Ecowrap</b> – Vishakha's Eco-Friendly ML Recommender 🌍
# </p>
# """, unsafe_allow_html=True)


# streamlit_app.py
# Ecowrap — Eco-Themed Streamlit UI (no external images)
# Uses recommend_alternatives_fixed.RecommenderFixed (API-first, local fallback)

import streamlit as st
import requests
import time
from pathlib import Path

# Try to import local recommender for fallback (no sklearn required)
try:
    from recommend_alternatives_fixed import RecommenderFixed
    LOCAL_RECOMMENDER_AVAILABLE = True
except Exception:
    LOCAL_RECOMMENDER_AVAILABLE = False

# CONFIG
API_URL = "http://127.0.0.1:8001/recommend"  # change if your API runs elsewhere
st.set_page_config(page_title="Ecowrap", page_icon="🌿", layout="centered")

# ---------- Styles ----------
st.markdown(
    """
    <style>
    /* Page background and main container */
    .main {
        background: linear-gradient(180deg, #f6fff6 0%, #ffffff 100%);
    }
    /* Header */
    .ecowrap-header {
        padding: 18px;
        border-radius: 10px;
        background: linear-gradient(90deg,#2F9E44 0%, #68D391 100%);
        color: white;
        box-shadow: 0 6px 18px rgba(50, 115, 60, 0.08);
    }
    .card {
        background: white;
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 12px;
        box-shadow: 0 6px 18px rgba(46, 125, 50, 0.06);
    }
    .small-muted { color: #5b6b5b; font-size: 0.9rem; }
    .badge {
        display:inline-block;
        padding:6px 10px;
        border-radius:12px;
        font-weight:600;
        color: #fff;
        margin-right:6px;
        font-size:0.85rem;
    }
    .badge-snack { background:#FFB74D; color:#2b2b2b; }
    .badge-dairy { background:#4DB6AC; }
    .badge-grain { background:#90CAF9; color:#2b2b2b; }
    .badge-beverage { background:#81C784; color:#2b2b2b; }
    .badge-confectionery { background:#FF8A80; color:#2b2b2b; }
    .badge-spices { background:#A1887F; color:#fff; }
    .score-pill {
        padding:6px 10px;
        border-radius:999px;
        background:#e9f8ee;
        color:#1d6b31;
        font-weight:700;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- Header ----------
st.markdown(
    "<div class='ecowrap-header' style='text-align:center'>"
    "<h1 style='margin:0'>Ecowrap</h1>"
    "<div style='opacity:0.95; margin-top:6px'>An eco-friendly product recommender — find biodegradable alternatives</div>"
    "</div>",
    unsafe_allow_html=True,
)

st.write("")  # spacing

# ---------- Input Area ----------
with st.container():
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### Search product")
    cols = st.columns([3, 2])
    with cols[0]:
        product_name = st.text_input("Product name", placeholder="e.g., RoohAfza, Lays Classics Salted")
    with cols[1]:
        product_code = st.text_input("Product code (OpenFoodFacts 'code')", placeholder="e.g., 8901491101837")

    cols2 = st.columns([1, 1, 1])
    with cols2[0]:
        top_k = st.selectbox("Suggestions", [3, 5, 7], index=1)
    with cols2[1]:
        allow_cross = st.checkbox("Allow cross-category fallback", value=False)
    with cols2[2]:
        run_button = st.button("Recommend", key="recommend_btn")
    st.markdown("</div>", unsafe_allow_html=True)

st.write("")

# ---------- Helper: category badge ----------
def category_badge(cat):
    if not cat:
        return "<span class='badge badge-snack'>unknown</span>"
    c = str(cat).lower()
    if "snack" in c:
        cls = "badge-snack"
    elif "dairy" in c:
        cls = "badge-dairy"
    elif "grain" in c:
        cls = "badge-grain"
    elif "beverage" in c or "syrup" in c:
        cls = "badge-beverage"
    elif "confection" in c or "chocolate" in c:
        cls = "badge-confectionery"
    elif "spice" in c:
        cls = "badge-spices"
    else:
        cls = "badge-snack"
    return f"<span class='badge {cls}'>{cat}</span>"

# ---------- Main action ----------
if run_button:
    if (not product_name or product_name.strip() == "") and (not product_code or product_code.strip() == ""):
        st.error("Please enter a product name or a product code.")
    else:
        st.info("Searching... (API first, local fallback)")

        payload = {
            "product_name": product_name.strip() or None,
            "code": product_code.strip() or None,
            "top_k": int(top_k),
            "allow_cross_category": allow_cross
        }

        result_data = None
        used_api = False

        # Try API
        try:
            resp = requests.post(API_URL, json=payload, timeout=4)
            if resp.status_code == 200:
                result_data = resp.json().get("result") or resp.json()
                used_api = True
            else:
                st.warning(f"API returned status {resp.status_code}; falling back to local.")
        except Exception:
            st.info("API unreachable or timed out — falling back to local recommender.")

        # Local fallback
        if result_data is None:
            if not LOCAL_RECOMMENDER_AVAILABLE:
                st.error("Local recommender not available. Ensure recommend_alternatives_fixed.py is present.")
                st.stop()
            try:
                recsys = RecommenderFixed()
                result_data = recsys.recommend(product_name or None, product_code or None, top_k=top_k, allow_cross_category=allow_cross)
            except Exception as e:
                st.error(f"Local recommender failed: {e}")
                st.stop()

        # Validate result
        if not result_data or ("error" in result_data and result_data.get("error")):
            st.error("Product not found or recommendations unavailable.")
            st.stop()

        # ---------- Display product card ----------
        product = result_data.get("product") or result_data
        recs = result_data.get("recommendations") or []

        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("### Product")
        cols = st.columns([4, 1])
        with cols[0]:
            st.write("**Name:**", product.get("name", "N/A"))
            cat_html = category_badge(product.get("category", "unknown"))
            st.markdown(cat_html, unsafe_allow_html=True)
            st.markdown("<div class='small-muted'>Source: API" + (" (remote)" if used_api else " (local)") + "</div>", unsafe_allow_html=True)
        with cols[1]:
            st.markdown("<div style='text-align:right'>", unsafe_allow_html=True)
            st.markdown(f"<div class='score-pill'>{product.get('score', 'N/A')}</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        # ---------- Recommendations ----------
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("### Recommendations")
        if not recs:
            st.info("No suitable alternatives found.")
        else:
            for r in recs:
                rname = r.get("product_name") or r.get("name") or "Unknown"
                rscore = r.get("score", "N/A")
                rcat = r.get("category", "unknown")
                rsim = r.get("similarity")
                # Build line with small details
                line = f"**{rname}** — Score: {rscore} — Category: {rcat}"
                if rsim is not None:
                    line += f" — sim: {round(float(rsim),3)}"
                st.markdown(line)
                st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        # ---------- Footer note ----------
        st.markdown("<div style='padding:6px; color:#6b6b6b;'>Tip: Prefer searching by product code for exact matches. Use name when code is unknown.</div>", unsafe_allow_html=True)

# ---------- bottom footer ----------
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<div style='text-align:center; color:#6b6b6b'>Ecowrap — An eco-friendly product recommender • Built for demonstration</div>", unsafe_allow_html=True)
