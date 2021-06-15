// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)
   
   @R2
   M=0
   @R1
   D=M
   @END   
   D;JEQ   // if R1=0 goto END
   @R0
   D=M
   @END   
   D;JEQ   // if R0=0 goto END

   @R1
   D=M
   @n
   M=D    // n = R1
   @i
   M=1    // i = 1
   @R0
   D=M
   @mult
   M=D    // mult = R0
  
(LOOP)
   @i
   D=M
   @n
   D=D-M
   @STOP
   D;JGE  // if i >= n goto STOP
   
   @R0
   D=M
   @mult
   M=M+D  // Adding R0 to it self, R1 times
   @i
   M=M+1
   @LOOP
   0;JMP
   
(STOP)
   @mult
   D=M
   @R2
   M=D

(END)
   
   
   
   