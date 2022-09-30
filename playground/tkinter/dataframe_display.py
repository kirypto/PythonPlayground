from datetime import datetime, timedelta
from tkinter import Frame, Tk, Scale, HORIZONTAL, Misc
from typing import Iterable, Any, Dict, Union

from matplotlib.axes import Axes
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from numpy import linspace
from pandas import DataFrame, to_datetime

from playground.math.periodics import generate_periodic_data


class DataFrameLinePlot(Frame):
    _figure_canvas: FigureCanvasTkAgg
    _plot_axes: Axes

    # noinspection SpellCheckingInspection
    def __init__(self, master: Misc, *args, toolbar: bool = False, figsize=None, **kwargs) -> None:
        super(DataFrameLinePlot, self).__init__(master, *args, **kwargs)
        figure = Figure(figsize=figsize)
        self._plot_axes = figure.add_subplot(111)
        self._figure_canvas = FigureCanvasTkAgg(figure, master=self)
        self._figure_canvas.draw()
        if toolbar:
            NavigationToolbar2Tk(self._figure_canvas).update()
        self._figure_canvas.get_tk_widget().pack()

    def pack(self, *args, **kwargs) -> None:
        super(DataFrameLinePlot, self).pack(*args, **kwargs)

    def plot(
            self, dataframe: DataFrame, columns: Iterable[Any] = None, column_plot_kwargs: Dict[Any, dict] = None,
            x_labels_as_dates: bool = False,
    ) -> None:
        self._plot_axes.clear()
        column_plot_kwargs = column_plot_kwargs or {}

        column_names = []
        for column in (columns or dataframe.columns):
            plot_kwargs = column_plot_kwargs[column] if column in column_plot_kwargs else {}
            self._plot_axes.plot(dataframe.index, dataframe[column], **plot_kwargs)
            column_names.append(column)
        self._plot_axes.legend(column_names)
        if x_labels_as_dates:
            self._plot_axes.figure.autofmt_xdate()
        self._figure_canvas.draw()


def _main():
    root = Tk()
    root.title('Plotting in Tkinter')
    line_plot = DataFrameLinePlot(root, toolbar=True, figsize=(10, 5))
    line_plot.pack()

    def render_data(offset: Union[str, float]) -> None:
        offset = float(offset)
        now = datetime.now() + timedelta(hours=offset)
        end = now + timedelta(days=5)
        num_data_points = 100
        seconds_per_day = 24 * 60 * 60
        timestamp_index = to_datetime(linspace(now.timestamp(), end.timestamp(), num_data_points) * 1000000000)
        data = {
            f"{period_in_days} Day": generate_periodic_data(now.timestamp(), end.timestamp(), num_data_points, period_in_days * seconds_per_day)
            for period_in_days in range(1, 5)
        }
        data_frame = DataFrame(index=timestamp_index, data=data)
        line_plot.plot(data_frame, x_labels_as_dates=True)

    slider = Scale(master=root, from_=0, to=500, orient=HORIZONTAL, command=render_data, length=300)
    slider.pack()

    render_data(0)

    root.mainloop()


if __name__ == "__main__":
    _main()
