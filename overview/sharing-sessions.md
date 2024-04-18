---
description: Share access to your session with other members
---

# 🙋‍♂️ Sharing Sessions

***

{% hint style="info" %}
<mark style="color:yellow;">Only one shared session per channel globally</mark>

This is enforced to mitigate multiple bot responses resulting from multiple shared sessions

<mark style="color:yellow;">Session resolving logic</mark>

Members who do not have an active session in the shared session channel will be resolved to the shared session in the channel. Users with their own session in a shared session channel are resolved to their own session
{% endhint %}

{% hint style="danger" %}
Leaving shared sessions unattended can generate risks for account and usage abuse by other members.&#x20;
{% endhint %}

***

```
`/sharing_options [ role / user ] [ time ] [ iterations ] [ type ]`
```

<details>

<summary>Sharing with a role</summary>

`/sharing_options [ role ]`

* Share access with a role (time, iterations, and types)

</details>

<details>

<summary>Sharing with a user</summary>

`/sharing_options [ user ]`

* Share access with a user (time, iterations, and types)

</details>

<details>

<summary>Time sharing options</summary>

`/sharing_options [ role / user ] [ time ] [ amount ]`

* Adds an amount of time to allow access
* Excepts formats:
  * s, second, seconds
  * m, minute, minutes
  * h, hour, hours
  * d, day, days
  * w, week weeks

Examples:

* &#x20;`/sharing_options [ role ] [ time ] [ 1 hour]`
* `/sharing_options [ user ] [ time ] [ 3 days ]`
* `/sharing_options [ role ] [ time ] [ 2w ]`

</details>

<details>

<summary>Iterations sharing options</summary>

`/sharing_options [ role / user ] [ iterations ] [ number ]`

* Number of iterations a user can push through the bot (in any type)
* Session variables such as `number` influence iterative deductions, for example image number set to two will deduct two iterations from the user when the two images return

</details>

<details>

<summary>Sharing access types</summary>

`/sharing_options [ role / share ] [ type ]`

Types:

* Chat - text generative iterations
* Image - DALL E Image Generations
* Visual - GPT Visual
* Fast Embed - One-time and looped embeds
* Full Embed - embedding in looped condition
* Set - Ability for user or role to change session configuration using set

</details>
