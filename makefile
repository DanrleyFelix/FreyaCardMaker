start:
	pipenv run start

build-windows:
	pipenv run build-windows

build-linux:
	pipenv run build-linux &&\
	cp -r 'card attributes' data FreyaCardMaker.desktop index 'card backgrounds' \
	design.qss icon.png interface 'card ranks' \
	fonts icons presets 'card rating' images dist/