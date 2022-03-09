COLUMNS_ACT = [
    'act_write',
    'act_track',
    'act_read',
    'act_do',
    'act_find',
    'act_excite',
    'act_memories',
]

OPTIONS_ACT = {
    'Never': 1,
    'Rarely': 2,
    'Sometimes': 3,
    'Very Often': 4,
    'Always': 5
}

COLUMNS_STREAM = [
    'stream_explore_can',
    'stream_explore_satisfied',
    'stream_explore_aligns',
    'stream_rediscovery_more',
    'stream_interact_more',
    'stream_find_can',
    'stream_discovered_different',
    'stream_recommend_outside',
    'stream_library_overview',
]

OPTIONS_STREAM = {
    'Strongly disagree': 1,
    'Disagree': 2,
    'Neither argee nor disagree': 3,
    'Agree': 4,
    'Strongly agree': 5
}

COLUMNS = [
              'time',
              'gender',
              'age',
              'country',
          ] + COLUMNS_ACT + [
              'music_background',
              'hours_all',
              'hours_active',
              'source_category',
              'source_streaming',
              'playlist_terms',
              'size_library',
              'discover_new',
              'discover_re_desire',
              'discover_re_actual',
              'discover_re_why',
              'sources_discover',
              'discover_strategy',
              'explore_terms',
              'discover_artists',
              'context',
              'discover_motivation',
          ] + COLUMNS_STREAM + [
              'comments',
          ]

LABELS_ACT = """
I write about music on social media
I keep track of new music that I come across (e.g. new artists or recordings)
I read or search the internet for things related to music
I do music-related activities in my free time
I try to find out more about music I’m not familiar with
I pick certain music to motivate or excite me
I listen to music to trigger the associated memories / put myself into associated  mood
""".strip().split('\n')

LABELS_STREAM = """
There are many options for music exploration and discovery
I am satisfied with the options for music exploration and discovery that are available
The way terms "music exploration and discovery" are used aligns well with my perception
I would like more functionality to rediscover my library
I would like to interact with my library in more ways than current systems allow
I can usually quickly find the music that I want to listen to
I have discovered music that is different from what I usually listen to through recommendations
There should be more recommendations outside of my comfort zone
It is easy for me to get an overview and manage my library
""".strip().split('\n')

OPTIONS_FREQUENCY = [
    'Every day',
    'Once or several times per week',
    'Once or several times per month',
    'Once or several times per year',
    'Never or almost never'
]
