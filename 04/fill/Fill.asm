// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.


(START)
   // if keyboard is pressed, goto BLACKEN
   @KBD
   D=M
   @BLACKEN
   D;JNE
   
   @WHITEN
   0;JMP

(BLACKEN)
   // Setting the variable fill to -1(1111111111111111)
   @fill
   M=-1
   
   @FILL
   0;JMP

(WHITEN)
   // Setting the variable fill to 0
   @fill
   M=0
   
   @FILL
   0;JMP
   
(FILL)
   // This sets the whole screen black, or white, according to fill's value
   
   // n = 8192
   @8192
   D=A
   @n
   M=D
   
   // initializing i = 0
   @i
   M=0
   
(LOOP)
   // addr is the variable which holds the exact adrees which we need to manipulate:
   // we add i to the screen's adress, while i ranges up until 8192, and stops there.

   // if i = n goto START
   @i
   D=M
   @n
   D=D-M
   @START
   D;JEQ
   
   // addr = SCREEN + i
   @SCREEN
   D=A
   @addr
   M=D
   @i
   D=D+M
   @addr
   M=D
   
   // RAM[addr] = fill
   @fill
   D=M
   @addr
   A=M
   M=D
   
   // i++
   @i
   M=M+1
   
   @LOOP
   0;JMP