'Dictionary Transform' takes a flat dictionary as input and transforms the data into a nested dictionary. 

Dictionary Transform stored a single data source for each user. The data can be transformed multiple times, overwriting the previously transformed dictionary.  

Requirements: 
Mongodb listening on port 27017

To transform data using the python script pass json data from a file and provide the nesting levels as arguments:
cat ../test/test_input.json |  python nested_dict.py currency country


API usage: 

To upload data:
curl -u example_user:example_password -X POST -F file=@test_input.json http://127.0.0.1:5000/input
To transform data, provide the nested keys as levels:
curl -H "Content-Type: application/json"  -X POST -d '{"levels": ["currency", "city"]}' -u example_user:example_password http://127.0.0.1:5000/transform
To get transformed dictionary:
curl -u example_user:example_password  -X GET http://127.0.0.1:5000/output

Unit tests:
python -m test_dict_transform
