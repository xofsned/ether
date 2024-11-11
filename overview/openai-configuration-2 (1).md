---
description: Configure bot-to-bot chat
---

# ⚙️ B2B Options

***

<details>

<summary>Bot Share</summary>

_`/b2b-options [ bot_share ] [ @botmention ]`_

By default, Ether ignores all bots - even when chatbot-option 'no-mention' is set Enabled (allowing Ether to respond to all messages without ping requirement).

Allow Ether to hear messages from a specific bot using bot\_share option

</details>

<details>

<summary>Bot Share Delay</summary>

_`/b2b-options [ bot_share_delay ] [ delay amount ]`_

Sets the delay in Ether's responses to the other bot

Range:

* 3 seconds \~ 120 seconds

</details>

<details>

<summary>Return Ping</summary>

_`/b2b-options [ return_ping ] [ enabled / disabled ]`_

Builds in a ping to the message author in Ether's response when message author is a bot in the bot\_share

</details>

<details>

<summary>Chat Logger</summary>

_`/b2b-options [ chat_logger ] [ enabled / disabled ]`_

Chat logger allows the owner of the session to generate logs from bot-2-bot chat

Limitations & configuration:

* Will log ONLY - Ether's messages and the 'other bot' added in bot\_share
* set\_chat\_user\_1 and set\_chat\_user\_2 must be configured for Ether and the other bot for logging

</details>

<details>

<summary>Chat User 1 &#x26; Chat User 2</summary>

_`/b2b-options [ set_chat_user_1 ] [ name ]`_\
_`/b2b-options [ set_chat_user_2 ] [ name ]`_

Example...

* Ether is set to 'assistant' in set\_chat\_user\_2, the 'other bot' added in bot\_share is set in set\_chat\_user\_2 as 'user'

Applies bot ID's of Ether and other bot in bot\_share to the logger service

Purpose is for setting assistant, user, system role respectively for logger and b2b members

</details>

<details>

<summary>Download Log</summary>

_`/b2b-options [ download_log ] [ option ]`_

Download logs generated by the logger

Options:

* single block of text
* tagname tabbed (tagnames from chat\_user\_1 and chat\_user\_2 implemented)
* OpenAI tuning dict structures log into json format (must have chat\_user\_1 and chat\_user\_2 set)

</details>

<details>

<summary>Clear Log</summary>

_`/b2b-options [ clear_log ] [ clear_log ]`_

Clears the chat generated log when chat\_logger has been enabled

</details>