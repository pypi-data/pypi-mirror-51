from ..models.personModel import personModel, classModel, schoolModel
from .models.urlModel import (GET_FRIEND_URL, GET_CLASSMATES_URL,
                              INVITE_FRIEND_URL, DELETE_FRIEND_URL, GET_CLAZZS_URL)
import time


def get_user_id(self, name: str) -> str:
    """
    转换名字为id
    :param name:
    :return:
    """
    classmates = self.get_classmates()
    for classmate in classmates:
        if classmate.name == name:
            return classmate.id
    return ""


def get_classmates(self, clazz: classModel = None) -> list:
    """
    返回年级里指定班级里学生列表和朋友列表
    默认返回本班
    :param self:
    :return:
    """
    classmates = list()
    clazzId = self.clazz.id if clazz == None else clazz.id
    r = self._session.get(GET_CLASSMATES_URL, params={
        "r": f"{self.id}student",
        "clazzId": clazzId
    })
    json_obj = r.json()
    for classmate in json_obj:
        b = int(classmate["birthday"]) / \
            1000 if classmate.get("birthday") else 0
        classmates.append(personModel(
            name=classmate["name"],
            id=classmate["id"],
            birthday=b if b > 0 else 0,
            clazz=classModel(
                id=classmate["clazz"]["id"],
                name=classmate["clazz"]["name"]
            ),
            school=schoolModel(
                id=classmate["clazz"]["school"]["id"],
                name=classmate["clazz"]["school"]["name"]
            ),
            code=classmate["code"],
            email=classmate["email"],
            qq_number=classmate["im"],
            gender="男" if classmate["gender"] == "1" else "女",
            mobile=classmate["mobile"]
        ))
    return classmates


def get_friends(self) -> list:
    friends = []
    json_data = self._session.get(
        f"{GET_FRIEND_URL}?d={int(time.time())}") \
        .json()
    for each in json_data["friendList"]:
        friends.append(personModel(
            name=each["friendName"],
            id=each["friendId"]
        ))

    return friends


def invite_friend(self, user_id: str) -> str:
    """
    邀请朋友
    :param user_id:用户id
    :return:
    """
    p = {
        "friendId": user_id,
        "isTwoWay": "true"
    }
    r = self._session.get(
        f"{INVITE_FRIEND_URL}?d={int(time.time())}", params=p)
    json = r.json()
    if json["result"] == "success":
        return "success"
    elif json["message"] == "已发送过邀请，等待对方答复":
        return "已发送过邀请，等待对方答复"
    else:
        return ""


def remove_friend(self, user_id: str) -> bool:
    """
    删除朋友
    :param user_id:用户id可以通过getUserId获取
    :return:
    """
    p = {"friendId": user_id}
    r = self._session.get(
        f"{DELETE_FRIEND_URL}?d={int(time.time())}", params=p)
    if r.json()["result"] != "success":
        return False
    else:
        return True


def get_clazzs(self) -> list:
    l = list()
    r = self._session.get(f"{GET_CLAZZS_URL}?d={int(time.time())}")
    json = r.json()
    for each in json["clazzs"]:
        l.append(classModel(
            name=each["name"],
            id=each["id"]
        ))
    return l
