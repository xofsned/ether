---
description: 'Last Updated: Feb 2nd, 2024'
---

# 🛠️ In development

***

### In the workshop or in testing

✅ = finished, ⚙️ = in testing, ✖️ = in progress

{% tabs %}
{% tab title="Features" %}
* ✖️ Fine Tuning
* ✖️ Streamed Embeds
* ✖️ Additional file type support
* ✖️ Generating training data from streamed embeds
* ✖️ Additional functionality repairs & updates
* ✅ No Mention - disable or enable requirement to mention Ether in message
* ✅ Built-in Profiles - configurations for sessions for quick selection
{% endtab %}

{% tab title="Configurations" %}
* ✖️ Fine tuning options
* ✖️ Extending associations utility for generating fine tuning data
* ✅ Extended sharing options
* ✅ Session configuration by message description
* ✅ DALL E 3 updates
  * style
  * dimensions
  * number
{% endtab %}

{% tab title="Commands" %}
_Splitting /ether into multiple slash commands_

✖️  /fine-tuning

_Command refactor for Feb 2024:_ ✅

* /association-options
* /chatbot-options
* /manager
* /openai-options
* /profiles
* /sharing-options
* /terms
{% endtab %}

{% tab title="Bugs" %}
* ✖️ Ability to draw, embed, etc - in message reply
* ✖️ Ability to add a prompt along with other variables in one iteration
* ✖️ Errors in stacked context
* ✖️ Ability to change or disable extension when extensions is maxed
* ✅ Ether not responding to users who have active sessions when they are accessing in a different shared session
* ✅ Bug fixes to keyword embed
* ✅ Sessions not displaying when exceeding certain number or other?
* ✅ In fast environment, in image generation, Ether replies to wrong message
{% endtab %}

{% tab title="Integrations" %}
* ✖️ SQL for embeddings
* ⚙️ PCAP for embeddings
* ⚙️ OCSF for embeddings
* ⚙️ JSON for embeddings
* ⚙️ XML for embeddings
{% endtab %}
{% endtabs %}

***

### Future goals & early designs

<details>

<summary>Fine tuning</summary>

New slash command option for:

* uploading training data
* viewing uploaded data
* viewing fine tuned models
* accessing and using fine tuned models
* viewing the training details

Modified Associations:

* optional comma separator in associations
* ability for multi user data generation
  * e.g. one user asks questions, another answers, all generated into fine tuning data

</details>

<details>

<summary>Streamed embeds</summary>

Streamed embeds, in the context of feedback loops or continuously supplied data

</details>

<details>

<summary>Stronger multi-language support</summary>

Ability to generate custom keywords to replace words such as 'draw' in any language

Ability to set a session to be visual or draw specific, setting every message automatically into a specific service

</details>

***

### Archives
