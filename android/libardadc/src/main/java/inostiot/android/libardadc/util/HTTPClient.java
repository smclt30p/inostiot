package inostiot.android.libardadc.util;

import okhttp3.OkHttpClient;

/**
 * A HTTP client based around OkHttp3, that supports
 * connection pooling.
 */
public abstract class HTTPClient {

    private static OkHttpClient client;

    /**
     * Get the HTTP client singleton
     * @return The OkHttp client singleton
     */
    public static OkHttpClient getHttpClient() {
        if (HTTPClient.client == null) {
            HTTPClient.client = new OkHttpClient();
        }
        return HTTPClient.client;
    }


}
