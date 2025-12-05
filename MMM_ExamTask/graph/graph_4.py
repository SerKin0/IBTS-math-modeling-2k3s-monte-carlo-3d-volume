import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['CMU Serif', 'Computer Modern Serif', 'DejaVu Serif']
plt.rcParams['mathtext.fontset'] = 'cm'
plt.rcParams['pdf.fonttype'] = 42
plt.rcParams['ps.fonttype'] = 42
plt.rcParams['axes.unicode_minus'] = False

df = pd.read_csv('tests/data.csv', low_memory=False)
target_y = 11.265771973094854

df['delta_abs'] = np.abs(df['mean_data'] - target_y)
df['delta_percent'] = (df['delta_abs'] / df['delta_abs'].max()) * 100

max_delta_percent = df['delta_percent'].max()
min_delta_percent = df['delta_percent'].min()
mean_delta_percent = df['delta_percent'].mean()

fig, ax = plt.subplots(figsize=(12, 7.5), dpi=300)

ax.scatter(df['count_points'], df['delta_percent'], label='Отклонение от теоретического')

min_val = df['delta_percent'].min()
max_val = df['delta_percent'].max()
ymin = min_val * 0.98
ymax = max_val * 1.02
ax.set_ylim(bottom=ymin, top=ymax)

ax.set_xlabel('Количество точек, $N$', fontsize=14)
ax.set_ylabel('Отклонение от target_y, $\\Delta$ (%)', fontsize=14)

ax.grid(True, linestyle='--', alpha=0.5, which='both')
ax.legend(fontsize=12, loc='best', framealpha=0.9)
ax.tick_params(axis='both', which='major', labelsize=12)
ax.set_xlim(left=0)

ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{int(x):d}'))
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x:.0f}%'))

plt.tight_layout()

output_filename = 'MMM_ExamTask/graph/graph_4.pdf'
plt.savefig(output_filename, 
            format='pdf',
            dpi=300,
            bbox_inches='tight',
            pad_inches=0.1,
            transparent=False,
            facecolor='white',
            edgecolor='none')

print(f"График сохранён в файл: {output_filename}")
# plt.show()
plt.close(fig)