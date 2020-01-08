'''
This will scrape Oddschecker for all Arb opportunities, whenever they are found,
a results HTML file will be generated.

SpiceBucks
'''

#------------------------------------------------------------------

import numpy as np
from fractions import Fraction

from webscraping.website import CWebsite
from util.message import message
import util.utilities as ut
from templates.HTML_template_elements import make_html

#------------------------------------------------------------------

DEFAULT_LINK_ATTR_NAME = "href"
ODDSCHECKER_HOME = "https://www.oddschecker.com/"

#------------------------------------------------------------------

BET_AMOUNT = 100
INCLUDE_INPLAY = False

MIN_OPP = 1.03
MAX_OPP = 1.2
DISALLOWED_MARKETS = [
    "Half Time Winning Margin",
    "To Score 2 Or More Goals",
    "To Score A Hat-Trick.",
    "Last Goalscorer",
    "To Score 3+ Goals",
    "To Score 4+ Goals",
    "Score After 6 Games",
    "To Win Set 1 And Win",
    "Not To Win A Set",
    "Set 1 Score Groups",
    "Score After 2 Games"
]

#------------------------------------------------------------------

class CWebCrawler(object):
    """
    Contains all the functionality for finding arb opps on Oddschecker.
    """
    def __init__(self, name="Oddschecker Web Crawler"):
        self.m_name = name
        self.all_results = []
        self.m_homepage = CWebsite( ODDSCHECKER_HOME , ODDSCHECKER_HOME, name="oddschecker_home" )

    # ------------------------------------------------------------------
    # public methods
    # ------------------------------------------------------------------

    def run(self):
        """
        Finds the odds, runs forever.
        """
        sport_specific_home_tags = self.m_homepage.getClasses(["nav-link beta-footnote"])
        sport_specific_home_tags
        for sports_home_tag in sport_specific_home_tags:
            if sports_home_tag.hasAttr(DEFAULT_LINK_ATTR_NAME):
                message.logDebug("Examining " + sports_home_tag.getName() + " arbitrage opportunities.")

                try:
                    sport_home = CWebsite(sports_home_tag.getAttr(DEFAULT_LINK_ATTR_NAME),
                                          ODDSCHECKER_HOME, name=sports_home_tag.getName())
                except:
                    message.logWarning("Unable to load webpage, skipping to next sport")
                    continue

                game_tags = sport_home.getClasses(["beta-callout full-height-link whole-row-link"])
                for game_tag in game_tags:
                    if game_tag.hasAttr(DEFAULT_LINK_ATTR_NAME):
                        game_name = game_tag.getAttr("data-event-name")
                        if game_name is None:
                            message.logError("game name not found!")
                        message.logDebug("Examining arbitrage opportunities in game: " + game_name + ".")

                        try:
                            game_webpage = CWebsite(sport_home.getHomeURL() + game_tag.getAttr(DEFAULT_LINK_ATTR_NAME),
                                                    ODDSCHECKER_HOME, name=game_name)
                        except:
                            message.logWarning("Unable to load webpage, skipping to next match")
                            continue

                        if INCLUDE_INPLAY == False:
                            if len(game_webpage.getClasses("no-arrow in-play")) > 0:
                                message.logDebug("Game is in play, skipping.")
                                continue
                        try:
                            market_tags = game_webpage.getClasses("market-dd select-wrap")[0].getClasses(
                                "select-item beta-callout")
                        except:
                            message.logWarning("Unable to load market tags, skipping to next match")
                            continue

                        market_tags = [m for m in market_tags if m.getName() not in DISALLOWED_MARKETS]
                        market_tags.reverse()
                        for market_tag in market_tags:

                            message.logDebug("Considering market: " + market_tag.getName() + ".")

                            try:
                                market_webpage = CWebsite(
                                    sport_home.getHomeURL() + market_tag.getAttr(DEFAULT_LINK_ATTR_NAME),
                                    ODDSCHECKER_HOME, name=game_name + ": " + market_tag.getName())
                            except:
                                message.logWarning("Unable to load webpage, skipping to next market")
                                continue

                            self._check_website(market_webpage)

    # ------------------------------------------------------------------
    # public methods
    # ------------------------------------------------------------------

    def _check_website(self, website, supress=False, verify=False):
        """
        Checks one website for arb opps.
        """
        if isinstance(website, str):
            website = CWebsite(website, ODDSCHECKER_HOME, name=website)
        table_tags = website.getClasses("diff-row evTabRow bc")
        bet_names = [""] * len(table_tags)
        best_odds = np.zeros(len(table_tags))
        best_odds_ind = [0] * len(table_tags)
        for tnum, table in enumerate(table_tags):
            for tchild, table_elem in enumerate(table.getChildren()):
                if len(table_elem.getClasses("beta-sprite add-to-bet-basket")) == 1:
                    name = table_elem.getClasses("beta-sprite add-to-bet-basket")[0].getAttr("data-name")
                    if name != None:
                        bet_names[tnum] = name
                if "wo-col" in table_elem.getClassName():
                    break
                if table_elem.hasAttr("data-odig"):
                    if table_elem.hasAttr("data-o"):
                        if isinstance(table_elem.getAttr("data-o"), (str, int)):
                            if table_elem.getAttr("data-o") != "" and "np" not in table_elem.getClassName():
                                if float(table_elem.getAttr("data-odig")) > best_odds[tnum]:
                                    best_odds[tnum] = float(table_elem.getAttr("data-odig"))
                                    best_odds_ind[tnum] = tchild

        if len(best_odds) > 1:
            if min(best_odds) > 0:
                bet_goodness = (1. / sum(1. / best_odds))

                if MIN_OPP < bet_goodness < MAX_OPP:

                    # Find websites with best odds
                    best_sites = []
                    for best_odd_index in best_odds_ind:
                        best_odd_column = website.getClasses("eventTableHeader")[0].getChildren()[best_odd_index]
                        best_sites.append(best_odd_column.getChildren()[0].getChildren()[0].getAttr("title"))

                    arb_opp = str((1. / sum(1. / best_odds)) * BET_AMOUNT - BET_AMOUNT)
                    correct_bets = (BET_AMOUNT / best_odds) * (1 / sum(1. / best_odds))

                    instructions = []
                    for bet_num in range(len(correct_bets)):
                        odds = Fraction(best_odds[bet_num] - 1).limit_denominator(1000)
                        msg = "BET " + str(round(correct_bets[bet_num],2)) + " on selection " + bet_names[
                            bet_num] + " on website " + \
                              best_sites[bet_num] + " at odds " + str(odds.numerator) + "/" + str(
                            odds.denominator) + "."
                        instructions.append(msg)

                    self._processResult({
                        "Name": website.getName(),
                        "Arbitrage Opportunity": str(round(float(arb_opp), 2)),
                        "Link": website.getURL(),
                        "Instructions": instructions},
                        supress=supress,
                        verify=verify
                    )
                    return True
        return False

    def _processResult(self, result, supress=False, verify=False):
        """
        Is run when a result is found.
        """
        self.all_results.append(result)
        if verify:
            self._check_results()
        name = result["Name"].split(":")
        if not supress:
            message.logResult("#------------------------------------------------------------------")
            message.logResult("ARBITRAGE OPPORTUNITY OF " + result["Arbitrage Opportunity"] + " FOUND!")
            message.logResult("GAME: " + name[0])
            message.logResult("MARKET: " + name[1])
            message.logResult("LINK: " + result["Link"])
            message.logResult("#------------------------------------------------------------------")
            for r in result["Instructions"]:
                message.logResult(r)
            message.logResult("#------------------------------------------------------------------")
        html = make_html(self.all_results)

        with open("results.html", "w") as file:
            file.write(html)

        # then beep
        if not supress:
            ut.beep('templates/ding.wav')

    def _check_results(self):
        links = [r["Link"] for r in self.all_results]
        self.all_results = []
        for l in links:
            self._check_website(l, verify=True)

if __name__ == "__main__":
    go = CWebCrawler()
    go.run()


