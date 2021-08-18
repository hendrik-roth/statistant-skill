import os
import re
from functools import partial

import inflect
from mycroft import MycroftSkill, intent_file_handler
from word2number import w2n

from .exceptions import FileNotUniqueError, FunctionNotFoundError, ChartNotFoundError
from .filehandler import FileHandler
from .statistantcalc import StatistantCalc


class Statistant(MycroftSkill):
    def __init__(self):
        # init Skill
        super().__init__()

        # possible answers for adjustments of clusters
        self.cluster_adjustments = ['the title', 'the axis labels', 'the number of clusters']

        # possible answers for adjustments of charts
        self.chart_adjustments = ['the title', 'the axis labels', 'the color', 'the scale of the axis']

        # possible colors for charts
        self.colors = ['red', 'blue', 'green', 'brown', 'yellow', 'white', 'black', 'pink', 'cyan', 'magenta']

        # possible chart types
        self.chart_types = ["histogram",
                            "bar chart", "barchart", "bar plot", "barplot",
                            "line chart", "linechart", "line plot", "lineplot",
                            "box plot", "boxplot", "box chart", "boxchart",
                            "scatter plot", "scatterplot", "scatter chart", "scatterchart"]

        # init directory named "statistant/source_files" in home directory if it does not exists for reading files
        # init directory named "statistant/results" in home directory if it does not exists to save results
        # directory is for reading files
        parent_dir = os.path.expanduser("~")
        directories = ("statistant/source_files", "statistant/results")
        concat_root_path = partial(os.path.join, parent_dir)
        make_directory = partial(os.makedirs, exist_ok=True)
        for path_items in map(concat_root_path, directories):
            make_directory(path_items)

    def init_calculator(self, filename, func=None):
        """
        Function for initialising StatistantCalculator.

        Parameters
        ----------
        filename
            is filename of file on which calculation should be performed
        func
            function which should be performed

        Returns
        -------
        calc
            StatistantCalculator Object
        """
        calc = None
        try:
            file_handler = FileHandler(filename)
            calc = StatistantCalc(file_handler.content, filename, func)
        except FileNotFoundError:
            self.speak_dialog('FileNotFound.error', {'filename': filename})
        except FileNotUniqueError:
            self.speak_dialog('FileNotUnique.error', {'filename': filename})

        return calc

    def handle_basic_stats(self, message, func):
        """
        Function for performing basic statistical functions.
        This function contains extracting filename, col, lower and upper from utterance;
        reading the file with FileHandler and calculating specific function with StatistantCalc.

        Parameters
        ----------
        func
            Function which should be performed.
            Possible function names are: average, median, mode, variance, standard deviation, minimum, maximum, sum
        message
            User Utterance of intent

        Returns
        -------
        result
            Result of statistical calculation (one value)

        """
        result = None

        filename = message.data.get('file')
        col = message.data.get('colname').lower()
        lower = message.data.get('lower')
        upper = message.data.get('upper')

        if lower is not None:
            lower = w2n.word_to_num(lower)
            upper = w2n.word_to_num(upper)

        try:
            calc = self.init_calculator(filename)
            if lower is not None and upper is not None:
                result = calc.stats_basic(func, col, True, lower, upper)
            else:
                result = calc.stats_basic(func, col)

        except KeyError:
            self.speak_dialog('KeyError', {'colname': col, 'func': func})
        except IndexError:
            self.speak_dialog('IndexError', {'func': func})
        except FunctionNotFoundError:
            self.speak_dialog('FunctionNotFound.error', {'func': func})

        return result

    @intent_file_handler('mean.intent')
    def handle_mean(self, message):
        """
        Function for handling special mean intent.
        A user can ask Mycroft for calculating the average (mean) of 2 specific rows in a column of a file.

        Parameters
        ----------
        message
            Message Bus event information from the intent parser
        """
        func = "average"
        filename = message.data.get('file')
        col = message.data.get('colname').lower()

        try:
            calc = self.init_calculator(filename)

            first_val = w2n.word_to_num(message.data.get('first'))
            sec_val = w2n.word_to_num(message.data.get('second'))

            mean = calc.mean_2_cells(first_val, sec_val, col)

            self.speak_dialog('mean', {'avg': mean})

        except KeyError:
            self.speak_dialog('KeyError', {'colname': col, 'func': func})
        except IndexError:
            self.speak_dialog('IndexError', {'func': func})

    @intent_file_handler('basicstats.intent')
    def handle_statistical_basic(self, message):
        """
        function for handling statistical basic intent

        Parameters
        ----------
        message
            Message Bus event information from the intent parser
        """
        func = message.data.get('function')
        result = self.handle_basic_stats(message, func)
        if result is not None:
            self.speak_dialog('basicstats', {'function': func, 'result': result})

    @intent_file_handler('quantiles.intent')
    def handle_quantile(self, message):
        """
        function for handling quantiles.

        Parameters
        ----------
        message
            Message Bus event information from the intent parser
        """
        filename = message.data.get('file')
        col = message.data.get('colname').lower()
        result = None

        percentile_utterance = message.data.get('percentile')
        # fallback for first - ninth. Mycroft will not save 1st, 2nd, ... but "first", "second"...
        ordinal_helper = self.w2ordinal(percentile_utterance)
        percentile_text = ordinal_helper if ordinal_helper is not None else percentile_utterance
        percentile = int(re.findall(r'\d+', percentile_text)[0]) / 100

        lower = message.data.get('lower')
        upper = message.data.get('upper')

        if lower is not None:
            lower = w2n.word_to_num(lower)
            upper = w2n.word_to_num(upper)

        calc = self.init_calculator(filename)

        if not 0 < percentile < 1:
            # percentile has to be between 0 and 1
            self.speak_dialog('percentile.error')
        elif lower is not None and upper is not None:
            result = calc.quantiles(col, percentile, True, lower, upper)
        else:
            result = calc.quantiles(col, percentile)
        if result is not None:
            self.speak_dialog('quantiles', {'percentile': percentile, 'quantile': result})

    @staticmethod
    def w2ordinal(text):
        """
        Function for transforming a word like "first" into 1st.
        Works from "first" until "ninth"
        Parameters
        ----------
        text
            is the text which should be transformed

        Returns
        -------
        word_to_number_mapping[text]
            ordinal number of transformed text
        """
        p = inflect.engine()
        word_to_number_mapping = {}

        for i in range(1, 10):
            word_form = p.number_to_words(i)  # 1 -> 'one'
            ordinal_word = p.ordinal(word_form)  # 'one' -> 'first'
            ordinal_number = p.ordinal(i)  # 1 -> '1st'
            word_to_number_mapping[ordinal_word] = ordinal_number  # 'first': '1st'
        return word_to_number_mapping[text] if text in word_to_number_mapping.keys() else None

    def cluster_validator(self, response):
        """
        function to validate the possible adjustments for the cluster analysis

        Parameters
        -------
        response
            response from user

        Returns
        -------
        requested_adjustments
            requestet adjustments of user
        """

        requested_adjustments = []
        for adjustment in self.cluster_adjustments:
            if adjustment in response:
                requested_adjustments.append(adjustment)
        return requested_adjustments

    @intent_file_handler('cluster.intent')
    def handle_cluster(self, message):
        """
        function for handling cluster intent.
        A User can ask mycroft to create a cluster analysis with 2 columns.
        The User can do several adjustments on the cluster analysis.

        Parameters
        -------
        message
            Message Bus event information from the intent parser
        """
        # Init variables
        func = "clusteranalysis"
        filename = message.data.get('file')
        x_col = message.data.get('colname_x').lower()
        y_col = message.data.get('colname_y').lower()
        num_clusters = w2n.word_to_num(message.data.get('num_clusters'))

        title = None
        x_label = None
        y_label = None

        try:
            calc = self.init_calculator(filename, func)

            # ask if user wants to adjust something
            want_adjustment = self.ask_yesno('want.adjustments', {'function': func, 'more': ''})

            # if user asks, what he can adjust
            if want_adjustment == "what can i adjust":
                want_adjustment = self.ask_yesno('what.can.adjust', {'adjustments': 'the title, '
                                                                                    'the axis labels, '
                                                                                    'or the number of clusters'})
            # while user wants to adjust something
            while want_adjustment == "yes":
                adjustment = self.get_response('what.want.to.adjust',
                                               validator=self.cluster_validator,
                                               on_fail='adjustment.fail',
                                               data={'adjustments': 'the title, '
                                                                    'the axis labels or '
                                                                    'the number of clusters',
                                                     'optional': 'What would you like to adjust?'}, num_retries=2)
                if adjustment == "the title":
                    title = self.get_response('name.title')
                elif adjustment == "the axis labels":
                    x_label = self.get_response('name.x_axis.label')
                    y_label = self.get_response('name.y_axis.label')
                elif adjustment == "the number of clusters":
                    num_clusters = w2n.word_to_num(self.get_response('name.number.clusters'))
                else:
                    self.speak_dialog('adjustment.fail', {'adjustments': 'the title, '
                                                                         'the axis labels or '
                                                                         'the number of clusters',
                                                          'optional': ''})

                want_adjustment = self.ask_yesno('want.adjustments', {'function': func, 'more': 'more'})

            # if user don´t wants to adjust something
            if want_adjustment == "no":
                calc.cluster(x_col, y_col, num_clusters, title, x_label, y_label)
            else:
                self.speak_dialog('could.not.understand')
                calc.cluster(x_col, y_col, num_clusters, title, x_label, y_label)

            self.speak_dialog('cluster', {'colname_x': x_col,
                                          'colname_y': y_col,
                                          'file': filename,
                                          'num_clusters': num_clusters})

        # Error handling
        except KeyError:
            self.speak_dialog('KeyError', {'colname': f"{x_col} or {y_col}", 'func': func})

    def charts_validator(self, response):
        """
        function to validate the possible adjustments for the charts

        Parameters
        -------
        response
            response from user

        Returns
        -------
        requested_adjustments
            requestet adjustments of user
        """

        requested_adjustments = []
        for adjustment in self.chart_adjustments:
            if adjustment in response:
                requested_adjustments.append(adjustment)
        return requested_adjustments

    def color_validator(self, response):
        """
        function to validate the possible colors for seaborn plots

        Parameters
        -------
        response
            response from user

        Returns
        -------
        colors
            requestet colors of user
        """

        requested_colors = []
        for color in self.colors:
            if color in response:
                requested_colors.append(color)
        return requested_colors

    @intent_file_handler('charts.intent')
    def handle_charts(self, message):
        """
        Function for performing chart visualizations.
        This function contains extracting filename, columns and adjustments;
        reading the file with FileHandler and calculating specific charts.

        Parameters
        ----------
        message
            Message Bus event information from the intent parser
        """

        func = "clusteranalysis"
        filename = message.data.get('file')
        x_col = message.data.get('colname_x').lower()

        title = None
        x_label = None
        y_label = None
        x_lim = None
        y_lim = None
        color = None

        if message.data.get('colname_y') is None:
            y_col = None
        else:
            y_col = message.data.get('colname_y').lower()

        chart_type = message.data.get('chart_type').lower()

        if chart_type in self.chart_types:

            try:
                calc = self.init_calculator(filename, func)

                # ask if user wants to adjust something
                want_adjustment = self.ask_yesno('want.adjustments', {'function': chart_type, 'more': ''})

                # if user asks, what he can adjust
                if want_adjustment == "what can i adjust":
                    want_adjustment = self.ask_yesno('what.can.adjust', {'adjustments': 'the title, '
                                                                                        'the axis labels, '
                                                                                        'the color or '
                                                                                        'the scale of the axis'})

                while want_adjustment == "yes":
                    adjustment = self.get_response('what.want.to.adjust',
                                                   validator=self.charts_validator,
                                                   on_fail='adjustment.fail',
                                                   data={'adjustments': 'the title, '
                                                                        'the axis labels, '
                                                                        'the color or '
                                                                        'the scale of the axis',
                                                         'optional': 'What would you like to adjust?'}, num_retries=2)
                    if adjustment == "the title":
                        title = self.get_response('name.title')
                    elif adjustment == "the axis labels":
                        x_label = self.get_response('name.x_axis.label')
                        y_label = self.get_response('name.y_axis.label')
                    elif adjustment == "the color":
                        color = self.get_response('name.color', {'chart_type': chart_type},
                                                  validator=self.color_validator,
                                                  on_fail='color.fail',
                                                  num_retries=2)
                    elif adjustment == "the scale of the axis":
                        # todo: scale axis adjustment
                        pass
                    else:
                        self.speak_dialog('adjustment.fail', {'adjustments': 'the title, '
                                                                             'the axis labels, '
                                                                             'the color or '
                                                                             'the scale of the axis',
                                                              'optional': ''})

                    want_adjustment = self.ask_yesno('want.adjustments', {'function': chart_type, 'more': 'more'})

                if want_adjustment == "no":
                    calc.charts(chart_type, x_col, y_col, title, x_label, y_label, x_lim, y_lim, color)
                else:
                    self.speak_dialog('could.not.understand')
                    calc.charts(chart_type, x_col, y_col, title, x_label, y_label, x_lim, y_lim, color)

                if y_col is None:
                    self.speak_dialog('charts.one.column', {'chart_type': chart_type,
                                                            'colname_x': x_col,
                                                            'file': filename})
                else:
                    self.speak_dialog('charts', {'chart_type': chart_type,
                                                 'colname_x': x_col,
                                                 'colname_y': y_col,
                                                 'file': filename})

            # Error handling
            except KeyError:
                self.speak_dialog('KeyError', {'colname': f"{x_col} or {y_col}", 'func': func})
            except ChartNotFoundError:
                self.speak_dialog('ChartNotFound.error', {'chart_type': chart_type})
        else:
            self.speak_dialog('ChartNotFound.error', {'chart_type': chart_type})


def create_skill():
    return Statistant()
