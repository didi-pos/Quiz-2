<div align="center">
<h1>Quiz 2</h1>
  <p>
    Ingeniería Electrónica · Universidad Santo Tomás
    <br>
    <b>Didier Posse</b>
    <br>
    <em>Ejecución del código</em>
  </p>
</div>

<hr>

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
