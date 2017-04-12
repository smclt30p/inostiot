package inostiot.inostiot.graph;

import com.github.mikephil.charting.data.Entry;

import java.util.ArrayList;


public class WalkingDataset extends ArrayList<Entry> {

    private int max = 0;
    private int currX = 0;

    public WalkingDataset(int max) {
        this.max = max;
    }

    // @Override
    public void add(int entry) {

        if (this.size() >= max + 1) {
            this.remove(0);
            for (int i = 0; i < this.size(); i++) {
                this.get(i).setX(i);
            }
        }

        super.add(new LineEntry(currX, entry));
        currX++;

    }

}

class LineEntry extends Entry {
    LineEntry(float x, float y) {
        super(x, y);
    }
}
