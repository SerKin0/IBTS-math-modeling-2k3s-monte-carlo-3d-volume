import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Установка шрифта CMU Serif для красивого PDF
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['CMU Serif', 'Computer Modern Serif', 'DejaVu Serif']
plt.rcParams['mathtext.fontset'] = 'cm'  # Для математических символов
plt.rcParams['pdf.fonttype'] = 42  # Сохранение шрифтов как текста (не как кривых)
plt.rcParams['ps.fonttype'] = 42   # То же для PostScript

# Чтение данных
df = pd.read_csv('tests/data.csv', low_memory=False)

# Создание фигуры с высоким разрешением
fig, ax = plt.subplots(figsize=(12, 7.5), dpi=300)

# Основной график
ax.scatter(df['count_points'], df['random_error_data'], label='Случайная погрешность')

# Автоматические границы с учетом горизонтальной линии
min_val = df['random_error_data'].min()
max_val = df['random_error_data'].max()

# Добавляем отступы и учитываем горизонтальную линию
ymin = min_val * 0.98
ymax = max_val * 1.02
ax.set_ylim(bottom=ymin, top=ymax)

# Настройки осей и заголовка
ax.set_xlabel('Количество точек, $N$', fontsize=14)
ax.set_ylabel('Случайная погрешность объема, $t$', fontsize=14)
# Сетка
ax.grid(True, linestyle='--', alpha=0.5, which='both')

# Легенда
ax.legend(fontsize=12, loc='best', framealpha=0.9)

# Настройка тиков
ax.tick_params(axis='both', which='major', labelsize=12)
ax.set_xlim(left=0)

# Форматирование чисел на осях
ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{int(x):d}'))
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x:.2f}'))

# Улучшаем расположение подписей
plt.tight_layout()

# Сохранение в PDF с высоким качеством
output_filename = 'MMM_ExamTask/graph/graph_3.pdf'
plt.savefig(output_filename, 
            format='pdf',
            dpi=300,
            bbox_inches='tight',
            pad_inches=0.1,
            transparent=False,
            facecolor='white',
            edgecolor='none')

print(f"График сохранён в файл: {output_filename}")

# Показываем график (опционально)
# plt.show()

# Закрываем фигуру для экономии памяти
plt.close(fig)