from typing import List
from sqlmodel import SQLModel
from models.game import (
    BattingResultBase,
    AtbatResultBase,
    AtbatResultEnum,
    PitchingResultBase,
    PicherResultEnum,
)


def isCountedAtbat(result):
    return result in (
        "SH",
        "DH",
        "TH",
        "HR",
        "RH",
        "DP",
        "GO",
        "FO",
        "LO",
        "MP",
        "FF",
        "FC",
        "KO",
        "MK",
        "DT",
    )


class StatsBase(SQLModel):
    number: str
    name: str


class BattingStatsRead(StatsBase):
    avg: float
    games: int
    pa: int
    ab: int
    hits: int
    dh: int
    th: int
    hr: int
    rh: int
    bases: int
    rbi: int
    runs: int
    ko: int
    bb: int
    hbp: int
    sb: int
    sf: int
    steels: int
    dp: int
    obp: float
    slg: float
    ops: float
    scpos_avg: float

    def __init__(
        self,
        player_number: str,
        player_name: str,
        battingResults: List[BattingResultBase],
        atbatResults: List[AtbatResultBase],
    ):
        self.number = player_number
        self.name = player_name

        games = 0
        rbi = 0
        runs = 0
        steels = 0
        for battingResult in battingResults:
            games += 1
            rbi += battingResult.rbi
            runs += battingResult.runs
            steels += battingResult.steels

        pa = 0
        ab = 0
        hits = 0
        dh = 0
        th = 0
        hr = 0
        rh = 0
        bases = 0
        ko = 0
        bb = 0
        hbp = 0
        sb = 0
        sf = 0
        dp = 0
        scpos_ab = 0  # 得点圏打率計算用
        scpos_hits = 0  # 得点圏打率計算用

        for atbatResult in atbatResults:
            pa += 1
            ab += 1 if isCountedAtbat(atbatResult.result) else 0
            scpos_ab += (
                1 if atbatResult.is_scpos and isCountedAtbat(atbatResult.result) else 0
            )
            match atbatResult.result:
                case AtbatResultEnum.SH:
                    hits += 1
                    bases += 1
                    scpos_hits += 1 if atbatResult.is_scpos else 0
                case AtbatResultEnum.DH:
                    hits += 1
                    dh += 1
                    bases += 2
                    scpos_hits += 1 if atbatResult.is_scpos else 0
                case AtbatResultEnum.TH:
                    hits += 1
                    th += 1
                    bases += 3
                    scpos_hits += 1 if atbatResult.is_scpos else 0
                case AtbatResultEnum.HR:
                    hits += 1
                    hr += 1
                    bases += 4
                    scpos_hits += 1 if atbatResult.is_scpos else 0
                case AtbatResultEnum.RH:
                    hits += 1
                    rh += 1
                    bases += 4
                    scpos_hits += 1 if atbatResult.is_scpos else 0
                case AtbatResultEnum.SB:
                    sb += 1
                case AtbatResultEnum.SF:
                    sf += 1
                case AtbatResultEnum.DP:
                    dp += 1
                case AtbatResultEnum.KO:
                    ko += 1
                case AtbatResultEnum.MK:
                    ko += 1
                case AtbatResultEnum.BB:
                    bb += 1
                case AtbatResultEnum.IB:
                    bb += 1
                case AtbatResultEnum.HP:
                    hbp += 1
                case AtbatResultEnum.DT:
                    ko += 1

        self.avg = hits / ab if ab != 0 else "-"
        self.games = games
        self.pa = pa
        self.ab = ab
        self.hits = hits
        self.dh = dh
        self.th = th
        self.hr = hr
        self.rh = rh
        self.bases = bases
        self.rbi = rbi
        self.runs = runs
        self.ko = ko
        self.bb = bb
        self.hbp = hbp
        self.sb = sb
        self.sf = sf
        self.steels = steels
        self.dp = dp
        self.obp = (
            (hits + bb + hbp) / (ab + bb + hbp + sf)
            if (ab + bb + hbp + sf) != 0
            else "-"
        )
        self.slg = bases / ab if ab != 0 else "-"
        self.ops = "-" if self.obp == "-" or self.slg == "-" else self.obp + self.slg
        self.scpos_avg = scpos_hits / scpos_ab if scpos_ab != 0 else "-"


class PitchingStatsRead(StatsBase):
    era: float
    games: int
    starts: int
    wins: int
    loses: int
    holds: int
    saves: int
    win_pct: float
    innings: int
    pitchs: int
    batters: int
    hits: int
    hr: int
    ko: int
    ko_pct: float
    bb: int
    hbp: int
    balks: int
    runs: int
    earned_runs: int
    oav: float
    k_bb: float
    whip: float

    def __init__(
        self,
        player_number: str,
        player_name: str,
        pitchingResults: List[PitchingResultBase],
    ):
        self.number = player_number
        self.name = player_name

        games = 0
        starts = 0
        wins = 0
        loses = 0
        holds = 0
        saves = 0
        innings = 0
        pitchs = 0
        batters = 0
        hits = 0
        hr = 0
        ko = 0
        bb = 0
        hbp = 0
        balks = 0
        runs = 0
        earned_runs = 0

        for pitchingResult in pitchingResults:
            games += 1

            if pitchingResult.pitching_order == 1:
                starts += 1

            match pitchingResult.result:
                case PicherResultEnum.WIN:
                    wins += 1
                case PicherResultEnum.LOSE:
                    loses += 1
                case PicherResultEnum.HOLD:
                    holds += 1
                case PicherResultEnum.SAVE:
                    saves += 1

            innings += pitchingResult.innings
            pitchs += pitchingResult.pitchs
            batters += pitchingResult.batters
            hits += pitchingResult.hits
            hr += pitchingResult.homeruns
            ko += pitchingResult.strikeouts
            bb += pitchingResult.walks
            hbp += pitchingResult.hit_by_pitch
            balks += pitchingResult.balks
            runs += pitchingResult.runs
            earned_runs += pitchingResult.earned_runs

        self.era = round(earned_runs * 9 / innings, 2) if innings != 0 else "-"
        self.games = games
        self.starts = starts
        self.wins = wins
        self.loses = loses
        self.holds = holds
        self.saves = saves
        self.innings = innings
        self.pitchs = pitchs
        self.batters = batters
        self.hits = hits
        self.hr = hr
        self.ko = ko
        self.ko_pct = round(ko * 9 / innings, 2) if innings != 0 else "-"
        self.bb = bb
        self.hbp = hbp
        self.balks = balks
        self.runs = runs
        self.earned_runs = earned_runs
        self.oav = (
            round(hits / (batters - bb - hbp), 2) if (batters - bb - hbp) != 0 else "-"
        )
        self.k_bb = round(ko / bb, 2) if bb != 0 else "-"
        self.whip = round((hits + bb) / innings, 2) if innings != 0 else "-"
