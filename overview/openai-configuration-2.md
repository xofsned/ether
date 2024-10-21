---
description: Configure Ether's built-in AI for your user / bot interactions
---

# ⚙️ Built-In AI Configuration

{% hint style="info" %}
Ether's built-in AI will work for those who do not have an active session in the message channel, and also when there are no shared sessions in the message channel.

Options set in /ether-ai only apply to the user setting the options (per user setting)
{% endhint %}

<details>

<summary>Select Prompt</summary>

_`/ether-ai [ select_prompt ] [ prompt ]`_

Select a prompt to use in your interactions

Options:

* None
* Esoteric
* Philosopher
* Astrologer
* Programmer
* Technical Assistant
* Divination
* Abstraction&#x20;
* Wrong Answers Only
* Sassy
* Troll

</details>

<details>

<summary>Select Model</summary>

_`/ether-ai [ model ] [ model option ]`_

Select model to use in your interactions

Options:

* Nemo&#x20;
  * [https://huggingface.co/lmstudio-community/Mistral-Nemo-Instruct-2407-GGUF](https://huggingface.co/lmstudio-community/Mistral-Nemo-Instruct-2407-GGUF)
* YCoder
  * [https://huggingface.co/lmstudio-community/Yi-Coder-9B-Chat-GGUF](https://huggingface.co/lmstudio-community/Yi-Coder-9B-Chat-GGUF)
* Mathstral
  * [https://huggingface.co/lmstudio-community/mathstral-7B-v0.1-GGUF](https://huggingface.co/lmstudio-community/mathstral-7B-v0.1-GGUF)

</details>

<details>

<summary>Select Temperature</summary>

_`/ether-ai [ temperature ] [ amount ]`_

Adjusts the temperature of the AI model in your interactions

</details>

<details>

<summary>Select Token Limit</summary>

_`/ether-ai [ tokens ] [ amount ]`_

Sets the token limit for your interactions

</details>
