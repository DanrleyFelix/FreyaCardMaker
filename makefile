build-windows:
	pipenv run pyinstaller --noconsole --name="Freya Card Maker" --icon="icon.ico" --add-data="icon.ico;." --onefile main.py

build-linux:
	pipenv run pyinstaller --noconsole --name="Freya Card Maker" --icon="icon.ico" --onefile main.py

