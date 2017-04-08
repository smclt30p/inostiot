#include <stdint.h>
#include <string.h>
#include <stdio.h>

char packet[32];

#define HANDSHAKE_OK 1

char calculate_checksum(const char *packet) {
  char check = 0;
  for (int i = 0; i < 31; i++) {
    if (*(packet + i) % 2 == 0) {
      check++;
    }
  }
  return check;
}

const char *read_packet() {
  for (int i = 0; true ;) {
    if (Serial.available()) {
      packet[i] = Serial.read();
      i++;
      if ( i > sizeof(packet) - 1) {
        return packet;
      }
    }
  }
  return NULL;
}

void write_packet(const char *data) {
  memset(packet, 0, sizeof(packet));
  memcpy(packet, data, strlen(data) + 1);
  packet[31] = calculate_checksum(packet);
  for (int i = 0; i < sizeof(packet); i++) {
    Serial.write(packet[i]);
  }
}

uint8_t handshake() {
  write_packet("SYN");
  char *test = read_packet();
  if (strcmp(test, "ACK") != 0) {
    write_packet("NAK");
    return handshake();
  }
  test = read_packet();

  if (strcmp(test, "SYN") != 0) {
    write_packet("NAK");
    return handshake();
  }
  write_packet("ACK");

  return HANDSHAKE_OK;
}

void setup() {
  Serial.begin(9600);
  handshake();
}

void loop() {

}
