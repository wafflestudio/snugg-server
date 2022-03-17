source ~/.bashrc

cd /home/ec2-user/snugg-server
git checkout develop --quiet
git pull origin develop

source venv/bin/activate
pip3 install -r requirements.txt --quiet

python3 manage.py migrate
python3 manage.py check

pkill -f gunicorn
gunicorn snugg.wsgi --bind 127.0.0.1:8000 --daemon
sudo nginx -t
sudo service nginx restart
