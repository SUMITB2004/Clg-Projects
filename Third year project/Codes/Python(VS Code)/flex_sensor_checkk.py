#define FLEX_PIN 34

int threshold = 2500;   // adjust this
bool isPressed = false;

void setup() {
  Serial.begin(115200);
}

void loop() {
  int value = analogRead(FLEX_PIN);
  Serial.println(value);

  // Detect bend (press)
  if (value > threshold && !isPressed) {
    Serial.println("CLICK");
    isPressed = true;
    delay(300);  // debounce
  }

  // Detect release
  if (value < threshold - 200) {
    isPressed = false;
  }

  delay(50);
}