# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['chicken_dinner',
 'chicken_dinner.assets',
 'chicken_dinner.models',
 'chicken_dinner.models.match',
 'chicken_dinner.models.telemetry',
 'chicken_dinner.pubgapi',
 'chicken_dinner.visual']

package_data = \
{'': ['*'],
 'chicken_dinner.assets': ['maps/Baltic_Main_Low_Res.png',
                           'maps/Baltic_Main_Low_Res.png',
                           'maps/Baltic_Main_Low_Res.png',
                           'maps/Baltic_Main_Low_Res.png',
                           'maps/Baltic_Main_Low_Res.png',
                           'maps/Baltic_Main_Low_Res.png',
                           'maps/Desert_Main_Low_Res.png',
                           'maps/Desert_Main_Low_Res.png',
                           'maps/Desert_Main_Low_Res.png',
                           'maps/Desert_Main_Low_Res.png',
                           'maps/Desert_Main_Low_Res.png',
                           'maps/Desert_Main_Low_Res.png',
                           'maps/DihorOtok_Main_Low_Res.png',
                           'maps/DihorOtok_Main_Low_Res.png',
                           'maps/DihorOtok_Main_Low_Res.png',
                           'maps/DihorOtok_Main_Low_Res.png',
                           'maps/DihorOtok_Main_Low_Res.png',
                           'maps/DihorOtok_Main_Low_Res.png',
                           'maps/Erangel_Main_Low_Res.png',
                           'maps/Erangel_Main_Low_Res.png',
                           'maps/Erangel_Main_Low_Res.png',
                           'maps/Erangel_Main_Low_Res.png',
                           'maps/Erangel_Main_Low_Res.png',
                           'maps/Erangel_Main_Low_Res.png',
                           'maps/Range_Main_Low_Res.png',
                           'maps/Range_Main_Low_Res.png',
                           'maps/Range_Main_Low_Res.png',
                           'maps/Range_Main_Low_Res.png',
                           'maps/Range_Main_Low_Res.png',
                           'maps/Range_Main_Low_Res.png',
                           'maps/Savage_Main_Low_Res.png',
                           'maps/Savage_Main_Low_Res.png',
                           'maps/Savage_Main_Low_Res.png',
                           'maps/Savage_Main_Low_Res.png',
                           'maps/Savage_Main_Low_Res.png',
                           'maps/Savage_Main_Low_Res.png']}

install_requires = \
['requests>=2.22,<3.0']

extras_require = \
{'visual': ['matplotlib>=3.1,<4.0', 'pillow>=6.1,<7.0']}

setup_kwargs = {
    'name': 'chicken-dinner',
    'version': '0.9.0',
    'description': 'PUBG JSON API Wrapper and Game Telemetry Visualizer',
    'long_description': 'Chicken Dinner\n==============\n\n|rtd| |pypi| |pyversions|\n\n.. |rtd| image:: https://img.shields.io/readthedocs/chicken-dinner.svg\n    :target: http://chicken-dinner.readthedocs.io/en/latest/\n\n.. |pypi| image:: https://img.shields.io/pypi/v/chicken-dinner.svg\n    :target: https://pypi.python.org/pypi/chicken-dinner\n\n.. |pyversions| image:: https://img.shields.io/pypi/pyversions/chicken-dinner.svg\n    :target: https://pypi.python.org/pypi/chicken-dinner\n\nPython PUBG JSON API Wrapper and (optional) playback visualizer.\n\nSamples\n-------\n\n* `Erangel - squads <http://chicken-dinner.readthedocs.io/en/latest/sample_erangel.html>`_\n* `Miramar - solos <http://chicken-dinner.readthedocs.io/en/latest/sample_miramar.html>`_\n* `Sanhok - duos <http://chicken-dinner.readthedocs.io/en/latest/sample_sanhok.html>`_\n* `Vikendi - duos <http://chicken-dinner.readthedocs.io/en/latest/sample_vikendi.html>`_\n\nInstallation\n------------\n\nTo install chicken-dinner, use pip. This will install the core dependencies\n(``requests`` library) which provide functionality to the API wrapper classes.\n\n.. code-block:: bash\n\n    pip install chicken-dinner\n\nTo use the playback visualizations you will need to install the library with\nextra dependencies for plotting (``matplotlib`` and ``pillow``).\nFor this you can also use pip:\n\n.. code-block:: bash\n\n    pip install chicken-dinner[visual]\n\nTo generate the animations you will also need ``ffmpeg`` installed on your\nmachine. On Max OSX you can install ``ffmpeg`` using brew.\n\n.. code-block:: bash\n\n    brew install ffmpeg\n\nYou can install ffmpeg on other systems from `here <https://www.ffmpeg.org/download.html>`_.\n\nUsage\n-----\n\nWorking with the low-level API class.\n\n.. code-block:: python\n\n    from chicken_dinner.pubgapi import PUBGCore\n\n    api_key = "your_api_key"\n    pubgcore = PUBGCore(api_key, "pc-na")\n    shroud = pubgcore.players("player_names", "shroud")\n    print(shroud)\n\n    # {\'data\': [{\'type\': \'player\', \'id\': \'account.d50f...\n\nWorking with the high-level API class.\n\n.. code-block:: python\n\n    from chicken_dinner.pubgapi import PUBG\n\n    api_key = "your_api_key"\n    pubg = PUBG(api_key, "pc-na")\n    shroud = pubg.players_from_names("shroud")[0]\n    shroud_season = shroud.get_current_season()\n    squad_fpp_stats = shroud_season.game_mode_stats("squad", "fpp")\n    print(squad_fpp_stats)\n\n    # {\'assists\': 136, \'boosts\': 313, \'dbnos\': 550, \'daily_kills\':...\n\nVisualizing telemetry data\n\n.. code-block:: python\n\n    from chicken_dinner.pubgapi import PUBG\n\n    api_key = "your_api_key"\n    pubg = PUBG(api_key, "pc-na")\n    shroud = pubg.players_from_names("shroud")[0]\n    recent_match_id = shroud.match_ids[0]\n    recent_match = pubg.match(recent_match_id)\n    recent_match_telemetry = recent_match.get_telemetry()\n    recent_match_telemetry.playback_animation("recent_match.html")\n\nRecommended playback settings:\n\n.. code-block:: python\n\n    telemetry.playback_animation(\n        "match.html",\n        zoom=True,\n        labels=True,\n        label_players=[],\n        highlight_winner=True,\n        label_highlights=True,\n        size=6,\n        end_frames=60,\n        use_hi_res=False,\n        color_teams=True,\n        interpolate=True,\n        damage=True,\n        interval=2,\n        fps=30,\n    )\n\nSee the `documentation <http://chicken-dinner.readthedocs.io>`_ for more\ndetails.\n\nUpdating Assets\n---------------\n\nThis package uses PUBG map images and a dictionary of asset names/ids for use with generating\ntelemetry visualizations as well as naming values in telemetry events and objects.\n\nTo update the map images and asset dictionary, run the following commands.\n\n.. code-block:: bash\n\n    python -m chicken_dinner.assets.maps\n    python -m chicken_dinner.assets.dictionary\n\nMore Examples\n-------------\n\nSetup\n~~~~~\n\nCreating a ``PUBG`` instance.\n\n.. code-block:: python\n\n    from chicken_dinner.pubgapi import PUBG\n\n    api_key = "my_api_key"\n    pubg = PUBG(api_key=api_key, shard="steam")\n\n\nPlayer Examples\n~~~~~~~~~~~~~~~\n\nGetting information for a player by their name.\n\n.. code-block:: python\n\n    # Creates a Players instance (iterable Player instances)\n    players = pubg.players_from_names("chocoTaco")\n\n    # Take the first Player instance from the iterable\n    chocotaco = players[0]\n\n    chocotaco.name\n    # chocoTaco\n\n    chocotaco.match_ids\n    # [\'e0b3cb15-929f-4b42-8873-68a8f9998d2b\', \'dd25cf69-77f1-4791-9b14-657e904d3534\'...\n\n    chocotaco.id\n    # \'account.15cbf322a9bc45e88b0cd9f12ef4188e\'\n\n    chocotaco.url\n    # \'https://api.playbattlegrounds.com/shards/steam/players/account.15cbf322a9bc45e88b0cd9f12ef4188e\'\n\n\nOr get the player instance from the id.\n\n.. code-block:: python\n\n    # Creates a Players instance (iterable Player instances)\n    players = pubg.players_from_ids("account.15cbf322a9bc45e88b0cd9f12ef4188e")\n\n    # Take the first Player instance from the iterable\n    chocotaco = players[0]\n\n\nGet information about multiple players and matches that they participated together.\n\n.. code-block:: python\n\n    # Creates a Players instance (iterable of Player instances)\n    players = pubg.players_from_names(["shroud", "chocoTaco"])\n\n    players.ids\n    # [\'account.d50fdc18fcad49c691d38466bed6f8fd\', \'account.15cbf322a9bc45e88b0cd9f12ef4188e\']\n\n    players.names_to_ids()\n    # {\'shroud\': \'account.d50fdc18fcad49c691d38466bed6f8fd\', \'chocoTaco\': \'account.15cbf322a9bc45e88b0cd9f12ef4188e\'}\n\n    players.ids_to_names()\n    # {\'account.d50fdc18fcad49c691d38466bed6f8fd\': \'shroud\', \'account.15cbf322a9bc45e88b0cd9f12ef4188e\': \'chocoTaco\'}\n\n    players.shared_matches()\n    # [\'e0b3cb15-929f-4b42-8873-68a8f9998d2b\', \'dd25cf69-77f1-4791-9b14-657e904d3534\'...\n\n    shroud = players[0]\n    chocotaco = players[1]\n\nSeason Examples\n~~~~~~~~~~~~~~~\n\nGet an iterable of ``Seasons`` objects\n\n.. code-block:: python\n\n    seasons = pubg.seasons()\n\n    seasons.ids\n    # [\'division.bro.official.2017-beta\', \'division.bro.official.2017-pre1\'...\n\n    # Get the current season\n    current_season = seasons.current()\n\n\nWork with a ``Season`` instance\n\n.. code-block:: python\n\n    season = pubg.current_season()\n\n    season.id\n    # \'division.bro.official.pc-2018-04\'\n\n    season.is_current()\n    # True\n\n    season.is_offseason()\n    # False\n\n    # Get a player-season for a specific player\n    chocotaco_season = season.get_player("account.15cbf322a9bc45e88b0cd9f12ef4188e")\n\n\nGetting information about a player-season\n\n.. code-block:: python\n\n    # Using the factory instance directly\n    chocotaco_season = pubg.player_season("account.15cbf322a9bc45e88b0cd9f12ef4188e", "division.bro.official.pc-2018-04")\n\n    # Using a season\n    season = pubg.current_season()\n    chocotaco_season = season.get_player("account.15cbf322a9bc45e88b0cd9f12ef4188e")\n\n    # Using a player\n    chocotaco = pubg.players_from_names("chocoTaco")[0]\n    chocotaco_season = chocotaco.get_season("division.bro.official.pc-2018-04")\n\n    chocotaco_season.id\n    # {\'player_id\': \'account.15cbf322a9bc45e88b0cd9f12ef4188e\', \'season_id\': \'division.bro.official.pc-2018-04\'}\n\n    chocotaco_season.player_id\n    # \'account.15cbf322a9bc45e88b0cd9f12ef4188e\'\n\n    chocotaco_season.season_id\n    # \'division.bro.official.pc-2018-04\'\n\n    chocotaco_season.match_ids("solo", "fpp")\n    # [\'4b0c5898-7149-4bcc-8da7-df4cdc07fd80\', \'b26880e5-916d-4be8-abd7-45d8dddb6df3\'...\n\n    chocotaco_season.game_mode_stats("solo", "fpp")\n    # {\'assists\': 38, \'boosts\': 498, \'dbnos\': 0, \'daily_kills\': 18, \'daily_wins\': 0, \'damage_dealt\': 95036.79...\n\n\nLeaderboards\n~~~~~~~~~~~~\n\nLeaderboards give the top 25 players for a particular game mode.\n\n.. code-block:: python\n\n    solo_fpp_leaderboard = pubg.leaderboard("solo-fpp")\n\n    solo_fpp_leaderboard.game_mode\n    # \'solo-fpp\'\n\n    solo_fpp_leaderboard.ids\n    # [\'account.cfb13f65d5d1452294efbe7e730f7b1c\', \'account.9affa4ff8e5746bbb6a199f1a773c659\'...\n\n    solo_fpp_leaderboard.names\n    # [\'HuYa-17152571\', \'Huya_15007597_LS\', \'Douyu-7250640\', \'Douyu-4778209\', \'DouYu-1673291\'...\n\n    solo_fpp_leaderboard.ids_to_names()\n    # {\'account.f897d4a4b22f45cb8a85008039f5069e\': \'HuYaTv-19488958\', \'account.8ca07daf6c084dea81aacc00616fde9c\': \'Breukin224\'...\n\n    solo_fpp_leaderboard.names_to_ids()\n    # {\'HuYaTv-19488958\': \'account.f897d4a4b22f45cb8a85008039f5069e\', \'Breukin224\': \'account.8ca07daf6c084dea81aacc00616fde9c\'...\n\n    # Info about a player at particular rank\n    solo_fpp_leaderboard.name(1)\n    # \'HuYa-17152571\'\n\n    solo_fpp_leaderboard.id(1)\n    # \'account.cfb13f65d5d1452294efbe7e730f7b1c\'\n\n    solo_fpp_leaderboard.stats(1)\n    # {\'rank_points\': 6344, \'wins\': 82, \'games\': 1591, \'win_ratio\': 0.0515399128, \'average_damage\': 247, \'kills\': 3218...\n\n    # Get a player object for a player at rank 1\n    player = solo_fpp_leaderboard.get_player(1)\n\nSamples\n~~~~~~~\n\nGet randomly sampled match ids.\n\n.. code-block:: python\n\n    samples = pubg.samples()\n\n    samples.match_ids\n    # [\'98192d81-8700-4e28-981d-00b14dfbb3c9\', \'7ce51ef0-6f73-4974-9bb6-532dec58355d\'...\n\n\nAPI Status\n~~~~~~~~~~\n\nGet the current API status\n\n.. code-block:: python\n\n    status = pubg.status()\n\n    status.id\n    # \'pubg-api\'\n\n    # Refreshes the API status\n    status.refresh()\n\nMatches\n~~~~~~~\n\nGet match information\n\n.. code-block:: python\n\n    match = pubg.match("e0b3cb15-929f-4b42-8873-68a8f9998d2b")\n\n    match.asset_id\n    # \'44b787fd-c153-11e9-8b6c-0a586467d436\'\n\n    match.created_at\n    # \'2019-08-18T00:29:00Z\'\n\n    match.duration\n    # 1686\n\n    match.game_mode\n    # \'duo-fpp\'\n\n    match.id\n    # \'e0b3cb15-929f-4b42-8873-68a8f9998d2b\'\n\n    match.is_custom\n    # False\n\n    match.map_id\n    # \'Baltic_Main\'\n\n    match.map_name\n    # \'Erangel (Remastered)\'\n\n    match.rosters_player_names\n    # {\'9354f12b-8e79-4ca2-9465-6bdfa6b4bca9\': [\'Vealzor\', \'Colin630\'], \'c2eb2ecf-96d5-42c3-b0cb-49d734a716a6\': [\'KillaCon\', \'FriendlyOrc\']...\n\n    match.telemetry_url\n    # \'https://telemetry-cdn.playbattlegrounds.com/bluehole-pubg/steam/2019/08/18/00/58/44b787fd-c153-11e9-8b6c-0a586467d436-telemetry.json\'\n\n    match.url\n    # \'https://api.playbattlegrounds.com/shards/steam/matches/e0b3cb15-929f-4b42-8873-68a8f9998d2b\'\n\nGet rosters and associated participants\n\n.. code-block:: python\n\n    # Get rosters\n    rosters = match.rosters\n\n    # Get single roster\n    roster = rosters[0]\n\n    roster.player_ids\n    # [\'account.7046d72ec24e45a7b0282d390dea91e5\', \'account.9a154840c7db4f7f88def5198b9393b6\']\n\n    roster.player_names\n    # [\'Vealzor\', \'Colin630\']\n\n    roster.stats\n    # {\'rank\': 44, \'team_id\': 12, \'won\': \'false\'}\n\n    roster.won\n    # False\n\n    # Participant from a roster\n    roster_participants = roster.participants\n    participant = roster_participant[0]\n\n    participant.name\n    # \'Vealzor\'\n\n    participant.player_id\n    # \'account.7046d72ec24e45a7b0282d390dea91e5\'\n\n    participant.stats\n    # {\'dbnos\': 1, \'assists\': 0, \'boosts\': 0, \'damage_dealt\': 113.032738...\n\n    participant.teammates_player_ids\n    # [\'account.9a154840c7db4f7f88def5198b9393b6\']\n\n    participant.teammates_player_names\n    # [\'Colin630\']\n\n    participant.won\n    # False\n\n    # Get Participant instances for teammates\n    teammates = participant.teammates\n\nGet all Participants from Match\n\n.. code-block:: python\n\n    match_participants = match.participants\n\n\nTelemetry\n~~~~~~~~~\n\nGet a Telemetry instance from a particular match\n\n.. code-block:: python\n\n    # Using the PUBG instance\n    url = \'https://telemetry-cdn.playbattlegrounds.com/bluehole-pubg/steam/2019/08/18/00/58/44b787fd-c153-11e9-8b6c-0a586467d436-telemetry.json\'\n    telemetry = pubg.telemetry(url)\n\n    # Using a Match instance\n    match = pubg.match("e0b3cb15-929f-4b42-8873-68a8f9998d2b")\n    telemetry = match.get_telemetry()\n\n    # All available event types\n    telemetry.event_types()\n    # [\'log_armor_destroy\', \'log_care_package_land\', \'log_care_package_spawn\', \'log_game_state_periodic\', \'log_heal\'...\n\n    # All specific events\n    care_package_lands = telemetry.filter_by("log_care_package_land")\n\n    telemetry.map_id()\n    # \'Baltic_Main\'\n\n    telemetry.map_name()\n    # \'Erangel (Remastered)\'\n\n    telemetry.num_players()\n    # 100\n\n    telemetry.num_teams()\n    # 50\n\n    telemetry.platform\n    # \'pc\'\n\n    # Generates an HTML5 animation with ffmpeg\n    telemetry.playback_animation("match.html")\n\n    # Many more functions related to positions, circles, damages. Refer to docs\n\n\nTelemetry events and objects are generic class wrappers. They are constructed\nwhen the Telemetry instance is created. This makes them telemetry version-agnostic,\nbut requires some work to inspect their contents and structure. The TelemetryEvent\nand TelemetryObject classes also transform the payload keys to snake_case.\n\nTelemetryEvents are containers for event key-values and structures which contain a\nhierarchy of TelemetryObjects.\n\n`Telemetry Events <https://documentation.pubg.com/en/telemetry-events.html>`_\n\n.. code-block:: python\n\n    # Get all TelemetryEvents as a list\n    events = telemetry.events\n\n    # Get one of the events\n    event = events[0]\n\n    event.event_type\n    # log_match_definition\n\n    event.timestamp\n    # \'2019-08-18T00:29:00.0807375Z\'\n\n    event.to_dict()\n    # {\'_D\': \'2019-08-18T00:29:00.0807375Z\', \'_T\': \'LogMatchDefinition\', \'match_id\': \'match.bro.official.pc-2018-04.steam.duo-fpp.na.2019.08.18.00.e0b3cb15-929f-4b42-8873-68a8f9998d2b\', \'ping_quality\': \'low\', \'season_state\': \'progress\'}\n\n    print(event.dumps())\n    # {\n    #     "_D": "2019-08-18T00:29:00.0807375Z",\n    #     "_T": "LogMatchDefinition",\n    #     "match_id": "match.bro.official.pc-2018-04.steam.duo-fpp.na.2019.08.18.00.e0b3cb15-929f-4b42-8873-68a8f9998d2b",\n    #     "ping_quality": "low",\n    #     "season_state": "progress"\n    # }\n\n    # Each event key can be grabbed as an attribute or key\n    event.ping_quality\n    # low\n\n    event["ping_quality"]\n    # low\n\n\nTelemetryObjects refer to entities such as players, items, locations, vehicles, etc.\nEach TelemetryObject contains a ``reference`` attribute which is the key in the parent\nTelemetryEvent or TelemetryObject that refers to this TelemetryObject.\n\n`Telemetry Objects <https://documentation.pubg.com/en/telemetry-objects.html>`_\n\n.. code-block:: python\n\n    # All available event types\n    telemetry.event_types()\n    # [\'log_armor_destroy\', \'log_care_package_land\', \'log_care_package_spawn\', \'log_game_state_periodic\', \'log_heal\'...\n\n    kill_events = telemetry.filter_by("log_player_kill")\n    kill = kill_events[0]\n\n    kill.keys()\n    # [\'attack_id\', \'killer\', \'victim\', \'assistant\', \'dbno_id\', \'damage_reason\'...\n\n    killer = kill.killer\n    killer.keys()\n    # [\'reference\', \'name\', \'team_id\', \'health\', \'location\', \'ranking\', \'account_id\', \'is_in_blue_zone\', \'is_in_red_zone\', \'zone\']\n\n    killer.name\n    # \'WigglyPotato\'\n\n    victim = kill.victim\n    victim.keys()\n    # [\'reference\', \'name\', \'team_id\', \'health\', \'location\', \'ranking\', \'account_id\', \'is_in_blue_zone\', \'is_in_red_zone\', \'zone\']\n\n    victim.name\n    # \'qnle\'\n\n    victim.to_dict()\n    # {\'account_id\': \'account.d9c2d8dc8c03412eadfa3e59c8f3c16a\', \'health\': 0, \'is_in_blue_zone\': False, \'is_in_red_zone\': False...\n\n    for k, v in victim.items():\n        print(k, v)\n    # reference victim\n    # name qnle\n    # team_id 43\n    # health 0\n    # location TelemetryObject location object\n    # ranking 0\n    # account_id account.d9c2d8dc8c03412eadfa3e59c8f3c16a\n    # is_in_blue_zone False\n    # is_in_red_zone False\n    # zone [\'georgopol\']\n',
    'author': 'Christopher Flynn',
    'author_email': 'crf204@gmail.com',
    'url': 'https://github.com/crflynn/chicken-dinner',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
