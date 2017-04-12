package inostiot.android.libardadc.adc;

import java.io.IOException;

/**
 * Created by Ognjen Galić for InostIOT 2017
 */
public class ADCException extends Exception {
    ADCException(Exception e) { super(e); }
    ADCException(String s) { super(s); }
    ADCException() { super(); }
}
