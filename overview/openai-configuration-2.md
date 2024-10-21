---
description: Configure your LM Studio experience
---

# ⚙️ LM Studio Configuration

***

<details>

<summary>Default session configuration</summary>

* model - None
* temperature - 0.7
* top\_k - 0
* top\_p - 0
* endpoint - None
* repeat penalty - 0
* frequency penalty - 0
* presence penalty - 0
* logit bias - 0
* seed - None
* tokens - 2000
* top string - None

</details>

<details>

<summary>Endpoint</summary>

_`/lmstudio-options [ endpoint ] [ web endpoint ]`_

Enter an endpoint to use with LM Studio API

</details>

<details>

<summary>Add a prompt</summary>

_`/lmsudio-options [ add_prompt ] [ new prompt ]`_

Give the session a prompt to be used by the author and any members accessing the session as a shared session.&#x20;

</details>

<details>

<summary>User prompt</summary>

_`/lmstudio-options [ user_prompt ] [ prompt ]`_

Give a user their own prompt to be used when they message the bot.

</details>

<details>

<summary>Manage the prompt</summary>

_`/lmstudio-options [ manage_prompt ] [ option ]`_

View or clear the prompt in the active session.

Options:

* `view`
* `clear`

</details>

<details>

<summary>model selection</summary>

_`/lmstudio-options [ model ] [ user provided model ]`_

User gives the model name string supplied to them by LM Studio API

</details>

<details>

<summary>Temperature</summary>

_`/lmstudio-options [ temperature ] [ amount ]`_

Selects the temperature level for the model

Options:

* `0.1 ~ 1.0`

</details>

<details>

<summary>Tokens</summary>

_`/openai-options [ tokens ] [ amount ]`_

Selects the maximum tokens to use on a transaction (including context tokens)

Options:

* `50 ~ 4000`

</details>

<details>

<summary>Frequency</summary>

_`/lmstudio-options [ frequency_penalty ] [ amount ]`_

Selects the frequency penalty&#x20;

Options:

* `0.1 ~ 1.0`

</details>

<details>

<summary>Repeat</summary>

_`/lmstudio-options [ repeat_penalty ] [ amount ]`_

Selects the repeat penalty&#x20;

Options:

* `0.1 ~ 1.0`

</details>

<details>

<summary>Presence</summary>

_`/lmstudio-options [ presence_penalty ] [ amount ]`_

Selects the presence penalty&#x20;

Options:

* `0.1 ~ 1.0`

</details>

<details>

<summary>Top_P</summary>

_`/lmstudio-options [ top_p ] [ amount ]`_

Selects the top\_p amount

Options:

* `0.1 ~ 1.0`

</details>

<details>

<summary>Top_K</summary>



_`/lmstudio-options [ top_k ] [ amount ]`_

Selects the top\_k amount

Options:

* `0.1 ~ 1.0`

</details>

<details>

<summary>Stop String</summary>

_`/lmstudio-options [ stop_string ] [ string ]`_

Add a stop string to be used in LM Studio API parsing

</details>

<details>

<summary>Seed</summary>

_`/lmstudio-options [ frequency_penalty ] [ amount ]`_

Choose a seed to use in LM Studio API parsing

</details>

<details>

<summary>Logit Bias</summary>

_`/lmstudio-options [ logit_bias ] [ amount ]`_

Selects the logit bias amount

Options:

* `0.1 ~ 1.0`

</details>
