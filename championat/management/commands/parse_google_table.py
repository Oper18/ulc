# coding: utf-8

from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from django.core.management.base import BaseCommand
from championat.models import Season, League, Group, Team, Game


def parse_sheet():
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

    # The ID and range of a sample spreadsheet.
    SAMPLE_SPREADSHEET_ID = '1eLTLOjUv0R04OzFd0TeOLVBjayd4MxANAnryW_JIuJA'
    SAMPLE_RANGE_NAME = 'Календарь!A2:J'

    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=SAMPLE_RANGE_NAME).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
    else:
        games = []
        teams = {}
        for row in values:
            try:
                home = row[3]
                visitors = row[4]
                if int(row[0][-2:]) > 6:
                    date = row[2][:5] + ' ' + row[0] + '.2019'
                else:
                    date = row[2][:5] + ' ' + row[0] + '.2020'
                date = datetime.datetime.strptime(date, '%H:%M %d.%m.%Y')
                if row[5] == 'ПО':
                    l = 1
                    g = row[5]
                elif row[5] == 'СТ':
                    l = 2
                    g = row[5]
                else:
                    try:
                        l = row[5][0]
                        g = row[5][1]
                    except:
                        continue
                try:
                    home_goals = row[8]
                except:
                    home_goals = None
                try:
                    visitors_goals = row[9]
                except:
                    visitors_goals = None

                # print('{}, {}, {}, {}, {}, {}, {}, {}'.format(date, home, visitors, l, g, row[3], home_goals, visitors_goals))
                games.append((date, home, visitors, l, g, row[6], home_goals, visitors_goals))
            except:
                continue

            else:
                if str(l) in teams.keys():
                    if str(g) not in teams[str(l)].keys() and str(g) != 'ПО' and str(g) != 'СТ':
                        teams[str(l)][str(g)] = [home, visitors]
                        teams[str(l)][str(g)+'_copy'] = [home.lower(), visitors.lower()]
                    elif str(g) in teams[str(l)].keys() and str(g) != 'ПО' and str(g) != 'СТ':
                        if home.lower() not in teams[str(l)][str(g)+'_copy']:
                            teams[str(l)][str(g)+'_copy'].append(home.lower())
                            teams[str(l)][str(g)].append(home)
                        if visitors.lower() not in teams[str(l)][str(g)+'_copy']:
                            teams[str(l)][str(g)+'_copy'].append(visitors.lower())
                            teams[str(l)][str(g)].append(visitors)

                else:
                    teams[str(l)] = {str(g): [home, visitors]}
                    teams[str(l)] = {str(g)+'_copy': [home.lower(), visitors.lower()]}

    for i in teams.keys():
        keys_for_del = []
        for j in teams[i].keys():
            if '_copy' in j:
                keys_for_del.append(j)
        for j in keys_for_del:
            teams[i].pop(j)


    return teams, games


class Command(BaseCommand):

    def handle(self, *args, **options):
        teams, games = parse_sheet()

        season = Season.objects.get(year=2020)

        for l in teams.keys():
            league, created = League.objects.get_or_create(name=l,
                                                           season=season)

            for g in teams[l].keys():
                group, created = Group.objects.get_or_create(name=g,
                                                             league=league)

                for t in teams[l][g]:
                    team, created = Team.objects.get_or_create(name=t)
                    team.group.add(group)

        print(games)
        for game in games:
            # print(game)
            Game.objects.get_or_create(home=Team.objects.get(name__icontains=game[1]),
                                       visitors=Team.objects.get(name__icontains=game[2]),
                                       home_goals=game[6],
                                       visitors_goals=game[7],
                                       game_date=game[0],
                                       season=season,
                                       off=False if not game[6] and not game[7] else True,
                                       group=Group.objects.get(name=game[4], league=League.objects.get(name=game[3])) if game[4] != 'ПО' and game[4] != 'СТ' else None,
                                       tour=game[5]
                                       )
