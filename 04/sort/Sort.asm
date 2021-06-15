// File name: Sort.asm

// Sorts the array starting at the adress in RAM[14]
// with length as specified in RAM[15], in a descending
// order.

// Explanation: I used the Bubble sort algorithm, as recommended.

   @R15
   D=M
   @length
   M=D   // length = RAM[15]

(OUTERLOOP)   
   @1 
   D=A
   @length
   D=D-M
   @END
   D;JEQ  // if length = 1, goto END (Because then, the array is sorted - only 1 item)
   
   @i   // set the counter of inner loop to 0
   M=0
   @j
   M=1
   
(INNERLOOP)
   @length
   D=M
   @j
   D=D-M  
   
   @INCLENGTH  // if j = length , increment the length value by 1 (goto INCLENGTH)
   D;JEQ
   
   @i
   D=M
   @R14
   A=M+D
   D=M
   @R0
   M=D   // R0 <-- RAM[R14 + i]
   
   @j
   D=M
   @R14
   A=M+D
   D=M
   @R1
   M=D  // R1 <-- RAM[R14 + j]
   
   @R0
   D=M
   @R1
   D=D-M
   
   @SWAP
   D;JLT  // Swap a[i] and a[j](=a[i+1]) if a[i] < a[j]
   
   @NEXT  // Increment i and j
   0;JMP
   
(SWAP)
   @R1
   D=M
   @temp
   M=D   // temp = RAM[1]
   
   @R0
   D=M
   @R1
   M=D   // RAM[1] = RAM[0]
   
   @temp
   D=M
   @R0
   M=D   // RAM[0] = temp
   
   // We then assign the swapped values - R0 and R1 to RAM[R14 + i] and RAM[R14 + j]
   
   @i
   D=M
   @R14
   A=M+D
   D=A
   @R2
   M=D  // assert adress of a[i] to R2
   
   @j
   D=M
   @R14
   A=M+D
   D=A
   @R3
   M=D  // assert adress of a[j] to R3
   
   @R0
   D=M
   @R2
   A=M
   M=D // RAM[R2] = RAM[0] <==> RAM[R14 + i] = RAM[0]
   
   @R1
   D=M
   @R3
   A=M
   M=D  // RAM[R3] = RAM[1] <==> RAM[R14 + j] = RAM[1]
   
(NEXT)
   @i
   M=M+1
   @j
   M=M+1
   @INNERLOOP
   0;JMP
   
(INCLENGTH)
   @length
   M=M-1
   @OUTERLOOP
   0;JMP
   
(END)


   
   
   
   
   
   
   
  

   
   
   
   
   

   