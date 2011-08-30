/*
  KnitterKey
  Types on the matrix keyboard of a Brother Electroknit KH930.
   
  You may use this code for anything you damned well please, so
  long as it's neighborly and--given the opportunity--you share a
  beer or Club Mate with Travis Goodspeed.
  
  Each of the digital I/O pins should be connected to the bases of
  the column 547 NPN transistors through 1.2K resistors.  The analog I/O
  pins should be connected to the row transistors in a similar manner.
  Collectors should face the row side, while emitters face the column side.
  The emitters of the row transistors should connect to the collectors of
  the column transistors.
  
  N.B., that this code was written as a quick and dirty hack.  Like all
  such hacks, you're probably better off rewriting it than trying to adapt
  it to your needs.
 */
 
//Configurations stuff:
#define default_track 1
#define default_pattern 903
#define default_offset -1


//! Presses a key by its code.  Use keypress() instead.
void key(int row, int col){
  int rows[4]={A0, A1, A2, A3};
  
  digitalWrite(rows[row], HIGH);
  digitalWrite(col, HIGH);
  delay(500);
  letoff();
  delay(500);
}

//! Clears the input.
void letoff(){
  digitalWrite(A0, LOW);
  digitalWrite(A1, LOW);
  digitalWrite(A2, LOW);
  digitalWrite(A3, LOW);
  for(int i=0;i<10;i++)
    digitalWrite(i, LOW);
}

#define C 0x80
#define CR 0x81
#define CE 0x82
#define STEP 0x83
#define VAR1 0x84
#define VAR2 0x85
#define VAR3 0x86
#define VAR4 0x87
#define VAR5 0x88
#define VAR6 0x89
#define KHC 0x89
#define VAR7 0x8A
#define KRC 0x8A

#define CHECK 0x8B
#define MEMO 0x8C
#define INPT 0x8D
#define LEFT 0x8E
#define RIGHT 0x8F
#define SOUND 0x90
#define BLACKSQUARE 0x91
#define WHITESQUARE 0x92
#define M 'M'
#define START 0x93
#define SEL1 0x94
#define SEL2 0x95
#define S 'S'
#define R 'R'
#define YELLOW 0x96
#define GREEN 0x97

//! keypress
void keypress(char c){
  switch(c){
  case C:
    key(1,1);
    break;
  case CR:
    key(1,8); //CR
    break;
  case CE:
    key(1,7); //CE
    break;
  case 1: case '1':
    key(0,8); //1
    break;
  case 2: case '2':
    key(0,7); //2
    break;
  case 3: case '3':
    key(0,6); //3
    break;
  case 4: case '4':
    key(0,5);
    break;
  case 5: case '5':
    key(0,4);
    break;
  case 6: case '6':
    key(0,3);
    break;
  case 7: case '7':
    key(0,2);
    break;
  case 8: case '8':
    key(0,1);
    break;
  case 9: case '9':
    key(0,0);
    break;
  case 0: case '0':
    key(0,9);
    break;
  case STEP:
    key(1,9);
    break;
  case VAR1:
    key(3,9);
    break;
  case VAR2:
    key(3,8);
    break;
  case VAR3:
    key(3,6);
    break;
  case VAR4:
    key(3,5);
    break;
  case VAR5:
    key(3,7);
    break;
  case VAR6: //case KHC:
    key(3,4);
    break;
  case VAR7: //case KRC:
    key(3,3);
    break;
  case CHECK:
    key(2,8);
    break;
  case MEMO:
    key(2,6);
    break;
  case INPT:
    key(2,9);
    break;
  case LEFT:
    key(2,1);
    break;
  case RIGHT:
    key(2,2);
    break;
  case SOUND:
    key(2,7);
    break;
  case BLACKSQUARE:
    key(2,3);
    break;
  case WHITESQUARE:
    key(2,4);
    break;
  case M:
    key(1,2);
    break;
  case START:
    key(3,0);
    break;
  case SEL1:
    key(1,0);
    break;
  case SEL2:
    key(2,0);
    break;
  case 'S':
    key(3,1);
    break;
  case 'R':
    key(3,2);
    break;
  case YELLOW:
    key(1,6);
    break;
  case GREEN:
    key(1,5);
    break;
  }
}

//! Tries all numbers to test keyboard.
void selftest(){
  keypress(CE);
  typeint(123);
  keypress(CE);
  typeint(456);
  keypress(CE);
  typeint(789);
  keypress(CE);
  typeint(101);
  keypress(CE);
  
}

//! Loads a track of data from the floppy disk.
void loaddisk(int track){
  //Now load file from disk.
  //Track should probably be 1.
  keypress(CE);
  typeint(551);
  delay(1000); //none
  keypress(STEP);
  delay(2000);
  keypress(track);
  keypress(STEP);
  delay(10000);
  
  //while(1);
}

void typeint(int number){
  int
    hundreds=(number/100)%10,
    tens=(number/10)%10,
    ones=number%10;
   keypress(hundreds);
   keypress(tens);
   keypress(ones);
   delay(1000);
}

void printpattern(int pattern, int offset){
  //Custom patterns begin at 0x900 in BCD.
  //Offset is positive for green, negative for yellow.
  //Offsets of more than 9 will cause trouble.
  
  //keypress(KHC);  //For the love of god, start with this on.
  keypress(CE);
  keypress(STEP);//delay(1000);
  keypress(STEP);//delay(1000);
  keypress(CE);//delay(1000);
  
  typeint(pattern);
  
  keypress(STEP);
  delay(1000);
  
  //Do the offset.
  keypress(CE);
  if(offset>=0){
    keypress(GREEN);
    typeint(offset);
  }else{
    keypress(YELLOW);
    typeint(abs(offset));
  }
  
  keypress(STEP);
  delay(1000);
  
  while(1);
}

void setup() {                
  // initialize the digital pin as an output.
  // Pin 13 has an LED connected on most Arduino boards:
  pinMode(13, OUTPUT);     
  
  pinMode(A0, OUTPUT);
  pinMode(A1, OUTPUT);
  pinMode(A2, OUTPUT);
  pinMode(A3, OUTPUT);
  
  for(int i=0;i<10;i++)
    pinMode(i, OUTPUT);
  
  letoff();
  
  digitalWrite(13, HIGH);   // set the LED on
  //Startup delay in case we're just being plugged in.
  
  //delay(1000);
  //selftest();
  delay(3000);
  
  //Load a pattern from the emulated disk.
  loaddisk(default_track);
  
  //Set up pattern 903 centered at 1 yellow.
  printpattern(default_pattern,default_offset);
  digitalWrite(13, LOW);   // cut the LED to show that we're ready to print
}

//! Main loop.
void loop() {
  //Everything is done in setup() after a reset.
  //This loop only exists for the hell of it.
  
  digitalWrite(13, LOW);    // set the LED off
  delay(1000);
  
  digitalWrite(13, HIGH);   // set the LED on
  delay(1000);
}



