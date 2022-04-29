APP_NAME='taxi-fare-price-loic'

# ----------------------------------
#         LOCAL SET UP
# ----------------------------------

install_requirements:
	@pip install -r requirements.txt

# ----------------------------------
#         HEROKU COMMANDS
# ----------------------------------

streamlit:
	-@streamlit run app.py

heroku_login:
	-@heroku login

heroku_create_app:
	-@heroku create ${APP_NAME}

deploy_heroku:
	-@git push heroku master
	-@heroku ps:scale web=1

# ----------------------------------
#    LOCAL INSTALL COMMANDS
# ----------------------------------
install:
	@pip install . -U

clean:
	@rm -fr */__pycache__
	@rm -fr __init__.py
	@rm -fr build
	@rm -fr dist
	@rm -fr *.dist-info
	@rm -fr *.egg-info


# ----------------------------------
#      DOCKER CREATION
# ----------------------------------
PACKAGE_LOC = '.'
DOCKER_NAME=$(shell python ${PACKAGE_LOC}/config.py 'PROJECT_NAME')_image

docker_build:
	@docker build --tag=${DOCKER_NAME} .
	@echo "docker image: ${DOCKER_NAME}"
	@docker build --tag=${DOCKER_NAME}_amd64 --platform linux/amd64 .
	@echo "docker image: ${DOCKER_NAME}_amd64"

docker_run:
	@docker run \
		-e PORT=8000 \
		-p 8000:8000 \
		${DOCKER_NAME}

# ----------------------------------
#      DEPLOY ON GOOGLE CLOUD
# ----------------------------------
# GCP project id
PROJECT_ID=$(shell python ${PACKAGE_LOC}/config.py 'PROJECT_ID')

# choose your region from https://cloud.google.com/storage/docs/locations#available_locations
REGION=$(shell python ${PACKAGE_LOC}/config.py 'REGION')

deploy_to_google:
	@gcloud config set project ${PROJECT_ID}
	@docker build -t eu.gcr.io/${PROJECT_ID}/${DOCKER_NAME}_amd64 --platform linux/amd64 .
	@docker push eu.gcr.io/${PROJECT_ID}/${DOCKER_NAME}_amd64
	@gcloud run deploy \
    --image eu.gcr.io/${PROJECT_ID}/${DOCKER_NAME}_amd64 \
    --platform managed \
    --region ${REGION} \
    --set-env-vars "GOOGLE_APPLICATION_CREDENTIALS=/credentials.json"
