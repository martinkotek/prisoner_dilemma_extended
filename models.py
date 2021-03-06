from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random

doc = """
This is a one-shot "Prisoner's Dilemma". Two players are asked separately
whether they want to cooperate or defect. Their choices directly determine the
payoffs.
"""


class Constants(BaseConstants):
    name_in_url = 'prisoner_dilemma_extended'
    players_per_group = 2
    num_rounds = 1

    instructions_template = 'prisoner_dilemma_extended/Instructions.html'

    # payoff if 1 player defects and the other cooperates""",
    betray_payoff = c(25)
    betrayed_payoff = c(0)

    # payoff if both players cooperate or both defect
    both_cooperate_payoff = c(20)
    both_defect_payoff = c(5)


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    ct_upfront_amount = models.PositiveIntegerField(
        min=0, max=Constants.both_cooperate_payoff/5,
        doc="""Amount paid to the second player"""
    )

    ct_promised_amount = models.PositiveIntegerField(
        min=0, max=Constants.both_cooperate_payoff,
        doc="""Quantity of units to produce"""
    )

    ct_actual_amount = models.PositiveIntegerField(
        min=0, max=Constants.both_cooperate_payoff,
        doc="""Amount paid to the second player"""
    )

    pd_decision = models.CharField(
        choices=['Cooperate', 'Defect'],
        doc="""This player's decision""",
        widget=widgets.RadioSelect()
    )

    def role(self):
        if self.id_in_group == 1:
            return 'player_1'
        else:
            return 'player_2'

    def other_player(self):
        return self.get_others_in_group()[0]


    def set_payoff(self):

        points_matrix = {
            'Cooperate':
                {
                    'Cooperate': Constants.both_cooperate_payoff,
                    'Defect': Constants.betrayed_payoff
                },
            'Defect':
                {
                    'Cooperate': Constants.betray_payoff,
                    'Defect': Constants.both_defect_payoff
                }
        }

        self.payoff = (points_matrix[self.pd_decision]
                       [self.other_player().pd_decision])
