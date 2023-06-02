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

## Correr imagen de Docker

### Windows
```
docker build -t black_list:v1 .
docker run -p 3003:3003 black_list:v1
```

[Implementar deploy en AWS Beanstalk](https://docs.aws.amazon.com/es_es/elasticbeanstalk/latest/dg/using-features.rolling-version-deploy.html)

git clone https://git-codecommit.us-east-1.amazonaws.com/v1/repos/dreamteam_blacklist_e1 dreamteam_blacklist_e1
