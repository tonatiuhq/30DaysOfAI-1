import streamlit as st
import pathlib
import re

# --- Configuration ---
APP_DIR = pathlib.Path('app')
MD_DIR = pathlib.Path('md')

# --- Helper Functions ---
def update_params():
    """Updates the URL query param to the selected number."""
    st.query_params.day = st.session_state.day_selection

def format_day(day_num):
    """Formats the number (e.g., 2) as a display string (e.g., 'Day 2')."""
    return f'Day {day_num}'

# --- File Discovery ---
try:
    matches = []
    for path in APP_DIR.glob('day*.py'):
        match = re.search(r'day(\d+)\.py', path.name)
        if match:
            matches.append((int(match.group(1)), path))

    # Sort by number, e.g., (1, path) comes before (2, path)
    matches.sort()
    
    # Create a list of the numbers (options)
    day_options = [num for num, path in matches]

except FileNotFoundError:
    day_options = []

# --- State and Navigation ---
query_params = st.query_params

# Determine the initial day number
initial_day_num = day_options[0] if day_options else None # Default to the first day's number (e.g., 1)

if "day" in query_params and day_options:
    try:
        # Convert ?day=2 (string "2") to integer 2
        day_num_from_url = int(query_params.day)
        
        # Check if the number is in our valid list
        if day_num_from_url in day_options:
            initial_day_num = day_num_from_url # Override default
            
    except (ValueError, TypeError):
        # Ignore invalid params like ?day=abc or ?day=
        pass 

# Set the session state (now storing a number)
# This is done only once if it's not already set
if "day_selection" not in st.session_state:
    st.session_state.day_selection = initial_day_num
else:
    # Ensure session state is valid if it *is* set
    if st.session_state.day_selection not in day_options and day_options:
        st.session_state.day_selection = initial_day_num


# --- Dynamic Logo Based on Sidebar State ---
# Logo for when sidebar is expanded (icon only)
logo_icon = "https://www.streamlit.io/images/brand/streamlit-mark-color.svg"

# Logo for when sidebar is collapsed (full logo with text)
logo_full = "https://www.streamlit.io/images/brand/streamlit-logo-primary-colormark-darktext.svg"

# Set the logo with icon_image parameter for collapsed sidebar state
st.logo(logo_full, link="https://streamlit.io", icon_image=logo_icon, size="large")

# --- Page Title ---

# --- Sidebar ---
st.sidebar.title("30 Days of AI")
st.sidebar.markdown("The `#30DaysOfAI` is a coding challenge designed to help you get started in building AI apps with Streamlit.")

# Create the selectbox (only if there are day options)
if day_options:
    selected_day_num = st.sidebar.selectbox(
        'Start the Challenge 👇', 
        day_options, # Use the list of numbers [1, 2, ...] as options
        key="day_selection",
        on_change=update_params, # Updates URL to ?day=2
        format_func=format_day # Use this function to display "Day 1", "Day 2", ...
    )
else:
    selected_day_num = None
    st.sidebar.info("Daily challenges will appear here once published!")

# --- Dynamic Content Display ---
if not day_options:
    # --- Welcome Page (No Challenge Files Found) ---
    st.title("🚀 Welcome to the 30 Days of AI Challenge!")
    
    st.markdown("""
    ¡Bienvenidos! 👋

    Prepárate para un emocionante viaje para crear aplicaciones basadas en IA con **Streamlit** y **Snowflake**.
    
    ### 🎯 Qué aprenderás
    
    Durante los próximos 30 días, progresarás desde conceptos básicos hasta técnicas avanzadas:
    
    - 💬 **Semana 1 (Días 1-7)**: Fundamentos: Tus primeras llamadas LLM, streaming y almacenamiento en caché
    
    - 🗨️ **Semana 2 (Días 8-14)**: Creación de chatbots: Interfaces de chat y estado de sesión
    
    - 📚 **Semana 3 (Días 15-21)**: Aplicaciones RAG: Recuperación-Generación Aumentada
    
    - 🚀 **Semana 4 (Días 22-30)**: Funciones avanzadas: IA multimodal, agentes e implementación
    
    ### 📅 ¡El desafío comienza pronto!
    
    Se publicarán desafíos diarios a medida que avancemos en el recorrido de 30 días. Cada día encontrarás:
    - 📝 Un nuevo desafío de programación
    - 💡 Explicaciones detalladas
    - 🎓 Conceptos clave y mejores prácticas
    
    ### 🛠️ Requisitos previos
    
    - **[Cuenta de prueba gratuita de Snowflake](https://signup.snowflake.com/?trial=student&cloud=aws&region=us-west-2&utm_source=streamlit-campaign&utm_campaign=30daysofai)** con Cortex AI habilitado
    - **Python 3.10+**
    - Conocimientos básicos de Python
    
    ### 🔗 Prepárate
    
    Asegúrate de:
    
    1. Tener instaladas las dependencias necesarias (`pip install -r requirements.txt`)
    
    2. Tener lista tu credencial de Snowflake
    
    3. ¡Una mente curiosa y ganas de aprender! 🎉
    
    ---
    
    **¡No se pierdan el Día 1!** El contenido del desafío aparecerá aquí a medida que avancemos cada día.
    
    Compartan su experiencia en redes sociales con **#30DaysOfAI** 🚀
    """)
    
    st.info("💡 **Tip**: Daily challenges will appear in the sidebar once they're published.")

elif selected_day_num:
    
    # Create the main display name (e.g., "Day 2")
    display_name = format_day(selected_day_num)
    
    try:
        # --- 1. Load Python File Content ---
        py_file_path = APP_DIR / f'day{selected_day_num}.py'
        lines = py_file_path.read_text(encoding='utf-8').splitlines()
        subtitle = lines[1].lstrip("# ") if len(lines) > 1 else ""
        code_to_display = "\n".join(lines[3:])

        # --- 2. Load and Parse Markdown File Content ---
        intro_content = ""
        expander_content = ""
        try:
            md_file_path = MD_DIR / f'day{selected_day_num}.md'
            if md_file_path.is_file():
                full_explanation_content = md_file_path.read_text(encoding='utf-8')
                parts = full_explanation_content.split("---", 1)
                intro_content = parts[0].strip()
                if len(parts) == 2:
                    expander_content = parts[1].strip()
        except Exception as e:
            st.warning(f"Could not load explanation file: {e}")

        # --- 3. Display Content in Order ---
        
        # 3.1. Header and Subheader
        st.header(f':primary[:material/calendar_today:] {display_name}')
        if subtitle:
            st.subheader(subtitle)

        # 3.2. Markdown Intro
        if intro_content:
            st.markdown(intro_content)

        # 3.3. Code Expander
        with st.expander("See the code:", expanded=True):
            st.code(code_to_display, language='python')
            
        # 3.4. Explanation Expander
        if expander_content:
            with st.expander("See the explanation", expanded=True):
                st.markdown(expander_content)

    except FileNotFoundError:
        st.error(f'Error: Could not find file: {py_file_path}')
    except Exception as e:
        st.error(f"An error occurred while trying to read the file: {e}")
