"""Build the four-page report and its Markdown companion from shared content."""
import csv
import platform
import textwrap
from pathlib import Path
from statistics import median
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.image import imread
from matplotlib.font_manager import FontProperties

ROOT = Path(__file__).resolve().parents[1]
DATA = list(csv.DictReader((ROOT / 'results/results.csv').open()))

def selected(algorithm, kind, n):
    return [r for r in DATA if (r['algorithm'], r['input'], int(r['n'])) == (algorithm, kind, n)]

def timing(algorithm, kind, n):
    return median(float(r['time_ms']) for r in selected(algorithm, kind, n))

CARD = [
    ('Questions', 'Edit: does DP remove repeated work, and how much storage do two rows save? Search: how much work does KMP avoid on late mismatches?'),
    ('Sizes', 'Edit, all versions: 2, 4, 6, 8; iterative versions also 64, 128, 256, 512, 1024. Search: 1024, 2048, 4096, 8192; pattern m=n/16. Each algorithm spans at least four sizes and a fourfold range.'),
    ('Inputs', 'Edit: equal A^n / A^n (best recursive path), disjoint A^n / B^n (full branching), seeded random over A-D. Search: B^n / A^m (early mismatch), A^n / A^(m-1)B (late mismatch, naive worst case), seeded random over A-D.'),
    ('Metrics', 'Count recursive calls, interior DP cells, allocated DP integer slots, and character comparisons inside algorithms. Search work includes LPS comparisons. Record five individual times and plot the median.'),
    ('Predictions', 'Disjoint recursion grows exponentially, equal recursion linearly. Both DP versions do n squared cell updates; two rows use linear storage. Naive late-mismatch search grows quadratically because m grows with n; KMP stays linear.'),
    ('Planned plots', 'Common-size edit work (log y), DP storage (log y), total search comparisons (log y), median edit and search timings (log y). Each chart answers one growth or resource question.'),
]
METHOD = ('The design was committed before the first experiment (docs/EXPERIMENT_DESIGN.md); no post-run design changes were made. '
          'Seed 20261108 fixes inputs, answers and counters, but cannot fix wall-clock time. Each case has five untimed warmups, '
          'then five measured invocations with counters enabled; search timing includes LPS construction. '
          'There are 450 measured rows. JVM warmup is modest rather than a full JMH study. '
          'Java 25.0.2 runs Java-17-targeted classes on Windows amd64. The recursive cap of 8 is a chosen budget, not a measured hardware maximum.')
EDIT = (f'Disjoint recursion reaches 398,593 calls at n=8, whereas each DP version evaluates 64 cells. '
        f'At n=1024, both iterative versions evaluate 1,048,576 cells. The full table allocates 1,050,625 integer slots; '
        f'two rows allocate 2,050, a 512.5-fold reduction. Their disjoint median times are '
        f'{timing("table", "disjoint", 1024):.4f} and {timing("two_rows", "disjoint", 1024):.4f} ms, respectively. '
        'This supports the predicted work and storage trends. Equal-string recursion follows one diagonal, while both DP implementations still fill every interior cell. '
        'Calls and DP cells are different work units, so their counts illustrate growth, not an exact time conversion. Slots exclude object headers and recursive stack frames.')
SEARCH = (f'At n=8192 and m=512, late mismatches require 3,932,672 naive comparisons and 16,894 KMP comparisons including preprocessing: '
          f'a {3932672/16894:.1f}-fold work ratio. Their medians are {timing("naive", "late_mismatch", 8192):.4f} and '
          f'{timing("kmp", "late_mismatch", 8192):.4f} ms. This matches the predicted quadratic versus linear trend for this input design. '
          'KMP is not universally cheaper: at the largest early-mismatch case, naive uses 7,681 comparisons versus 8,703 for KMP including LPS. '
          'Random cases usually reject naive candidates early. The three panels use separate vertical ranges, so compare labeled values rather than line heights across panels.')
ANSWERS = [
    ('Which search input was slowest?', 'Late mismatch at n=8192 was the slowest naive search in this experiment. Every candidate matches 511 characters before failing on the final B, so naive repeatedly scans the same text. KMP retains prefix information and avoids most repeated comparisons.'),
    ('How large could recursive edit distance handle?', 'The largest tested length was 8 for both strings; disjoint inputs already caused 398,593 recursive calls. The experiment deliberately stopped there because the branching recurrence grows exponentially. No failure threshold or maximum feasible length was measured, so 8 is a tested cap rather than a hardware limit.'),
    ('What do two rows gain and lose?', 'Two rows retain the same distance and O(nm) running time with O(min(n,m)) auxiliary array storage. At n=1024 they save a factor of 512.5 in allocated integer slots. Discarding earlier rows removes the straightforward full-table traceback for reconstructing edits, although more advanced reconstruction methods exist.'),
    ('Which search should the city platform use?', 'KMP is the safer default for long logs because it gives O(n+m) worst-case search including preprocessing. The late-mismatch data demonstrate why this matters for repetitive inputs. Naive search can be simpler and cheaper on short or immediately rejected patterns; exact matching also does not itself correct spelling.'),
]
TIME = ('Measured times were positive but small at short lengths, and some curves were not monotone. '
        'JIT compilation, allocation, garbage collection, CPU scheduling and instrumentation can affect a five-run median; '
        'the fixed case order can also bias timing comparisons. For example, the largest early-mismatch naive/KMP medians were '
        f'{timing("naive", "early_mismatch", 8192):.4f}/{timing("kmp", "early_mismatch", 8192):.4f} ms. '
        'Operation counts provide more stable evidence of growth than a claim based on one laptop timing. These numbers are observations, not universal speed guarantees.')
CAPTIONS = {
    'edit_work.png': 'Disjoint recursion branches rapidly; table and two-row work coincide at n squared cells.',
    'edit_storage.png': 'Two rows reduce measured DP slots while preserving the same cell updates and answer.',
    'search_work.png': 'Late mismatches separate naive quadratic growth from KMP linear work; preprocessing is included.',
    'search_time.png': 'Late mismatches cost naive the most time; early-mismatch and random timings need their own scale.',
    'edit_time.png': 'Iterative timings grow at larger sizes, but the small cases show warmup and clock noise.',
}

def markdown():
    parts = ['# Experiment Design Card', '| Field | Plan recorded before runs |', '|---|---|']
    parts += [f'| {key} | {value} |' for key, value in CARD]
    parts += ['\n## Method and scope\n', METHOD, '\n## Edit distance: prediction versus result\n', EDIT]
    for image in ['edit_work.png', 'edit_storage.png']:
        parts += [f'\n![{image[:-4].replace("_", " ")}](results/plots/{image})\n', CAPTIONS[image]]
    parts += ['\n## String search: prediction versus result\n', SEARCH]
    for image in ['search_work.png', 'search_time.png']:
        parts += [f'\n![{image[:-4].replace("_", " ")}](results/plots/{image})\n', CAPTIONS[image]]
    parts += ['\n## Short answers\n']
    for title, answer in ANSWERS:
        parts += [f'\n### {title}\n', answer]
    parts += ['\n## Time measurements\n', TIME, '\n![Edit median time](results/plots/edit_time.png)\n', CAPTIONS['edit_time.png'],
              '\n## Correctness and evidence\n', 'JUnit 5: 8 test methods passed, including all supplied references, empty inputs, overlaps, exact counter checks and 100 seeded comparisons per family. Search random tests also use String.indexOf as an independent oracle. A second experiment run matched all 450 rows after excluding time_ms. See results/VALIDATION.md. Definitions and limitations are explicit so the claims can be checked against results/results.csv.']
    (ROOT / 'REPORT.md').write_text('\n\n'.join(parts), encoding='utf-8')

def page(number, title):
    fig = plt.figure(figsize=(8.27, 11.69), facecolor='white')
    fig.text(.075, .955, 'CITY SEARCH & SPELL-CHECK', fontsize=10, color='#158477', weight='bold')
    fig.text(.075, .916, title, fontsize=20, weight='bold', color='#172b45')
    fig.text(.075, .035, 'DAA Assignment 4 | DP and string algorithms', fontsize=8, color='#52627a')
    fig.text(.925, .035, str(number), fontsize=9, ha='right', color='#52627a')
    return fig

def paragraph(fig, text, y, size=10, width=103, color='#25354a'):
    renderer = fig.canvas.get_renderer()
    font = FontProperties(family='DejaVu Sans', size=size)
    limit = fig.bbox.width * .85
    lines, current = [], ''
    for word in text.split():
        candidate = (current + ' ' + word).strip()
        if current and renderer.get_text_width_height_descent(candidate, font, False)[0] > limit:
            lines.append(current)
            current = word
        else:
            current = candidate
    if current:
        lines.append(current)
    for line in lines:
        fig.text(.075, y, line, fontsize=size, color=color, va='top')
        y -= size / (11.69 * 72) * 1.42
    return y - .012

def image(fig, name, bottom, height):
    ax = fig.add_axes([.055, bottom, .89, height])
    ax.imshow(imread(ROOT / 'results/plots' / name)); ax.axis('off')
    paragraph(fig, CAPTIONS[name], bottom - .004, size=9, width=112)

def pdf():
    with PdfPages(ROOT / 'REPORT.pdf', metadata={'Title': 'City Search & Spell-Check - Experiment Report'}) as out:
        fig = page(1, 'Experiment Design Card')
        y = .862
        for key, value in CARD:
            fig.text(.075, y, key.upper(), fontsize=10, weight='bold', color='#2464a5')
            y = paragraph(fig, value, y - .023, size=10, width=99) - .01
        fig.text(.075, y, 'METHOD AND SCOPE', fontsize=10, weight='bold', color='#2464a5')
        paragraph(fig, METHOD, y - .023, size=9.5, width=107)
        out.savefig(fig); plt.close(fig)
        fig = page(2, 'Edit distance: work and storage')
        image(fig, 'edit_work.png', .58, .29)
        image(fig, 'edit_storage.png', .26, .28)
        paragraph(fig, EDIT, .215, size=10, width=103)
        out.savefig(fig); plt.close(fig)
        fig = page(3, 'Search: adversarial inputs matter')
        image(fig, 'search_work.png', .58, .29)
        image(fig, 'search_time.png', .26, .29)
        paragraph(fig, SEARCH, .215, size=10, width=103)
        out.savefig(fig); plt.close(fig)
        fig = page(4, 'Interpretation and short answers')
        image(fig, 'edit_time.png', .665, .22)
        y = .62
        for title, answer in ANSWERS:
            fig.text(.075, y, title, fontsize=10, weight='bold', color='#2464a5')
            y = paragraph(fig, answer, y - .022, size=9.4, width=111) - .006
        fig.text(.075, y, 'WHAT THE CLOCK CAN AND CANNOT SHOW', fontsize=10, weight='bold', color='#2464a5')
        y = paragraph(fig, TIME, y - .022, size=9.4, width=111)
        paragraph(fig, 'Correctness: 8 JUnit 5 methods passed, with all reference cases and 100 seeded checks per family. Repeating the experiment reproduced every non-time field in all 450 rows.', y, size=9, width=116)
        out.savefig(fig); plt.close(fig)

if __name__ == '__main__':
    import sys
    if '--markdown-only' in sys.argv: markdown()
    else: markdown(); pdf()
