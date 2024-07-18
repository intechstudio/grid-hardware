int data_pin_array[5] = { 12, 10, 8, 6, 4 };
int clock_pin_array[5] = { 11, 9, 7, 5, 3 };
int readChar;

const int buttonPin = 2;

int buttonState = 0;
int lastButtonState = HIGH;
unsigned long lastDebounceTime = 0; // the last time the output pin was toggled
unsigned long debounceDelay = 50; // the debounce time; increase if the output flickers

unsigned long time_of_last_print = 0;
void setup()
{
  
  pinMode(buttonPin, INPUT_PULLUP);
  Serial.begin(2000000);
  Serial.println("Jig Started!");

  for (int i = 0; i<5; i++){

    pinMode(clock_pin_array[i], INPUT_PULLUP);
    pinMode(data_pin_array[i], INPUT_PULLUP);

  }

  time_of_last_print = micros();
}

uint32_t data_in[5] = {0};

int32_t data_out[5] = {9999,9999,9999,9999,9999};

uint8_t state[5] = {255, 255, 255, 255, 255}; // 255 means it is not initialized
uint8_t currentSensor = 0;
unsigned long time[5] = {0};

uint8_t printing = 0;

uint8_t active_index = 0;

void loop()
{

  uint8_t i = active_index;
    
  if (state[i] == 255){
    if (digitalRead(clock_pin_array[i]) == HIGH){
      //Serial.println("S255-H");
      time[i] = micros();
    }
    else if (micros()-time[i] > 1000*10){ // elapesd time since last high is more then 10ms
      state[i] = 0; 
    }
    else{
      //Serial.println("S255-L");
    }
  } else if (state[i] != 254) {
    
    if (state[i]%2 == 0){
      //Serial.println("S0-E");
      if (digitalRead(clock_pin_array[i]) == LOW && (micros()-time[i] > 100)){ //falling edge

        time[i] = micros();
        bitWrite(data_in[i], state[i]/2, (!digitalRead(data_pin_array[i]) & 0x1));
        state[i]++;
        if (state[i] > 24*2){
          data_in[i] = data_in[i]>>1;
          if (((data_in[i]>>20) & 0b1) == 1){ // check sign bit
            data_out[i] = (data_in[i]&0x0fffff);// invert the output
            data_out[i]*=-1;
          }
          else{
            data_out[i] = (data_in[i]&0x0fffff);
          }
          data_in[i] = 0;
          state[i] = 254;
          
          // data ready
          //Serial.print(i);
          //Serial.print(":");
          //Serial.println(data_out[i]);
          //Serial.flush();
          
          active_index = (active_index+1)%5;

        }
        
      }
    } else{
      //Serial.println("S0-O");
      if (digitalRead(clock_pin_array[i]) == HIGH && (micros()-time[i] > 400)){ //raising edge
        time[i] = micros();
        state[i]++;
      }
    }
  }


  if (state[0] == 254 && state[1] == 254 && state[2] == 254 && state[3] == 254 && state[4] == 254){

    float avg;
    avg=(data_out[0]+data_out[1]+data_out[2]+data_out[3]+data_out[4])/5;

    float data_out_avg[5] = {9999,9999,9999,9999,9999};
    data_out_avg[0]=data_out[0]-avg;
    data_out_avg[1]=data_out[1]-avg;
    data_out_avg[2]=data_out[2]-avg;
    data_out_avg[3]=data_out[3]-avg;
    data_out_avg[4]=data_out[4]-avg;
    int result_status = 0;
    int i, j, k;
    i=0;
    j=0;
    k=0;
    while (i<5){
      if (data_out_avg[i]>50){
        j++;
      }
      if (data_out_avg[i]>150 || data_out_avg[i]<-150 ){
        k++;
      }
      i++;
    }
    if (k>0) {
      result_status = 2;
    } else {
      if (j>0) {
        result_status = 1;
      } else {
        result_status = 0;
      }
    } 

      //readChar = Serial.read();
        //avg=0;
        /*Serial.print((data_out[0])/100);
        Serial.print(",");
        Serial.print((data_out[1])/100);
        Serial.print(",");
        Serial.print((data_out[2])/100);
        Serial.print(",");
        Serial.print((data_out[3])/100);
        Serial.print(",");
        Serial.print((data_out[4])/100);
        Serial.print(",");
        Serial.println(avg/100);*/
        Serial.print((data_out[0]));
        Serial.print(",");
        Serial.print((data_out[1]));
        Serial.print(",");
        Serial.print((data_out[2]));
        Serial.print(",");
        Serial.print((data_out[3]));
        Serial.print(",");
        Serial.print((data_out[4]));
        Serial.print(",");

        /*if (k>0) {
          Serial.println("INVALID MEASUREMENT");
        } else {*/
          if (result_status) {
            Serial.println("FAIL");
          } else {
            Serial.println("PASS");
          }
        //} 
        state[0] = 255;
        state[1] = 255;
        state[2] = 255;
        state[3] = 255;
        state[4] = 255;
        time[0] = 0;
        time[1] = 0;
        time[2] = 0;
        time[3] = 0;
        time[4] = 0;
        printing = 0;
        active_index=0;

        Serial.flush();
    
  }
}
