const int pot_num = 2;

// A0: Stearing Wheel
// A1: Accelerator
const int potPins[pot_num] = {A0, A1};



// Exponential Moving Average
const int brake = 3;

struct EMA {
  float alpha;
  float filterValue;
};

EMA filters[pot_num];

void initFilters() {
  for (int i = 0; i < pot_num; i++) {
    filters[i].alpha = 0.3;
    filters[i].filterValue = analogRead(potPins[i]);
  }
}

float updateFilterValue(int index) {
  float currentValue = (float)analogRead(potPins[index]);
  filters[index].filterValue = (filters[index].alpha * currentValue) +
                                  ((1 - filters[index].alpha) * filters[index].filterValue);
  return filters[index].filterValue;
}

void setup() {
    Serial.begin(9600);
    pinMode(brake, INPUT_PULLUP);
    initFilters();

}

void loop() {
    // filter analogic values
    for (int i = 0; i < pot_num; i++) {
      float filterValue = updateFilterValue(i);
    }
    
    int steeringWheelState = (int)filters[0].filterValue;
    int aceleratorState = filters[1].filterValue;
    int brakeState = !digitalRead(brake);


    Serial.print(steeringWheelState);
    Serial.print(";");
    Serial.print(aceleratorState);
    Serial.print(";");
    Serial.print(brakeState);
    Serial.print("\n");

    delay(40);
}
