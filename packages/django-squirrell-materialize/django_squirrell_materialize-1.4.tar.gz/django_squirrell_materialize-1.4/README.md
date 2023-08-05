# Guía de los Paquetes de Python (PIP)
Estos paquetes nos permiten instalar los proyectos que deseemos con un simple comando. Tenemos dos formas de compartir dichos paquetes, dependiendo de si lo queremos publicar para todo el mundo o de forma privada. Si lo subimos a su propio repositorio oficial: [PyPi](https://pypi.org) los archivos serán completamente públicos. Por lo que si queremos mantener nuestro paquete privado debemos utilizar cualquier via que nos permita almacenar el directorio, como *GitHub* con un repositorio privado.

## 1. Registrarnos en PyPi
Si queremos compartirlo de forma pública tenemos que registrarnos [aquí](https://pypi.org/account/register/). Este repositorio nos permitirá almacenar las diferentes versiones del proyecto.

## 2. Herramientas necesarias
Tenemos que comprobar que tenemos *Python* y *Pip* instalado.
```
python -V  # para python version (2/3)
python -m pip --version
```
De no estar instalados no podremos continuar, así que instálalos de no tenerlos.

Instalamos los paquetes necesarios, teniendo en cuenta de que **si tenemos diferentes librerias de Python en el sistema** tenemos que instalarle los paquetes a la que vayamos a usar posteriormente. Simplemente indicándole `sudo phyton3 -m pip install ...` sustituyendo el 3 por la versión que queramos.

- **Setuptools:** [Setuptools](https://pypi.org/project/setuptools/) se utiliza para crear y distrubuir los paquetes de Python.
- **Wheel:** El paquete [Wheel](https://pypi.org/project/wheel/) nos permite realizar el comando `bdist_wheel` que crea el archivo ejecutable `.whl`, `pip install` se encarga de su ejecución.
- **Twine:** El paquete [Twine](https://pypi.org/project/twine/) nos aporta una conexión segura para subir los archivos a *PyPi*. 
- **Tqdm:** Es usado internamente por Twine.

```
sudo python -m pip install --upgrade pip setuptools wheel
sudo python -m pip install tqdm
sudo python -m pip install --user --upgrade twine
```
> Al indicarle `--user` tenemos que cercionarnos posteriormente de usar siempre los comandos con permisos `sudo`, de lo contrario no funcionarán y tampoco nos arrojará un error descriptivo.

## 3. Creación del proyecto
Creamos un directorio para nuestro paquete, en este ejemplo se va a llamar `paquete_pkg`, el nombre de este directorio no va a una vez que esté subido, así que mientras maś descriptivo mejor.

Ahora entramos en nuestro directorio y creamos un archivo vacio que será nuestro script. A nuestro script lo vamos a llamar `hola`.
```
cd paquete_pkg

touch hola
```
Ahora abriremos `hola`.
```
nano hola
```
Y le añadimos solo un par de líneas:
```
#!/usr/bin/env python3

echo "hey there, this is my first pip package"
```
Una vez guardado, vamos a hacerlo ejectuable:
`chmod +x hola`

Lo siguiente es crear el archivo `setup.py`
`touch setup.py`

Y le añadimos toda la información del paquete:
```
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
     name='nombre de nuestro paquete',  
     version='0.1',
     scripts=['hola'] ,
     author="Deepak Kumar",
     author_email="deepak.kumar.iet@gmail.com",
     description="A Docker and AWS utility package",
     long_description=long_description,
   long_description_content_type="text/markdown",
     url="https://github.com/javatechy/dokr",
     packages=setuptools.find_packages(),
     include_package_data=True,
     zip_safe=True,
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )
```
> El nombre que le demos más arriba será el nombre con el que se subirá.

## 4. Compilar el paquete
Vamos a la carpeta de nuestro proyecto y ejecutamos `python setup.py bdist_wheel`. Esto creará la toda la estructura del paquete.

## 5. Instalar en local
Si queremos comprobar su funcionamiento lo instalamos localmente así:
`python -m pip install dist/hola-0.1-py3-none-any.whl`

> Recuerda usar la versión de Python en la que has instalado todo lo anterior.

## 6. Subir el pip
1. Creamos el archivo `.pypirc` en nuestro directorio principal.
   - **Para Windows:** `C:\Users\UserName\.pypirc`
   - **Para Linux:** `~/.pypirc `
  
2. Añadimos el siguiente contenido al archivo y reemplazamos `usuario` con nuestro nombre de usuario.
```
[distutils] 
index-servers=pypi
[pypi] 
repository = https://upload.pypi.org/legacy/ 
username =usuario
```
3. Finalmente, para subir nuestro paquete usamos *Twine*:
`python -m twine upload dist/*`

Si queremos instalar dicho paquete simplemente hacemos:
`pip install nombredelpaquete`

## 7. Actualizar nuestro paquete
Abrimos nuestro `setup.py` y aumentamos su versión. Ejemplo: `version='0.1'` -> `version='0.2'`. Podemos aumentar su versión cómo queramos, es decir, podemos añadirle otro decimal.

Abrimos la terminal en nuestro paquete y ejecutamos `python setup.py sdist` para que actualice el paquete con los nuevos cambios.

Volvemos a subir nuestro paquete con:
`python -m twine upload dist/*`

### Añadir archivos No Python
Si queremos añadir a nuestro paquete archivos que no sean de Python tenemos que crear un archivo `MANIFEST.in` en la raíz de nuestro paquete. Nuestro archivo de ejemplo queda así:
```
include MANIFEST.in
graft templates
graft static
global-include *.html *.js *.css

```
- `include` -> se utiliza para indicar qué archivo y/o tipo de archivo incluye.
- `global-include` -> incluye todos los archivos listados.
- `graft` -> incluye todos los archivos de la carpeta que elijamos.

### Cosas importantes
- Si tenemos problemas a la hora de subir una nueva versión y nos indica que esa versión ya existe, entramos en `dist/` y borramos las versiones anteriores.
- Si borramos el paquete en el repositorio oficial ese repositorio desaparece y se convierten en inutilizable.
- Los subdirectorios que se queramos que se instalen tienen que llevar el archivo `__init__.py`. De lo contrario, al instalarlo en el entorno virtual no lo traera.

> El último punto hay que comprobar si hay que añadirlo a todas las carpetas o solo a la primera.

#### Enlaces de referencia
+ [Build Your First pip Package](https://dzone.com/articles/executable-package-pip-install).
+ [PyPI How to upload a new version](https://github.com/fhamborg/news-please/wiki/PyPI---How-to-upload-a-new-version).
+ [Adding Non-Code Files](https://python-packaging.readthedocs.io/en/latest/non-code-files.html).
+ [Creating a Source Distribution](https://docs.python.org/2/distutils/sourcedist.html#commands).









