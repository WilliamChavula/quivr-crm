from datetime import datetime
from pathlib import Path
from random import randint
from typing import Union

import pandas as pd

from django.contrib.auth import get_user_model
from django.contrib.auth.models import User as UserModel

from channel.models import Mode, Channel
from client.models import Client
from lead.models import Lead, LeadStatus, Priority
from userprofile.models import UserProfile
from team.models import Team


User: UserModel = get_user_model()


def seed_users(file_name: str) -> None:
    users_path = Path.cwd().joinpath(f"core/data/{file_name}")

    users_data = pd.read_csv(users_path)
    users_dict = users_data.to_dict()

    users = [
        UserProfile(
            user=User.objects.create_user(
                username=users_dict["username"][idx],
                email=users_dict["email"][idx],
                password=users_dict["password"][idx],
                first_name=users_dict["first_name"][idx],
                last_name=users_dict["last_name"][idx],
            ),
            role=users_dict["role"][idx],
            date_joined=datetime.strptime(
                users_dict["date_joined"][idx], "%Y-%m-%d %H:%M:%S"
            ),
            team=Team.objects.get(name__iexact=users_dict["team"][idx]),
        )
        for idx in users_dict["id"]
    ]

    UserProfile.objects.bulk_create(users)


def seed_leads(file_name: str) -> None:
    data_path = Path.cwd().joinpath(f"core/data/{file_name}")
    data = pd.read_csv(data_path).to_dict()

    leads = [
        Lead(
            name=data["name"][idx],
            teams=_get_team(),
            email=data["email"][idx],
            phone=data["phone"][idx],
            social=data["social"][idx],
            address=data["address"][idx],
            created_by=User.objects.get(pk=int(data["created_by"][idx])),
            priority=Priority(data["priority"][idx]),
            status=LeadStatus(data["status"][idx]),
            preferred_communication=Mode(data["preferred_communication"][idx]),
            is_client=data["is_client"][idx],
        )
        for idx in data["id"]
    ]

    Lead.objects.bulk_create(leads)


def seed_clients(file_name: str) -> None:
    data_path = Path.cwd().joinpath(f"core/data/{file_name}")
    data = pd.read_csv(data_path).to_dict()

    clients = [
        Client(
            name=data["name"][idx],
            email=data["email"][idx],
            phone=data["phone"][idx],
            social=data["social"][idx],
            address=data["address"][idx],
            description=data["description"][idx],
            team=_get_team(),
            created_by=User.objects.get(pk=int(data["created_by"][idx])),
            preferred_communication=Mode(data["preferred_communication"][idx]),
        )
        for idx in data["id"]
    ]

    Client.objects.bulk_create(clients)


def seed_channels(file_name: str) -> None:
    data_path = Path.cwd().joinpath(f"core/data/{file_name}")
    data = pd.read_csv(data_path)

    channels = [
        Channel(
            mode=Mode(row.mode),
            team_contacting=Team.objects.get(name__iexact=row.team_contacting),
            date_contacted=datetime.strptime(row.date_contacted, "%m/%d/%y %H:%M:%S"),
            content_object=_get_content_type(row.content_object),
        )
        for row in data.itertuples()
    ]

    Channel.objects.bulk_create(channels)


def _get_team() -> Team:
    team_count = Team.objects.count()

    team_id = randint(1, team_count)

    return Team.objects.get(pk=team_id)


def _get_content_type(obj_type: str) -> Union[Lead, Client]:
    idx = randint(1, 100)
    obj: Union[Lead, Client]

    if idx == 5:
        idx += 1

    if obj_type == "Lead":
        obj = Lead.objects.get(pk=idx)
    elif obj_type == "Client":
        obj = Client.objects.get(pk=idx)

    return obj
