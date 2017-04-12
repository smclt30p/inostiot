package inostiot.inostiot;


import android.app.Activity;
import android.content.Intent;
import android.os.AsyncTask;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import inostiot.android.libardadc.adc.ADC;


public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        Button start = (Button) findViewById(R.id.start);
        final EditText ip = (EditText) findViewById(R.id.ip_address);


        start.setOnClickListener(new View.OnClickListener() {

            @Override
            public void onClick(View v) {
                runcheck(ip);
            }
        });

    }

    private void runcheck(EditText ip) {
        ServerCheckWorker worker = new ServerCheckWorker(this, ip.getText().toString());
        worker.execute();
    }
}

class ServerCheckWorker extends AsyncTask<Void, Void, Boolean> {

    private Activity parent;
    private String ip;

    public ServerCheckWorker(Activity parent, String ip) {
        this.parent = parent;
        this.ip = ip;
    }

    @Override
    protected Boolean doInBackground(Void... params) {
        ADC adc = new ADC(ip);
        return adc.auth();
    }

    @Override
    protected void onPostExecute(Boolean aBoolean) {
        if (aBoolean) {
            Intent i = new Intent("inost.iot.monitor");
            Bundle extras = new Bundle();
            extras.putString("ip", ip);
            i.putExtras(extras);
            parent.startActivity(i);
        } else {
            Toast.makeText(parent, "Server invalid!", Toast.LENGTH_LONG).show();
        }
    }
}
