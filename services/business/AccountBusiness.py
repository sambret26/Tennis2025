from repositories.PaymentRepository import PaymentRepository
from repositories.TransactionRepository import TransactionRepository

def getAccountBalance():
    totalDeposit = 0
    totalWithdrawal = 0
    payments = PaymentRepository.getAllPayments()
    transactions = TransactionRepository.getAllTransactions()
    totalPayments = sum(payment.amount for payment in payments)
    for transaction in transactions:
        if transaction.type == 0:
            totalWithdrawal += transaction.amount
        elif transaction.type == 1:
            totalDeposit += transaction.amount

    return AccountBalance(totalPayments, totalDeposit, totalWithdrawal).toDict()

def getAccountBalanceForDay(day):
    amountDayBefore = 0
    withdraws = 0
    paymentsBefore = PaymentRepository.getAllPaymentsBeforeDay(day)
    paymentsDB = PaymentRepository.getAllPaymentsForDay(day)
    payments = [payment.toDictForList() for payment in paymentsDB]
    transactionBefore = TransactionRepository.getAllTransactionBeforeDay(day)
    withdrawDay = TransactionRepository.getAllWithdrawalForDay(day)
    for transaction in transactionBefore:
        if transaction.type == 0:
            amountDayBefore -= transaction.amount
        if transaction.type == 1:
            amountDayBefore += transaction.amount
    for payment in paymentsBefore:
        amountDayBefore += payment.amount
    withdraws = sum(withdraw.amount for withdraw in withdrawDay)
    return AccountBalanceForDay(amountDayBefore, payments, withdraws).toDict()

class AccountBalance:
    def __init__(self, totalPayments, totalDeposit, totalWithdrawal):
        self.totalPayments = totalPayments
        self.totalDeposit = totalDeposit
        self.totalWithdrawal = totalWithdrawal

    def toDict(self):
        return {
            'totalPayments': self.totalPayments,
            'totalDeposit': self.totalDeposit,
            'totalWithdrawal': self.totalWithdrawal
        }

class AccountBalanceForDay:
    def __init__(self, amountDayBefore, payments, withdraws):
        self.amountDayBefore = amountDayBefore
        self.payments = payments
        self.withdraws = withdraws

    def toDict(self):
        return {
            'amountDayBefore': self.amountDayBefore,
            'payments': self.payments,
            'withdraws': self.withdraws
        }