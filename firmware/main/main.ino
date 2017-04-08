#include <stdint.h>
#include <string.h>
#include <stdio.h>

#define HANDSHAKE_OK 1
#define HANDSHAKE_LED 13

#define PACKET_SIZE 16
#define BAUDRATE 115200

char packet[PACKET_SIZE];
char strbuf[PACKET_SIZE];

char calculate_checksum(const char *packet) {
  char check = 0;
  for (int i = 0; i < PACKET_SIZE - 1; i++) {
    if (*(packet + i) % 2 == 0) {
      check++;
    }
  }
  return check;
}

const char *read_packet(char *buf) {
  for (int i = 0; true ;) {
    if (Serial.available()) {
      buf[i] = Serial.read();
      i++;
      if ( i > sizeof(packet) - 1) {
        return buf;
      }
    }
  }
  return NULL;
}

void write_packet(const char *data) {
  memset(packet, 0, sizeof(packet));
  memcpy(packet, data, strlen(data) + 1);
  packet[PACKET_SIZE - 1] = calculate_checksum(packet);
  for (int i = 0; i < sizeof(packet); i++) {
    Serial.write(packet[i]);
  }
}

uint8_t handshake() {
  write_packet("SYN");
  char *test = read_packet(packet);
  if (strcmp(test, "ACK") != 0) {
    write_packet("NAK");
    return handshake();
  }
  test = read_packet(packet);

  if (strcmp(test, "SYN") != 0) {
    write_packet("NAK");
    return handshake();
  }
  write_packet("ACK");

  digitalWrite(HANDSHAKE_LED, HIGH);
  return HANDSHAKE_OK;
}

void reset_board() {
  digitalWrite(HANDSHAKE_LED, LOW);
  asm volatile("jmp 0");
}

void setup() {
  Serial.begin(BAUDRATE);
  pinMode(HANDSHAKE_LED, OUTPUT);
  if (!handshake()) {
    reset_board();
  }
}

int analog_read(int pin) {
  pinMode(A0 + pin, INPUT);
  return analogRead(A0 + pin);
}

uint8_t test_command(char *buf, char *cmd, uint8_t lookup) {
  if (strncmp(buf, cmd, lookup) == 0) return 1;
  return 0;
}

void loop() {
  char *test = read_packet(strbuf);
  if (test_command(test, "GET ", 4)) {
    test += 4;
    int port = atoi(test);
    int read = analog_read(port);
    sprintf(strbuf, "%d", read);
    write_packet(strbuf);
  }
}

