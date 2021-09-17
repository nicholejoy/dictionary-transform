import sys
import simplejson as json
import argparse


def read_data_from_stdin():
    json_string = ''
    for line in sys.stdin:
        json_string += line
    try:
        return json.loads(json_string)
    except json.errors.JSONDecodeError:
        raise NestedException("Incorrect input given. JSON Expected.")


class NestedException(Exception):
    def __init__(self, text):
        self.text = text
        self.code = 400
        super().__init__(text)


class NestedDict:
    def __init__(self, levels):
        if not levels:
            raise NestedException("Require at least one nesting level 0 given")
        self.json_input = []  # takes list of dictionaries
        self.levels = list(dict.fromkeys(levels))  # Accept only the first instance of a level
        self.data_dict = {}

    def add_next_key(self, levels, row_in_input):
        if not levels:
            leaf_list = [row_in_input]
            return leaf_list
        next_level = levels[0]
        try:
            key = row_in_input[next_level]
        except KeyError:
            raise NestedException('Input Json does not have complete data for {0} \n'.format(next_level))
        nested_dict = {
            key: self.add_next_key(levels[1:], {x: row_in_input[x] for x in row_in_input if x != next_level})}
        return nested_dict

    def combine_dicts(self, row_dict, data_dict):
        if isinstance(row_dict, list):
            for row in row_dict:
                if row not in data_dict:
                    data_dict.append(row)
            return
        for key, value in row_dict.items():
            if key in data_dict:
                self.combine_dicts(row_dict[key], data_dict[key])
            else:
                data_dict[key] = value

    def parse_rows(self):
        for row in self.json_input:
            row_dict = self.add_next_key(self.levels, row)
            self.combine_dicts(row_dict, self.data_dict)

    def set_data(self, data):
        self.json_input = data

    def get_data(self):
        return self.data_dict

    def __str__(self):
        return json.dumps(self.get_data(), indent=4)


def main():
    parser = argparse.ArgumentParser(description='Convert flat dictionary to nested dictionary')
    parser.add_argument('levels', nargs='*', help='column name of nested levels')
    args = parser.parse_args()
    nested_dict = NestedDict(args.levels)
    nested_dict.set_data(read_data_from_stdin())
    nested_dict.parse_rows()
    sys.stdout.write(str(nested_dict))


if __name__ == '__main__':
    main()
