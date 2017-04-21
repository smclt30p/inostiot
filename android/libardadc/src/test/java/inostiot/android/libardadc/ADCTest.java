package inostiot.android.libardadc;

import inostiot.android.libardadc.adc.ADCPort;
import inostiot.android.libardadc.adc.ADC;
import org.junit.Test;

import java.util.ArrayList;

import static org.junit.Assert.*;

/**
 * Created by Ognjen Galić for InostIOT 2017
 */
public class ADCTest {

    private ADC adc = new ADC("192.168.1.199");

    @Test
    public void auth() throws Exception {
        assertTrue(adc.auth());
    }

    /**
     * This may fail due to ADC hysteresis! Beware!
     */
    @Test
    public void analogRead() throws Exception {

        ArrayList<ADCPort> ports = new ArrayList<>();
        ports.add(new ADCPort(1));
        ports.add(new ADCPort(2));
        ports = adc.readPorts(ports);
        assertEquals(1023, ports.get(0).getValue());

    }

}