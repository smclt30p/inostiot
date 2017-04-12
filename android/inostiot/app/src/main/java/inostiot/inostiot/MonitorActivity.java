package inostiot.inostiot;

import android.app.Activity;
import android.content.Intent;
import android.graphics.Color;
import android.os.AsyncTask;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;

import com.github.mikephil.charting.charts.LineChart;
import com.github.mikephil.charting.components.XAxis;
import com.github.mikephil.charting.components.YAxis;
import com.github.mikephil.charting.data.LineData;
import com.github.mikephil.charting.data.LineDataSet;

import java.util.ArrayList;
import java.util.Locale;

import inostiot.android.libardadc.adc.ADC;
import inostiot.android.libardadc.adc.ADCException;
import inostiot.android.libardadc.adc.ADCPort;
import inostiot.inostiot.graph.ColoredADCPort;
import inostiot.inostiot.graph.WalkingDataset;

public class MonitorActivity extends AppCompatActivity {

    private GraphWorker worker;

    @Override
    protected void onSaveInstanceState(Bundle outState) {
        worker.cancel(true);
        outState.putBundle("state", worker.prepareResume());
        outState.putBoolean("resuming", true);
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {

        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_monitor);

        Intent intent = getIntent();
        Bundle extras = intent.getExtras();
        String ip = extras.getString("ip");

        LineChart chart = (LineChart) findViewById(R.id.chart);

        XAxis x = chart.getXAxis();
        YAxis y = chart.getAxisLeft();
        YAxis y2 = chart.getAxisRight();

        x.setAxisMinimum(0);
        x.setAxisMaximum(9);
        y.setAxisMaximum(1024);
        y2.setAxisMaximum(1024);
        y.setAxisMinimum(0);
        y2.setAxisMaximum(0);

        if (savedInstanceState != null) {

            boolean resuming = savedInstanceState.getBoolean("resuming", false);

            if (resuming) {
                worker = new GraphWorker(this, ip, chart, true);
                worker.resume(savedInstanceState.getBundle("state"));
                worker.execute();
            }

        } else {
            worker = new GraphWorker(this, ip, chart, false);
            worker.execute();
        }
    }
}


class GraphWorker extends AsyncTask<Void, Object, Void> {

    private LineChart chart;
    private boolean resuming;
    private boolean running = true;
    private String ip;
    private Activity parent;

    private ArrayList<ADCPort> ports;
    private ArrayList<WalkingDataset> walkingDatasets;
    private ArrayList<LineDataSet> lineDataSets;

    GraphWorker(Activity parent, String ip, LineChart chart, boolean resuming) {

        this.parent = parent;

        if (!resuming) {
            ports = new ArrayList<>();
            walkingDatasets  = new ArrayList<>();
            this.ip = ip;
        }

        this.chart = chart;
        this.resuming = resuming;
        lineDataSets = new ArrayList<>();


    }

    @Override
    public Void doInBackground(Void...params) {

        ADC adc = new ADC(ip);

        if (!resuming) {

            if (!adc.auth()) throw new RuntimeException("Server invalid!");

            ports.add(new ColoredADCPort(0, "#FF0000"));
            walkingDatasets.add(new WalkingDataset(10));

            ports.add(new ColoredADCPort(1, "#00FF00"));
            walkingDatasets.add(new WalkingDataset(10));

            ports.add(new ColoredADCPort(2, "#FF00FF"));
            walkingDatasets.add(new WalkingDataset(10));

            ports.add(new ColoredADCPort(3, "#0000FF"));
            walkingDatasets.add(new WalkingDataset(10));

            ports.add(new ColoredADCPort(4, "#FFFF00"));
            walkingDatasets.add(new WalkingDataset(10));

            ports.add(new ColoredADCPort(5, "#00FFFF"));
            walkingDatasets.add(new WalkingDataset(10));

        }


        while (running) {

            try {

                ports = adc.readPorts(ports);
                publishProgress((Object)ports);

                try {
                    Thread.sleep(1000);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }

            } catch (ADCException e) {
                e.printStackTrace();
                break;
            }

        }

        return null;

    }

    void resume(Bundle data) {
        this.ports = (ArrayList<ADCPort>) data.getSerializable("ports");
        this.walkingDatasets = (ArrayList<WalkingDataset>) data.getSerializable("walkingDatasets");
        this.ip = data.getString("ip");
        this.chart.invalidate();
    }

    Bundle prepareResume() {
        Bundle data = new Bundle();
        data.putSerializable("ports", ports);
        data.putSerializable("walkingDatasets", walkingDatasets);
        data.putString("ip", ip);
        return data;
    }

    @Override
    protected void onProgressUpdate(Object... values) {

        ArrayList<ADCPort> ports = (ArrayList<ADCPort>) values[0];

        lineDataSets.clear();

        for (int i = 0; i < ports.size(); i++) {

            ColoredADCPort port = (ColoredADCPort) ports.get(i);
            WalkingDataset dataset = walkingDatasets.get(i);

            dataset.add(port.getValue());

            LineDataSet lineDataSet = new LineDataSet(dataset, String.format(Locale.ENGLISH, "Sensor %d", i));
            lineDataSet.setCircleColor(Color.parseColor(port.getColor()));
            lineDataSet.setColor(Color.parseColor(port.getColor()));
            lineDataSet.setDrawValues(false);

            lineDataSets.add(lineDataSet);

        }

        final LineData data = new LineData();

        for (LineDataSet set : lineDataSets) {
            data.addDataSet(set);
        }

        chart.setData(data);
        chart.postInvalidate();

        super.onProgressUpdate();
    }

    public void stopRunner() {
        this.running = false;
    }

}
