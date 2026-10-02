# Проект АСУ etalon-260913

Проект автоматизации  

- Логика управления написана для контроллера KRAX PLC-932
- Визуализация написана на python3+qtpy

# Сборка 

Собрать deb
```console 
debuild -uc -us -b
```
Собрать wheel
```console
python3 -m build --wheel
```

# Установка

deb установить
```console
sudo apt install <имя deb>
```

wheel установить
```console
#создаем venv окружение с доступом к уже установленным 
#системным пакетам (python3-pyqt5 например нужен)
python3 -m venv .venv --system-site-packages
# активируем созданную venv
source .venv/bin/activate
# установим
pip install etalon-260913-py3-none-any.whl
```

## Зависимости

PyQt5/PyQt6, pysca, concreteui, concrete6

pysca/concreteui/concrete6 выложены в https://apt.vlinnik.ru, Настройка репозитория в https://apt.vlinnik.ru/readme.txt

# Запуск

Если запускаем из исходников, то

```
PYTHONPATH=src python3 -m gui 
```
Если из установленного wheel
```console
python3 -m gui 
```

Если из установленного deb
```console
pysca-hmi run gui 
# или 
pysca project run gui
```
Также при установке deb создается ярлык приложения kmn-260811, который запускает
приложение привычным способом

# Замечания

- добавление модуля concrete6 требует использование navbar, не очевидно и нигде не жалуется. 