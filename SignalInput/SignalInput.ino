#define CUTOFF 45
void setup() {
  Serial.begin(9600);
  pinMode(LED_BUILTIN, OUTPUT);
}

void loop() {
  int sensorValue = analogRead(A0);
  if (sensorValue > CUTOFF){
    digitalWrite(LED_BUILTIN, HIGH);
    Serial.println(sensorValue);
  } else {
    Serial.println(0);
    digitalWrite(LED_BUILTIN, LOW);
  }
  delay(10);   
}