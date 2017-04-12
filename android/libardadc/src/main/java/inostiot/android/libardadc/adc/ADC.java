package inostiot.android.libardadc.adc;

import inostiot.android.libardadc.util.HTTPClient;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.Response;
import org.json.JSONArray;
import org.json.JSONObject;

import java.io.IOException;
import java.util.ArrayList;

/**
 * A client for the ADC server written for Inost 2017.
 * The server is running on a Rapsberry Pi with an Arduino
 * connected as the ADC converter, and it servers the data
 * over a REST server.
 */
public class ADC implements ADCSensor {

    private final String serverIp;
    private static final String VERSION_ENDPOINT = "http://%s/api?version";
    private static final String PORT_ENDPOINT = "http://%s/api?ports=%s";

    /**
     * Construct a new ADC client with the REST
     * server located at the specified address
     * @param serverIp the ADC server address
     */
    public ADC(String serverIp) {
        this.serverIp = serverIp;
    }

    /**
     * Do a test-auth request to the server to verify that
     * it indeed is the ADC server.
     * @return if the server is sane
     */
    public boolean auth() {

        OkHttpClient client = HTTPClient.getHttpClient();

        Request request = new Request.Builder()
                .url(String.format(VERSION_ENDPOINT, this.serverIp))
                .build();

        try {

            Response response = client.newCall(request).execute();

            if (response.code() != 200) {
                return false;
            }

            JSONObject object = new JSONObject(response.body().string());
            String status = object.getString("status");
            if (status.equals("OK")) return true;

        } catch (IOException e) {
            e.printStackTrace();
            return false;
        }

        return false;
    }

    /**
     * Reads the ADC analog ports and updates the
     * objects with the values
     * @param ports Array of ADCPorts to be read
     * @return Returns the updated ports
     */
    @Override
    public ArrayList<ADCPort> readPorts(ArrayList<ADCPort> ports) throws ADCException {

        StringBuilder requestParameter = new StringBuilder();

        for (int i = 0; i < ports.size(); i++) {
            if (i == ports.size() - 1)
                requestParameter.append(String.format("%s",Integer.toString(ports.get(i).getPortNumber())));
            else
                requestParameter.append(String.format("%s,",Integer.toString(ports.get(i).getPortNumber())));
        }

        String url = String.format(PORT_ENDPOINT, this.serverIp, requestParameter.toString());

        OkHttpClient client = HTTPClient.getHttpClient();
        Request request = new Request.Builder()
                .url(url)
                .build();

        try {

            Response response = client.newCall(request).execute();

            if (response.code() != 200) {
                throw new ADCException("HTTP Response invalid!");
            }

            JSONObject object = new JSONObject(response.body().string());
            if (!object.getString("status").equals("OK")) {
                throw new ADCException("Invalid status code!");
            }

            JSONArray data = object.getJSONArray("rdata");

            for (int i = 0; i < data.length(); i++) {
                ports.get(i).setValue(data.getJSONObject(i).getInt("value"));
            }

            return ports;

        } catch (Exception e) {
            throw new ADCException(e);
        }

    }

}
