CC = ghc
CFLAGS = -O2 -Wall

all: build

build: Main.hs
	$(CC) $(CFLAGS) -o similaridade Main.hs

run: build
	./similaridade res.txt sep.txt c1.txt c2.txt

clean:
	rm -f similaridade *.o *.hi

.PHONY: all build run clean
