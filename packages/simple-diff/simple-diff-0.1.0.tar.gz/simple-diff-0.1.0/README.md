# simple_diff
A simple diff tool for dictionary and list

```python
>>> import simple_diff
>>> old_dict = {'a':1, 'b':2, 'c':3, 'd':4}
>>> new_dict = {'b':1, 'c':3, 'd':4, 'e':5}    
>>> 
>>> simple_diff.dict_diff(old_dict, new_dict)
{
  'created': [{'key': 'e', 'value': 5}], 
  'deleted': [{'key': 'a', 'value': 1}], 
  'unchanged': [{'key': 'd', 'value': 4}, {'key': 'c', 'value': 3}], 
  'modified': [{'old': {'key': 'b', 'value': 2}, 'new': {'key': 'b', 'value': 1}}]
}
>>> 
>>> old_list = [{'index':1, 'name': 'bob'}, {'index':2, 'name': 'john'}, {'index':3, 'name': 'tom'}]
>>> new_list = [{'index':2, 'name': 'john'}, {'index':3, 'name': 'kevin'}, {'index':4, 'name': 'mary'}]
>>> simple_diff.list_diff(old_list, new_list, key= 'index')             
{
  'created': [{'index': 4, 'name': 'mary'}], 
  'deleted': [{'index': 1, 'name': 'bob'}], 
  'unchanged': [{'index': 2, 'name': 'john'}], 
  'modified': [{'old': {'index': 3, 'name': 'tom'}, 'new': {'index': 3, 'name': 'kevin'}}]
}
```
