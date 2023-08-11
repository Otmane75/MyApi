uint8_t* hexStringToBytes(const char* hexString) {

  // Calculer la longueur du tableau
  int len = strlen(hexString);
  len = len / 2;
  
  // Allouer le tableau
  uint8_t* bytes = (uint8_t*) malloc(len);

  // Convertir chaque paire d'hex en uint8_t
  int j = 0;
  for (int i = 0; i < strlen(hexString); i+=2) {
    char buf[3];
    buf[0] = hexString[i];
    buf[1] = hexString[i+1];
    buf[2] = 0;
    
    bytes[j] = strtoul(buf, NULL, 16);
    j++;
  }

  return bytes;
}

void setup() {

  // Exemple
  const char* hex = "01AB4590";
  
  uint8_t* values = hexStringToBytes(hex);

  // Afficher le tableau
  for(int i=0; i<4; i++) {
    Serial.print(values[i]);
    Serial.print(" "); 
  }

}
