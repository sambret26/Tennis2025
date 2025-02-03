from flask import Blueprint, jsonify, request
from repositories.UserRepository import UserRepository
from models.User import User
import jwt
from config import Config

SECRET_KEY = Config.SECRET_KEY

userBp = Blueprint('userBp', __name__, url_prefix='/users')

@userBp.route('/connect', methods=['POST'])
def connectUser():
    data = request.json
    user = UserRepository.getUserByName(data['username'])
    if not user:
        return jsonify({'message': 'User not found!'}), 404
    if user.password != data['password']:
        return jsonify({'message': 'Wrong password!'}), 401
    token = jwt.encode(user.toDict(), SECRET_KEY, algorithm='HS256')
    return jsonify({'token': token}), 200

@userBp.route('/create', methods=['POST'])
def createAccount():
    data = request.json
    user = UserRepository.getUserByName(data['username'])
    if user:
        return jsonify({'message': 'User already exists!'}), 409
    user = User.fromJson(data)
    UserRepository.addUser(user)
    token = jwt.encode(user.toDict(), SECRET_KEY, algorithm='HS256')
    return jsonify({'token': token}), 200

@userBp.route('/<int:userId>/role', methods=['PUT'])
def updateRole(userId):
    user = UserRepository.getUserById(userId)
    if not user:
        return jsonify({'message': 'User not found!'}), 404
    newRole = int(request.json['newRole'])
    if newRole < user.profileValue or user.superAdmin == 1:
        if user.profileValue == 2:
            user = UserRepository.updateProfile(userId, newRole, 1)
        else :
            user = UserRepository.updateProfile(userId, newRole, user.superAdmin)
        token = jwt.encode(user.toDict(), SECRET_KEY, algorithm='HS256')
        return jsonify({'token': token}), 200
    else : 
        return jsonify({'message': 'You cannot change the role of this user!'}), 403
    
@userBp.route('/admin/connect', methods=['POST'])
def connectAdmin():
    data = request.json
    password = data['password']
    userId = int(data['userId'])
    newRole = int(data['newRole'])
    admin = UserRepository.getAdminWithPassword(password)
    if not admin:
        return jsonify({'message': 'Invalid password!'}), 401
    user = UserRepository.updateProfile(userId, newRole, 0)
    token = jwt.encode(user.toDict(), SECRET_KEY, algorithm='HS256')
    return jsonify({'token': token}), 200
