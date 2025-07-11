from pymongo import MongoClient
import pandas as pd

from config.app import Config

class MongoDBService:
    def __init__(self, config: Config):
        self.client = MongoClient(config.mongodb.srv)
        self.business_db = self.client["eiBusiness"]
        self.accounts_db = self.client["eiAccounts"]

    def list_accounts(self):
        accounts_col = self.accounts_db["accounts"]

        pipeline = [
            {
                "$match": {
                    "isBuyer": True,
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "accountId": 1,
                    "categories": 1,
                    "subcategories": 1,
                    "origin": 1,
                    "channel": 1,
                    "source": 1,
                    "operation": 1,
                    "createdAt": 1,
                    "requirementOdooCode": 1,
                    "odooRequirementCode": 1,
                    "requirementVid": 1,
                }
            }
        ]

        result = list(accounts_col.aggregate(pipeline))
        return pd.DataFrame(result)

    def list_requirements(self):
        requirements_col = self.business_db["requirements"]

        pipeline = [
            {
                "$match": {
                    "operation": { "$ne": "backlog" },
                    "requirementVid": { "$exists": True, "$nin": [None, ''] }
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "accountId": 1,
                    "categories": 1,
                    "subcategories": 1,
                    "origin": 1,
                    "channel": 1,
                    "source": 1,
                    "operation": 1,
                    "createdAt": 1,
                    "requirementOdooCode": 1,
                    "odooRequirementCode": 1,
                    "requirementVid": 1,
                }
            }
        ]

        result = list(requirements_col.aggregate(pipeline))
        return pd.DataFrame(result)

