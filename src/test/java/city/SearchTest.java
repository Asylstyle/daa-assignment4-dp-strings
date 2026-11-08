package city;

import java.util.List;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class SearchTest {
    @Test void referencesAndOverlaps() {
        for (StringSearch search : new StringSearch[]{new NaiveSearch(), new KmpSearch()}) {
            assertEquals(List.of(10), search.search("ABABDABACDABABCABAB", "ABABCABAB"));
            assertEquals(List.of(0,1,2,3), search.search("AAAAA", "AA"));
            assertEquals(List.of(0,2,4), search.search("ABABABA", "ABA"));
            assertEquals(List.of(), search.search("abc", "z"));
            assertEquals(List.of(), search.search("a", "abc"));
            assertEquals(List.of(), search.search("", "a"));
            assertThrows(IllegalArgumentException.class, () -> search.search("abc", ""));
            assertThrows(IllegalArgumentException.class, () -> search.search("", ""));
        }
    }
    @Test void countsActualComparisonsIncludingPreprocessing() {
        NaiveSearch naive = new NaiveSearch();
        naive.search("AAAAA", "AAB");
        assertEquals(9, naive.counters().comparisons);
        KmpSearch kmp = new KmpSearch();
        kmp.search("AAAAA", "AAB");
        assertEquals(8, kmp.counters().comparisons);
        assertEquals(3, kmp.counters().lpsComparisons);
    }
}
