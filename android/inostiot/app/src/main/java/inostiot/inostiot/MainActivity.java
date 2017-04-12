package inostiot.inostiot;


import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;


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
                Intent i = new Intent("inost.iot.monitor");
                Bundle extras = new Bundle();
                extras.putString("ip", ip.getText().toString());
                i.putExtras(extras);
                startActivity(i);
            }
        });

    }
}
