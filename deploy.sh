source ~/.bashrc

cd /home/ec2-user/snugg-server
git checkout develop --quiet
git pull origin develop

docker-compose down
docker-compose up -d
