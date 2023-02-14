python -m venv mozarkFinanceSystem
source mozarkFinanceSystem/bin/activate
python -m pip install Django

cd mozarkFinanceSystem
django-admin startproject financeSystem
cd financeSystem
python manage.py runserver

ctrl+C
python manage.py startapp financeApps