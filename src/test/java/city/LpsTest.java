package city;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class LpsTest {
    @Test void referenceArrays() {
        KmpSearch kmp = new KmpSearch();
        assertArrayEquals(new int[]{0,1,2,0,1,2,3,3}, kmp.lps("AAACAAAA"));
        assertArrayEquals(new int[]{0,0,1,2,0,1,2,3,4}, kmp.lps("ABABCABAB"));
        assertArrayEquals(new int[0], kmp.lps(""));
        assertArrayEquals(new int[]{0,1,2,3}, kmp.lps("AAAA"));
    }
}
