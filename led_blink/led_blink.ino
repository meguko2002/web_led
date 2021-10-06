const int LED_PIN = 27;
void setup() {
  pinMode(LED_PIN, OUTPUT);
  Serial.begin(115200);
}

void loop() {
  static int led_state = 0;
  if (Serial.available()) {
    int byte_from_py = Serial.read();
    if (byte_from_py == 0)led_state = 0;
    else if (byte_from_py == 1)led_state = 1;
    Serial.write(led_state);
//    Serial.print(led_state);
  }
  digitalWrite(LED_PIN, led_state);
}
