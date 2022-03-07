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
