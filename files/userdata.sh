#!/bin/bash

cd /tmp &&
echo "updating packages"
yum update -y &&
echo "installing docker"
amazon-linux-extras install docker &&
usermod -a -G docker ec2-user &&
systemctl enable --now docker &&
echo "vm.max_map_count=262144" >> /etc/sysctl.conf &&


echo "installing docker compose"
curl -L https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose &&
chmod +x /usr/local/bin/docker-compose &&
yum install git -y &&

echo "starting docker-compose"
sysctl -w vm.max_map_count=262144 

echo "logging into ec2-user to build airflow"
sudo -u ec2-user -i <<'EOF'

pwd
whoami 

echo "Connecting to my git remote repository and getting the docker-compose file for airflow"
git init
touch linux-git-install.txt
git config --global init.defaultBranch "ec2"
git config --global user.name "Joaoluislins"
git config --global user.email "joaoluislins@gmail.com"
git add .
git commit -m "New linux git install commit"
git remote add origin https://Joaoluislins:senhateste@github.com/Joaoluislins/algotrader-aws-airflow.git
git fetch
git checkout -m origin/main docker-compose.yaml 

echo "building airflow client"
mkdir -p ./dags ./logs ./plugins
echo -e "AIRFLOW_UID=$(id -u)" > .env
echo -e "AIRFLOW_GID=0" >> .env
echo -e "sync_password=senhateste" >> .env 
/usr/local/bin/docker-compose up airflow-init 
/usr/local/bin/docker-compose up -d

EOF