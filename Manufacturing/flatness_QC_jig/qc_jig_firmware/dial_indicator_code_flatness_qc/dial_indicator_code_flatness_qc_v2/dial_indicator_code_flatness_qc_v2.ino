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

float data_out[5] = {9999,9999,9999,9999,9999};
float data_out_2[5] = {9999,9999,9999,9999,9999};

uint8_t state[5] = {255, 255, 255, 255, 255}; // 255 means it is not initialized
uint8_t currentSensor = 0;
uint8_t currentArray[5] = {0, 0, 0, 0, 0};
unsigned long time[5] = {0};

uint8_t printing = 0;

void loop()
{
  for (uint8_t i=0; i<5; i++){
    if (state[i] == 255){
      if (digitalRead(clock_pin_array[i]) == HIGH){
        //Serial.println("S255-H");
        time[i] = micros();
      }
      else if (micros()-time[i] > 1000*30){ // elapesd time since last high is more then 10ms
        state[i] = 0; 
      }
      else{
        //Serial.println("S255-L");
      }
    } else {
      if (state[i]%2 == 0){
        //Serial.println("S0-E");
        if (digitalRead(clock_pin_array[i]) == LOW){ //falling edge
          if (micros() - time[i] >= 100){
            bitWrite(data_in[i], state[i]/2, (!digitalRead(data_pin_array[i]) & 0x1));
            state[i]++;
            if (state[i] > 24*2){
              data_in[i] = data_in[i]>>1;
              if (((data_in[i]>>20) & 0b1) == 1){ // check sign bit
                if (currentArray[i] == 0){
                  data_out[i] = (data_in[i]&0x0fffff);// invert the output
                  data_out[i]*=-1;
                } else {
                  data_out_2[i] = (data_in[i]&0x0fffff);// invert the output
                  data_out_2[i]*=-1;
                }
              }
              else{
                if (currentArray[i] == 0){
                  data_out[i] = (data_in[i]&0x0fffff);
                } else {
                  data_out_2[i] = (data_in[i]&0x0fffff);
                }
              }
              data_in[i] = 0;
              state[i] = 0;
              currentArray[i]++;
              if (currentArray[i] == 2){
                currentArray[i] = 0;
              }
              // data ready
              //Serial.println(data_out[i]);
            }
          }
        } else {
          time[i] = micros();
        }
      } else{
        //Serial.println("S0-O");
        if (digitalRead(clock_pin_array[i]) == HIGH){ //raising edge
          state[i]++;
          time[i] = micros();
        }
      }
    }
  }
  int reading = digitalRead(buttonPin);

  // check to see if you just pressed the button
  // (i.e. the input went from LOW to HIGH), and you've waited long enough
  // since the last press to ignore any noise:

  // If the switch changed, due to noise or pressing:
  if (reading != lastButtonState) {
    // reset the debouncing timer
    lastDebounceTime = millis();
  }

  if ((millis() - lastDebounceTime) > debounceDelay) {
    // whatever the reading is at, it's been there for longer than the debounce
    // delay, so take it as the actual current state:

    // if the button state has changed:
    if (reading != buttonState) {
      buttonState = reading;

      // only toggle the LED if the new button state is HIGH
      if (state[0] == 255 || state[1] == 255 || state[2] == 255 || state[3] == 255 || state[4] == 255){
        buttonState = HIGH;
      }

      if (buttonState == LOW){
        printing = 1;
        }
    }
  }

  if (printing){
    uint8_t matching = 1;
    for (int i = 0; i < 5; i++){
      if (data_out[i] != data_out_2[i]){
        //matching = 0;
      }
    }
    
    float avg;
    //avg=(data_out[0]+data_out[1]+data_out[2]+data_out[3]+data_out[4])/5;
    avg=0;
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
    if (matching){
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
        Serial.print((data_out_avg[0])/100);
        Serial.print(",");
        Serial.print((data_out_avg[1])/100);
        Serial.print(",");
        Serial.print((data_out_avg[2])/100);
        Serial.print(",");
        Serial.print((data_out_avg[3])/100);
        Serial.print(",");
        Serial.print((data_out_avg[4])/100);
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
    }
  }


  // save the reading. Next time through the loop, it'll be the lastButtonState:
  lastButtonState = reading;

  if (false && micros()-time_of_last_print > 2000000UL) {
  // read the incoming byte:
    Serial.print(data_out[0]);
    Serial.print(" ");
    Serial.print(data_out[1]);
    Serial.print(" ");
    Serial.print(data_out[2]);
    Serial.print(" ");
    Serial.print(data_out[3]);
    Serial.print(" ");
    Serial.println(data_out[4]);

    state[0] = 255;
    state[1] = 255;
    state[2] = 255;
    state[3] = 255;
    state[4] = 255;

    time_of_last_print = micros();
  }
}
