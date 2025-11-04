import streamlit as st
import cv2
import mediapipe as mp
import numpy as np
import threading
from queue import Queue
import time

# Configuración de MediaPipe
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
pose = mp_pose.Pose(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

# Variables globales con protección de hilos
class SharedData:
    def __init__(self):
        self.mutex = threading.Lock()  # Mutex para proteger datos compartidos
        self.postura = "Desconocida"
        self.frame = None
        self.running = False
        
shared = SharedData()

def calcular_angulo(punto1, punto2, punto3):
    """
    Calcula el ángulo entre tres puntos (útil para detectar posturas)
    """
    # Convertir puntos a arrays numpy
    a = np.array([punto1.x, punto1.y])
    b = np.array([punto2.x, punto2.y])
    c = np.array([punto3.x, punto3.y])
    
    # Vectores
    ba = a - b
    bc = c - b
    
    # Calcular ángulo
    cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
    angle = np.arccos(np.clip(cosine_angle, -1.0, 1.0))
    
    return np.degrees(angle)

def detectar_postura(landmarks):
    """
    Detecta si la persona está PARADA o SENTADA basándose en landmarks
    """
    try:
        # Obtener puntos clave (lado izquierdo del cuerpo)
        cadera = landmarks[mp_pose.PoseLandmark.LEFT_HIP.value]
        rodilla = landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value]
        tobillo = landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value]
        
        # Calcular el ángulo de la rodilla
        angulo_rodilla = calcular_angulo(cadera, rodilla, tobillo)
        
        # Calcular la relación de altura entre cadera y rodilla
        altura_cadera_rodilla = abs(cadera.y - rodilla.y)
        
        # Lógica de detección:
        # Si el ángulo de la rodilla es menor a 120° -> SENTADO
        # Si el ángulo es mayor a 150° -> PARADO
        if angulo_rodilla < 120:
            return "SENTADO 🪑", angulo_rodilla
        elif angulo_rodilla > 150:
            return "PARADO 🧍", angulo_rodilla
        else:
            return "TRANSICIÓN", angulo_rodilla
            
    except Exception as e:
        return "Error en detección", 0

def procesar_video():
    """
    Hilo principal que captura y procesa el video
    """
    cap = cv2.VideoCapture(0)
    
    while shared.running:
        ret, frame = cap.read()
        if not ret:
            continue
            
        # Convertir BGR a RGB (MediaPipe usa RGB)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Procesar con MediaPipe
        results = pose.process(frame_rgb)
        
        # Dibujar landmarks en el frame
        if results.pose_landmarks:
            mp_drawing.draw_landmarks(
                frame,
                results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS,
                mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
                mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2, circle_radius=2)
            )
            
            # Detectar postura
            postura, angulo = detectar_postura(results.pose_landmarks.landmark)
            
            # ===== SECCIÓN CRÍTICA =====
            # Usar mutex para actualizar datos compartidos de forma segura
            shared.mutex.acquire()
            try:
                shared.postura = postura
                shared.frame = frame
            finally:
                shared.mutex.release()  # Siempre liberar el mutex
            # ===== FIN SECCIÓN CRÍTICA =====
            
            # Agregar texto al frame
            cv2.putText(frame, f"Postura: {postura}", (10, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(frame, f"Angulo rodilla: {angulo:.1f}", (10, 70),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
        
        # Actualizar frame en datos compartidos
        shared.mutex.acquire()
        try:
            shared.frame = frame
        finally:
            shared.mutex.release()
        
        time.sleep(0.03)  # ~30 FPS
    
    cap.release()

# ===== INTERFAZ STREAMLIT =====
def main():
    st.set_page_config(page_title="Detección de Postura", page_icon="🧍", layout="wide")
    
    st.title("🚹 Detección de posturas: Parado vs Sentado ⚖︎")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📹 Video en tiempo real")
        frame_placeholder = st.empty()
    
    with col2:
        st.subheader("📊 Estado actual")
        postura_placeholder = st.empty()
        
        st.markdown("---")
        st.markdown("### 💡 Instrucciones:")
        st.markdown("""
        1. Colócate frente a la cámara
        2. La app detectará tu postura automáticamente
        3. Prueba estar **parado** y **sentado**
        """)
        
        st.markdown("---")
        st.markdown("### 🔧 Conceptos técnicos:")
        
        with st.expander("🧵 Hilos (Threads)"):
            st.write("""
            **¿Qué son?** Los hilos permiten ejecutar múltiples tareas simultáneamente.
            
            **En este proyecto:** Un hilo captura y procesa el video continuamente 
            mientras otro hilo mantiene la interfaz actualizada y responsive.
            
            **Sin hilos:** La aplicación se "congelaría" mientras procesa cada frame.
            """)
        
        with st.expander("🔒 Mutex (Exclusión Mutua)"):
            st.write("""
            **¿Qué es?** Un mutex es un mecanismo de sincronización que actúa como 
            un "candado" para proteger datos compartidos.
            
            **En este proyecto:** Protege las variables `postura` y `frame` para que 
            solo un hilo pueda modificarlas a la vez.
            """)
        
        with st.expander("⚠️ Sección Crítica"):
            st.write("""
            **¿Qué es?** Porción de código donde se accede o modifica recursos compartidos 
            entre múltiples hilos.
            
            **En este proyecto:** Cada vez que actualizamos `shared.postura` o `shared.frame`, 
            usamos `mutex.acquire()` antes y `mutex.release()` después.
            """)
        
        with st.expander("🚦 Semáforos"):
            st.write("""
            **¿Qué son?** Controlan cuántos hilos pueden acceder a un recurso simultáneamente.
            
            **Diferencia con Mutex:** 
            - Mutex: Solo 1 hilo a la vez
            - Semáforo: N hilos a la vez (configurable)
            
            **En este proyecto:** Se podría usar para limitar cuántos frames se procesan 
            simultáneamente y evitar sobrecarga del sistema.
            """)
    
    col_btn1, col_btn2 = st.columns(2)
    
    with col_btn1:
        if st.button("▶️ Iniciar Detección", use_container_width=True):
            if not shared.running:
                shared.running = True
                thread = threading.Thread(target=procesar_video, daemon=True)
                thread.start()
                st.success("¡Detección iniciada!")
    
    with col_btn2:
        if st.button("⏹️ Detener", use_container_width=True):
            shared.running = False
            st.info("Detección detenida")
    
    # Loop principal de visualización
    while shared.running:
        # Leer datos compartidos de forma segura
        shared.mutex.acquire()
        try:
            current_frame = shared.frame
            current_postura = shared.postura
        finally:
            shared.mutex.release()
        
        # Mostrar frame
        if current_frame is not None:
            frame_rgb = cv2.cvtColor(current_frame, cv2.COLOR_BGR2RGB)
            frame_placeholder.image(frame_rgb, channels="RGB", use_container_width=True)
        
        # Mostrar postura con estilo
        if current_postura == "PARADO 🧍":
            postura_placeholder.success(f"## {current_postura}")
        elif current_postura == "SENTADO 🪑":
            postura_placeholder.info(f"## {current_postura}")
        else:
            postura_placeholder.warning(f"## {current_postura}")
        
        time.sleep(0.1)

if __name__ == "__main__":
    main()
