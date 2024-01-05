import requests
from model.model import TierInfo, TierListInfo


# 참조->
def get_tier(queue, tier, division, lp) -> TierInfo:
    return TierInfo(
        queue=queue,
        tier=tier,
    division = division,
    lp = lp
    )

def test(riot_id: str,
             tag: str
             ):
        api_key ='RGAPI-3a4da499-c1da-4432-ade4-5770b7db0090'

        url1 = f'https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{riot_id}/{tag}?api_key={api_key}'
        # f 포멧팅 해주고 ,아이디 {},태그{},API{}
        res = requests.get(url1).json()

        puu_id = res['puuid']
        url2 = f'https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{puu_id}?api_key={api_key}'
        res2 = requests.get(url2).json()
        summonor_id = res2['id']

        url3 = f'https://kr.api.riotgames.com/lol/league/v4/entries/by-summoner/{summonor_id}?api_key={api_key}'
        res3 = requests.get(url3).json()

        tier_list = []
        for league in res3:
            if league['queueType'] == 'RANKED_SOLO_5x5':
                queue = league['queueType']
                solo_rank_tier = league['tier']
                solo_rank_division = league['rank']
                solo_rank_lp = league['leaguePoints']
                tier = get_tier(queue, solo_rank_tier, solo_rank_division, solo_rank_lp)
                tier_list.append(tier)
            elif league['queueType'] == 'RANKED_FLEX_SR':
                queue = league['queueType']
                flex_rank_tier = league['tier']
                flex_rank_division = league['rank']
                flex_rank_lp = league['leaguePoints']
                tier = get_tier(queue, flex_rank_tier, flex_rank_division, flex_rank_lp)
                tier_list.append(tier)
        return TierListInfo(
            total_tier_list=tier_list
        )
