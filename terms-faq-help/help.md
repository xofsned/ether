---
description: Most common help topics
---

# ⁉️ Help

{% hint style="info" %}
Ether's Support Server: [https://discord.com/invite/gSMNvfDGa2](https://discord.com/invite/gSMNvfDGa2)
{% endhint %}

<details>

<summary>Ether is saying the API key is invalid, but it was just created</summary>

_OpenAI requires the API organization to initialize billing and make an initial payment. OpenAI refuses the key if the key is invalid or not fully initialized._

</details>

<details>

<summary>Ether is not responding to mentions or replies</summary>

* Double check that Ether has the correct permissions to message in the channel
* Check OpenAI status for outages
* Exit and re-initialize the session
* Check your OpenAI API account for any key errors, quota limits, or unpaid invoices

</details>

<details>

<summary>Used keyword <code>embed</code> and Ether stopped responding</summary>

_From a previous bug, hopefully fixed in recent editions_

* Restart the session, alter the configuration as needed, then try using the embed keyword again

</details>

<details>

<summary>Ether is returning large messages and weird syntax</summary>

_This is likely a ChatGPT hallucination caused from too high of temperature combined with no prompt or context_

</details>

<details>

<summary>When <code>nicknames</code> are enabled Ether provides many responses in a single message</summary>

_Nicknames, when enabled, require supplementary prompting to explain to ChatGPT that the context is a multi user discussion with nicknames before each message. Adding details to the prompt can help ChatGPT discern the nicknames in context._

</details>

<details>

<summary>After using <code>set</code> to alter configuration, some variables are broken</summary>

_Options for repairing or re-initializing variables:_

* Use slash command to reset the variable
* Re-initialize the session to reload defaults
* Upload a previously saved configuration to apply

</details>
