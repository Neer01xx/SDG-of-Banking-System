import numpy as np
import os

from customer_server import CustomerServer
from account_server import AccountServer
from sim_utils import SimUtils

class Simulator():
    def __init__(self, id, env, params):
        self.id = id
        self.env = env
        self.customer_server = CustomerServer({
                                      "customer_json_url": params["customer_json_url"]
                                     })
        self.account_server = AccountServer(env)

    def run(self, params):
        for day in range(1, 1 + params["no_of_days"]):
            print("Day", day)
            deposit = 0
            withdrawal = 0
            if self.env.getDate().day == 1:
                self.updateSalaries()
            for customer_index, customer in self.customer_server.getCustomerDetails().iterrows():
                if np.random.uniform() < customer["Deposit_Rate"]:
                    if not self.account_server.checkCustomer(customer["Customer_Id"]):
                        self.account_server.addNewAccount(customer["Customer_Id"])
                    else:
                        deposit_amount = round(SimUtils.randomize(customer["Deposit_Amount"]), 2)
                        if deposit_amount > 0:
                            self.account_server.deposit(customer["Customer_Id"], deposit_amount)
                if np.random.uniform() < customer["Withdrawal_Rate"]:
                    if not self.account_server.checkCustomer(customer["Customer_Id"]):
                        self.account_server.addNewAccount(customer["Customer_Id"])
                    else:
                        withdrawal_amount = round(SimUtils.randomize(customer["Withdrawal_Amount"]), 2)
                        withdrawal_luck = customer["Withdrawal_Luck"]
                        if withdrawal_amount > 0:
                            self.account_server.withdrawal(customer["Customer_Id"], withdrawal_amount, withdrawal_luck)
                if np.random.uniform() < customer["Loan_Rate"]:
                    if not self.account_server.checkLoan(customer["Customer_Id"]):
                        loan_amount = round(customer["Loan_Amount"], 2)
                        if loan_amount > 0:
                            self.account_server.getLoan(customer["Customer_Id"], loan_amount,customer["Loan_Interest_Rate"],customer["Loan_Tenure"])
            self.env.incrementDate()
        os.makedirs(os.getcwd() + "/output/" + str(self.id))
        self.customer_server.saveDetails(os.getcwd() + "/output/" + str(self.id) + "/customer_details.csv")
        self.account_server.saveDetails(os.getcwd() + "/output/" + str(self.id) + "/account_details.csv", os.getcwd() + "/output/" + str(self.id) + "/transaction_details.csv",os.getcwd() + "/output/" + str(self.id) + "/loan_details.csv")
            
    
    def updateSalaries(self):
        for account_index, account in self.account_server.getAccountDetails().iterrows():
            customer_index = self.customer_server.getCustomerDetails()[self.customer_server.getCustomerDetails()["Customer_Id"] == account["Customer_Id"]].index.values[0]
            salary = self.customer_server.getCustomerDetails().at[customer_index, "Salary"]
            self.account_server.deposit(account["Customer_Id"], salary)
            
                    
    
