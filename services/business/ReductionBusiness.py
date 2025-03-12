from repositories.ReductionRepository import ReductionRepository
from repositories.PlayerBalanceRepository import PlayerBalanceRepository
from models.Reduction import Reduction

reductionRepository = ReductionRepository()
playerBalanceRepository = PlayerBalanceRepository()

def updateReduction(player, reductions, balance):
    reductionRepository.deleteAllReductionsByPlayerId(player.id)

    # Ajouter les nouveaux reductions
    newReductions = []
    for reductionData in reductions:
        newReductions.append(Reduction(
            playerId=player.id,
            amount=reductionData['amount'],
            reason=reductionData['reason'],
            default=reductionData['default']
        ))

    reductionRepository.addReductions(newReductions)
    playerBalanceRepository.updatePlayerBalanceForPlayerId(player.id, balance)
    result = [reduction.toDict() for reduction in newReductions]
    return result