package inostiot.android.libardadc.adc;

/**
 * Created by Ognjen Galić for InostIOT 2017
 */
public class ADCPort {

    private final int portNumber;
    private int value = -1;

    /**
     * Construct an object representing the port on the
     * ADC system. The max number of ports is 5 for
     * the Arduino Uno and 10 for the Arduino Mega
     * @param portNumber port number on the Arduino
     * @throws ADCException if the port is >5
     */
    public ADCPort(int portNumber) throws ADCException {
        if (portNumber > 5) {
            throw new ADCException();
        }
        this.portNumber = portNumber;
    }

    /**
     * Gets the port number that this object represents
     * on the ADC located on the Arduino
     * @return the object port number on the Arduini
     */
    public int getPortNumber() {
        return portNumber;
    }

    /**
     * Returns the last updated reading of the port with a
     * max resolution of 1024
     * @return the last updated reading of the port
     */
    public int getValue() {
        return value;
    }

    /**
     * Sets the value after updating with @ADC
     * @param value the value that @ADC puts in
     */
    public void setValue(int value) {
        this.value = value;
    }
}
