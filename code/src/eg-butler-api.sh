source venv/bin/activate
#flask run --host=0.0.0.0 --debugger
#python run.py
HOME=/home/gvalera/eg-butler
echo HOME=$HOME
echo Certificates:
ls -l $HOME/pki/*
echo Configuration:
ls -l ${HOME}/eg-butler.ini
echo python ${HOME}/eg-butler-api.py ${HOME}/eg-butler.ini
     python ${HOME}/eg-butler-api.py ${HOME}/eg-butler.ini
echo

