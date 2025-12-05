import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['CMU Serif', 'Computer Modern Serif', 'DejaVu Serif']
plt.rcParams['mathtext.fontset'] = 'cm'  
plt.rcParams['pdf.fonttype'] = 42  
plt.rcParams['ps.fonttype'] = 42   

# Чтение данных
df = pd.read_csv('tests/data.csv')

# Значение для горизонтальной линии
target_y = 11.265771973094854

# Создание фигуры с высоким разрешением
fig, ax = plt.subplots(figsize=(12, 8), dpi=300)

# Основной график
ax.plot(df['count_points'], df['mean_data'], 
        'o-', color='blue', markersize=4, 
        linewidth=2, label='Среднее значение')

# Добавление погрешностей
ax.errorbar(df['count_points'], df['mean_data'],
           yerr=df['random_error_data'],
           fmt='none',
           ecolor='red',
           elinewidth=1,
           capsize=5,
           capthick=1,
           alpha=0.7,
           label='Случайная погрешность')

# Горизонтальная линия с заданным значением
ax.axhline(y=target_y, color='purple', linestyle='--', linewidth=2, 
           label=f'y = {target_y:.6f}')

# Автоматические границы с учетом горизонтальной линии
min_val = (df['mean_data'] - df['random_error_data']).min()
max_val = (df['mean_data'] + df['random_error_data']).max()

# Добавляем отступы и учитываем горизонтальную линию
ymin = min(min_val * 0.999, target_y * 0.995)
ymax = max(max_val * 1.001, target_y * 1.005)
ax.set_ylim(bottom=ymin, top=ymax)

# Настройки осей и заголовка
ax.set_xlabel('Количество точек, $N$', fontsize=14)
ax.set_ylabel('Среднее значение, $V$', fontsize=14)

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
output_filename = 'MMM_ExamTask/graph/graph_1.pdf'
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