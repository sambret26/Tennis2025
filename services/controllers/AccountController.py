from flask import Blueprint, jsonify, request
from services.business import AccountBusiness

accountBp = Blueprint('accountBp', __name__, url_prefix='/accounts')

@accountBp.route('/', methods=['GET'])
def getAccountBalance():
    accountBalance = AccountBusiness.getAccountBalance()
    return jsonify(accountBalance), 200

@accountBp.route('/<string:day>', methods=['GET'])
def getAccountBalanceForDay(day):
    accountBalance = AccountBusiness.getAccountBalanceForDay(day)
    return jsonify(accountBalance), 200