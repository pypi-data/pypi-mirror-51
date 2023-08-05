# -*- coding:utf-8 -*-
"""
@file
@brief To format a pandas dataframe
"""
import warnings


def df2rst(df, add_line=True, align="l", column_size=None, index=False,
           list_table=False, title=None, header=True, sep=',',
           number_format=None, replacements=None):
    """
    Builds a string in :epkg:`RST` format from a :epkg:`dataframe`.

    @param      df              dataframe
    @param      add_line        (bool) add a line separator between each row
    @param      align           ``r`` or ``l`` or ``c``
    @param      column_size     something like ``[1, 2, 5]`` to multiply the column size
    @param      index           add the index
    @param      list_table      use the `list_table <http://docutils.sourceforge.net/docs/ref/rst/directives.html#list-table>`_
    @param      title           used only if *list_table* is True
    @param      header          add one header
    @param      sep             separator if *df* is a string and is a filename to load
    @param      number_format   formats number in a specific way, if *number_format*
                                is an integer, the pattern is replaced by
                                ``{numpy.float64: '{:.2g}'}`` (if *number_format* is 2),
                                see also :epkg:`pyformat.info`
    @param      replacements    replacements just before converting into RST (dictionary)
    @return                     string

    If *list_table* is False, the format is the following.

    *None* values are replaced by empty string (4 spaces).
    It produces the following results:

    ::

        +------------------------+------------+----------+----------+
        | Header row, column 1   | Header 2   | Header 3 | Header 4 |
        | (header rows optional) |            |          |          |
        +========================+============+==========+==========+
        | body row 1, column 1   | column 2   | column 3 | column 4 |
        +------------------------+------------+----------+----------+
        | body row 2             | ...        | ...      |          |
        +------------------------+------------+----------+----------+

    If *list_table* is True, the format is the following:

    ::

        .. list-table:: title
            :widths: 15 10 30
            :header-rows: 1

            * - Treat
              - Quantity
              - Description
            * - Albatross
              - 2.99
              - anythings
            ...

    .. versionchanged:: 1.8
        Parameter *number_format* was added.

    .. versionchanged:: 1.9
        Nan value are replaced by empty string even if
        *number_format* is not None.
        Parameters *replacements* was added.
    """
    import numpy
    typstr = str

    if isinstance(df, str):
        import pandas
        df = pandas.read_csv(df, encoding="utf-8", sep=sep)
    else:
        df = df.copy()

    def patternification(value, pattern):
        if isinstance(value, float) and numpy.isnan(value):
            return ""
        return pattern.format(value)

    def nan2empty(value):
        if isinstance(value, float) and numpy.isnan(value):
            return ""
        return value

    if number_format is not None:
        if isinstance(number_format, int):
            number_format = "{:.%dg}" % number_format
            import pandas
            typ1 = numpy.float64
            _df = pandas.DataFrame({'f': [0.12]})
            typ2 = list(_df.dtypes)[0]
            number_format = {typ1: number_format, typ2: number_format}
        df = df.copy()
        for name, typ in zip(df.columns, df.dtypes):
            if name in number_format:
                pattern = number_format[name]
                df[name] = df[name].apply(
                    lambda x: patternification(x, pattern))
            elif typ in number_format:
                pattern = number_format[typ]
                df[name] = df[name].apply(
                    lambda x: patternification(x, pattern))

    # check empty strings
    col_strings = df.select_dtypes(include=[object]).columns
    for c in col_strings:
        df[c] = df[c].apply(nan2empty)

    if index:
        df = df.reset_index(drop=False).copy()
        ind = df.columns[0]

        def boldify(x):
            try:
                return "**{0}**".format(x)
            except Exception as e:
                raise Exception(
                    "Unable to boldify type {0}".format(type(x))) from e

        try:
            values = df[ind].apply(boldify)
        except Exception:
            warnings.warn("Unable to boldify the index (1).", SyntaxWarning)

        try:
            df[ind] = values
        except Exception:
            warnings.warn("Unable to boldify the index (2).", SyntaxWarning)

    def align_string(s, align, length):
        if len(s) < length:
            if align == "l":
                return s + " " * (length - len(s))
            elif align == "r":
                return " " * (length - len(s)) + s
            elif align == "c":
                m = (length - len(s)) // 2
                return " " * m + s + " " * (length - m - len(s))
            else:
                raise ValueError(
                    "align should be 'l', 'r', 'c' not '{0}'".format(align))
        else:
            return s

    def complete(cool):
        if list_table:
            i, s = cool
            if s is None:
                s = ""
            if isinstance(s, float) and numpy.isnan(s):
                s = ""
            else:
                s = typstr(s).replace("\n", " ")
            if replacements is not None:
                if s in replacements:
                    s = replacements[s]
            return (" " + s) if s else s
        else:
            i, s = cool
            if s is None:
                s = " " * 4
            if isinstance(s, float) and numpy.isnan(s):
                s = ""
            else:
                s = typstr(s).replace("\n", " ")
            i -= 2
            if replacements is not None:
                if s in replacements:
                    s = replacements[s]
            s = align_string(s.strip(), align, i)
            return s

    if list_table:

        def format_on_row(row):
            one = "\n      -".join(map(complete, enumerate(row)))
            res = "    * -" + one
            return res

        rows = [".. list-table:: {0}".format(title if title else "").strip()]
        if column_size is None:
            rows.append("    :widths: auto")
        else:
            rows.append("    :widths: " + " ".join(map(str, column_size)))
        if header:
            rows.append("    :header-rows: 1")
        rows.append("")
        if header:
            rows.append(format_on_row(df.columns))
        rows.extend(map(format_on_row, df.values))
        rows.append("")
        table = "\n".join(rows)
        return table
    else:
        length = [(len(_) if isinstance(_, typstr) else 5) for _ in df.columns]
        for row in df.values:
            for i, v in enumerate(row):
                length[i] = max(length[i], len(typstr(v).strip()))
        if column_size is not None:
            if len(length) != len(column_size):
                raise ValueError("length and column_size should have the same size {0} != {1}".format(
                    len(length), len(column_size)))
            for i in range(len(length)):
                if not isinstance(column_size[i], int):
                    raise TypeError(
                        "column_size[{0}] is not an integer".format(i))
                length[i] *= column_size[i]

        ic = 2
        length = [_ + ic for _ in length]
        line = ["-" * l for l in length]
        lineb = ["=" * l for l in length]
        sline = "+%s+" % ("+".join(line))
        slineb = "+%s+" % ("+".join(lineb))
        res = [sline]

        res.append("| %s |" % " | ".join(
            map(complete, zip(length, df.columns))))
        res.append(slineb)
        res.extend(["| %s |" % " | ".join(map(complete, zip(length, row)))
                    for row in df.values])
        if add_line:
            t = len(res)
            for i in range(t - 1, 3, -1):
                res.insert(i, sline)
        res.append(sline)
        table = "\n".join(res) + "\n"
        return table


def df2html(self, class_table=None, class_td=None, class_tr=None,
            class_th=None):
    """
    Converts the table into a :epkg:`html` string.

    @param  self            dataframe (to be added as a class method)
    @param  class_table     adds a class to the tag ``table`` (None for none)
    @param  class_td        adds a class to the tag ``td`` (None for none)
    @param  class_tr        adds a class to the tag ``tr`` (None for none)
    @param  class_th        adds a class to the tag ``th`` (None for none)
    """
    clta = ' class="%s"' % class_table if class_table is not None else ""
    cltr = ' class="%s"' % class_tr if class_tr is not None else ""
    cltd = ' class="%s"' % class_td if class_td is not None else ""
    clth = ' class="%s"' % class_th if class_th is not None else ""

    rows = ["<table%s>" % clta]
    rows.append(("<tr%s><th%s>" % (cltr, clth)) + ("</th><th%s>" %
                                                   clth).join(self.columns) + "</th></tr>")
    septd = "</td><td%s>" % cltd
    strtd = "<tr%s><td%s>" % (cltr, cltd)

    typstr = str

    def conv(s):
        if s is None:
            return ""
        else:
            return typstr(s)

    for row in self.values:
        s = septd.join(conv(_) for _ in row)
        rows.append(strtd + s + "</td></tr>")
    rows.append("</table>")
    rows.append("")
    return "\n".join(rows)
