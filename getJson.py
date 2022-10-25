import json
if __name__ == '__main__':
  project_branches ="""{
      "branches": [
          {
              "name": "master",
              "isMain": true,
              "type": "BRANCH",
              "status": {},
              "excludedFromPurge": true
          }
      ]
  }"""

  print("Checking if percentage key exists in JSON")
  result = json.loads(project_branches)
  element = "branches"
  x = getJson("branches", result)
  y = getJson("name", result["branches"][0])
  print(y)
