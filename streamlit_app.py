import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import chardet

# Set page config
st.set_page_config(
    page_title="Uso de IA en ADSO",
    page_icon="🤖",
    layout="wide"
)

# Title and description
st.title("Análisis de Uso de Inteligencia Artificial en Formación")
st.markdown("Dashboard para analizar los resultados de la encuesta sobre el uso de IA en procesos formativos")

# Function to detect file encoding and load data
@st.cache_data
def load_data(file_path='temp_survey_data.csv'):
    # First detect the encoding
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read())
    
    file_encoding = result['encoding']
    st.info(f"Formato de archivo encontrado: {file_encoding}")
    
    # Define column names in English for easier processing
    columns = {
        "Marca temporal": "timestamp",
        "¿Cuál inteligencia artificial es la que más usa en su día a día?": "most_used_ai",
        "¿Se ha vuelto dependiente de alguna IA?": "ai_dependency",
        "¿Cómo afecta la IA en su proceso formativo(ADSO)?": "ai_impact",
        "¿Se considera usted menos inteligente después del uso constante de una IA?": "feel_less_intelligent",
        "¿Cuál sector laboral cree usted que fue consumido en su totalidad por las IA?": "ai_dominated_sector",
        "¿En que área considera usted que la IA puede aumentar nuestra capacidad de adquirir conocimiento?": "ai_learning_area"
    }
    
    # Try loading with detected encoding
    try:
        df = pd.read_csv(file_path, encoding=file_encoding)
    except:
        # If that fails, try common encodings
        encodings_to_try = ['latin1', 'ISO-8859-1', 'cp1252']
        for enc in encodings_to_try:
            try:
                df = pd.read_csv(file_path, encoding=enc)
                st.success(f"Satisfactoriamente cargado con la codificacion: {enc} ")
                break
            except:
                continue
        else:
            # If all attempts fail
            raise Exception("No se puede cargar el CSV, no tiene ningun formato comun o conocido")
    
    # Rename columns for easier handling
    df = df.rename(columns=columns)
    
    # Convert timestamp to datetime
    try:
        df['timestamp'] = pd.to_datetime(df['timestamp'], format='%Y/%m/%d %I:%M:%S %p GMT-5')
    except:
        # If standard format fails, try a more flexible approach
        df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
    
    return df

try:
    # Add file uploader to allow users to upload their CSV
    uploaded_file = st.file_uploader("Subir archivo CSV", type=['csv'])
    
    if uploaded_file is not None:
        # Save the uploaded file temporarily
        with open("temp_survey_data.csv", "wb") as f:
            f.write(uploaded_file.getbuffer())
        df = load_data("temp_survey_data.csv")
    else:
        # Try to load the default file
        df = load_data()
    
    # Display the raw data if users want to see it
    with st.expander("Ver datos en bruto"):
        st.dataframe(df)
    
    # Create tabs for different analysis views
    tab1, tab2, tab3 = st.tabs(["Uso de IA", "Impacto en formación", "Sectores y áreas"])
    
    with tab1:
        st.header("Uso de Inteligencia Artificial")
        
        # Distribution of most used AI
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("IA más utilizada")
            ai_counts = df['most_used_ai'].value_counts()
            
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.pie(ai_counts, labels=ai_counts.index, autopct='%1.1f%%', startangle=90)
            ax.axis('equal')
            st.pyplot(fig)
        
        with col2:
            st.subheader("Dependencia de IA")
            dependency_counts = df['ai_dependency'].value_counts()
            
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.barplot(x=dependency_counts.index, y=dependency_counts.values, palette="viridis", ax=ax)
            ax.set_ylabel("Número de respuestas")
            ax.set_xlabel("Nivel de dependencia")
            st.pyplot(fig)
    
    with tab2:
        st.header("Impacto en la Formación")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("¿Se sienten menos inteligentes?")
            intelligence_counts = df['feel_less_intelligent'].value_counts()
            
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.barplot(x=intelligence_counts.index, y=intelligence_counts.values, palette="viridis", ax=ax)
            ax.set_ylabel("Número de respuestas")
            ax.set_xlabel("Respuesta")
            st.pyplot(fig)
        
        with col2:
            st.subheader("Comentarios sobre impacto formativo")
            
            # Show a word cloud or just list the responses
            impact_responses = df['ai_impact'].dropna()
            if not impact_responses.empty:
                st.write("Respuestas:")
                for response in impact_responses:
                    st.write(f"- {response}")
            else:
                st.write("No hay suficientes respuestas para analizar.")
    
    with tab3:
        st.header("Sectores y Áreas de Aplicación")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Sectores dominados por IA")
            sector_counts = df['ai_dominated_sector'].value_counts()
            
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.barplot(x=sector_counts.values, y=sector_counts.index, palette="viridis", ax=ax)
            ax.set_xlabel("Número de respuestas")
            ax.set_ylabel("Sector")
            st.pyplot(fig)
        
        with col2:
            st.subheader("Áreas donde la IA puede aumentar el aprendizaje")
            learning_counts = df['ai_learning_area'].value_counts()
            
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.barplot(x=learning_counts.values, y=learning_counts.index, palette="viridis", ax=ax)
            ax.set_xlabel("Número de respuestas")
            ax.set_ylabel("Área")
            st.pyplot(fig)
    
    # Add a section for cross-analysis
    st.header("Análisis cruzado")
    
    # Relationship between most used AI and feeling less intelligent
    st.subheader("Relación entre IA más usada y sentirse menos inteligente")
    
    cross_tab = pd.crosstab(df['most_used_ai'], df['feel_less_intelligent'])
    
    fig, ax = plt.subplots(figsize=(12, 6))
    cross_tab.plot(kind='bar', stacked=True, ax=ax)
    ax.set_xlabel("IA más usada")
    ax.set_ylabel("Número de respuestas")
    ax.legend(title="¿Se siente menos inteligente?")
    st.pyplot(fig)
    
    # Add concluding insights
    st.header("Conclusiones")
    st.write("""
    Basado en los datos recopilados, podemos observar:
    
    1. Chat GPT parece ser la IA más utilizada entre los encuestados.
    2. La mayoría de los usuarios no se sienten menos inteligentes después de usar IA.
    3. El desarrollo de software/programación es considerado tanto un sector dominado por IA como un área donde la IA puede aumentar el aprendizaje.
    4. Las opiniones sobre el impacto de la IA en la formación son variadas, desde positivas hasta preocupaciones sobre la dependencia.
    """)

except Exception as e:
    st.error(f"Error al cargar o procesar los datos: {e}")
    st.write("Intenta subir el archivo usando el cargador de archivos arriba.")
    
    # Add troubleshooting tips
    st.warning("Consejos para solucionar problemas de codificación:")
    st.write(""" """)

# Add a footer
st.markdown("---")
st.markdown("Desarrollado para análisis de encuesta sobre uso de IA en formación ADSO")