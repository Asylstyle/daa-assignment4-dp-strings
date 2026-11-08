"""Print-ready figures derived exclusively from the submitted raw measurements."""
import csv
from collections import defaultdict
from pathlib import Path
from statistics import median

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import FixedLocator, FuncFormatter, LogLocator, NullFormatter

ROOT = Path(__file__).resolve().parents[1]
PLOTS = ROOT / 'results/plots'
COLORS = {'table': '#2166ac', 'two_rows': '#13816f', 'naive': '#c05a26', 'kmp': '#2166ac'}
STYLES = {'table': ('o', '-'), 'two_rows': ('s', '--'), 'naive': ('o', '-'), 'kmp': ('s', '--')}
AUDIT = []
plt.rcParams.update({
    'font.family': 'DejaVu Sans', 'font.size': 12, 'axes.titlesize': 12,
    'axes.titleweight': 'bold', 'axes.labelsize': 12, 'xtick.labelsize': 10,
    'ytick.labelsize': 10, 'axes.spines.top': False, 'axes.spines.right': False,
    'axes.edgecolor': '#aab5c2', 'axes.labelcolor': '#27364a', 'text.color': '#172b45',
    'xtick.color': '#52627a', 'ytick.color': '#52627a',
    'figure.facecolor': 'white', 'savefig.facecolor': 'white',
})


def load():
    groups = defaultdict(list)
    with (ROOT / 'results/results.csv').open() as stream:
        for row in csv.DictReader(stream):
            for key in row.keys() - {'algorithm', 'input'}:
                row[key] = float(row[key]) if key == 'time_ms' else int(row[key])
            groups[row['algorithm'], row['input'], row['n']].append(row)
    return groups


def series(groups, algorithm, kind, metric, maximum=None):
    sizes = sorted(n for a, t, n in groups if a == algorithm and t == kind
                   and (maximum is None or n <= maximum))
    middle, low, high = [], [], []
    for n in sizes:
        values = [r['comparisons'] + r['lps_comparisons'] if metric == 'total_comparisons'
                  else r[metric] for r in groups[algorithm, kind, n]]
        middle.append(median(values)); low.append(min(values)); high.append(max(values))
        AUDIT.append({'algorithm': algorithm, 'input': kind, 'n': n, 'metric': metric,
                      'median': middle[-1], 'minimum': low[-1], 'maximum': high[-1], 'runs': len(values)})
    return sizes, middle, low, high


def plot(ax, groups, algorithm, kind, metric, label, maximum=None, spread=False):
    x, y, low, high = series(groups, algorithm, kind, metric, maximum)
    marker, line = STYLES[algorithm]
    color = COLORS[algorithm]
    if spread:
        # Observed range, not a confidence interval or standard error.
        ax.fill_between(x, low, high, color=color, alpha=.12, linewidth=0)
        ax.vlines(x, low, high, color=color, linewidth=1, alpha=.5)
    ax.plot(x, y, marker=marker, linestyle=line, linewidth=2.1, markersize=5,
            color=color, label=label, markerfacecolor='white', markeredgewidth=1.5)
    return x, y


def log_axis(ax, sizes, log_y=True):
    ax.set_xscale('log', base=2)
    ax.xaxis.set_major_locator(FixedLocator(sizes))
    ax.xaxis.set_major_formatter(FuncFormatter(lambda value, _: f'{int(value):,}'))
    ax.xaxis.set_minor_locator(FixedLocator([]))
    if log_y:
        ax.set_yscale('log')
        ax.yaxis.set_major_locator(LogLocator(base=10, numticks=5))
        ax.yaxis.set_minor_formatter(NullFormatter())
    ax.grid(axis='y', which='major', color='#d9e1e9', linewidth=.7)
    ax.set_axisbelow(True)
    ax.margins(x=.12, y=.16)


def finish(fig, filename, title, subtitle, handles=None, labels=None):
    fig.suptitle(title, fontsize=16, weight='bold', y=.98)
    fig.text(.5, .885, subtitle, ha='center', fontsize=10, color='#52627a')
    if handles:
        fig.legend(handles, labels, loc='lower center', bbox_to_anchor=(.5, .005),
                   ncol=len(handles), frameon=False, fontsize=11)
    fig.subplots_adjust(left=.09, right=.985, top=.75, bottom=.23, wspace=.28)
    fig.savefig(PLOTS / filename, dpi=300)
    plt.close(fig)


def edit_work(groups):
    fig, axes = plt.subplots(1, 2, figsize=(10, 4.25))
    for kind, color, marker in [('equal', '#13816f', 'o'), ('disjoint', '#c05a26', 's'),
                                ('random', '#2166ac', '^')]:
        x, y, _, _ = series(groups, 'recursive', kind, 'calls', 8)
        axes[0].plot(x, y, marker=marker, color=color, linewidth=2, markersize=5,
                     label=kind.capitalize(), markerfacecolor='white')
    axes[0].set(title='A  Direct recursion', xlabel='String length n (UTF-16 units)',
                ylabel='Recursive calls (count; log scale)')
    log_axis(axes[0], [2,4,6,8])
    axes[0].set_xscale('linear')
    axes[0].set_xticks([2,4,6,8])
    axes[0].legend(fontsize=10, frameon=False, loc='upper left')
    dp_values = None
    for algorithm in ['table', 'two_rows']:
        for kind in ['equal', 'disjoint', 'random']:
            sizes, values, _, _ = series(groups, algorithm, kind, 'cells', 8)
            if dp_values is None:
                dp_values = values
            assert values == dp_values, 'Cannot merge distinct measured curves'
    axes[1].plot(sizes, dp_values, 'D-', color='#2166ac', markersize=5,
                 linewidth=2, markerfacecolor='white')
    axes[1].set(title='B  Both iterative versions', xlabel='String length n (UTF-16 units)',
                ylabel='Interior DP cells (count)')
    axes[1].set_xticks([2,4,6,8]); axes[1].set_yticks(dp_values)
    axes[1].grid(axis='y', color='#d9e1e9'); axes[1].set_axisbelow(True)
    axes[1].text(.04, .94, 'Table = two rows\nAll three input types',
                 transform=axes[1].transAxes, va='top', fontsize=11)
    finish(fig, 'edit_work.png', 'Edit distance: repeated work versus DP',
           'Separate panels preserve each counter; recursive calls use a logarithmic y axis.')


def storage(groups):
    fig, axes = plt.subplots(1, 2, figsize=(10, 4.25))
    values = {}
    for algorithm in ['table', 'two_rows']:
        x, y = plot(axes[0], groups, algorithm, 'disjoint', 'allocated_cells',
                    algorithm.replace('_', ' ').capitalize())
        values[algorithm] = y
    log_axis(axes[0], [2,8,64,256,1024])
    axes[0].set(title='A  Allocated array payload', xlabel='String length n (log2 scale)',
                ylabel='Integer slots (count; log scale)')
    ratios = [a / b for a, b in zip(values['table'], values['two_rows'])]
    axes[1].plot(x, ratios, 'D-', color='#13816f', linewidth=2, markersize=5)
    log_axis(axes[1], [2,8,64,256,1024], log_y=False)
    axes[1].set(title='B  Storage reduction', xlabel='String length n (log2 scale)',
                ylabel='Table slots / two-row slots (ratio)', ylim=(0,640))
    axes[1].annotate(f'{ratios[-1]:,.1f}x at n={x[-1]:,}', (x[-1], ratios[-1]),
                     xytext=(-7,13), textcoords='offset points', ha='right',
                     fontsize=11, weight='bold', color='#13816f')
    handles, labels = axes[0].get_legend_handles_labels()
    finish(fig, 'edit_storage.png', 'Edit distance: the storage saved by two rows',
           'Measured array lengths; excludes JVM headers, stack frames and other objects.', handles, labels)


def search(groups, timed=False):
    metric = 'time_ms' if timed else 'total_comparisons'
    fig, axes = plt.subplots(1, 3, figsize=(10,4.25), sharey=not timed)
    for ax, kind, title in zip(axes, ['early_mismatch','late_mismatch','random'],
                               ['A  Early mismatch','B  Late mismatch','C  Random']):
        for algorithm, label in [('naive','Naive'), ('kmp','KMP including LPS')]:
            plot(ax, groups, algorithm, kind, metric, label, spread=timed)
        log_axis(ax, [1024,2048,4096,8192]); ax.set_title(title, pad=12)
        if timed:
            ax.yaxis.set_major_locator(LogLocator(base=10, subs=(1,5), numticks=10))
            ax.yaxis.set_major_formatter(FuncFormatter(lambda value, _: f'{value:g}'))
    if not timed:
        axes[0].set_ylim(500, 1e7)
    fig.supxlabel('Text length n (UTF-16 units; log2 scale), pattern length m = n/16', y=.11, fontsize=11)
    axes[0].set_ylabel('Time (ms; log scale)' if timed else 'Total character comparisons (log scale)')
    handles, labels = axes[0].get_legend_handles_labels()
    finish(fig, 'search_time.png' if timed else 'search_work.png',
           'String search: measured running time' if timed else 'String search: total comparison cost',
           'Median of 5 runs; bands = observed min-max, not confidence intervals. Y ranges differ.' if timed
           else 'Shared y scale across inputs. KMP includes both search and LPS comparisons.', handles, labels)


def edit_time(groups):
    fig, axes = plt.subplots(1,3,figsize=(10,4.25),sharey=True)
    for ax, kind, title in zip(axes, ['equal','disjoint','random'],
                               ['A  Equal strings','B  Disjoint strings','C  Random strings']):
        for algorithm in ['table','two_rows']:
            plot(ax, groups, algorithm, kind, 'time_ms',
                 algorithm.replace('_',' ').capitalize(), spread=True)
        log_axis(ax, [2,8,64,256,1024]); ax.set_title(title, pad=12)
    axes[0].set_ylabel('Time (ms; log scale)')
    fig.supxlabel('String length n (UTF-16 units; log2 scale)', y=.11, fontsize=11)
    handles, labels = axes[0].get_legend_handles_labels()
    finish(fig, 'edit_time.png', 'Iterative edit distance: measured running time',
           'Median of 5 runs; bands = observed min-max. Shared y scale; allocation and counters included.', handles, labels)


def main():
    PLOTS.mkdir(parents=True,exist_ok=True)
    AUDIT.clear()
    groups = load()
    edit_work(groups); storage(groups); search(groups); search(groups,timed=True); edit_time(groups)
    unique = {(r['algorithm'],r['input'],r['n'],r['metric']):r for r in AUDIT}
    with (ROOT / 'results/plot_data.csv').open('w',newline='') as stream:
        writer = csv.DictWriter(stream,fieldnames=list(AUDIT[0]))
        writer.writeheader(); writer.writerows(unique.values())
    print('Saved five 300-dpi figures and their source-point audit table')


if __name__ == '__main__': main()
