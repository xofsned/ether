---
description: Configure Ether's chatbot options
---

# ⚙️ Chatbot Configuration

***

{% hint style="info" %}
Chatbot options are relative to Discord and Ether as a chatbot
{% endhint %}

***

<details>

<summary>Defaults</summary>

* context: 0
* nicknames: False
* no\_mention: False
* advanced\_image: False
* interactions: False
* custom\_keywords: None&#x20;

</details>

<details>

<summary>Context Amount</summary>

&#x20;_`/chatbot-options [ context_amount ] [ amount ]`_

Choose the number of previous messages to send as context

Options:

* `1 - 10`

</details>

<details>

<summary>Context Type</summary>

&#x20;_`/chatbot-options [ context_type ] [ type ]`_

Types:

* Stacked
  * Wraps each individual message in context with its own role and API message string
* Combined
  * Combines all context as one block of text, wrapped in the role and prompt
* Segmented
  * Collects only the message author messages in context
* Alternating
  * Alternating context attempts to construct the context for LM Studio alternating context API call structure

</details>

<details>

<summary>Nicknames</summary>

&#x20;_`/chatbot-options [ nicknames ] [ option ]`_

Enable nickname resolving in context (may require additional prompting for ChatGPT to discern the nicknames)

Options:

* `enabled`
* `disabled`

</details>

<details>

<summary>No mention</summary>

_`/chatbot-options [ no_mention ] [ option ]`_

Enable or disable the requirement to mention the bot in discussion

Options:

* `enabled`
* `disabled`

</details>

<details>

<summary>Ignore users</summary>

_`/chatbot-options [ ignore_users ] [ option ]`_

Enables a requirement for Discord users to use bot mention while no\_mention option is also enabled. This feature allows users to have chat among b2b chat without interrupting or prompting the bots.&#x20;

In other words, this override allows for the no\_mention feature to only be applied to other bots when using the /advanced-options and b2b chat utilities.

</details>
