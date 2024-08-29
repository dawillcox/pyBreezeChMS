import breeze_chms_api.breeze
import json
# from breeze import ENDPOINTS

api = breeze_chms_api.breeze.breeze_api()
   # def _request(self,
   #               endpoint: ENDPOINTS,
   #               command: str = '',
   #               params: Mapping[str, Union[str, int, float, Mapping, Sequence]]
   #               = dict(),
   #               headers: dict = dict(),
   #               timeout: int = 60,
   #               ):

# f = api._request(ENDPOINTS.HISTORY, 'list')
# f = api.list_people(limit=1)

# f = api.list_contributions(start='2024-07-14', end='2024-07-14', person_id=32963302)
f = api.list_funds()

print(json.dumps(f, indent=2))
