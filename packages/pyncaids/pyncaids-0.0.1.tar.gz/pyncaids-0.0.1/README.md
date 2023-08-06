# pyncaids

National Competent Authority (NCA) identifiers as a Python module

```python
import pyncaids

nca = pyncaids.NCA()

authority_list = nca.nca_by_authority_id("GB-FCA")
>>> [{'authority_id': 'GB-FCA', 'country': 'United Kingdom', 'authority_name': 'Financial Conduct Authority'}]

authority_list = nca.nca_by_partial_authority_id("FM")
>>> [{'authority_id': 'AT-FMA', 'country': 'Austria', 'authority_name': 'Austria Financial Market Authority'},
>>>  {'authority_id': 'IS-FME', 'country': 'Iceland', 'authority_name': 'Financial Supervisory Authority'},
>>>  {'authority_id': 'LI-FMA', 'country': 'Liechtenstein', 'authority_name': 'Financial Market Authority Liechtenstein'}]

authority_list = nca.nca_by_country("United Kingdom")
>>> [{'authority_id': 'GB-FCA', 'country': 'United Kingdom', 'authority_name': 'Financial Conduct Authority'}]

authority_list = nca.nca_by_partial_country("it")
>>> [{'authority_id': 'LT-BL', 'country': 'Lithuania', 'authority_name': 'Bank of Lithuania'},
>>>  {'authority_id': 'GB-FCA', 'country': 'United Kingdom', 'authority_name': 'Financial Conduct Authority'}]

authority_list = nca.nca_by_authority_name("Financial Conduct Authority")
>>> [{'authority_id': 'GB-FCA', 'country': 'United Kingdom', 'authority_name': 'Financial Conduct Authority'}]

authority_list = nca.nca_by_partial_authority_name("Supervisory Authority")
>>> [{'authority_id': 'DK-DFSA', 'country': 'Denmark', 'authority_name': 'Danish Financial Supervisory Authority'},
>>>  {'authority_id': 'EE-FI', 'country': 'Estonia', 'authority_name': 'Estonia Financial Supervisory Authority'},
>>>  {'authority_id': 'FI-FINFSA', 'country': 'Finland', 'authority_name': 'Finnish Financial Supervisory Authority'},
>>>  {'authority_id': 'DE-BAFIN', 'country': 'Germany', 'authority_name': 'Federal Financial Supervisory Authority'},
>>>  {'authority_id': 'IS-FME', 'country': 'Iceland', 'authority_name': 'Financial Supervisory Authority'},
>>>  {'authority_id': 'NO-FSA', 'country': 'Norway', 'authority_name': 'The Financial Supervisory Authority of Norway'}]
```

Source: EBA