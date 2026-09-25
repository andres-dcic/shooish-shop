
#Preparativos terraform killercoda


sudo apt-get update
sudo apt-get install -y wget unzip

wget https://releases.hashicorp.com/terraform/1.12.2/terraform_1.12.2_linux_amd64.zip

unzip terraform_1.12.2_linux_amd64.zip

sudo install terraform /usr/local/bin/terraform

#Verificar
terraform version

#Crear infra
    #main.tf
    #variables.tf

#Desplegar primeramente localstack 
#docker-compose -f compose.localstack.yaml up -d

#Probar el endpoint
curl http://localhost:4566/_localstack/health


#Estando dentro del directorio de terraform
terraform init
terraform plan
terraform apply

#Instalar cli de AWS
sudo apt-get install -y curl unzip

curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" \
  -o "awscliv2.zip"

unzip awscliv2.zip

sudo ./aws/install

aws --version

#Configure credenciales de prueba para localstack
aws configure set aws_access_key_id test
aws configure set aws_secret_access_key test
aws configure set region us-east-1
aws --endpoint-url=http://localhost:4566 s3 ls

#



