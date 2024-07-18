
int data_pin_array[5] = { 12, 10, 8, 6, 4 };
int clock_pin_array[5] = { 11, 9, 7, 5, 3 };
uint8_t active_index = 0;
const int buttonPin = 2;


#define Resolution 100
#define UARTBaudRate 2000000
#define ADC_Threshold 0.5

#define DATA_BITS_LEN 24
#define INCH_BIT 23
#define SIGN_BIT 20
#define START_BIT -1 // -1 - no start bit

// data capture and decode functions
bool getRawBit() {
    bool data;
    while (digitalRead(clock_pin_array[active_index]) < ADC_Threshold)
        ;
    while (digitalRead(clock_pin_array[active_index]) > ADC_Threshold)
        ;
    data = digitalRead(data_pin_array[active_index]) < ADC_Threshold;
    return data;
}

long getRawData() {
    long out = 0;
    for (int i = 0; i < DATA_BITS_LEN; i++) {
        out |= getRawBit() ? 1L << DATA_BITS_LEN : 0L;
        out >>= 1;
    }
    return out;
}

long getValue(bool &inch) {

    unsigned long time = micros();

    while(1){
      if (digitalRead(clock_pin_array[active_index]) == HIGH){
        //Serial.println("S255-H");
        time = micros();
      }
      else if (micros()-time > 1000*10){ // elapesd time since last high is more then 10ms
        break;
      }
    }


  
    long out = getRawData();
    inch = out & (1L << INCH_BIT);
    bool sign = out & (1L << SIGN_BIT);
    out &= (1L << SIGN_BIT) - 1L;
    out >>= (START_BIT+1);
    if (sign)
        out = -out;
    return out;
}

// printing functions
void printBits(long v) {
    char buf[DATA_BITS_LEN + 1];
    for (int i = DATA_BITS_LEN - 1; i >= 0; i--) {
        buf[i] = v & 1 ? '1' : '0';
        v >>= 1;
    }
    buf[DATA_BITS_LEN] = 0;
    Serial.print(buf);
}

void prettyPrintValue(long value, bool inch) {
    double v = value;
#if Resolution == 100
    if (inch) {
        Serial.print(v / 2000, 4);
        Serial.print(" in");
    } else {
        Serial.print(v / 100, 2);
        Serial.print(" mm");
    }
#else
    if (inch) {
        Serial.print(v / 20000, 5);
        Serial.print(" in");
    } else {
        Serial.print(v / 1000, 3);
        Serial.print(" mm");
    }
#endif
}

void toggleLed() {
#ifdef LedPin
  static bool state = false;
  state = !state;
  digitalWrite(LedPin, state);
#endif
}

// Arduino setup and main loop

// defines for setting and clearing register bits
#ifndef cbi
#define cbi(sfr, bit) (_SFR_BYTE(sfr) &= ~_BV(bit))
#endif
#ifndef sbi
#define sbi(sfr, bit) (_SFR_BYTE(sfr) |= _BV(bit))
#endif

void setup() {


    pinMode(buttonPin, INPUT_PULLUP);
    
    for (int i = 0; i<5; i++){
  
      pinMode(clock_pin_array[i], INPUT_PULLUP);
      pinMode(data_pin_array[i], INPUT_PULLUP);
  
    }

    Serial.begin(UARTBaudRate);
    Serial.println("Jig started!");

}


void loop() {

    while(digitalRead(buttonPin)) {};

    int32_t data_out[5] = {0};
  
    bool inch;
    long value;
  
    for (int i = 0; i<5; i++){
      active_index = i;

      data_out[active_index] = getValue(inch)*10;
  
    }
        

    int32_t average = 0;
    for (int i = 0; i<5; i++){    
      average += data_out[i];
      Serial.print(data_out[i]/1000.0);
      Serial.print(", ");
  
    }
    average/=5;
    Serial.print("    ");
    for (int i = 0; i<5; i++){    
      Serial.print((data_out[i]-average)/1000.0);
      Serial.print(", ");
  
    }

    Serial.print("    ");
    // decide the result 
    
    int result_status = 0;
    
    int problem_count=0;
    for (int i=0; i<5; i++){
      if (data_out[i]-average>500 || data_out[i]-average<-1000 ){
        problem_count++;
      }
    }
    
    if (problem_count>0) {
      result_status = 1;
    } else {
      result_status = 0;
    } 
    
   if (result_status==0) {
      Serial.println("PASS");
    } else {
      Serial.println("FAIL");
    }

    Serial.flush();
    delay(100);
}
