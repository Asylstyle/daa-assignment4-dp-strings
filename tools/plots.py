"""Render every curve directly from per-run results, without hand-entered points."""
import csv
from collections import defaultdict
from pathlib import Path
from statistics import median
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import EngFormatter, MaxNLocator

ROOT = Path(__file__).resolve().parents[1]
PLOTS = ROOT / 'results' / 'plots'
PLOTS.mkdir(parents=True, exist_ok=True)
COLORS = {'recursive': '#a74130', 'table': '#2464a5', 'two_rows': '#158477',
          'naive': '#a74130', 'kmp': '#2464a5'}
LABELS = {'recursive': 'Recursive: calls', 'table': 'Table: DP cells',
          'two_rows': 'Two rows: DP cells', 'naive': 'Naive', 'kmp': 'KMP incl. LPS'}
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 11,
                     'axes.spines.top': False, 'axes.spines.right': False,
                     'figure.facecolor': 'white', 'savefig.facecolor': 'white'})

def load():
    groups = defaultdict(list)
    with (ROOT / 'results/results.csv').open() as stream:
        for row in csv.DictReader(stream):
            for key in row.keys() - {'algorithm', 'input'}:
                row[key] = float(row[key]) if key == 'time_ms' else int(row[key])
            groups[row['algorithm'], row['input'], row['n']].append(row)
    return groups

def curve(ax, groups, algorithm, input_type, metric, maximum=None, label=None):
    sizes = sorted(n for a, t, n in groups if a == algorithm and t == input_type
                   and (maximum is None or n <= maximum))
    values = []
    for n in sizes:
        runs = groups[algorithm, input_type, n]
        value = median([r['comparisons'] + r['lps_comparisons'] for r in runs]) if metric == 'total' else median(r[metric] for r in runs)
        values.append(value)
    ax.plot(sizes, values, marker='o', linewidth=2, markersize=5,
            color=COLORS[algorithm], label=label or LABELS[algorithm])

def finish(fig, name, title, caption):
    fig.suptitle(title, fontsize=16, fontweight='bold', x=0.5, y=0.98)
    fig.text(0.5, 0.015, caption, ha='center', fontsize=10, color='#34445a')
    fig.tight_layout(rect=(0, 0.07, 1, 0.90))
    fig.savefig(PLOTS / name, dpi=180)
    plt.close(fig)

def main():
    groups = load()
    fig, axes = plt.subplots(1, 3, figsize=(12.4, 4.1))
    for ax, kind in zip(axes, ['equal', 'disjoint', 'random']):
        for algorithm in ['recursive', 'table', 'two_rows']:
            curve(ax, groups, algorithm, kind, 'calls' if algorithm == 'recursive' else 'cells', 8)
        ax.set(title=kind.capitalize(), xlabel='Length n (UTF-16 units)', ylabel='Operations per call (log scale)', yscale='log')
        ax.set_xticks([2,4,6,8]); ax.grid(alpha=.2); ax.legend(fontsize=8)
    finish(fig, 'edit_work.png', 'Edit distance | repeated work at common sizes',
           'Disjoint recursion branches rapidly; the table and two-row curves coincide at n squared cells.')

    fig, ax = plt.subplots(figsize=(10, 3.8))
    for algorithm in ['table', 'two_rows']:
        curve(ax, groups, algorithm, 'disjoint', 'allocated_cells', label=algorithm.replace('_', ' ').capitalize())
    ax.set(xlabel='Length n (UTF-16 units)', ylabel='Allocated integer slots (log scale)', yscale='log')
    ax.grid(alpha=.2); ax.legend()
    finish(fig, 'edit_storage.png', 'Edit distance | allocated DP array slots',
           'The counter tracks actual array lengths; JVM headers and the recursive stack are excluded.')

    for metric, name in [('total', 'search_work.png'), ('time_ms', 'search_time.png')]:
        fig, axes = plt.subplots(1, 3, figsize=(12.4, 4.1))
        for ax, kind in zip(axes, ['early_mismatch', 'late_mismatch', 'random']):
            for algorithm in ['naive', 'kmp']:
                curve(ax, groups, algorithm, kind, metric)
            ax.set(title=kind.replace('_', ' ').capitalize(), xlabel='Text length n (UTF-16 units)',
                   ylabel='Character comparisons (log scale)' if metric == 'total' else 'Median time (ms; log scale)', yscale='log')
            ax.set_xticks([1024,2048,4096,8192]); ax.tick_params(axis='x', labelsize=9)
            ax.grid(alpha=.2); ax.legend(fontsize=9)
        finish(fig, name, 'String search | ' + ('total measured comparisons' if metric == 'total' else 'median of five measured runs'),
               'Pattern length m = n/16; KMP includes LPS preprocessing. Each panel has its own vertical range.')

    fig, axes = plt.subplots(1, 3, figsize=(12.4, 4.1))
    for ax, kind in zip(axes, ['equal', 'disjoint', 'random']):
        for algorithm in ['table', 'two_rows']:
            curve(ax, groups, algorithm, kind, 'time_ms', label=algorithm.replace('_', ' ').capitalize())
        ax.set(title=kind.capitalize(), xlabel='Length n (UTF-16 units)', ylabel='Median time (ms; log scale)', yscale='log')
        ax.grid(alpha=.2); ax.legend(fontsize=9)
    finish(fig, 'edit_time.png', 'Iterative edit distance | median of five measured runs',
           'Timings include allocation and enabled counters; JIT and scheduling can make short cases noisy.')
    print('Saved five plots from results/results.csv')

if __name__ == '__main__':
    main()
