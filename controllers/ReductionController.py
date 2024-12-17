from flask import Blueprint, jsonify, request
from repositories.ReductionRepository import ReductionRepository
from models.Reduction import Reduction

reductionBp = Blueprint('reductionBp', __name__, url_prefix='/reductions')

@reductionBp.route('/', methods=['GET'])
def getReductions():
    reductions = ReductionRepository.getAllReductions()
    return jsonify([reduction.toDict() for reduction in reductions]), 200

@reductionBp.route('/', methods=['POST'])
def addReduction():
    reduction = Reduction.fromJson(request.json)
    ReductionRepository.addReduction(reduction)
    return jsonify({'message': 'Reduction added successfully!'}), 201

@reductionBp.route('/multiple', methods=['POST'])
def addReductions():
    reductions = []
    for data in request.json:
        reductions.append(Reduction.fromJson(data))
    ReductionRepository.addReductions(reductions)
    return jsonify({'message': 'Reductions added successfully!'}), 201