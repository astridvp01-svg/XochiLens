import streamlit as st
import requests
from PIL import Image
import io

# Configuración de la página bajo principios de IHC
st.set_page_config(
    page_title="XochiLens - Sistema Experto de Puebla",
    page_icon="🌿",
    layout="centered"
)

st.title("🌿 XochiLens: Flora y Fauna de Puebla")
st.markdown("Sistema experto de visión artificial para campo en tiempo real")

st.markdown("### 📸 Captura directa en campo")
st.markdown("Toca el botón de abajo para activar la cámara de tu dispositivo, enfoca la especie (flora o fauna de Puebla Capital) y captura la imagen.")

# Componente nativo optimizado para móviles (Abre la cámara del dispositivo limpiamente)
camera_image = st.camera_input("Toma una foto de la especie")

if camera_image is not None:
    with st.spinner("Analizando características morfológicas y biológicas..."):
        # Procesamiento automático de la imagen capturada
        image = Image.open(camera_image)
        
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()
        
        try:
            # Petición automática al backend de FastAPI
            response = requests.post(
                "http://127.0.0.1:8000/analizar-especie/",
                files={"file": ("field_capture.jpg", img_byte_arr, "image/jpeg")}
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # Caso 1: Identificación exitosa con Ficha Técnica
                if "ficha_tecnica" in data:
                    ficha = data["ficha_tecnica"]
                    similitud = data["similitud"]
                    
                    st.success(f"¡Especie identificada con éxito! (Similitud: {similitud})")
                    
                    st.markdown("### 📋 Ficha Técnica Estructurada")
                    st.markdown(f"**Nombre Científico:** *{ficha['nombre_cientifico']}*")
                    st.markdown(f"**Nombre Común:** {ficha['nombre_comun']}")
                    st.markdown(f"**Nombre Náhuatl Regional:** {ficha['nombre_nahua']}")
                    
                    with st.expander("🔍 Morfología y Características Físicas", expanded=True):
                        st.write(ficha['morfologia'])
                        
                    with st.expander("🌍 Ecología y Ciclo de Vida en Puebla"):
                        st.write(ficha['ecologia_ciclo'])
                        
                    with st.expander("📌 Estatus Ecológico"):
                        st.write(ficha['estatus_ecologico'])

                # Caso 2: Alerta académica por similitud baja (Regla del proyecto)
                elif "alerta" in data:
                    st.warning(f"⚠️ {data['alerta']}")
                    st.markdown("### Sugerencias de especies cercanas:")
                    for sug in data["sugerencias"]:
                        st.markdown(f"- **{sug['nombre_comun']}** (*{sug['nombre_cientifico']}*)")
                        
            else:
                st.error("❌ Error al procesar la imagen en el servidor.")
                
        except requests.exceptions.ConnectionError:
            st.error("❌ Asegúrate de tener encendido tu backend en FastAPI (`uvicorn main:app --reload`).")