from code2.code2 import test
from model.model import TierListInfo
from fastapi import APIRouter

router =APIRouter(prefix='/summoner')

#@ python데코레이터 , java 어노테이션과 같지않음

@router.get(
    path='/tier',
    response_model=TierListInfo
)
def summoner_tier(
        riot_id:str,
        tag:str
) ->TierListInfo:
    return test(riot_id=riot_id, tag=tag)
