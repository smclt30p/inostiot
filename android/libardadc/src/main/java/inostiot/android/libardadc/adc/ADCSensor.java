package inostiot.android.libardadc.adc;

import java.util.ArrayList;

/**
 * Represents a system for reading ports on the
 * ADC server
 */
public interface ADCSensor {
    ArrayList<ADCPort> readPorts(ArrayList<ADCPort> ports) throws ADCException;
}
