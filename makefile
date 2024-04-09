CC=clang
FLAGS=-Wall -pedantic -std=c99
CFLAGS=-c -Wall -std=c99 -fPIC -pedantic
LIBS=-L. -lphylib

all: phylib

clean:
	rm -f *.o *.so *.svg phylib

libphylib.so: phylib.o
	$(CC) -lm phylib.o -shared -o libphylib.so

phylib.o: phylib.c phylib.h
	$(CC) $(CFLAGS) phylib.c -o phylib.o

phylib_wrap.c: phylib.i
	swig -python phylib.i

phylib.py: phylib.i
	swig -python phylib.i

phylib: server.py libphylib.so _phylib.so
	python3 server.py 55258

phylib_wrap.o: phylib_wrap.c
	$(CC) $(CFLAGS) phylib_wrap.c -I/usr/include/python3.11 -o phylib_wrap.o

_phylib.so: phylib_wrap.o
	$(CC) $(LIBS) $(FLAGS) -shared phylib_wrap.o -L/usr/lib/python3.11 -lpython3.11 -o _phylib.so
