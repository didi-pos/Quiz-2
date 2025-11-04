<div align="center">
<h1>Quiz 2</h1>
  <p>
    Ingeniería Electrónica · Universidad Santo Tomás
    <br>
    <b>Didier Posse</b>
    <br>
    <em>Primer Punto</em>
  </p>
</div>

<hr>

<div align="center">
  <h2>Explicación de la Aplicación</h2>
</div>

<ol>
  <li><br>
    <div align="center">
      <p><img width=850 src="https://github.com/user-attachments/assets/f3d84c56-8a72-4907-88cf-11d8ad782c15"/></p>
    </div>
    <p>
      En esta parte del código se define la clase <code>SharedData</code>, la cual contiene las variables que se van a compartir entre los distintos hilos.  
      Dentro de esta clase se inicializa un <b>mutex</b> usando <code>threading.Lock()</code>, que actúa como un candado para evitar que dos hilos modifiquen al mismo tiempo los mismos datos.  
      También se definen las variables <code>postura</code>, <code>frame</code> y <code>running</code>, que son las que se actualizarán constantemente desde el hilo principal de procesamiento de video.  
      <br><br>
      En resumen, este bloque prepara el entorno seguro donde ambos hilos (el de procesamiento y el de interfaz) pueden comunicarse sin interferirse entre sí, evitando errores o lecturas inconsistentes mientras se detecta la postura.
    </p>
  </li>

  <li><br>
    <div align="center">
      <p><img width=850 src="https://github.com/user-attachments/assets/d723a09c-3ad1-4b9b-953d-0e5d66dfb418"/></p>
    </div>
    <p>
      Aquí se encuentra la función <code>procesar_video()</code>, la cual se ejecuta en un hilo independiente cuando el usuario presiona el botón de iniciar detección.  
      Este hilo se encarga de capturar los cuadros desde la cámara en tiempo real usando <code>cv2.VideoCapture(0)</code> y procesarlos con <b>MediaPipe</b> para detectar los puntos del cuerpo.  
      Mientras el hilo está activo (<code>shared.running = True</code>), se ejecuta en bucle continuo.  
      <br><br>
      Cada iteración del bucle obtiene un nuevo frame, lo convierte a RGB, detecta los landmarks y calcula el ángulo de la rodilla con la función <code>calcular_angulo()</code>.  
      Con base en ese ángulo se determina si la persona está parada, sentada o en transición.  
      Todo esto ocurre sin detener la interfaz, gracias al uso de hilos.
    </p>
  </li>

  <li><br>
    <div align="center">
      <p><img width=850 src="https://github.com/user-attachments/assets/f6d7a5b3-7a2b-45cd-9f49-b03d090ca36d"/></p>
    </div>
    <p>
      En este fragmento está una parte fundamental del uso de hilos: la <b>sección crítica</b>.  
      Una vez que el hilo de procesamiento obtiene la nueva postura y el frame procesado, debe actualizar las variables compartidas <code>shared.postura</code> y <code>shared.frame</code>.  
      <br><br>
      Para hacerlo sin que otro hilo lea o escriba al mismo tiempo (lo que generaría inconsistencias), se utiliza el <b>mutex</b> con las instrucciones <code>shared.mutex.acquire()</code> y <code>shared.mutex.release()</code>.  
      Esto asegura que solo un hilo acceda a esa parte del código a la vez.  
      <br><br>
      Este mecanismo evita errores de concurrencia, como mostrar un frame viejo o una postura incorrecta mientras el otro hilo aún está actualizando los datos.
    </p>
  </li>

  <li><br>
    <div align="center">
      <p><img width=850 src="https://github.com/user-attachments/assets/4f5b3953-2598-463d-9dc2-40144b6bfb7c"/></p>
    </div>
    <p>
      En esta parte del código, el hilo de la interfaz (que mantiene actualizada la ventana de Streamlit) accede también a los mismos datos compartidos.  
      Antes de leer el frame o la postura actual, vuelve a usar el mismo <b>mutex</b> para garantizar que los datos se lean de forma segura.  
      <br><br>
      El uso del mutex en lectura y escritura permite que ambos hilos trabajen en paralelo sin sobreescribir información.  
      Así, mientras el hilo de procesamiento detecta la postura en tiempo real, el hilo de interfaz puede mostrar los resultados sin interrumpirlo.
    </p>
  </li>

  <li><br>
    <div align="center">
      <p><img width=850 src="https://github.com/user-attachments/assets/8db4df58-bff5-4b29-9c8d-7a985f4fdc83"/></p>
    </div>
    <p>
      En este último bloque, se inicia el hilo de procesamiento cuando el usuario hace clic en el botón “Iniciar Detección”.  
      Se crea un nuevo hilo con <code>threading.Thread(target=procesar_video, daemon=True)</code> y se ejecuta con <code>start()</code>.  
      <br><br>
      Al hacerlo, la aplicación lanza un proceso paralelo que se encarga de todo el manejo del video y detección de postura, mientras el hilo principal se mantiene manejando la interfaz gráfica.  
      De esta forma, la app no se congela y puede seguir actualizando los resultados en tiempo real.  
      <br><br>
      Si se quisiera controlar cuántos hilos pueden ejecutar simultáneamente partes del código, se podría usar un <b>semáforo</b>, aunque en este caso el mutex fue suficiente porque solo se necesita acceso exclusivo de un hilo a la vez.
    </p>
  </li>
</ol>

<hr>

<div align="center">
  <p><em>Segundo Punto</em></p>
</div>

<hr>

<div align="center">
  <h2>Ejecución de la Aplicación</h2>
</div>

<ol>
  <li><br>
    <div align="center">
      <p><img width=850 src="https://github.com/user-attachments/assets/c27bc325-9f67-456a-a421-d7ab7378ee43"/></p>
    </div>
    <p>
      Primero, para poder ejecutar correctamente el código, hay que hacerlo de manera <b>local</b>, es decir, tener el archivo descargado en nuestro PC y ejecutarlo desde un <b>entorno virtual</b>.  
      Esto es necesario porque si se quiere acceder a la cámara del computador y mostrar la parte de <b>visión artificial</b>, debe hacerse localmente. <b>Streamlit Cloud</b> funciona como un servidor remoto y, por seguridad, no puede acceder a la cámara.  
      En cambio, si se ejecuta desde el PC, ya no sería desde un servidor, sino de forma local, lo que además hace la ejecución de la app mucho más rápida.  
      <br><br>
      Otro punto importante es que el código no funciona con la versión más reciente de <b>Python (v3.13)</b>, ya que algunas librerías que se deben instalar (<code>streamlit</code>, <code>numpy</code>, <code>mediapipe</code>...) todavía no son compatibles.  
      En particular, la librería <code>mediapipe</code> <b>no es compatible con la versión 3.13</b>, pero sí con la versión <b>Python v3.11</b>.  
      Por eso, es necesario crear un entorno virtual con esa versión para ejecutar correctamente el código.  
      Aunque en la página de Streamlit existe la opción de cambiar la versión de Python usada, no nos sirve en este caso, ya que, al ejecutarse desde el servidor (Streamlit Cloud), igualmente no podría acceder a la cámara.
    </p>
  </li>
  
  <li><br>
    <div align="center">
      <p><img width=850 src="https://github.com/user-attachments/assets/9941f119-9073-4408-9ac4-f4d587a24b67"/></p>
    </div>
    <p>
      Para poder tener <b>Python v3.11</b> sin afectar el Python del sistema (v3.13), se deben seguir estos pasos:
      <ul>
        <li>Primero, instalar las dependencias necesarias con este comando: <br>
        <code>sudo apt install -y build-essential libssl-dev zlib1g-dev libncurses5-dev \
libffi-dev libsqlite3-dev libreadline-dev libbz2-dev liblzma-dev wget</code></li>
        <li>Luego, descargar <b>Python v3.11</b> con este otro comando: <br>
        <code>cd /tmp  
wget https://www.python.org/ftp/python/3.11.9/Python-3.11.9.tgz  
tar -xf Python-3.11.9.tgz</code></li>
        <li>Después, instalarlo y habilitarlo en paralelo con el Python del sistema usando: <br>
        <code>./configure --enable-optimizations --prefix=/usr/local/python3.11  
make -j$(nproc)  
sudo make altinstall</code></li>
      </ul><br>
      Finalmente, se puede verificar que ambas versiones de Python están instaladas, como se muestra en la imagen anterior.  
      Una vez se tiene <b>Python v3.11</b>, se crea e inicia el entorno virtual con:  
      <code>/usr/local/python3.11/bin/python3.11 -m venv &lt;nombre_entorno_virtual&gt;</code>  
      y se activa con:  
      <code>source &lt;nombre_entorno_virtual&gt;/bin/activate</code>.  
      Dentro del entorno virtual se instalan las librerías necesarias para correr el código:  
      <code>pip install streamlit opencv-python mediapipe numpy</code>.
    </p>
  </li>

  <li><br>
    <div align="center">
      <p><img width=850 src="https://github.com/user-attachments/assets/e96d0733-53fa-472a-90d8-4cd008cc1d48"/></p>
    </div>
    <p>
      Este sería el código de la aplicación, pero ejecutado de forma local, ya que, como mencioné antes, es necesario tenerlo en la PC para poder acceder a la cámara y que funcione correctamente la parte de <b>visión artificial</b>.
    </p>
  </li>

  <li><br>
    <div align="center">
      <p><img width=850 src="https://github.com/user-attachments/assets/2db5946a-a82b-457f-b41e-fc613b4f1b7f"/></p>
    </div>
    <p>
      Aquí se muestra cómo, con el comando <code>streamlit run App.py</code>, se empieza a ejecutar el código de manera local en el <b>puerto 8501</b>, el cual se conecta con Streamlit.  
      La aplicación se muestra en el navegador con acceso a la cámara, permitiendo ver en tiempo real la parte de visión artificial.
    </p>
  </li>

  <li><br>
    <div align="center">
      <p><img width=850 src="https://github.com/user-attachments/assets/38db07ed-7f3f-4ad3-9405-00259bf51363"/></p>
      <p><img width=850 src="https://github.com/user-attachments/assets/71757dda-71a9-4483-ac60-1b2d99395412"/></p>
    </div>
    <p>
      En estas imágenes se muestra <b>Streamlit corriendo localmente</b> en el puerto 8501 desde el navegador.  
      Se puede ver que detecta correctamente las dos posiciones propuestas (parado y sentado).  
      La detección se realiza mediante el <b>ángulo formado entre las rodillas y el torso</b> de la persona.  
      También se observa que tanto en el video como en la columna de estado, la app indica en qué postura está la persona, además del ángulo que se está calculando para determinar la posición detectada.
    </p>
  </li>
</ol>
