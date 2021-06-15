// File name: Divide.asm
// Divides the numbers stored in RAM[13] and RAM[14]
// and store R13/R14 in RAM[15]


   @R15  // initialize answer to 0
   M=0
   
   @R1   
   M=0  // Initializing counter - counting until divisor >= divident
   
   @R2
   M=1  // this will be the temporary quotient

   @R13
   D=M
   @R3   // RAM[3] <-- temporary divident
   M=D
   
   @R14
   D=M
   @R4  // RAM[4] <-- temporary divisor
   M=D
   

(LOOP)
   // if R13(The divident) is smaller than R14(the divisor)
   // Then goto END (the division - R15, stays 0)

   @R3
   D=M
   @R4
   D=D-M

   @END  
   D;JLT  

(DIVIDE)
   @R3
   D=M
   @R4
   D=D-M
    
   // If the divident is smaller than the divisor goto IFNEGATIVE
   @IFNEGATIVE  
   D;JLE
   
   // Shifting the value of the divisor the the left <==> multiplying
   // the value by 2 <==> adding the value to it self
   @R4
   M=M<<  
   
   @R1
   M=M+1  
   
   @DIVIDE
   0;JMP

(IFNEGATIVE)
   @R1
   M=M-1
   D=M
   
   // if counter <= 0, add the temporary quotient R2
   // to the original quotient - R15
   @ADDQUOTIENT  
   D;JLE
   
   @R2
   M=M<<   // Shifting the value of the temporary quotient left
   
   @IFNEGATIVE
   0;JMP
   
(ADDQUOTIENT)
   @R4
   D=M>>
   @R3
   M=M-D  // Incrimating the divident by 2 x (divisor's current value)
   
   @R14
   D=M
   @R4
   M=D  // restore R3 to the original divisor's value
   
   @R2
   D=M
   @R15
   M=M+D  // add the temporary quotient to the original one (the answer - RAM[15])
   
   @R2
   M=1   // Initialize it back to 1
   
   @LOOP
   0;JMP

(END)  