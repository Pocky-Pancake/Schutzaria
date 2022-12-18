def DecalcPerms(PermValue:int):
    "Decalculates the permission value and outputs a list of permission names in strings."
    if PermValue == 0:
        return []
    elif PermValue == -1:
        return ["administrator"]
    else:
        Perms = [
            {"name":"moderate_members",             "value":0x10000000000},
            {"name":"start_embedded_activities",    "value":0x8000000000},
            {"name":"send_messages_in_threads",     "value":0x4000000000},
            {"name":"use_external_stickers",        "value":0x2000000000},
            {"name":"create_private_threads",       "value":0x1000000000},
            {"name":"create_public_threads",        "value":0x800000000},
            {"name":"manage_threads",               "value":0x400000000},
            {"name":"manage_events",                "value":0x200000000},
            {"name":"request_to_speak",             "value":0x100000000},
            {"name":"use_slash_commands",           "value":0x80000000},
            {"name":"manage_emojis_and_stickers",   "value":0x40000000},
            {"name":"manage_webhooks",              "value":0x20000000},
            {"name":"manage_roles",                 "value":0x10000000},
            {"name":"manage_nicknames",             "value":0x8000000},
            {"name":"change_nickname",              "value":0x4000000},
            {"name":"use_voice_activation",         "value":0x2000000},
            {"name":"move_members",                 "value":0x1000000},
            {"name":"deafen_members",               "value":0x800000},
            {"name":"mute_members",                 "value":0x400000},
            {"name":"speak",                        "value":0x200000},
            {"name":"connect",                      "value":0x100000},
            {"name":"view_guild_insights",          "value":0x80000},
            {"name":"use_external_emojis",          "value":0x40000},
            {"name":"mention_everyone",             "value":0x20000},
            {"name":"read_message_history",         "value":0x10000},
            {"name":"attach_files",                 "value":0x8000},
            {"name":"embed_links",                  "value":0x4000},
            {"name":"manage_messages",              "value":0x2000},
            {"name":"send_tts_messages",            "value":0x1000},
            {"name":"send_messages",                "value":0x800},
            {"name":"view_channel",                 "value":0x400},
            {"name":"stream",                       "value":0x200},
            {"name":"priority_speaker",             "value":0x100},
            {"name":"view_audit_log",               "value":0x80},
            {"name":"add_reactions",                "value":0x40},
            {"name":"manage_guild",                 "value":0x20},
            {"name":"manage_channels",              "value":0x10},
            {"name":"administrator",                "value":0x8},
            {"name":"ban_members",                  "value":0x4},
            {"name":"kick_members",                 "value":0x2},
            {"name":"create_instant_invite",        "value":0x1},
        ]

        DecalculatedPerms = []
        for x in Perms:
            PermValue -= x["value"]
            if PermValue < 0:
                PermValue += x["value"]
            else:
                DecalculatedPerms.append(x["name"])
        if PermValue != 0:
            print("Warning: Invalid Permission Value.")
            return 0xff
        else:
            return DecalculatedPerms
