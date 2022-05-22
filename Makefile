.PHONY: build clean

build:
	pyinstaller -D -F -n spj -c spj.py
clean:
	rm -rf build dist spj.spec
