---
description: Configure your ChatGPT experience
---

# ⚙️ OpenAI Configuration

***

{% hint style="info" %}
Ether uses API options provided by OpenAI. Any limitations, constraints, or validations are solely for the operability and compliance of Ether with OpenAI's API.&#x20;
{% endhint %}

***

<details>

<summary>Default session configuration</summary>

* Tokens: 2000
* Context: 0
* Text model: GPT 3.5-Turbo
* Image model: DALL E 3
* Role: user
* Temperature: 0.3
* Nicknames: False
* Sharing: False
* Extensions: None
* Frequency: 0
* Presence: 0
* Top\_P: 0
* Prompt: None

</details>

<details>

<summary>Add a prompt</summary>

_`/openai-options [ add_prompt ] [ new prompt ]`_

Give the session a prompt to be used by the author and any members accessing the session as a shared session.&#x20;

</details>

<details>

<summary>Manage the prompt</summary>

_`/openai-options [ manage_prompt ] [ option ]`_

View or clear the prompt in the active session.

Options:

* `view`
* `clear`

</details>

<details>

<summary>Text model selection</summary>

_`/openai-options [ model ] [ option ]`_

Select a text generative model to use.

Options:

* `gpt-3.5-turbo`&#x20;
* `gpt-4`&#x20;
* `gpt-4-1106-preview`
* `gpt-4-0613`
* `gpt-4-0314`
* `gpt-3.5-turbo-16k-0613`
* `gpt-3.5-turbo-16k`
* `gpt-3.5-turbo-1106`
* `gpt-3.5-turbo-0613`
* `gpt-3.5-turbo-0301`

</details>

<details>

<summary>Image model selection</summary>

_`/openai-options [ image_model ] [ option ]`_

Selects the image model to use

Options:

* `DALL E 2`
* `DALL E 3`

</details>

<details>

<summary>Assistants</summary>

_`/openai-options [ assistant ] [ option ]`_

Selects an assistant to use

Options:

* `interpreter`

</details>

<details>

<summary>Temperature</summary>

_`/openai-options [ temperature ] [ amount ]`_

Selects the temperature level for the model

Options:

* `0.1 ~ 2.0`

</details>

<details>

<summary>Tokens</summary>

_`/openai-options [ tokens ] [ amount ]`_

Selects the maximum tokens to use on a transaction (including context tokens)

Options:

* `50 ~ 4000`

</details>

<details>

<summary>Role</summary>

_`/openai-options [ role ] [ option ]`_

Selects the role to give ChatGPT (OpenAI Role)

Options:

* `user`
* `system`

</details>

<details>

<summary>Frequency</summary>

_`/openai-options [ frequency ] [ amount ]`_

Selects the frequency penalty for context transactions

Options:

* `0.1 ~ 2.0`

</details>

<details>

<summary>Presence</summary>

_`/openai-options [ presence ] [ amount ]`_

Selects the presence penalty for context transactions

Options:

* `0.1 ~ 2.0`

</details>

<details>

<summary>Top_P</summary>

_`/openai-options [ top_p ] [ amount ]`_

Selects the top\_p nucleus sampling level

Options:

* `0.1 ~ 2.0`

</details>

<details>

<summary>Style of image</summary>

_`/openai-options [ style ] [ option ]`_

Selects the style of image to generate

Options:

* `Natural`
* `Vivid`

</details>

<details>

<summary>Number of images</summary>

_`/openai-options [ number ] [ amount ]`_

Selects the number of images to generate in each iteration

Options:

* `1 - 10`

</details>

<details>

<summary>Size of image</summary>

_`/openai-options [ size ] [ option ]`_

Selects the size image size to be generated

Options:

* `DALL E 2`
  * `256x256, 512x512, 1024x1024`
* `DALL E 3`
  * `1024x1024, 1024x1792, 1792x1024`

</details>

<details>

<summary>Revised prompt</summary>

_`/openai-options [ revised_prompt ] [ option ]`_

Selects to enable or disable displaying the returned revised prompt from DALL E 3 with the generated image

Options:

* `Enabled`
* `Disabled`

</details>
