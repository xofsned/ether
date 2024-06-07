---
description: Generate data from GPT - GPT chat (Bot to Bot chat)
---

# ⛓️ Advanced Options

***

{% hint style="info" %}
This feature assumes you operate or have another bot that will chat with other bots
{% endhint %}

***

<details>

<summary>Bot sharing</summary>

_`/advanced_options [ bot_share ] [ @botmention ]`_

Separate from general sharing options, this command allows specifically a bot's messages to be seen by Ether.

* Requires setting /sharing-options also
* Is not limited in any number of bots that can be added

</details>

<details>

<summary>Response delay</summary>

_`/advanced_options [ bot_share_delay ] [ amount in seconds ]`_

Sets the delay in Ether before responding, with a minimum setting of 3 seconds

</details>

<details>

<summary>Log generation &#x26; management</summary>

_`/advanced_options [ chat_logger ] [ enable ]`_

_`/advanced_options [ clear_log ]`_

_`/advanced_options [ download_log ] [ log type ]`_

When correctly configured before B2B chat, Ether can generate logs in .txt and .json from GPT vs GPT chat.

<mark style="color:yellow;">NOTE:</mark>&#x20;

* <mark style="color:yellow;">Tag-names MUST be set PRIOR to B2B chat (is appended during chat)</mark>
* <mark style="color:yellow;">Tag-names MUST be</mark> <mark style="color:yellow;"></mark>_<mark style="color:yellow;">**'assistant'**</mark>_ <mark style="color:yellow;"></mark><mark style="color:yellow;">and</mark> <mark style="color:yellow;"></mark>_<mark style="color:yellow;">**'user'**</mark>_ <mark style="color:yellow;"></mark><mark style="color:yellow;">to produce a complete JSON</mark>

Log types:

* Full block of text (messages between bots combined into a single block of text)
* Inline with tag-names (readability, user: message, assistant: message, separated line per line)
* JSON dictionary structure for OpenAI fine-tuning

Example of inline:

* Tagname1: Hello, how are you?
* Tagname2: Hello, I am well!

Example of JSON:

{ "messages": \[ { "role": "system", "content": "You are an assistant" }, { "role": "assistant", "content": "What was the most challenging aspect of your journey into space?" }, { "role": "user", "content": "The isolation....." },.......

</details>

<details>

<summary>Setting tag-names for logs</summary>

_`/advanced_options [ set_chat_user_1 ] [ name ]`_

_`/advanced_options [ set_chat_user_2 ] [ name ]`_

Chat user 1 represents the Ether bot, chat user 2 represents _the other bot._ When configured, these tag-names will be used as identifiers in log generation.

</details>

{% hint style="info" %}

{% endhint %}
