import moja.mojaService as mojaService
from repositories.CompetitionRepository import CompetitionRepository
from models.Competition import Competition

competitionRepository = CompetitionRepository()

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