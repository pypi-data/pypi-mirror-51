from functools import singledispatch
import datetime
import re
from inspect import signature

from ..nodes import Row, Col, Table, Cell


def writer_visitor(writer):
    @singledispatch
    def visitor(_):
        pass

    @visitor.register
    def _(self: Row):
        for child in self.children:
            visitor(child)

    @visitor.register
    def _(self: Col):
        for child in self.children:
            visitor(child)

    @visitor.register
    def _(self: Table):
        def get_obj_attr(obj, field):
            for key in field.split("."):
                obj = getattr(obj, key)
                if obj is None:
                    break
            return obj

        row, col = self.row, self.col
        if self.cell_height:
            for i in range(len(self.data) + 1):
                writer.worksheet.set_row(self.row + i, self.cell_height)
        for i, column in enumerate(self.columns):
            width = column.width or self.cell_width
            if width:
                writer.worksheet.set_column(self.col + i, self.col + i, width)
            writer.write(row, col + i, column.title, self.cell_format)

        for i, item in enumerate(self.data):

            def format_from_style(style_css):
                rv = {}
                for style in style_css.split(";"):
                    style = style.strip()
                    if style == "":
                        continue
                    k, v = re.split(r"\s*:\s*", style)
                    rv[k] = v
                return rv

            for j, column in enumerate(self.columns):
                fmt = {}
                if isinstance(self.cell_style, str):
                    fmt.update(format_from_style(self.cell_style))

                else:
                    for styles, condition in self.cell_style.items():
                        sig = signature(condition)
                        if (
                            condition(item, column)
                            if len(sig.parameters) == 2
                            else condition(item)
                        ):
                            fmt.update(format_from_style(styles))
                if column.attr:
                    val = get_obj_attr(item, column.attr)
                else:
                    sig = signature(column.render)
                    if len(sig.parameters) == 1:
                        val = column.render(item)
                    else:
                        val = column.render(item, column)
                if isinstance(val, datetime.datetime):
                    fmt["num_format"] = self.datetime_format or "yyyy-mm-dd hh:mm:ss"
                if isinstance(val, datetime.date):
                    fmt["num_format"] = self.date_format or "yyyy-mm-dd"
                if isinstance(val, datetime.time):
                    fmt["num_format"] = self.time_format or "hh:mm:ss"

                writer.write(row + i + 1, col + j, val, {**self.cell_format, **fmt})

    @visitor.register
    def _(self: Cell):
        colspan = self.colspan or 1
        rowspan = self.rowspan or 1
        if rowspan == 1 and self.height:
            writer.worksheet.set_row(self.row, self.height)
        if colspan == 1 and rowspan == 1:
            writer.write(self.row, self.col, self.value, self.cell_format)
        else:
            writer.merge_range(
                self.row,
                self.col,
                self.row + rowspan - 1,
                self.col + colspan - 1,
                self.value,
                self.cell_format,
            )

    return visitor
