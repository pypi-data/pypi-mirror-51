import configparser

import humanize
import imgkit
import jinja2
import simplejson as json

from optimus.audf import *
from optimus.dataframe.plots.functions import plot_frequency, plot_missing_values, plot_hist
from optimus.helpers.check import is_column_a
from optimus.helpers.columns import parse_columns
from optimus.helpers.columns_expression import zeros_agg, count_na_agg, hist_agg, percentile_agg, count_uniques_agg
from optimus.helpers.constants import RELATIVE_ERROR
from optimus.helpers.decorators import time_it
from optimus.helpers.functions import absolute_path
from optimus.helpers.json import json_converter
from optimus.helpers.logger import logger
from optimus.helpers.output import print_html
from optimus.helpers.raiseit import RaiseIt
from optimus.profiler.functions import fill_missing_col_types, \
    write_json, write_html, PYSPARK_NUMERIC_TYPES
from optimus.profiler.templates.html import FOOTER, HEADER

HISTOGRAM_FREQUENCY_CHART_THRESHOLD = 30


class Profiler:

    def __init__(self, output_path=None):
        """

        :param output_path:
        """

        config = configparser.ConfigParser()
        # If not path defined. Try to load from the config.ini file
        if output_path is None:
            try:
                # try to load the config file
                config.read("config.ini")
                output_path = config["PROFILER"]["Output"]
            except (IOError, KeyError):
                logger.print("Config.ini not found")
                output_path = "data.json"

        self.html = None
        self.json = None
        self.path = output_path
        self.rows_count = None
        self.cols_count = None
        self.columns_dtypes = None

    def _count_data_types(self, df, columns, infer=False):
        """
        Count the number of int, float, string, date and booleans and output the count in json format
        :param df: Dataframe to be processed
        :param columns: Columns to be processed
        :param infer: infer the column datatype

        :return: json
        """

        count_by_data_type = df.cols.count_by_dtypes(columns, infer)

        def _count_data_types(col_name):
            """
            Function for determine if register value is float or int or string.
            :param col_name:
            :return:
            """

            # Get the greatest count by column data type
            null_missed_count = {"null": count_by_data_type[col_name]['null'],
                                 "missing": count_by_data_type[col_name]['missing'],
                                 }

            greatest_data_type_count = max(count_by_data_type[col_name], key=count_by_data_type[col_name].get)
            if greatest_data_type_count == "string" or greatest_data_type_count == "boolean":
                cat = "categorical"
            elif greatest_data_type_count == "int" or greatest_data_type_count == "decimal":
                cat = "numeric"
            elif greatest_data_type_count == "date":
                cat = "date"
            elif greatest_data_type_count == "array":
                cat = "array"
            elif greatest_data_type_count == "binary":
                cat = "binary"
            elif greatest_data_type_count == "null":
                cat = "null"
            else:
                cat = None

            col = {}
            col['dtype'] = greatest_data_type_count
            col['type'] = cat
            col['details'] = {**count_by_data_type[col_name], **null_missed_count}

            return col

        columns = parse_columns(df, columns)

        # Info from all the columns
        type_details = {c: _count_data_types(c) for c in columns}

        results = {}
        count_types = {}

        # Count the categorical, numerical, boolean and date columns
        for v in type_details.values():
            name = v["type"]
            if name in count_types:
                count_types[name] += 1
            else:
                count_types[name] = 1

        count_types = fill_missing_col_types(count_types)

        results["count_types"] = count_types
        results["columns"] = type_details
        return results

    @time_it
    def run(self, df, columns="*", buckets=20, infer=False, relative_error=RELATIVE_ERROR, approx_count=True):
        """
        Return dataframe statistical information in HTML Format
        :param df: Dataframe to be analyzed
        :param columns: Columns to be analyzed
        :param buckets: Number of buckets calculated to print the histogram
        :param infer: infer data type
        :param relative_error: Relative Error for quantile discretizer calculation
        :param approx_count: Use approx_count_distinct or countDistinct
        :return:
        """

        columns = parse_columns(df, columns)

        output = self.to_json(df, columns, buckets, infer, relative_error, approx_count, dump=False)

        # Load jinja
        template_loader = jinja2.FileSystemLoader(searchpath=absolute_path("/profiler/templates/out"))
        template_env = jinja2.Environment(loader=template_loader, autoescape=True)

        # Render template
        # Create the profiler info header
        html = ""
        general_template = template_env.get_template("general_info.html")
        html = html + general_template.render(data=output)

        template = template_env.get_template("one_column.html")

        # Create every column stats
        for col_name in columns:
            hist_pic = None
            freq_pic = None

            col = output["columns"][col_name]
            if "hist" in col["stats"]:
                hist_dict = col["stats"]["hist"]

                if col["column_dtype"] == "date":
                    hist_year = plot_hist({col_name: hist_dict["years"]}, "base64", "years")
                    hist_month = plot_hist({col_name: hist_dict["months"]}, "base64", "months")
                    hist_weekday = plot_hist({col_name: hist_dict["weekdays"]}, "base64", "weekdays")
                    hist_hour = plot_hist({col_name: hist_dict["hours"]}, "base64", "hours")
                    hist_minute = plot_hist({col_name: hist_dict["minutes"]}, "base64", "minutes")
                    hist_pic = {"hist_years": hist_year, "hist_months": hist_month, "hist_weekdays": hist_weekday,
                                "hist_hours": hist_hour, "hist_minutes": hist_minute}

                elif col["column_dtype"] == "int" or col["column_dtype"] == "string" or col["column_dtype"] == "decimal":
                    hist = plot_hist({col_name: hist_dict}, output="base64")
                    hist_pic = {"hist_numeric_string": hist}

            if "frequency" in col:
                freq_pic = plot_frequency({col_name: col["frequency"]}, output="base64")

            html = html + template.render(data=col, freq_pic=freq_pic, hist_pic=hist_pic)

        # Save in case we want to output to a html file
        self.html = html + df.table_html(10)

        # Display HTML
        print_html(self.html)

        # JSON
        # Save in case we want to output to a json file
        self.json = output

        # Save file in json format
        write_json(output, self.path)

    def to_image(self, output_path):
        """
        Save the profiler result as image
        :param self:
        :param output_path: path where the image will be saved
        :return:
        """
        css = absolute_path("/css/styles.css")
        imgkit.from_string(self.html, output_path, css=css)

        print_html("<img src='" + output_path + "'>")

    def to_file(self, path=None, output="html"):
        """
        Save profiler data to a file in the specified format (html, json)
        :param output: html or json
        :param path: filename in which the data will be saved
        :return:
        """

        if path is None:
            RaiseIt.value_error(path, "str")

        # We need to append a some extra html tags to display it correctly in the browser.
        if output is "html":
            if self.html is None:
                RaiseIt.not_ready_error(
                    "You must first run the profiler, then it can be exported. Try op.profiler.run(df, '*')")

            write_html(HEADER + self.html + FOOTER, path)
        elif output is "json":
            if self.json is None:
                RaiseIt.not_ready_error(
                    "You must first run the profiler, then it can be exported. Try op.profiler.run(df, '*')")

            write_json(self.json, path)
        else:

            RaiseIt.type_error(output, ["html", "json"])

    def to_json(self, df, columns="*", buckets=10, infer=False, relative_error=RELATIVE_ERROR, approx_count=True,
                sample=10000,
                dump=True):
        """
        Return the profiling data in json format
        :param df: Dataframe to be processed
        :param columns: column to calculate the histogram
        :param buckets: buckets on the histogram
        :param infer:
        :param relative_error:
        :param approx_count:
        :param sample: numbers of rows to retrieve with random sampling
        :param dump: return a json or a Python Object

        :return: json file
        """

        # Get the stats for all the columns
        output = self.columns(df, columns, buckets, infer, relative_error, approx_count)

        # Add the General data summary to the output
        cols_count = self.cols_count
        rows_count = self.rows_count

        dataset_info = {'cols_count': cols_count,
                        'rows_count': rows_count,
                        'size': humanize.naturalsize(df.size())}

        output["summary"].update(dataset_info)

        output["sample"] = {"columns": [{"title": cols} for cols in df.cols.names()],
                            "value": df.sample_n(sample).rows.to_list(columns)}

        if dump is True:
            output = json.dumps(output, ignore_nan=True, default=json_converter)
        return output

    def columns(self, df, columns, buckets=10, infer=False, relative_error=RELATIVE_ERROR, approx_count=True):
        """
        Return statistical information about a specific column in json format
        :param df: Dataframe to be processed
        :param columns: Columns that you want to profile
        :param buckets: Create buckets divided by range. Each bin is equal.
        :param infer: try to infer the column datatype
        :param relative_error: relative error when the percentile is calculated. 0 is more exact as slow 1 more error and faster
        :param approx_count: Use the function approx_count_distinct or countDistinct. approx_count_distinct is faster
        :return: json object
        """

        columns = parse_columns(df, columns)

        self.rows_count = df.count()
        self.cols_count = len(df.columns)

        # Initialize Objects
        columns_info = {}
        columns_info['columns'] = {}
        columns_info['name'] = df._name

        columns_info['rows_count'] = humanize.intword(self.rows_count)
        logger.print("Processing General Stats...")

        # Get columns data types. This is necessary to make the pertinent histogram calculations.
        count_dtypes = self._count_data_types(df, columns, infer)
        self.columns_dtypes = count_dtypes

        stats = self.general_stats(df, columns, buckets, relative_error, approx_count)

        columns_info["count_types"] = count_dtypes["count_types"]
        columns_info['size'] = humanize.naturalsize(df.size())

        # Cast columns to the data type infer by count_data_types()
        # df = Profiler.cast_columns(df, columns, count_dtypes).cache()

        frequency_cols = []
        for col_name in columns:
            if stats[col_name]["count_uniques"] <= HISTOGRAM_FREQUENCY_CHART_THRESHOLD:
                frequency_cols.append(col_name)

        # Calculate stats
        logger.print("Processing Frequency ...")
        freq = df.cols.frequency(frequency_cols, buckets, True, self.rows_count)

        # Missing
        total_count_na = 0
        for col_name in columns:
            total_count_na = total_count_na + stats[col_name]["count_na"]
        columns_info["summary"] = {}
        columns_info["summary"]['missing_count'] = total_count_na
        columns_info["summary"]['p_missing'] = round(total_count_na / self.rows_count * 100, 2)

        # Calculate percentage
        for col_name in columns:
            col_info = {}

            col_info["stats"] = stats[col_name]

            if freq is not None:
                if col_name in freq:
                    col_info["frequency"] = freq[col_name]

            col_info["stats"].update(self.extra_stats(df, col_name, stats))

            col_info['name'] = col_name
            col_info['column_dtype'] = count_dtypes["columns"][col_name]['dtype']
            col_info["dtypes_stats"] = count_dtypes["columns"][col_name]['details']
            col_info['column_type'] = count_dtypes["columns"][col_name]['type']

            columns_info['columns'][col_name] = {}
            columns_info['columns'][col_name] = col_info

        return columns_info

    def general_stats(self, df, columns, buckets=10, relative_error=RELATIVE_ERROR, approx_count=True):
        columns = parse_columns(df, columns)
        n = 30
        list_columns = [columns[i * n:(i + 1) * n] for i in range((len(columns) + n - 1) // n)]
        # we have problems sending +100 columns at the same time. Process in batch

        result = {}
        for i, cols in enumerate(list_columns):
            logger.print("Batch {BATCH_NUMBER}. Processing columns{COLUMNS}".format(BATCH_NUMBER=i, COLUMNS=cols))

            funcs = [count_uniques_agg]
            exprs = df.cols.create_exprs(cols, funcs, approx_count)

            # TODO: in basic calculations funcs = [F.min, F.max]
            funcs = [F.min, F.max, F.stddev, F.kurtosis, F.mean, F.skewness, F.sum, F.variance, zeros_agg]
            exprs.extend(df.cols.create_exprs(cols, funcs))

            # TODO: None in basic calculation
            funcs = [percentile_agg]
            exprs.extend(df.cols.create_exprs(cols, funcs, df, [0.05, 0.25, 0.5, 0.75, 0.95],
                                              relative_error))

            funcs = [count_na_agg]
            exprs.extend(df.cols.create_exprs(cols, funcs, df))
            result.update(df.cols.exec_agg(exprs))

        exprs = []
        n = 30
        result_hist = {}
        list_columns = [columns[i * n:(i + 1) * n] for i in range((len(columns) + n - 1) // n)]
        for i, cols in enumerate(list_columns):
            logger.print(
                "Batch Histogram {BATCH_NUMBER}. Processing columns{COLUMNS}".format(BATCH_NUMBER=i, COLUMNS=cols))

            funcs = [hist_agg]
            min_max = None

            for col_name in cols:

                if is_column_a(df, col_name, PYSPARK_NUMERIC_TYPES):
                    min_max = {"min": result[col_name]["min"], "max": result[col_name]["max"]}

                if result[col_name]["count_uniques"] > HISTOGRAM_FREQUENCY_CHART_THRESHOLD:
                    exprs.extend(df.cols.create_exprs(col_name, funcs, df, buckets, min_max))

            agg_result = df.cols.exec_agg(exprs)
            if agg_result is not None:
                result_hist.update(agg_result)

        # Merge results
        for col_name in result:
            if col_name in result_hist:
                result[col_name].update(result_hist[col_name])
        return result

    def extra_stats(self, df, col_name, stats):
        """
        Specific Stats for numeric columns
        :param df:
        :param col_name:
        :param stats:
        :return:
        """

        col_info = {}

        max_value = stats[col_name]["max"]
        min_value = stats[col_name]["min"]

        if is_column_a(df, col_name, PYSPARK_NUMERIC_TYPES):
            stddev = stats[col_name]['stddev']
            mean = stats[col_name]['mean']

            quantile = stats[col_name]["percentile"]
            if max_value is not None and min_value is not None:
                col_info['range'] = max_value - min_value
            else:
                col_info['range'] = None

            col_info['median'] = quantile["0.5"]

            q1 = quantile["0.25"]
            q3 = quantile["0.75"]

            if q1 is not None and q3 is not None:
                col_info['interquartile_range'] = q3 - q1
            else:
                col_info['interquartile_range'] = None

            if mean != 0 and mean is not None:
                col_info['coef_variation'] = round((stddev / mean), 5)
            else:
                col_info['coef_variation'] = None

            mad = df.cols.mad(col_name)
            if mad is not None:
                col_info['mad'] = round(df.cols.mad(col_name), 5)
            else:
                col_info['mad'] = None

        col_info['p_count_na'] = round((stats[col_name]['count_na'] * 100) / self.rows_count, 2)
        col_info['p_count_uniques'] = round((stats[col_name]['count_uniques'] * 100) / self.rows_count, 2)
        return col_info

    @staticmethod
    @time_it
    def cast_columns(df, columns, count_dtypes):
        """
        Cast column depending of inferred data type.
        :param df: Dataframe to be analyzed
        :param columns: Dataframe columns to be analyzed
        :param count_dtypes: String with columns and data types
        :return: Dataframe with casted columns
        """
        # Cast every column to a specific type to ensure the correct profiling
        # For example if we calculate the min or max of a string column with numeric values the result will be incorrect
        for col_name in columns:
            dtype = count_dtypes["columns"][col_name]['dtype']
            # Not force date type conversion, we can not trust that is going to be representative
            if dtype in ["string", "float", "int", "boolean"]:
                df = df.cols.cast(col_name, dtype)
        return df

    @staticmethod
    def missing_values(df, columns):
        """
        Rerturn the missing values columns statistics
        :param df: Dataframe to be analyzed
        :param columns: columns to be analyzed
        :return:
        """
        columns = parse_columns(df, columns)

        data = {}
        cols = {}
        rows_count = df.count()
        for col_name in columns:
            missing_count = df.cols.count_na(col_name)

            data[col_name] = {"missing": missing_count,
                              "%": str(round(missing_count / rows_count, 2)) + "%"}

        cols["data"] = data
        cols["count"] = rows_count

        plot_missing_values(cols)
