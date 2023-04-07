## Preparar Entorno Virtual

# Crear entorno virtual
python3 -m venv venv
# Activar entorno virtual
source venv/bin/activate
# En caso de que se quiera desactivar el entorno virtual
deactivate
# Dirigirse a la carpeta del componente
```
cd MISO_Devops_Grupo_JASA/black_list
```
-- Instalar dependencias
```
pip3 install -r requirements.txt
```
-- En caso de que se quiera correr el componente de Flask individualmente local
-- black-list
```
export FLASK_APP=application.py
flask run -p 3000
```

