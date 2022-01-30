import pandas as pd


class ResultsSerializer():
    input_type = ''
    is_male_competition = True

    def __init__(
        self, input_type: str, is_male_competition: bool = True
    ) -> None:
        self.input_type = input_type
        self.is_male_competition = is_male_competition

    def main(self) -> None:
        raw_data = self.get_data()

        calculated_results = self.calculate_results(raw_data)

    def get_data(self, path: str = 'Decathlon.csv') -> pd.DataFrame:
        if self.input_type == 'csv':
            header_names = (
                'full_name',
                '100_metres',
                'long_jump',
                'shot_put',
                'high_jump',
                '400_metres',
                '110_metres_hurdles',
                'discus_throw',
                'pole_vault',
                'javelin_throw',
                '1500_metres'
            ) if self.is_male_competition else (
                'full_name',
                '100_metres',
                'discus_throw',
                'pole_vault',
                'javelin_throw',
                '400_metres',
                '100_metres_hurdles',
                'long_jump',
                'shot_put',
                'high_jump',
                '1500_metres'
            )

            raw_data = pd.read_csv(
                path, delimiter=';', header=0, names=header_names
            )

            return raw_data

    def validate_data(self, data: pd.DataFrame):
        pass

    def calculate_results(self, data: pd.DataFrame) -> pd.DataFrame:
        POINTS_SYSTEM = {
            '100_metres': {'A': 25.4347, 'B': 18, 'C': 1.81, 'event': 'track'},
            'long_jump': {'A': 0.14354, 'B': 220, 'C': 1.4, 'event': 'field'},
            'shot_put': {'A': 51.39, 'B': 1.5, 'C': 1.05, 'event': 'field'},
            'high_jump': {'A': 0.8465, 'B': 75, 'C': 1.42, 'event': 'field'},
            '400_metres': {'A': 1.53775, 'B': 82, 'C': 1.81, 'event': 'track'},
            '110_metres_hurdles': {'A': 5.74352, 'B': 28.5, 'C': 1.92,
                                   'event': 'track'},
            '100_metres_hurdles': {'A': 5.74352, 'B': 28.5, 'C': 1.92,
                                   'event': 'track'},
            'discus_throw': {'A': 12.91, 'B': 4, 'C': 1.1, 'event': 'field'},
            'pole_vault': {'A': 0.2797, 'B': 100, 'C': 1.35, 'event': 'field'},
            'javelin_throw': {'A': 10.14, 'B': 7, 'C': 1.08, 'event': 'field'},
            '1500_metres': {'A': 0.03768, 'B': 480, 'C': 1.85,
                            'event': 'track'}
        }

        total_points = 0

        for key in data.keys():


    def order_results(self, data: pd.DataFrame) -> pd.DataFrame:
        pass

    def export_results(self, data: pd.DataFrame):
        pass


if __name__ == '__main__':
    ResultsSerializer(input_type='csv').main()
