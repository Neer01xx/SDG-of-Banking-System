from sim_utils import SimUtils
import pandas as pd
import numpy as np

class AccountServer:
    def __init__(self, env, params = None):
        self.env = env
        self.account_details = pd.DataFrame({
                "Account_No" : [],
                "Customer_Id" : [],
                "Customer_Debt" : [], 
                "Current_Amount" : [] 
            }
        )

        self.transaction_details = pd.DataFrame({
                "Account_No" : [],
                "Date" : [],
                "Type" : [],
                "Amount" : []
            }
        )
        
        self.loan_details = pd.DataFrame({
                "Loan_Account_No" : [],
                "Account_No" : [],
                "Loan_Date" : [],
                "Interest_Rate" : [],
                "Loan_Amount" : [],
                "Loan_Tenure" : [],
                "Monthly_Payable_Amount" : []
            }
        )
        
    def getAccountDetails(self):
        return self.account_details
    
    def addNewAccount(self, customer_id):
        acc_id = SimUtils.gen_uuid_id()
        self.account_details = self.account_details.append({
            "Account_No" : acc_id,
            "Customer_Id" : customer_id,
            "Customer_Debt" : 0, 
            "Current_Amount" : 0
        }, ignore_index = True)
        
        print("New account added with id", acc_id, "for customer id", customer_id)
    
    def checkCustomer(self, customer_id):
        return customer_id in self.account_details["Customer_Id"].values
    
    def deposit(self, customer_id, amount):
        account_index = self.account_details[self.account_details["Customer_Id"] == customer_id].index.values[0]
        account_id = self.account_details.at[account_index, "Account_No"]
        if amount <= 0:
            return
        self.account_details.at[account_index, "Current_Amount"] = self.account_details.at[account_index, "Current_Amount"] + amount
        self.env.bank_amount += amount
        self.transaction_details = self.transaction_details.append({
            "Account_No" : account_id,
            "Date" : self.env.getDate(),
            "Type" : "D", 
            "Amount" : amount
        }, ignore_index = True)
        
        print("Deposited", amount, "for account number", account_id)
    
    def withdrawal(self, customer_id, amount, luck):
        account_index = self.account_details[self.account_details["Customer_Id"] == customer_id].index.values[0]
        account_id = self.account_details.at[account_index, "Account_No"]
        if np.random.uniform() < luck:
            amount = np.random.uniform() * self.account_details.at[account_index, "Current_Amount"]
        if amount > self.account_details.at[account_index, "Current_Amount"] or amount <  0:
            return
        self.account_details.at[account_index, "Current_Amount"] = self.account_details.at[account_index, "Current_Amount"] - round(amount, 2)
        self.env.bank_amount -= round(amount, 2)
        self.transaction_details = self.transaction_details.append({
            "Account_No" : account_id,
            "Date" : self.env.getDate(),
            "Type" : "W", 
            "Amount" : amount
        }, ignore_index = True)
        
        print("Withdrew", amount, "for account number", account_id)
        
    def saveDetails(self, account_details_url, transaction_details_url,loan_details_url):
        self.account_details.to_csv(account_details_url)
        self.transaction_details.to_csv(transaction_details_url)
        self.loan_details.to_csv(loan_details_url)
        print("Account details saved to ", account_details_url)
        print("Transaction details saved to ", transaction_details_url)
        print("Loan details saved to ", loan_details_url)
        
    def checkLoan(self, customer_id):
        account_index = self.account_details[self.account_details["Customer_Id"] == customer_id].index.values[0]
        account_no = self.account_details.at[account_index, "Account_No"]
        return account_no in self.loan_details["Account_No"].values
    
    def getLoan(self, customer_id, loan_amount, interest_rate, loan_tenure):
        loan_acc_no = SimUtils.gen_uuid_id()
        
        account_index = self.account_details[self.account_details["Customer_Id"] == customer_id].index.values[0]
        account_no = self.account_details.at[account_index, "Account_No"]
        if loan_amount <= 0:
            return
        self.account_details.at[account_index, "Customer_Debt"] = self.account_details.at[account_index, "Customer_Debt"] + loan_amount
        self.env.bank_amount -= loan_amount
        
        rate = interest_rate/(12*100)
        n = loan_tenure*12
        emi = loan_amount * rate * (((1+rate)**n)/(((1+rate)**n)-1))
        
        self.loan_details = self.loan_details.append({
            "Loan_Account_No" : loan_acc_no,
            "Account_No" : account_no,
            "Loan_Date"  : self.env.getDate(),
            "Loan_Amount" : loan_amount,
            "Loan_Tenure" : loan_tenure,
            "Interest_Rate" :interest_rate,
            "Monthly_Payable_Amount" : emi
        }, ignore_index = True)
        
        print("New loan added with loan_account_no", loan_acc_no, "for customer id", account_no)
        
        
    
        
        
        