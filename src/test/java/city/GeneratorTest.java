package city;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class GeneratorTest {
    @Test void seedAndShapesAreStable() {
        assertEquals(InputGenerator.edit("random", 32), InputGenerator.edit("random", 32));
        assertEquals(InputGenerator.search("random", 1024), InputGenerator.search("random", 1024));
        var pair = InputGenerator.search("late_mismatch", 1024);
        assertEquals(1024, pair.first().length());
        assertEquals(64, pair.second().length());
        assertEquals('B', pair.second().charAt(63));
        assertThrows(IllegalArgumentException.class, () -> InputGenerator.edit("typo", 4));
    }
}
