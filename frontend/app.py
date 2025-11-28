"""
SweetSwap AI - Streamlit Frontend
Run with: streamlit run frontend/app.py
"""
import streamlit as st
import requests
from typing import Optional

# Color palette
CARDINAL = "#C52233"
MADDER = "#A51C30"
AUBURN = "#A7333F"
BURGUNDY = "#74121D"
CHOCOLATE_COSMOS = "#580C1F"
LIGHT_BG = "#F9F5F5"

# API endpoint
API_BASE_URL = "http://localhost:8000"

st.set_page_config(
    page_title="SweetSwap AI",
    page_icon="🍹",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Custom CSS
st.markdown(
    f"""
    <style>
    .main {{
        background-color: {LIGHT_BG};
    }}
    .stButton>button {{
        background-color: {AUBURN};
        color: white;
        border-radius: 8px;
        border: none;
        padding: 0.5rem 2rem;
        font-weight: 600;
    }}
    .stButton>button:hover {{
        background-color: {MADDER};
    }}
    .substitution-card {{
        background: linear-gradient(135deg, {CARDINAL} 0%, {CHOCOLATE_COSMOS} 100%);
        padding: 2rem;
        border-radius: 16px;
        color: white;
        margin: 1rem 0;
    }}
    .comparison-card {{
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }}
    .metric-box {{
        background: {LIGHT_BG};
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
        margin: 0.5rem;
    }}
    h1 {{
        color: {CARDINAL};
    }}
    </style>
    """,
    unsafe_allow_html=True,
)


def call_api(drink_name: str, include_nutrition: bool = True) -> Optional[dict]:
    """Call the FastAPI /substitute endpoint."""
    try:
        response = requests.post(
            f"{API_BASE_URL}/substitute",
            json={"drink_name": drink_name, "include_nutrition": include_nutrition},
            timeout=10,
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.ConnectionError:
        st.error("❌ Could not connect to backend API. Make sure FastAPI is running on http://localhost:8000")
        return None
    except requests.exceptions.RequestException as e:
        st.error(f"❌ API Error: {e}")
        return None


def format_sugar_delta(delta: Optional[float]) -> str:
    """Format sugar delta with color coding."""
    if delta is None:
        return "N/A"
    if delta < 0:
        return f"✅ {abs(delta):.1f}g less"
    elif delta > 0:
        return f"⚠️ {delta:.1f}g more"
    return "➡️ Same"


def format_caffeine_delta(delta: Optional[float]) -> str:
    """Format caffeine delta."""
    if delta is None:
        return "N/A"
    if delta < 0:
        return f"📉 {abs(delta):.1f}mg less"
    elif delta > 0:
        return f"📈 {delta:.1f}mg more"
    return "➡️ Same"


def main():
    st.title("🍹 SweetSwap AI")
    st.markdown("### Find diabetes-friendly drink substitutions")
    st.markdown("---")

    # Input section
    drink_input = st.text_input(
        "Enter a drink name:",
        placeholder="e.g., Mango Boba Tea, Starbucks Caramel Frappuccino...",
        key="drink_input",
    )

    col1, col2 = st.columns([2, 3])
    with col1:
        search_button = st.button("🔍 Find Substitute", type="primary", use_container_width=True)
    with col2:
        include_nutrition = st.checkbox("Include nutrition data", value=True)

    # Process request
    if search_button and drink_input:
        with st.spinner("Finding your perfect substitute..."):
            result = call_api(drink_input.strip(), include_nutrition)
            
            if result:
                st.markdown("---")
                
                # Substitution card
                st.markdown(
                    f"""
                    <div class="substitution-card">
                        <h2>✨ {result.get('substitute_name', 'Unknown')}</h2>
                        <p style="font-size: 1.1em; margin-top: 1rem;">
                            {result.get('substitute_notes', 'No notes available')}
                        </p>
                        <p style="margin-top: 1rem; opacity: 0.9;">
                            <strong>Source:</strong> {result.get('source', 'unknown').upper()}
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                
                # Comparison metrics
                sugar_delta = result.get("sugar_delta")
                caffeine_delta = result.get("caffeine_delta")
                
                if sugar_delta is not None or caffeine_delta is not None:
                    st.markdown("### 📊 Nutrition Comparison")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown(
                            f"""
                            <div class="comparison-card">
                                <h4 style="color: {CARDINAL}; margin-bottom: 1rem;">Sugar Reduction</h4>
                                <div class="metric-box">
                                    <h2 style="color: {CARDINAL}; margin: 0;">
                                        {format_sugar_delta(sugar_delta)}
                                    </h2>
                                </div>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )
                    
                    with col2:
                        st.markdown(
                            f"""
                            <div class="comparison-card">
                                <h4 style="color: {CARDINAL}; margin-bottom: 1rem;">Caffeine Change</h4>
                                <div class="metric-box">
                                    <h2 style="color: {CARDINAL}; margin: 0;">
                                        {format_caffeine_delta(caffeine_delta)}
                                    </h2>
                                </div>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )
                
                # Feedback section (placeholder)
                st.markdown("---")
                st.markdown("### 💬 Was this helpful?")
                feedback_col1, feedback_col2 = st.columns(2)
                with feedback_col1:
                    if st.button("👍 Yes, helpful!", key="thumbs_up"):
                        st.success("Thanks for your feedback!")
                with feedback_col2:
                    if st.button("👎 Not quite right", key="thumbs_down"):
                        st.info("We'll use this to improve our suggestions!")
    
    elif search_button and not drink_input:
        st.warning("⚠️ Please enter a drink name first!")
    
    # Sidebar with examples
    with st.sidebar:
        st.markdown(f"### 🎯 Try these examples:")
        example_drinks = [
            "Mango Boba Tea",
            "Starbucks Caramel Frappuccino",
            "Strawberry Milk Tea",
            "Matcha Latte",
            "Thai Iced Tea",
        ]
        for drink in example_drinks:
            if st.button(f"🍹 {drink}", key=f"example_{drink}", use_container_width=True):
                st.session_state.drink_input = drink
                st.rerun()
        
        st.markdown("---")
        st.markdown("### ℹ️ About")
        st.markdown(
            """
            **SweetSwap AI** helps you find 
            diabetes-friendly drink alternatives 
            with lower sugar content.
            
            Powered by:
            - Custom substitution database
            - USDA Nutrition API
            - Google Gemini AI
            """
        )


if __name__ == "__main__":
    main()

