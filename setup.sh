python -m pip install --upgrade pip
pip install virtualenv
virtualenv venv --python=python3.8.2
venv\Scripts\activate
pip install -r requirements.txt
git config --global --edit 
git config credential.helper store
python createSQLLite3DB.py
