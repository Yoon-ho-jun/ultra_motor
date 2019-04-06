main : ArrayBaseStack.o ArrayBaseStackMain.o
	gcc -o main ArrayBaseStack.o ArrayBaseStackMain.o

ArrayBaseStack.o : ArrayBaseStack.c ArrayBaseStack.h
	gcc -c ArrayBaseStack.c

ArrayBaseStackMain.o : ArrayBaseStackMain.c ArrayBaseStack.h
	gcc -c ArrayBaseStackMain.c

