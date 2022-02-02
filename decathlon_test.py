import csv
import unittest
from decathlon import (CompetitionDataReceiver, ResultsProcessor,
                       ResultsSerializer)


class TestCompetitionDataReceiver(unittest.TestCase):
    """Test if CompetitionDataReceiver class returns correct results"""

    def setUp(self) -> None:
        """create a class instance"""
        self.receiver = CompetitionDataReceiver(True)
        self.receiver.set_csv_data('Decathlon.csv')

    def test_same_amount_of_data(self) -> None:
        """Whether csv file contains same amount of data"""
        with open('Decathlon.csv', mode='r') as file:
            self.csv_reader = csv.reader(
                file, delimiter=';'
            )

            self.assertEqual(
                sum(1 for _ in self.csv_reader), len(self.receiver.get_data())
            )

    def test_list_of_dicts_returned(self) -> None:
        """Whether returned data type is a list of dicts"""
        data = self.receiver.get_data()
        self.assertIsInstance(data, list)

        for competitor in data:
            self.assertIsInstance(competitor, dict)


class TestResultsProcessor(unittest.TestCase):
    """Test results processor is correctly calculating and ordering results"""

    def setUp(self) -> None:
        """process default data"""
        competition_data_receiver = CompetitionDataReceiver(True)
        competition_data_receiver.set_csv_data('Decathlon.csv')
        competition_data = competition_data_receiver.get_data()

        results_processor = ResultsProcessor(competition_data)
        self.results = results_processor.get_processed_results()

    def test_results_are_in_accending_order(self):
        """Whether the points are in descending order"""
        competitor_points = [
            competitor['points'] for competitor in self.results
        ]
        self.assertListEqual(
            competitor_points, sorted(competitor_points, reverse=True)
        )

    def test_correct_result(self) -> None:
        """Test if correct amount of points calculated"""
        points_to_test = [
            4200, 4200, 4200, 4200, 3494, 3199, 3199, 3199, 3199, 3099, 3099
        ]

        competitor_points = [
            competitor['points'] for competitor in self.results
        ]

        self.assertListEqual(
            points_to_test, competitor_points
        )
