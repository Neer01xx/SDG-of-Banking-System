from sim_utils import SimUtils
import pandas as pd

class CustomerServer:
    
    def __init__(self, params):
        json_data = SimUtils.get_json(params["customer_json_url"])
        self.customer_details = self.createCustomers({"json_data": json_data})
    
    def getCustomerDetails(self):
        return self.customer_details

    def createCustomers(self, params):
        data = {
              "Customer_Id": [],
              "Customer_Type": [],
              "Salary": [],
              "Employment": [],
              "Withdrawal_Rate": [],
              "Withdrawal_Amount": [],
              "Withdrawal_Luck": [],
              "Deposit_Rate": [],
              "Deposit_Amount": [],
              "Loan_Rate": [],
              "Loan_Amount": [],
              "Loan_Interest_Rate": [],
              "Loan_Tenure": [],
              "Credit_Score": []
            }

        #load data into a DataFrame object:
        df = pd.DataFrame(data)

        for i in params["json_data"] :
            load = i["load"]

            for j in range(load):
                cust_id = SimUtils.gen_uuid_id()
                cust_type = i["properties"]["cust_type"]
                employment = i["properties"]["employment"]

                salary = int(SimUtils.randomize(i["properties"]["salary"]))
                if salary >= 10000:
                    salary = round(salary, 2 - len(str(salary)))

                withdraw = i["properties"]["decision_params"]["withdrawal"]
                withdrawal_rate = SimUtils.randomize(withdraw["rate"])
                withdrawal_amount  = withdraw["amount"]
                withdrawal_luck = withdraw["luck"]

                deposit = i["properties"]["decision_params"]["deposit"]
                deposit_rate = SimUtils.randomize(deposit["rate"])
                deposit_amount  = deposit["amount"]
                
                loan = i["properties"]["decision_params"]["loan"]
                loan_rate = SimUtils.randomize(loan["rate"])
                loan_amount = SimUtils.randomize(loan["amount"])
                loan_interest_rate = loan["interest_rate"]
                loan_tenure = SimUtils.randomize(loan["tenure"])
                
                credit_score = 0

                cust_dict = {"Customer_Id" : cust_id, 
                     "Customer_Type": cust_type,
                     "Salary": salary,
                     "Employment": employment,
                     "Withdrawal_Rate": withdrawal_rate,
                     "Withdrawal_Amount": withdrawal_amount,
                     "Withdrawal_Luck": withdrawal_luck,
                     "Deposit_Rate": deposit_rate,
                     "Deposit_Amount": deposit_amount,
                     "Loan_Rate": loan_rate,
                     "Loan_Amount": loan_amount,
                     "Loan_Interest_Rate": loan_interest_rate,
                     "Loan_Tenure": loan_tenure,
                     "Credit_Score":  credit_score
                     }

                df = df.append(cust_dict, ignore_index = True)
                print("Customer with id", cust_id, "created")

        print("Entities created")
        return df
    
    def saveDetails(self, customer_details_url):
        self.customer_details.to_csv(customer_details_url)
        print("Customer details saved to ", customer_details_url)
        
    