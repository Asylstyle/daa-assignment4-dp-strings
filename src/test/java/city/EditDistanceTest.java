package city;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class EditDistanceTest {
    private EditDistance[] versions() {
        return new EditDistance[]{new RecursiveDistance(), new TableDistance(), new TwoRowDistance()};
    }
    @Test void referenceValuesAndEmptyStrings() {
        for (EditDistance algorithm : versions()) {
            assertEquals(3, algorithm.distance("kitten", "sitting"));
            assertEquals(2, algorithm.distance("flaw", "lawn"));
            assertEquals(5, algorithm.distance("intention", "execution"));
            assertEquals(3, algorithm.distance("", "abc"));
            assertEquals(3, algorithm.distance("abc", ""));
            assertEquals(0, algorithm.distance("abc", "abc"));
            assertEquals(0, algorithm.distance("", ""));
        }
    }
    @Test void countersResetAndStorageIsMeasured() {
        TableDistance table = new TableDistance();
        table.distance("abcd", "ef");
        assertEquals(8, table.counters().cells);
        assertEquals(15, table.counters().allocatedCells);
        table.distance("a", "b");
        assertEquals(1, table.counters().cells);
        TwoRowDistance rows = new TwoRowDistance();
        rows.distance("ab", "abcdef");
        assertEquals(6, rows.counters().allocatedCells);
    }
}
