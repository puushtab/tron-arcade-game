void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  int mesureX = analogRead(A0);
  int mesureY = analogRead(A1);
  Serial.print(mesureX);
  Serial.print(" ");
  Serial.println(mesureY);
  delay(20);
}
