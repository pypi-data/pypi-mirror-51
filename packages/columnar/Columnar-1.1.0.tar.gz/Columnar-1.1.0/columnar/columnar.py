import shutil
import re
import io
import operator
from functools import reduce
from itertools import zip_longest
from collections import namedtuple

from toolz import frequencies

from .exceptions import TableOverflowError


class Columnar():

    def __call__(self, data, headers, head=0, justify='l', wrap_max=5, max_column_width=None,
                 min_column_width=5, row_sep='-', column_sep='|', patterns=[], drop=[], select=[],
                 no_borders=False, terminal_width=shutil.get_terminal_size().columns):
        self.wrap_max = wrap_max
        self.max_column_width = max_column_width
        self.min_column_width = min_column_width
        self.justify = justify
        self.head = head
        self.terminal_width = terminal_width
        self.row_sep = row_sep
        self.column_sep = column_sep
        self.header_sep = '='
        self.patterns = self.compile_patterns(patterns)
        self.ansi_color_pattern = re.compile(r"\x1b\[.+?m")
        self.color_reset = "\x1b[0m"
        self.color_grid = None
        self.drop = drop
        self.select = select
        self.no_borders = no_borders

        if self.no_borders:
            self.column_sep = ' ' * 2
            self.row_sep = ''
            self.header_sep = ''
            headers = [text.upper() for text in headers]

        data = self.clean_data(data)
        data, headers = self.filter_columns(data, headers)
        logical_rows = self.convert_data_to_logical_rows([headers] + data)
        column_widths = self.get_column_widths(logical_rows)
        truncated_rows = self.wrap_and_truncate_logical_cells(logical_rows, column_widths)

        justification_map = {
            'l': lambda text, width: text.ljust(width),
            'c': lambda text, width: text.center(width),
            'r': lambda text, width: text.rjust(width)
        }
        justifications = []
        if type(justify) is str:
            justifications = [justification_map[justify]] * len(column_widths)
        else:
            justifications = [justification_map[spec] for spec in justify]

        table_width = sum(column_widths) + ((len(column_widths) + 1) * len(row_sep))
        out = io.StringIO()
        header = True
        self.write_row_separators(out, column_widths)
        for lrow, color_row in zip(truncated_rows, self.color_grid):
            for row in lrow:
                justified_row_parts = [justifier(text, width) for text, justifier, width in
                                       zip(row, justifications, column_widths)]
                colorized_row_parts = [self.colorize(text, code) for text, code in zip(justified_row_parts, color_row)]
                out.write(self.column_sep + self.column_sep.join(colorized_row_parts) + self.column_sep + '\n')
            if header:
                out.write(self.column_sep + (
                        self.header_sep * (table_width - (len(self.column_sep * 2)))) + self.column_sep + '\n')
                header = False
            else:
                if not self.no_borders:
                    self.write_row_separators(out, column_widths)
        return out.getvalue()

    def write_row_separators(self, out_stream, column_widths):
        cells = [self.row_sep * width for width in column_widths]
        out_stream.write(self.column_sep + self.column_sep.join(cells) + self.column_sep + '\n')

    def compile_patterns(self, patterns):
        out = []
        for regex, func in patterns:
            if regex is not re.Pattern:
                regex = re.compile(regex)
            out.append((regex, func))
        return out

    def colorize(self, text, code):
        if code == None:
            return text
        return ''.join([code, text, self.color_reset])

    def clean_data(self, data):
        carriage_return = re.compile('\r')
        tab = re.compile('\t')
        out = []
        for row in data:
            cleaned = []
            for cell in row:
                cell = str(cell)
                cell = carriage_return.sub('', cell)
                cell = tab.sub(' ' * 4, cell)
                cleaned.append(cell)
            out.append(cleaned)
        return out

    def filter_columns(self, data, headers):
        """
        Drop columns that meet drop criteria, unless they have been
        explicitly selected.
        """
        drop = set(self.drop)
        select_patterns = [re.compile(pattern, re.I) for pattern in self.select]
        select = len(select_patterns) > 0
        headers_out = []
        columns_out = []
        for header, column in zip(headers, zip(*data)):
            if select:
                for pattern in select_patterns:
                    if pattern.search(header):
                        headers_out.append(header)
                        columns_out.append(column)
            else:
                freqs = frequencies(column)
                if not set(freqs.keys()).issubset(drop):
                    headers_out.append(header)
                    columns_out.append(column)
        rows_out = list(zip(*columns_out))
        return rows_out, headers_out

    def convert_data_to_logical_rows(self, full_data):
        """
        Takes a list of lists of items. Returns a list of logical rows, where each logical
        row is a list of lists, where each sub-list in a logical row is a physical row to be
        printed to the screen. There will only be more than one phyical row in a logical
        row if one of the columns wraps past one line.
        """
        logical_rows = []
        color_grid = []
        for row in full_data:
            cells_varying_lengths = []
            color_row = []
            for cell in row:
                cell = self.apply_patterns(cell)
                cell, color = self.strip_color(cell)
                color_row.append(color)
                lines = cell.split('\n')
                cells_varying_lengths.append(lines)
            cells = [[cell_text or '' for cell_text in physical_row] for physical_row in
                     zip_longest(*cells_varying_lengths)]
            logical_rows.append(cells)
            color_grid.append(color_row)
        self.color_grid = color_grid
        return logical_rows

    def apply_patterns(self, cell_text):
        out_text = cell_text
        for pattern, func in self.patterns:
            if pattern.match(cell_text):
                out_text = func(cell_text)
                break
        return out_text

    def strip_color(self, cell_text):
        matches = [match for match in self.ansi_color_pattern.finditer(cell_text)]
        color_codes = None
        clean_text = cell_text
        if matches:
            clean_text = self.ansi_color_pattern.sub('', cell_text)
            color_codes = ''.join([match.group(0) for match in matches[:-1]])
        return clean_text, color_codes

    def distribute_between(self, diff, columns, n):
        subset = columns[:n]
        width = sum([column['width'] for column in subset])
        remainder = width - diff
        new_width = remainder // n
        for i in range(n): columns[i]['width'] = new_width
        return columns

    def widths_sorted_by(self, columns, key):
        return [column['width'] for column in sorted(columns, key=lambda x: x[key])]

    def current_table_width(self, columns):
        return sum([len(self.column_sep) + column['width'] for column in columns]) + len(self.column_sep)

    def get_column_widths(self, logical_rows):
        """
        Calculated column widths, taking into account the terminal width,
        the number of columns, and the column seperators that will be used
        to delimit columns.
        """

        max_widths = []
        for column in zip(*reduce(operator.add, logical_rows)):
            lengths = [len(cell) for cell in column]
            max_natural = max(lengths)
            max_width = max_natural if self.max_column_width == None else min(max_natural, self.max_column_width)
            max_widths.append(max_width)

        columns = sorted([{'column_no': no, 'width': width} for no, width in enumerate(max_widths)],
                         key=lambda x: x['width'], reverse=True)
        # apply min and max widths
        for column in columns:
            if column['width'] < self.min_column_width:
                column['width'] = self.min_column_width
            if self.max_column_width:
                if column['width'] > self.max_column_width:
                    column['width'] = self.max_column_width

        if self.current_table_width(columns) <= self.terminal_width:
            return self.widths_sorted_by(columns, 'column_no')

        # the table needs to be narrowed
        for i in range(len(columns)):
            # include the next largest column in the size reduction
            diff = self.current_table_width(columns) - self.terminal_width
            columns = self.distribute_between(diff, columns, i + 1)
            if i < len(columns) - 1 and columns[0]['width'] < columns[i + 1]['width']:
                # if the columns that were just shrunk are smaller than the next largest column,
                # keep distributing the size so we have evenly-shrunken columns
                continue
            elif columns[0]['width'] >= self.min_column_width and self.current_table_width(
                    columns) <= self.terminal_width:
                return self.widths_sorted_by(columns, 'column_no')

        raise TableOverflowError("Could not fit table in current terminal, try reducing the number of columns.")

    def wrap_and_truncate_logical_cells(self, logical_rows, column_widths):
        lrows_out = []
        for lrow in logical_rows:
            cells_out = []
            # for cell in map(lambda column_cells: reduce(lambda cell_list, cell: cell_list + [cell], column_cells, []), zip(*lrow)):
            for cell, width in zip(map(list, zip(*lrow)), column_widths):
                # at this point `cell` is a list of strings, representing each line of the cell's contents
                cell_out = []
                for line in cell:
                    while len(line) > width:
                        cell_out.append(line[:width])
                        line = line[width:]

                    cell_out.append(line)
                cells_out.append(cell_out[:self.wrap_max + 1])
            cells_out_padded = [[text or '' for text in line] for line in zip_longest(*cells_out)]
            lrows_out.append(cells_out_padded)
        return lrows_out
