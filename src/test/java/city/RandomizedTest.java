package city;

import java.util.ArrayList;
import java.util.List;
import java.util.Random;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class RandomizedTest {
    private String word(Random random, int length) {
        StringBuilder value = new StringBuilder();
        for (int i = 0; i < length; i++) value.append((char) ('a' + random.nextInt(3)));
        return value.toString();
    }
    @Test void hundredDistancePairsAgree() {
        Random random = new Random(20261108);
        for (int trial = 0; trial < 100; trial++) {
            String a = word(random, random.nextInt(7)), b = word(random, random.nextInt(7));
            int expected = new TableDistance().distance(a, b);
            assertEquals(expected, new RecursiveDistance().distance(a, b));
            assertEquals(expected, new TwoRowDistance().distance(a, b));
        }
    }
    @Test void hundredSearchPairsAgreeWithIndependentOracle() {
        Random random = new Random(42);
        for (int trial = 0; trial < 100; trial++) {
            String text = word(random, random.nextInt(100));
            String pattern = word(random, 1 + random.nextInt(12));
            List<Integer> expected = new ArrayList<>();
            for (int start = text.indexOf(pattern); start >= 0; start = text.indexOf(pattern, start + 1))
                expected.add(start);
            assertEquals(expected, new NaiveSearch().search(text, pattern));
            assertEquals(expected, new KmpSearch().search(text, pattern));
        }
    }
}
