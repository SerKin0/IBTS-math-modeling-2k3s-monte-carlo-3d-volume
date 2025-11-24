from math import log10, e
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.patches import Rectangle
from typing import List

from dataclasses import dataclass

# Установка настроек matplotlib
plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['mathtext.fontset'] = 'cm'
plt.rcParams['font.size'] = 14
plt.rcParams['axes.titlesize'] = 16
plt.rcParams['axes.labelsize'] = 15
plt.rcParams['xtick.labelsize'] = 13
plt.rcParams['ytick.labelsize'] = 13
plt.rcParams['legend.fontsize'] = 12
plt.rcParams['text.usetex'] = False

name_file = "temp" 


def format_number(number: float, roundoff: int, degree: int = 0) -> str:
    if degree != 0:
        scaled = number / (10 ** degree)
        formatted = f"{scaled:.{roundoff}f}".replace('.', ',')
        return f"{formatted}"
    return f"{number:.{roundoff}f}".replace('.', ',')

@dataclass
class Values:
    _name: str
    _units: str
    _data: List[float]
    _up_error: List[float]
    _down_error: List[float]
    _step: float
    _roundoff: int
    _degree: int
    _flag_error_label: bool

    def __init__(self,
                 data: List[float],
                 error: List[float],
                 degree: int = 0,
                 units: str = "",
                 name: str = "",
                 step: float = None,
                 roundoff: int = None,
                 flag_error_label: bool = True):
        self._name = name
        self._units = units
        self._data = data
        self._flag_error_label = flag_error_label
        self._degree = degree

        if len(data) == 0:
            raise ValueError("Переменная data пуста")

        if roundoff is None:
            max_err = max(error) if error else 0
            self._roundoff = max(1, -int(log10(max_err)) + 1) if max_err > 0 else 2
        else:
            if roundoff < 0:
                raise ValueError("Округление не может быть отрицательным!")
            self._roundoff = roundoff

        if step is None:
            self._step = 10 ** int(log10(max(data) - min(data)))
        else:
            self._step = step

        if len(data) != len(error):
            raise ValueError(f"Количество элементов в 'error' ({len(error)}) "
                           f"не равно количеству элементов в 'data' ({len(data)})")
        self._up_error = [value / 2 for value in error]
        self._down_error = [value / 2 for value in error]

    @property
    def data(self) -> List[float]:
        return self._data

    @data.setter
    def data(self, data: List[float]) -> None:
        if data is None:
            raise ValueError("Список 'data' пуст")
        if len(data) != len(self._up_error):
            print("WARNING: Количество элементов в 'data' не равно количеству в 'error'.")
            self._up_error.extend([0.] * (len(data) - len(self._up_error)))
            self._down_error.extend([0.] * (len(data) - len(self._down_error)))
        self._data = data

    @property
    def degree(self) -> int:
        return self._degree

    @degree.setter
    def degree(self, degree: int):
        if degree < 0:
            raise ValueError("Степень не может быть отрицательной")
        self._degree = degree

    @property
    def up_error(self) -> List[float]:
        return self._up_error

    @up_error.setter
    def up_error(self, error: List[float]) -> None:
        if self._data is None:
            raise ValueError("Сначала задайте данные в 'data'")
        if len(self._data) != len(error):
            raise ValueError("Количество элементов в 'error' не равно количеству в 'data'")
        self._up_error = error

    @property
    def down_error(self) -> List[float]:
        return self._down_error

    @down_error.setter
    def down_error(self, error: List[float]) -> None:
        if self._data is None:
            raise ValueError("Сначала задайте данные в 'data'")
        if len(self._data) != len(error):
            raise ValueError("Количество элементов в 'error' не равно количеству в 'data'")
        self._down_error = error

    @property
    def error(self) -> List[float]:
        return [value_up + value_down for value_up, value_down in zip(self._up_error, self._down_error)]

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name: str):
        self._name = name

    @property
    def roundoff(self) -> int:
        return self._roundoff

    @roundoff.setter
    def roundoff(self, roundoff: int):
        if roundoff < 0:
            raise ValueError("Округление не может быть отрицательным!")
        self._roundoff = roundoff

    @property
    def units(self) -> str:
        if self._degree != 0:
            return fr"{self._units} \times 10^{{{self._degree}}}"
        return self._units

    @property
    def step(self) -> float:
        return self._step

    @step.setter
    def step(self, step: float):
        if step is None:
            self._step = 10 ** int(log10(max(self._data) - min(self._data)))
        else:
            self._step = step

    @property
    def flag_error_label(self) -> bool:
        return self._flag_error_label

    @flag_error_label.setter
    def flag_error_label(self, flag_error_label: bool):
        self._flag_error_label = flag_error_label

    def steps(self) -> dict:
        return {
            val: format_number(val, self._roundoff, self._degree).replace('.', ',')
            for val in self._data
        }

# Данные с единицами измерения на русском
y = Values(
    [4.6, 5.8, 6.9, 7.9, 9.9, 11.3, 12.4, 13.2, 14.7, 15.4, 16.0, 16.5, 16.8, 16.4, 15.9, 14.7],
    [0.5, 0.5, 0.5, 0.5, 0.5, 0.1, 0.5, 0.1, 0.1, 0.5, 0.1, 0.4, 0.9, 0.4, 1.1, 1.8],
    name=r"\omega",
    step=1,
    units=r"\text{рад} / \text{с}",
    roundoff=1,
    flag_error_label=False
)
x = Values(
    [3.8, 4.9, 5.8, 6.5, 7.5, 8.6, 9.7, 10.8, 11.7, 13.0, 14.0, 14.9, 16.0, 17.8, 19.1, 21.3],
    [0.4123105625617661, 0.4123105625617661, 0.4123105625617661,
     0.4123105625617661, 0.4123105625617661, 0.1, 0.4123105625617661,
     0.1, 0.1, 0.4123105625617661, 0.1, 0.4123105625617661,
     0.9055385138137417, 0.4123105625617661, 1.3038404810405297, 2.6019223662515376],
    name="t",
    units=r"\text{с}",
    step=1,
    flag_error_label=False
)




with PdfPages(f'{name_file}.pdf') as pdf:
    fig, ax = plt.subplots(figsize=(14, 11))

    # Прямоугольники погрешностей
    for x_val, y_val, dx_up, dx_down, dy_up, dy_down in zip(
        x.data, y.data, x.up_error, x.down_error, y.up_error, y.down_error
    ):
        rect = Rectangle(
            (x_val - dx_down, y_val - dy_down), dx_up + dx_down, dy_up + dy_down,
            linewidth=0.5, edgecolor='gray', facecolor='lightgray', alpha=0.5
        )
        ax.add_patch(rect)

    # Экспериментальные точки
    ax.plot(x.data, y.data, 'o', color='black', markersize=2)

    # Теоретическая линия
    k1, b1 = (1.0546357214934412, 1.326948940464179)
    k2, b2 = (-0.39986604152712674, 23.367515070328125)
    x_theory = np.linspace(0, (b2 - b1) / (k1-k2), 2)
    k = k1
    b = b1
    y_theory = k * x_theory + b
    ax.plot(x_theory, y_theory, 'k--', linewidth=1)
    x_theory = np.linspace((b2 - b1) / (k1-k2), 24, 2)
    k = k2
    b = b2
    y_theory = k * x_theory + b
    ax.plot(x_theory, y_theory, 'k--', linewidth=1)

    # Линии погрешностей
    for x_val, dx_up, dx_down in zip(x.data, x.up_error, x.down_error):
        ax.axvline(x=x_val, color='gray', linestyle='--', linewidth=0.5, alpha=0.3)
        if x.flag_error_label:
            ax.axvline(x=x_val + dx_up, color='gray', linestyle='--', linewidth=0.5, alpha=0.3)
            ax.axvline(x=x_val - dx_down, color='gray', linestyle='--', linewidth=0.5, alpha=0.3)

    for y_val, dy_up, dy_down in zip(y.data, y.up_error, y.down_error):
        ax.axhline(y=y_val, color='gray', linestyle='--', linewidth=0.5, alpha=0.3)
        if y.flag_error_label:
            ax.axhline(y=y_val + dy_up, color='gray', linestyle='--', linewidth=0.5, alpha=0.3)
            ax.axhline(y=y_val - dy_down, color='gray', linestyle='--', linewidth=0.5, alpha=0.3)

    # Названия осей
    ax.set_xlabel(f"${x.name}$, ${x.units}$", fontsize=14)
    ax.set_ylabel(f"${y.name}$, ${y.units}$", fontsize=14)

    # Установка шага осей
    ax.xaxis.set_major_locator(ticker.MultipleLocator(x.step))
    ax.yaxis.set_major_locator(ticker.MultipleLocator(y.step))

    # Форматирование чисел для осей
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda temp, _: format_number(temp, x.roundoff, x.degree)))
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda temp, _: format_number(temp, y.roundoff, y.degree)))

    # Дополнительные оси для значений и погрешностей
    x_ticks_top = []
    x_ticks_labels_top = []
    x_ticks_ha = []

    if x.flag_error_label:
        for x_val, dx_up, dx_down in zip(x.data, x.up_error, x.down_error):
            x_ticks_top.extend([x_val - dx_down, x_val, x_val + dx_up])
            x_ticks_labels_top.extend([
                format_number(x_val - dx_down, x.roundoff, x.degree),
                format_number(x_val, x.roundoff, x.degree),
                format_number(x_val + dx_up, x.roundoff, x.degree)
            ])
            x_ticks_ha.extend(['right', 'center', 'left'])
    else:
        x_ticks_ha = ['center'] * len(x.data)
        x_ticks_top = x.data
        x_ticks_labels_top = [format_number(x_val, x.roundoff, x.degree) for x_val in x.data]

    ax_top = ax.secondary_xaxis('top')
    ax_top.set_xticks(x_ticks_top)
    texts_top = ax_top.set_xticklabels(x_ticks_labels_top, rotation=60, fontsize=10)
    for text, ha in zip(texts_top, x_ticks_ha):
        text.set_horizontalalignment(ha)

    y_ticks_right = []
    y_ticks_labels_right = []
    y_ticks_va = []

    if y.flag_error_label:
        for y_val, dy_up, dy_down in zip(y.data, y.up_error, y.down_error):
            y_ticks_right.extend([y_val - dy_down, y_val, y_val + dy_up])
            y_ticks_labels_right.extend([
                format_number(y_val - dy_down, y.roundoff, y.degree),
                format_number(y_val, y.roundoff, y.degree),
                format_number(y_val + dy_up, y.roundoff, y.degree)
            ])
            y_ticks_va.extend(['top', 'center', 'bottom'])
    else:
        y_ticks_va = ['center'] * len(y.data)
        y_ticks_right = y.data
        y_ticks_labels_right = [format_number(y_val, y.roundoff, y.degree) for y_val in y.data]

    ax_right = ax.secondary_yaxis('right')
    ax_right.set_yticks(y_ticks_right)
    texts_right = ax_right.set_yticklabels(y_ticks_labels_right, rotation=0, fontsize=10)
    for text, va in zip(texts_right, y_ticks_va):
        text.set_verticalalignment(va)
    ax_right.tick_params(axis='y', pad=10)

    # Сетка и пределы
    x_lims = []
    y_lims = []
    for x_val, dx_up, dx_down in zip(x.data, x.up_error, x.down_error):
        x_lims.extend([x_val, x_val + dx_up, x_val - dx_down])
    for y_val, dy_up, dy_down in zip(y.data, y.up_error, y.down_error):
        y_lims.extend([y_val, y_val + dy_up, y_val - dy_down])

    ax.grid(True, linestyle='--', alpha=0.5)
    delta_lims_x = (max(x_lims) - min(x_lims)) / 18
    delta_lims_y = (max(y_lims) - min(y_lims)) / 18
    ax.set_xlim(min(x_lims) - delta_lims_x, max(x_lims) + delta_lims_x)
    ax.set_ylim(min(y_lims) - delta_lims_y, max(y_lims) + delta_lims_y)

    # ax.legend()
    plt.tight_layout(pad=3.0)
    pdf.savefig(fig, bbox_inches='tight', dpi=300)
    plt.show()
    plt.close()

