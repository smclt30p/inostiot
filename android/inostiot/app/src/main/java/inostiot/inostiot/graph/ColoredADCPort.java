package inostiot.inostiot.graph;

import java.io.Serializable;

import inostiot.android.libardadc.adc.ADCPort;


public class ColoredADCPort extends ADCPort implements Serializable {

    private String color;

    public ColoredADCPort(int portNumber, String color) {
        super(portNumber);
        this.color = color;
    }

    public String getColor() {
        return color;
    }

    public void setColor(String color) {
        this.color = color;
    }
}
