# -*- coding: utf-8 -*-
"""
Module with the logic for the FamilyData sub-process

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from source.util import Assertor, Profiling, Tracking, Debugger

from .engine import Process, InputOperation, Signal, Extract, \
    Restructure, RestructurePois, Multiplex, OutputOperation, \
    RestructureRatings


class FinnFamilyDataProcessing(Process):
    """
    Implementation of processing of family statistics

    """

    @Tracking
    def __init__(self, family_data: dict):
        """
        Constructor / Instantiate the class.

        Parameters
        ----------
        family_data      : dict
                           dict with family statistics

        """
        super().__init__(name=self.__class__.__name__)
        self.start_process()
        self.input_operation(family_data)

        self.run_parallel([self.extract_1, self.extract_2, self.extract_3,
                           self.extract_4, self.extract_5, self.extract_6,
                           self.extract_7, self.extract_8])

        self.run_parallel([self.extract_9, self.restructure_1, self.restructure_2,
                           self.extract_10, self.restructure_3, self.extract_11,
                           self.restructure_4])

        self.run_parallel([self.multiplex_1, self.multiplex_2])
        self.run_parallel([self.restructure_5, self.restructure_6])

        self.multiplex_3()
        self.family_statistics = self.output_operation()
        self.end_process()

    @Profiling
    @Tracking
    def input_operation(self, data: object):
        """
        initial operation of the process

        """
        Assertor.assert_data_types([data], [dict])
        input_operation = InputOperation("Family Statistics")
        self.add_node(input_operation)

        input_signal = Signal(data, desc="Family Statistics", prettify_keys=True, length=6)
        self.add_signal(input_signal, "input_signal")
        self.add_transition(input_operation, input_signal)

    @Profiling
    @Debugger
    def extract_1(self):
        """
        method for extracting families with children shares

        """
        try:
            input_signal_family = self.get_signal("input_signal")
            families_with_children_operation = Extract(input_signal_family.data,
                                                       "families_with_children")
            self.add_node(families_with_children_operation)
            self.add_transition(input_signal_family, families_with_children_operation,
                                label="thread")
            families_with_children = families_with_children_operation.run()
            families_with_children_signal = Signal(families_with_children,
                                                   "Distribution of Families with Children")
            self.add_signal(families_with_children_signal, "families_with_children")
            self.add_transition(families_with_children_operation, families_with_children_signal,
                                label="thread")
        except Exception as extract_exception:
            self.exception_queue.put(extract_exception)

    @Profiling
    @Debugger
    def extract_2(self):
        """
        method for extracting age distribution of children

        """
        try:
            input_signal_family_dist = self.get_signal("input_signal")
            age_distribution_children_operation = Extract(input_signal_family_dist.data,
                                                          "age_distribution_children")
            self.add_node(age_distribution_children_operation)
            self.add_transition(input_signal_family_dist, age_distribution_children_operation,
                                label="thread")
            age_distribution_children = age_distribution_children_operation.run()
            age_distribution_children_signal = Signal(age_distribution_children,
                                                      "Age Distribution of Children")
            self.add_signal(age_distribution_children_signal, "age_distribution_children")
            self.add_transition(age_distribution_children_operation,
                                age_distribution_children_signal, label="thread")
        except Exception as extract_exception:
            self.exception_queue.put(extract_exception)

    @Profiling
    @Debugger
    def extract_3(self):
        """
        method for extracting high schools

        """
        try:
            input_signal_schools = self.get_signal("input_signal")
            schools_operation = Extract(input_signal_schools.data, "schools")
            self.add_node(schools_operation)
            self.add_transition(input_signal_schools, schools_operation, label="thread")
            schools = schools_operation.run()
            schools_signal = Signal(schools, "List of Schools")
            self.add_signal(schools_signal, "schools")
            self.add_transition(schools_operation, schools_signal, label="thread")
        except Exception as extract_exception:
            self.exception_queue.put(extract_exception)

    @Profiling
    @Debugger
    def extract_4(self):
        """
        method for extracting school ratings

        """
        try:
            input_signal_rating_schools = self.get_signal("input_signal")
            rating_school_operation = Extract(input_signal_rating_schools.data, "rating_schools")
            self.add_node(rating_school_operation)
            self.add_transition(input_signal_rating_schools, rating_school_operation,
                                label="thread")
            ratings = rating_school_operation.run()
            rating_school_signal = Signal(ratings, "Schools Rating")
            self.add_signal(rating_school_signal, "rating_schools")
            self.add_transition(rating_school_operation, rating_school_signal, label="thread")
        except Exception as extract_exception:
            self.exception_queue.put(extract_exception)

    @Profiling
    @Debugger
    def extract_5(self):
        """
        method for extracting kindergarten

        """
        try:
            input_signal_kindergardens = self.get_signal("input_signal")
            kindergarten_operation = Extract(input_signal_kindergardens.data, "kindergardens")
            self.add_node(kindergarten_operation)
            self.add_transition(input_signal_kindergardens, kindergarten_operation, label="thread")
            kindergarten = kindergarten_operation.run()
            kindergarten_signal = Signal(kindergarten, "List of Kindergartens")
            self.add_signal(kindergarten_signal, "kindergardens")
            self.add_transition(kindergarten_operation, kindergarten_signal, label="thread")
        except Exception as extract_exception:
            self.exception_queue.put(extract_exception)

    @Profiling
    @Debugger
    def extract_6(self):
        """
        method for extracting kindergarten ratings

        """
        try:
            input_signal_rating_kindergarden = self.get_signal("input_signal")
            kindergarten_ratings_operation = Extract(input_signal_rating_kindergarden.data,
                                                     "rating_kindergardens")
            self.add_node(kindergarten_ratings_operation)
            self.add_transition(input_signal_rating_kindergarden, kindergarten_ratings_operation,
                                label="thread")
            kindergarten_ratings = kindergarten_ratings_operation.run()
            kindergarten_ratings_signal = Signal(kindergarten_ratings, "Kindergarden Rating")
            self.add_signal(kindergarten_ratings_signal, "rating_kindergardens")
            self.add_transition(kindergarten_ratings_operation, kindergarten_ratings_signal,
                                label="thread")
        except Exception as extract_exception:
            self.exception_queue.put(extract_exception)

    @Profiling
    @Debugger
    def extract_7(self):
        """
        method for extracting high schools

        """
        try:
            input_signal_high_schools = self.get_signal("input_signal")
            highschools_operation = Extract(input_signal_high_schools.data, "highschools")
            self.add_node(highschools_operation)
            self.add_transition(input_signal_high_schools, highschools_operation, label="thread")
            highschools = highschools_operation.run()
            highschools_signal = Signal(highschools, "List of High Schools")
            self.add_signal(highschools_signal, "highschools")
            self.add_transition(highschools_operation, highschools_signal, label="thread")
        except Exception as extract_exception:
            self.exception_queue.put(extract_exception)

    @Profiling
    @Debugger
    def extract_8(self):
        """
        method for extracting family composition

        """
        try:
            input_signal_family_comp = self.get_signal("input_signal")
            family_composition_operation = Extract(input_signal_family_comp.data,
                                                   "family_composition")
            self.add_node(family_composition_operation)
            self.add_transition(input_signal_family_comp, family_composition_operation,
                                label="thread")
            family_composition = family_composition_operation.run()

            family_composition_signal = Signal(family_composition, "Family Composition")
            self.add_signal(family_composition_signal, "family_composition")
            self.add_transition(family_composition_operation, family_composition_signal,
                                label="thread")
        except Exception as extract_exception:
            self.exception_queue.put(extract_exception)

    @Profiling
    @Debugger
    def extract_9(self):
        """
        method for extracting families with children shares

        """
        try:
            families_with_children = self.get_signal("families_with_children")

            families_with_children_operation = Extract(
                families_with_children.data["families_with_children"], "values")
            self.add_node(families_with_children_operation)
            self.add_transition(families_with_children, families_with_children_operation,
                                label="thread")

            families_with_children_rest = {
                "families_with_children": families_with_children_operation.run()["values"]}

            families_with_children_rest_signal = Signal(families_with_children_rest,
                                                        "Shares of Families with Children")
            self.add_signal(families_with_children_rest_signal, "families_with_children_rest")

            self.add_transition(families_with_children_operation,
                                families_with_children_rest_signal, label="thread")
        except Exception as extract_exception:
            self.exception_queue.put(extract_exception)

    @Profiling
    @Debugger
    def restructure_1(self):
        """
        method for restructuring age distribution of children

        """
        try:
            age_distribution_children = self.get_signal("age_distribution_children")
            age_distribution_children_rest_operation = Restructure(
                age_distribution_children.data["age_distribution_children"],
                "Restructure Age Distribution of Children")
            self.add_node(age_distribution_children_rest_operation)
            self.add_transition(age_distribution_children, age_distribution_children_rest_operation,
                                label="thread")

            age_distribution_children_rest = age_distribution_children_rest_operation.run()

            age_distribution_children_rest_signal = Signal(
                age_distribution_children_rest, "Restructured Age Distribution of Children")
            self.add_signal(age_distribution_children_rest_signal, "age_distribution_children_rest")

            self.add_transition(age_distribution_children_rest_operation,
                                age_distribution_children_rest_signal, label="thread")
        except Exception as restructuring_exception:
            self.exception_queue.put(restructuring_exception)

    @Profiling
    @Debugger
    def restructure_2(self):
        """
        method for restructuring schools

        """
        try:
            schools = self.get_signal("schools")

            schools_rest_operation = RestructurePois(schools.data["schools"],
                                                     "Restructure List of Schools")
            self.add_node(schools_rest_operation)
            self.add_transition(schools, schools_rest_operation, label="thread")

            schools_rest = schools_rest_operation.run()

            schools_rest_signal = Signal(schools_rest, "Restructured List of Schools")
            self.add_signal(schools_rest_signal, "schools_rest")

            self.add_transition(schools_rest_operation, schools_rest_signal, label="thread")
        except Exception as restructuring_exception:
            self.exception_queue.put(restructuring_exception)

    @Profiling
    @Debugger
    def extract_10(self):
        """
        method for extracting school score

        """
        try:
            ratings_schools = self.get_signal("rating_schools")
            if ratings_schools.data:
                ratings_operation = Extract(ratings_schools.data["rating_schools"], "score")
                self.add_node(ratings_operation)
                self.add_transition(ratings_schools, ratings_operation, label="thread")

                ratings = {"rating_schools": ratings_operation.run()["score"]}

                ratings_signal = Signal(ratings, "Ratings Score of School")
                self.add_signal(ratings_signal, "score_schools")
                self.add_transition(ratings_operation, ratings_signal, label="thread")
            else:
                ratings = {"rating_schools": {"text": "", "neighborhood": "", "city": "",
                                              "cityName": "", "cityText": ""}}
                ratings_signal = Signal(ratings, "Ratings Score of School")
                self.add_signal(ratings_signal, "score_schools")
                self.add_transition(ratings_schools, ratings_signal, label="thread")
        except Exception as restructuring_exception:
            self.exception_queue.put(restructuring_exception)

    @Profiling
    @Debugger
    def restructure_3(self):
        """
        method for restructuring kindergartens

        """
        try:
            kindergartens = self.get_signal("kindergardens")

            kindergartens_rest_operation = RestructurePois(kindergartens.data["kindergardens"],
                                                           "Restructure List of Kindergartens")
            self.add_node(kindergartens_rest_operation)
            self.add_transition(kindergartens, kindergartens_rest_operation, label="thread")

            kindergartens_rest = kindergartens_rest_operation.run()

            kindergartens_rest_signal = Signal(kindergartens_rest,
                                               "Restructured List of Kindergartens")
            self.add_signal(kindergartens_rest_signal, "kindergardens_rest")

            self.add_transition(kindergartens_rest_operation, kindergartens_rest_signal,
                                label="thread")
        except Exception as restructuring_exception:
            self.exception_queue.put(restructuring_exception)

    @Profiling
    @Debugger
    def extract_11(self):
        """
        method for extracting kindergarten score

        """
        try:
            ratings_kindergarten = self.get_signal("rating_kindergardens")

            if ratings_kindergarten.data:
                ratings_operation = Extract(ratings_kindergarten.data["rating_kindergardens"],
                                            "score")
                self.add_node(ratings_operation)
                self.add_transition(ratings_kindergarten, ratings_operation, label="thread")

                ratings = {"rating_kindergardens": ratings_operation.run()["score"]}

                ratings_signal = Signal(ratings, "Ratings Score of Kindergartens")
                self.add_signal(ratings_signal, "score_kindergardens")
                self.add_transition(ratings_operation, ratings_signal, label="thread")
            else:
                ratings = {"rating_kindergardens": {"text": "", "neighborhood": "", "city": "",
                                                    "cityName": "", "cityText": ""}}
                ratings_signal = Signal(ratings, "Ratings Score of Kindergartens")
                self.add_signal(ratings_signal, "score_kindergardens")
                self.add_transition(ratings_kindergarten, ratings_signal, label="thread")
        except Exception as restructuring_exception:
            self.exception_queue.put(restructuring_exception)

    @Profiling
    @Debugger
    def restructure_4(self):
        """
        method for restructuring high schools

        """
        try:
            highschools = self.get_signal("highschools")

            highschools_rest_operation = RestructurePois(highschools.data["highschools"],
                                                         "Restructure List of High Schools")
            self.add_node(highschools_rest_operation)
            self.add_transition(highschools, highschools_rest_operation, label="thread")

            highschools_rest = highschools_rest_operation.run()

            highschools_rest_signal = Signal(highschools_rest,
                                             "Restructured List of High Schools")
            self.add_signal(highschools_rest_signal, "highschools_rest")

            self.add_transition(highschools_rest_operation, highschools_rest_signal,
                                label="thread")
        except Exception as restructuring_exception:
            self.exception_queue.put(restructuring_exception)

    @Profiling
    @Debugger
    def multiplex_1(self):
        """
        method for multiplexing all ratings statistics

        """
        try:
            score_kindergardens = self.get_signal("score_kindergardens")
            score_schools = self.get_signal("score_schools")

            multiplex_operation = Multiplex([score_kindergardens, score_schools],
                                            "Multiplex Ratings Information")
            self.add_node(multiplex_operation)
            self.add_transition(score_kindergardens, multiplex_operation, label="thread")
            self.add_transition(score_schools, multiplex_operation, label="thread")

            multiplex = {"ratings": multiplex_operation.run()}

            multiplex_signal = Signal(multiplex, "Multiplexed Ratings")
            self.add_signal(multiplex_signal, "ratings_multiplex")
            self.add_transition(multiplex_operation, multiplex_signal, label="thread")
        except Exception as multiplex_exception:
            self.exception_queue.put(multiplex_exception)

    @Profiling
    @Debugger
    def multiplex_2(self):
        """
        method for multiplexing family composition statistics

        """
        try:
            family_composition = self.get_signal("family_composition")
            families_with_children_rest = self.get_signal("families_with_children_rest")

            multiplex_operation = Multiplex([family_composition, families_with_children_rest],
                                            "Multiplex Composition Statistics")
            self.add_node(multiplex_operation)
            self.add_transition(family_composition, multiplex_operation, label="thread")
            self.add_transition(families_with_children_rest, multiplex_operation, label="thread")

            multiplex = multiplex_operation.run()
            multiplex["family_composition"]["values"].append(
                {"group": "Familier med barn",
                 "percent": multiplex.copy()["families_with_children"]})
            multiplex.pop("families_with_children")

            multiplex_signal = Signal(multiplex, "Multiplexed Composition Statistics")
            self.add_signal(multiplex_signal, "multiplex_composition")
            self.add_transition(multiplex_operation, multiplex_signal, label="thread")
        except Exception as multiplex_exception:
            self.exception_queue.put(multiplex_exception)

    @Profiling
    @Debugger
    def restructure_5(self):
        """
        method for restructuring family composition

        """
        try:
            composition_statistics = self.get_signal("multiplex_composition")

            composition_rest_operation = Restructure(
                composition_statistics.data["family_composition"],
                "Restructure Composition Statistics")
            self.add_node(composition_rest_operation)
            self.add_transition(composition_statistics, composition_rest_operation, label="thread")

            composition_rest = composition_rest_operation.run()

            composition_rest_signal = Signal(composition_rest,
                                             "Restructured Composition Statistics")
            self.add_signal(composition_rest_signal, "composition_rest")

            self.add_transition(composition_rest_operation, composition_rest_signal, label="thread")
        except Exception as restructuring_exception:
            self.exception_queue.put(restructuring_exception)

    @Profiling
    @Debugger
    def restructure_6(self):
        """
        method for restructuring ratings statistics

        """
        try:
            ratings = self.get_signal("ratings_multiplex")
            restructure_ratings_operation = RestructureRatings(
                ratings.data["ratings"], "Restructuring Family Rating Information")
            self.add_node(restructure_ratings_operation)
            self.add_transition(ratings, restructure_ratings_operation, label="thread")

            restructure_ratings = {"family_rating": restructure_ratings_operation.run()}
            restructure_ratings_signal = Signal(restructure_ratings,
                                                "Restructured Family Rating Information")

            self.add_signal(restructure_ratings_signal, "family_ratings")
            self.add_transition(restructure_ratings_operation, restructure_ratings_signal,
                                label="thread")
        except Exception as restructuring_exception:
            self.exception_queue.put(restructuring_exception)

    @Profiling
    @Debugger
    def multiplex_3(self):
        """
        method for multiplexing all family statistics to one dict

        """
        age_distribution_children_rest = self.get_signal("age_distribution_children_rest")
        schools_rest = self.get_signal("schools_rest")
        ratings = self.get_signal("family_ratings")
        kindergardens_rest = self.get_signal("kindergardens_rest")
        highschools_rest = self.get_signal("highschools_rest")
        composition_rest = self.get_signal("composition_rest")

        multiplex_operation = Multiplex(
            [age_distribution_children_rest, schools_rest, ratings, kindergardens_rest,
             highschools_rest, composition_rest], "Multiplex Family Statistics")

        self.add_node(multiplex_operation)
        self.add_transition(age_distribution_children_rest, multiplex_operation)
        self.add_transition(ratings, multiplex_operation)
        self.add_transition(schools_rest, multiplex_operation)
        self.add_transition(kindergardens_rest, multiplex_operation)
        self.add_transition(highschools_rest, multiplex_operation)
        self.add_transition(composition_rest, multiplex_operation)

        multiplex = multiplex_operation.run()
        multiplex_signal = Signal(multiplex, "Multiplexed Family Statistics", prettify_keys=True,
                                  length=6)
        self.add_signal(multiplex_signal, "multiplex_family_statistics")
        self.add_transition(multiplex_operation, multiplex_signal)

    @Profiling
    @Debugger
    def output_operation(self):
        """
        final operation of the process

        """
        multiplexed_family_statistics = self.get_signal("multiplex_family_statistics")
        output_operation = OutputOperation("Processed Family Statistics")
        self.add_node(output_operation)
        self.add_transition(multiplexed_family_statistics, output_operation)
        self.print_pdf()

        return multiplexed_family_statistics.data
