from enum import Enum
import InputData as Data
import scr.MarkovClasses as SupportLibrary
import ProblemOneAndTwo as P1

class HealthStats(Enum):
    """ health states of patients with HIV """
    WELL = 0
    STROKE = 1
    POST_STROKE = 2
    DEATH = 3
    BACKGROUND_DEATH = 4


class Therapies(Enum):
    """ mono vs. combination therapy """
    NONE = 0
    ANTICOAG = 1


class ParametersFixed():
    def __init__(self, therapy):

        # selected therapy
        self._therapy = therapy

        # simulation time step
        self._delta_t = Data.DELTA_T

        self._adjDiscountRate = Data.DISCOUNT * Data.DELTA_T

        # initial health state
        self._initialHealthState = HealthStats.WELL

        # annual treatment cost
        if self._therapy == Therapies.NONE:
            self._annualTreatmentCost = 0
        if self._therapy == Therapies.ANTICOAG:
            self._annualTreatmentCost = Data.Anticoag_COST

        # transition probability matrix of the selected therapy
        self._prob_matrix = []
        # treatment relative risk
        self._treatmentRR = 0

        # calculate transition probabilities depending of which therapy options is in use
        if therapy == Therapies.NONE:
            self._prob_matrix, p = SupportLibrary.continuous_to_discrete(P1.RATE_MATRIX, Data.DELTA_T)
        else:
            self._prob_matrix, p = SupportLibrary.continuous_to_discrete(P1.RATE_MATRIX_ANTI_COAG, Data.DELTA_T)

        self._annualStateCosts = Data.HEALTH_COST
        self._annualStateUtilities = Data.HEALTH_UTILITY

    def get_initial_health_state(self):
        return self._initialHealthState

    def get_delta_t(self):
        return self._delta_t

    def get_adj_discount_rate(self):
        return self._adjDiscountRate

    def get_transition_prob(self, state):
        return self._prob_matrix[state.value]

    def get_annual_state_cost(self, state):
        if state == HealthStats.DEATH:
            return 0
        else:
            return self._annualStateCosts[state.value]

    def get_annual_state_utility(self, state):
        if state == HealthStats.DEATH:
            return 0
        else:
            return self._annualStateUtilities[state.value]

    def get_annual_treatment_cost(self):
        return self._annualTreatmentCost
