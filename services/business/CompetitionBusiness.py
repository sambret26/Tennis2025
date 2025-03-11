import moja.mojaService as mojaService
from repositories.CompetitionRepository import CompetitionRepository
from repositories.PlayerAvailabilityRepository import PlayerAvailabilityRepository
from repositories.PlayerAvailabilityCommentRepository import PlayerAvailabilityCommentRepository
from repositories.PlayerBalanceRepository import PlayerBalanceRepository
from repositories.PlayerCategoriesRepository import PlayerCategoriesRepository
from repositories.ReductionRepository import ReductionRepository
from repositories.PaymentRepository import PaymentRepository
from repositories.PlayerRepository import PlayerRepository
from repositories.TransactionRepository import TransactionRepository
from repositories.TeamRepository import TeamRepository
from repositories.MatchRepository import MatchRepository
from models.Competition import Competition

competitionRepository = CompetitionRepository()
playerAvailabilityRepository = PlayerAvailabilityRepository()
playerAvailabilityCommentRepository = PlayerAvailabilityCommentRepository()
playerBalanceRepository = PlayerBalanceRepository()
playerCategoriesRepository = PlayerCategoriesRepository()
reductionRepository = ReductionRepository()
paymentRepository = PaymentRepository()
matchRepository = MatchRepository()
playerRepository = PlayerRepository()
transactionRepository = TransactionRepository()
teamRepository = TeamRepository()

def updateCompetitions():
    competitions = mojaService.getCompetitions()
    if competitions == None:
        return None
    competitionsInDB = competitionRepository.getCompetitions()
    competitionsIdToDelete = [competition.homologationId for competition in competitionsInDB]
    competitionsToAdd = []
    for competitionFFT in competitions["competitions"]:
        competition = Competition.fromFFT(competitionFFT)
        competitionInDB = next((comp for comp in competitionsInDB if comp.homologationId == competition.homologationId), None)
        if competitionInDB:
            if competition.isDifferent(competitionInDB):
                competition.id = competitionInDB.id
                competitionRepository.updateCompetition(competitionInDB.id, competition)
            competitionsIdToDelete.remove(competition.homologationId)
        else:
            competitionsToAdd.append(competition)
    competitionRepository.addCompetitions(competitionsToAdd)
    competitionRepository.deleteCompetitions(competitionsIdToDelete)
    return 200

def deleteData():
    playerAvailabilityRepository.deleteAllPlayerAvailabilities()
    playerAvailabilityCommentRepository.deleteAllPlayerAvailabilityComments()
    playerBalanceRepository.deleteAllPlayerBalances()
    playerCategoriesRepository.deleteAllPlayerCategories()
    reductionRepository.deleteAllReductions()
    paymentRepository.deleteAllPayments()
    matchRepository.deleteAllMatches()
    transactionRepository.deleteAllTransactions()
    teamRepository.deleteAllTeams()
    playerRepository.deleteAllPlayers()
