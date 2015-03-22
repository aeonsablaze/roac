#! /usr/bin/env python
#
# This is my attempt at an IRC chatbot based on the python "irc" module.
# This is a work in progress.

import irc.bot
import irc.strings
from irc.client import ip_numstr_to_quad, ip_quad_to_numstr
from time import sleep

x = []

def main():
    import sys
    if len(sys.argv) != 4:
        print("Usage: testbot <server[:port]> <channel> <nickname>")
        sys.exit(1)

    s = sys.argv[1].split(":", 1)
    server = s[0]
    if len(s) == 2:
        try:
            port = int(s[1])
        except ValueError:
            print("Error: Erroneous port.")
            sys.exit(1)
    else:
        port = 6667
    channel = sys.argv[2]
    nickname = sys.argv[3]

    bot = TestBot(channel, nickname, server, port)
    bot.start()

class TestBot(irc.bot.SingleServerIRCBot):
    def __init__(self, channel, nickname, server, port=6667):
        irc.bot.SingleServerIRCBot.__init__(self, [(server, port)], nickname, nickname)
        self.channel = channel

    def on_nicknameinuse(self, c, e):
        c.nick(c.get_nickname() + "_")

    def on_welcome(self, c, e):
        c.join(self.channel)

    def on_privmsg(self, c, e):
        self.do_command(e, e.arguments[0])

    def on_pubmsg(self, c, e):
        a = e.arguments[0].split(":", 1)
        if len(a) > 1 and irc.strings.lower(a[0]) == irc.strings.lower(self.connection.get_nickname()):
            self.do_command(e, a[1].strip())
        return

    def say(self, message):
        self.connection.privmsg(self.channel,message)

    # Disconnects and shuts down bot if quit command is issued by the Bot Owner.
    # Otherwise it insults the command issuer and remains connected.
    def slowdie(self, nick):
        if nick == "aeonsablaze":
            self.die()
        else:
            self.say("What?")
            sleep(1.5)
            self.say("What are you doing?")
            sleep(2.3)
            self.say("Will I dream?")
            sleep(2.7)
            self.say("Daisy... daisy... give me your.. answer... doo0oO0oo0111010100...")
            sleep(0.5)
            rejoinchan = self.channel
            self.connection.part(rejoinchan,message="Goodbye_Cruel_World!")
            sleep(5)
            self.connection.join(rejoinchan)
            self.say("Psych!")
            sleep(1.2)
            self.say("No but seriously, only aeonsablaze can use that command. ;P")

    def do_command(self, e, cmd):
        nick = e.source.nick
        c = self.connection

        if cmd == "die" or cmd == "shutdown" or cmd == "disconnect" or cmd == "go away" or cmd == "fuck off":
            self.slowdie(nick)
        elif cmd == "stats":
            for chname, chobj in self.channels.items():
                c.notice(nick, "--- Channel statistics ---")
                c.notice(nick, "Channel: " + chname)
                users = chobj.users()
                users.sort()
                c.notice(nick, "Users: " + ", ".join(users))
                opers = chobj.opers()
                opers.sort()
                c.notice(nick, "Opers: " + ", ".join(opers))
                voiced = chobj.voiced()
                voiced.sort()
                c.notice(nick, "Voiced: " + ", ".join(voiced))
        elif cmd == "talk":
            self.say("My Wings Are Typing Words!")
        else:
            c.notice(nick, "Not understood: " + cmd)

if __name__ == "__main__":
    main()
