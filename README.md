# Kridha
### create virtualenv in cloned folder
```pip install virtualenv```
```virtualenv venv```
### activate virtualenv
```.\venv\Scripts\activate```  or ```source .\venv\Scripts\activate```


### install requirements
```pip install -r requirements.txt```



### create branch at added Product,Categroy Data -- eg:'test'
```git chechkout test```
1 . ```python manage.py makemigrations```
2 . ```python manage.py migrate```

```git checkout master```

1 . ```python manage.py makemigrations```
2 . ```python manage.py migrate```
3 . ```python manage.py createsuperuser```
4 . ```python manage.py runserver```
