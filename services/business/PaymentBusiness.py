
from repositories.PlayerRepository import PlayerRepository
from repositories.PaymentRepository import PaymentRepository
from repositories.PlayerBalanceRepository import PlayerBalanceRepository
from models.Payment import Payment

playersRepository = PlayerRepository()
paymentRepository = PaymentRepository()
playerBalanceRepository = PlayerBalanceRepository()

def updatePayments(player, payments, balance):
    paymentRepository.deleteAllPaymentsByPlayerId(player.id)
    newPayments = []
    for paymentData in payments:
        newPayments.append(Payment(
            playerId=player.id,
            amount=paymentData['amount'],
            date=paymentData['date']
        ))
    paymentRepository.addPayments(newPayments)
    playerBalanceRepository.updatePlayerBalanceForPlayerId(player.id, balance)
    result = [payment.toDictForPlayer() for payment in newPayments]
    return result